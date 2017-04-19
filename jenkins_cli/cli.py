import argparse
import base64
import os
import random
import string
import sys
import jenkins_cli

__author__ = 'massimone88 <stefano.mandruzzato@gmail.com>'
__version__ = '1.0.0'

BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda ss: ss[0:-ord(ss[-1])]

import ConfigParser as configparser
import getpass
from Crypto.Cipher import AES

def die(msg):
    sys.stderr.write(msg + "\n")
    sys.exit(1)

CREATE_MAVEN_JOB = 'create_maven_job'
CREATE_FREESTYLE_MAVEN_JOB = 'create_freestyle_maven_job'
CREATE_ANGULAR_JOB = 'create_angular_job'
SET_JENKINS_PASSWORD = 'set_jenkins_password'
EXPORT_JOB_TO_CSV = 'export_job_to_csv_files'
CREATE_MAVEN_JOB_FROM_CSV = 'create_maven_job_from_csv'
CREATE_ANT_JOB_FROM_CSV = 'create_ant_job_from_csv'
CREATE_ANGULAR_JOB_FROM_CSV = 'create_angular_job_from_csv'
extra_actions = {
    CREATE_MAVEN_JOB: {'requiredAttrs':
                           ['job_name', 'repo_name', 'jdk', 'maven', 'path_pom', 'default_goal', 'dist_dir'],
                       'optionalBoolAttrs': []},
    CREATE_FREESTYLE_MAVEN_JOB: {'requiredAttrs':
                           ['job_name', 'repo_name', 'jdk', 'path_pom', 'maven', 'default_goal', 'dist_dir'],
                       'optionalBoolAttrs': []},
    CREATE_ANGULAR_JOB: {'requiredAttrs':
                             ['job_name', 'repo_name',  'path_grunt', 'default_grunt_task', 'dist_dir', 'node'],
                         'optionalBoolAttrs': ['no_bower', 'gulp']},
    SET_JENKINS_PASSWORD: {'requiredAttrs': []},
    EXPORT_JOB_TO_CSV: {'requiredAttrs': []},
    CREATE_MAVEN_JOB_FROM_CSV: {'requiredAttrs': ['filename']},
    CREATE_ANT_JOB_FROM_CSV: {'requiredAttrs': ['filename']},
    CREATE_ANGULAR_JOB_FROM_CSV: {'requiredAttrs': ['filename']},
    "fix_delete_workspace": {'requiredAttrs': []},
    "add_post_build_clean_workspace": {'requiredAttrs': []},
    'get_job_info': {'requiredAttrs': ['name'], 'optionalAttrs': ['depth']},
    'get_job_info_regex': {'requiredAttrs': ['pattern'], 'optionalAttrs': ['depth']},
    'get_job_name': {'requiredAttrs': ['name']},
    'debug_job_info': {'requiredAttrs': ['job_name']},
    'get_build_info': {'requiredAttrs': ['name', 'number'], 'optionalAttrs': ['depth']},
    'get_queue_info': {'requiredAttrs': []},
    'cancel_queue': {'requiredAttrs': []},
    'get_jobs': {'requiredAttrs': []},
    'copy_job': {'requiredAttrs': ['from_name', 'to_name']},
    'rename_job': {'requiredAttrs': ['from_name', 'to_name']},
    'delete_job': {'requiredAttrs': ['name']},
    'enable_job': {'requiredAttrs': ['name']},
    'disable_job': {'requiredAttrs': ['name']},
    'job_exists': {'requiredAttrs': ['name']},
    'jobs_count': {'requiredAttrs': []},
    'get_job_config': {'requiredAttrs': ['name']}
}


def populate_sub_parser(sub_parser):
    for action in extra_actions:
        sub_parser_action = sub_parser.add_parser(action)
        d = extra_actions[action]
        [sub_parser_action.add_argument("--%s" % arg, required=True)
         for arg in d['requiredAttrs']]
        try:
            [sub_parser_action.add_argument("--%s" % arg, required=False)
             for arg in d['optionalAttrs']]
        except Exception as e:
            pass
        try:
            [sub_parser_action.add_argument("--%s" % arg, required=False, action="store_true")
             for arg in d['optionalBoolAttrs']]
        except Exception as e:
            pass


parser = argparse.ArgumentParser(
    description="Jenkins API Command Line Interface")
parser.add_argument("-v", "--verbose", "--fancy",
                    help="Verbose mode",
                    action="store_true")
parser.add_argument("-c", "--config-file", action='append',
                    help=("Configuration file to use. Can be used "
                          "multiple times."))
parser.add_argument("--jenkins",
                    help=("Which configuration section should "
                          "be used. If not defined, the default selection "
                          "will be used."),
                    required=False)

subparsers = parser.add_subparsers(dest='action')

populate_sub_parser(subparsers)
arg = parser.parse_args()
args = arg.__dict__

files = arg.config_file or ['/etc/python-jenkins.cfg',
                            os.path.expanduser('~/.python-jenkins.cfg')]
print(files)
# read the config
config = configparser.ConfigParser()
try:
    config.read(files)
except Exception as e:
    print("Impossible to parse the configuration file(s): %s" %
          str(e))
    sys.exit(1)

ssl_verify = True
timeout = 60
jenkins_id = arg.jenkins
verbose = arg.verbose
action = arg.action
jenkins_namespace = None
jenkins_ur = None
jenkins_token = None
# Remove CLI behavior-related args
args.pop("jenkins")
args.pop("config_file")
args.pop("verbose")
args.pop("action")

if jenkins_id is None:
    try:
        jenkins_id = config.get('global', 'default')
    except Exception:
        die("Impossible to get the jenkins id "
            "(not specified in config file)")

try:
    jenkins_url = config.get(jenkins_id, 'url')
    jenkins_username = config.get(jenkins_id, 'username')
    jenkins_pwd_enc = None
    try:
        jenkins_pwd_enc = base64.b64decode(config.get(jenkins_id, 'pwd_enc'))
    except configparser.NoOptionError:
        pass
    if jenkins_pwd_enc and action != SET_JENKINS_PASSWORD:
        jenkins_pwd_key = config.get(jenkins_id, 'pwd_key')
        jenkins_pwd_iv = config.get(jenkins_id, 'pwd_iv')
        decryption_suite = AES.new(jenkins_pwd_key, AES.MODE_CBC, jenkins_pwd_iv)
        jenkins_pwd = decryption_suite.decrypt(jenkins_pwd_enc)
        jenkins_pwd = unpad(jenkins_pwd)
    else:
        print "please type of jenkins password:"
        jenkins_pwd = getpass.getpass()
        if action == SET_JENKINS_PASSWORD:
            raw = pad(jenkins_pwd)
            key = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(32))
            iv = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16))
            # Encryption
            encryption_suite = AES.new(key, AES.MODE_CBC, iv)
            pwd_enc = encryption_suite.encrypt(raw)
            config.set(jenkins_id, 'pwd_key', key)
            config.set(jenkins_id, 'pwd_iv', iv)
            config.set(jenkins_id, 'pwd_enc', base64.b64encode(pwd_enc))
            cfg_file = open(files[1], "w")
            config.write(cfg_file)
            cfg_file.close()
            exit(0)

except Exception as e:
    die("Impossible to get jenkins informations from configuration (%s)" % jenkins_id)

try:
    gitlab_namespace = config.get(jenkins_id, 'gitlab_namespace')
except:
    die("namespace is not set")

try:
    gitlab_url = config.get(jenkins_id, 'gitlab_url')
except:
    die("jenkins url is not set")

try:
    ssl_verify = config.getboolean('global', 'ssl_verify')
except Exception:
    pass
try:
    ssl_verify = config.getboolean(jenkins_id, 'ssl_verify')
except Exception:
    pass

try:
    timeout = config.getint('global', 'timeout')
except Exception:
    pass
try:
    timeout = config.getint(jenkins_id, 'timeout')
except Exception:
    pass

jenkinsUtil = jenkins_cli.IceJenkinsUtil(jenkins_url, jenkins_username, jenkins_pwd, gitlab_url, gitlab_namespace)
try:
    jenkinsUtil.call_custom_action(action, args)
except Exception as e:
    print jenkinsUtil.call_jenkins_method(action, args)
sys.exit(0)
