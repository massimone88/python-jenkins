import json
import sys

__author__ = 'massimone88 <stefano.mandruzzato@gmail.com>'
__version__ = '1.0.0'
import jenkins
import xml.etree.ElementTree
import csv
from clean_workspace_service import *

class IceJenkinsUtil(object):
    def __init__(self, url, username, pwd, gitlab_url, gitlab_namespace):
        self.jenkins = jenkins.Jenkins(url, username=username, password=pwd)
        self.gitlab_url = gitlab_url
        self.gitlab_namespace = gitlab_namespace

    def create_maven_job(self, args):
        name_job = args['job_name']
        repo_name = args['repo_name']
        maven = args['maven']
        path_pom = args['path_pom']
        default_goal = args['default_goal']
        dist_dir = args['dist_dir']
        jdk = args['jdk']
        try:
            self.jenkins.get_job_config(name_job)
            print "job found, delete before to create one job with the same name"
            self.jenkins.delete_job(name_job)
        except Exception as e:
            pass

        config = self.jenkins.get_job_config("TEMPLATE-MAVEN")
        print config
        git_ssh_url = "git@%s:%s/%s.git" % (self.gitlab_url, self.gitlab_namespace, repo_name)
        http_ssh_url = "https://%s/%s/%s.git" % (self.gitlab_url, self.gitlab_namespace, repo_name)
        config = config.replace("$CHANGE_ME_GIT_SSH_URL", git_ssh_url)
        config = config.replace("$CHANGE_ME_GIT_HTTP_URL_WITHOUT_DOT_GIT_ON_THE_END_OF_URL", http_ssh_url)
        config = config.replace("<jdk>Java6</jdk>", "<jdk>" + jdk.title() + "</jdk>")
        config = config.replace("<mavenName>maven 3.0.5</mavenName>", "<mavenName>" + maven + "</mavenName>")
        config = config.replace("$CHANGE_ME_PATH_POM", path_pom)
        config = config.replace("$CHANGE_ME_DEFAULT_GOAL", default_goal)
        config = config.replace("$CHANGE_ME_DIST_DIR", dist_dir)

        out = self.jenkins.create_job(name_job, config)
        print out

    def create_freestyle_maven_job(self, args):
        name_job = args['job_name']
        repo_name = args['repo_name']
        path_pom = args['path_pom']
        default_goal = args['default_goal']
        maven = args['maven']
        dist_dir = args['dist_dir']
        jdk = args['jdk']
        exist = False
        try:
            self.jenkins.assert_job_exists(name_job)
            print name_job + " job found, reconfig job"
            exist = True
        except jenkins.JenkinsException as e:
            pass

        config = self.jenkins.get_job_config("TEMPLATE-FREESTYLE-MAVEN")
        #print config
        git_ssh_url = "git@%s:%s/%s.git" % (self.gitlab_url, self.gitlab_namespace, repo_name)
        http_ssh_url = "https://%s/%s/%s.git" % (self.gitlab_url, self.gitlab_namespace, repo_name)
        gitlab_metadata = "%s/%s" % (self.gitlab_namespace, repo_name)
        config = config.replace("$CHANGE_ME_GITLAB_METADATA", gitlab_metadata)
        config = config.replace("$CHANGE_ME_GIT_SSH_URL", git_ssh_url)
        config = config.replace("$CHANGE_ME_GIT_HTTP_URL_WITHOUT_DOT_GIT_ON_THE_END_OF_URL", http_ssh_url)
        config = config.replace("<jdk>Java6</jdk>", "<jdk>" + jdk.title() + "</jdk>")
        config = config.replace("<mavenName>3.0.5</mavenName>", "<mavenName>" + maven + "</mavenName>")
        config = config.replace("$CHANGE_ME_PATH_POM", path_pom)
        config = config.replace("$CHANGE_ME_DEFAULT_GOAL", default_goal)
        config = config.replace("$CHANGE_ME_DIST_DIR", dist_dir)

        if exist:
            out = self.jenkins.reconfig_job(name_job, config)
        else:
            out = self.jenkins.create_job(name_job, config)
        #print out

    def create_ant_job(self, args):
        name_job = args['job_name']
        repo_name = args['repo_name']
        ant = args['ant']
        target = args['target']
        build = args['build']
        dist_dir = args['dist_dir']
        jdk = args['jdk']
        exist = False
        try:
            self.jenkins.assert_job_exists(name_job)
            print name_job + " job found, reconfig job"
            exist = True
        except jenkins.JenkinsException as e:
            pass

        config = self.jenkins.get_job_config("TEMPLATE-ANT")
        print config
        git_ssh_url = "git@%s:%s/%s.git" % (self.gitlab_url, self.gitlab_namespace, repo_name)
        http_ssh_url = "https://%s/%s/%s.git" % (self.gitlab_url, self.gitlab_namespace, repo_name)
        gitlab_metadata = "%s/%s" % (self.gitlab_namespace, repo_name)
        config = config.replace("$CHANGE_ME_GITLAB_METADATA", gitlab_metadata)
        config = config.replace("$CHANGE_ME_GIT_SSH_URL", git_ssh_url)
        config = config.replace("$CHANGE_ME_GIT_HTTP_URL_WITHOUT_DOT_GIT_ON_THE_END_OF_URL", http_ssh_url)
        config = config.replace("<jdk>Java6</jdk>", "<jdk>" + jdk.title() + "</jdk>")
        config = config.replace("<antName>(Default)</antName>", "<antName>" + ant + "</antName>")
        config = config.replace("$CHANGE_ME_BUILD", build)
        config = config.replace("$CHANGE_ME_TARGET", target)
        config = config.replace("$CHANGE_ME_DIST_DIR", dist_dir)

        if exist:
            out = self.jenkins.reconfig_job(name_job, config)
        else:
            out = self.jenkins.create_job(name_job, config)
        #print out

    def create_angular_job(self, args):
        name_job = args['job_name']
        repo_name = args['repo_name']
        default_grunt_task = args['default_grunt_task']
        node = args['node']
        dist_dir = args['dist_dir']
        no_bower = True if 'no_bower' in args.keys() else False
        gulp = True if 'gulp' in args.keys() else False
        exist = False
        try:
            self.jenkins.get_job_config(name_job)
            print name_job + " job found, reconfig job"
            exist = True
        except Exception as e:
            pass

        config = self.jenkins.get_job_config("TEMPLATE-ANGULAR")

        git_ssh_url = "git@%s:%s/%s.git" % (self.gitlab_url, self.gitlab_namespace, repo_name)
        http_ssh_url = "https://%s/%s/%s.git" % (self.gitlab_url, self.gitlab_namespace, repo_name)
        gitlab_metadata = "%s/%s" % (self.gitlab_namespace, repo_name)
        config = config.replace("$CHANGE_ME_GITLAB_METADATA", gitlab_metadata)
        config = config.replace("$CHANGE_ME_GIT_SSH_URL", git_ssh_url)
        config = config.replace("$CHANGE_ME_GIT_HTTP_URL_WITHOUT_DOT_GIT_ON_THE_END_OF_URL", http_ssh_url)
        config = config.replace("$CHANGE_ME_DEFAULT_GRUNT_TASK", default_grunt_task)
        config = config.replace("<nodeJSInstallationName>0.12.14</nodeJSInstallationName>", "<nodeJSInstallationName>" + node + "</nodeJSInstallationName>")
        config = config.replace("$CHANGE_ME_DIST_DIR", dist_dir)
        if no_bower:
            config = config.replace('bower install && bower update', '')
        if gulp:
            config = config.replace('grunt', 'gulp')
        if exist:
            out = self.jenkins.reconfig_job(name_job, config)
        else:
            out = self.jenkins.create_job(name_job, config)
        print out

    def call_custom_action(self, action, kwargs):
        print action, kwargs
        method = getattr(self, action)
        return method(kwargs)

    def call_jenkins_method(self, method_name, kwargs):
        method = getattr(self.jenkins, method_name)
        return method(**kwargs)

    def create_maven_job_from_csv(self, args):
        filename = args["filename"]
        with open(filename, 'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='"',skipinitialspace=True, quoting=csv.QUOTE_ALL)
            for row in spamreader:
                if row[0] == 'JOB_NAME':
                    continue
                arg = {
                    'job_name': row[0],
                    'repo_name': row[1],
                    'jdk': row[2],
                    'maven': row[3],
                    'path_pom': row[4],
                    'default_goal': row[5],
                    'dist_dir': row[6],
                    'command': row[7]
                  }
                if arg['job_name'].endswith("TAGS"):
                    self.create_freestyle_maven_job_tags(arg)
                else:
                    self.create_freestyle_maven_job(arg)

    def create_ant_job_from_csv(self, args):
        filename = args["filename"]
        with open(filename, 'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='"',skipinitialspace=True, quoting=csv.QUOTE_ALL)
            for row in spamreader:
                if row[0] == 'JOB_NAME':
                    continue
                #JOB_NAME, GITLAB URL, JDK, ANT, BUILD, TARGET, ARCHIVE, COMMAND
                arg = {
                    'job_name': row[0],
                    'repo_name': row[1],
                    'jdk': row[2],
                    'ant': row[3],
                    'build': row[4],
                    'target': row[5],
                    'dist_dir': row[6],
                    'command': row[7]
                  }
                self.create_ant_job(arg)

    def create_angular_job_from_csv(self, args):
        filename = args["filename"]
        with open(filename, 'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='"', skipinitialspace=True, quoting=csv.QUOTE_ALL)
            for row in spamreader:
                if row[0] == 'JOB_NAME':
                    continue
                #JOB_NAME, GITLAB URL, NODE, TARGET, ARCHIVE, COMMAND
                arg = {
                    'job_name': row[0],
                    'repo_name': row[1],
                    'node': row[2],
                    'default_grunt_task': row[3],
                    'dist_dir': row[4],
                    'command': row[5]
                  }
                if arg['job_name'].endswith("TAGS"):
                    self.create_angular_job_tags(arg)
                else:
                    self.create_angular_job(arg)

    def fix_delete_workspace(self, args):
        print 'delete_clean_maven'
        jobs = self.jenkins.get_all_jobs()
        for job in jobs:
            print job['name']
            job_config = self.jenkins.get_job_config(job['name'])
            while "<deleteDirs>false</deleteDirs>" in job_config:
                print "change deleteDirs on deleteWorkspace to true"
                job_config = job_config.replace("<deleteDirs>false</deleteDirs>", "<deleteDirs>true</deleteDirs>")
            #job_config = job_config.replace("<goals>$mavenGoal</goals>", "<goals>clean $mavenGoal</goals>")
            self.jenkins.reconfig_job(job['name'], job_config)

    def add_post_build_clean_workspace(self, args):
        print 'add_post_build_clean_workspace'
        jobs = self.jenkins.get_all_jobs()
        for job in jobs:
            delete_post = False
            job_config = self.jenkins.get_job_config(job['name'])
            if "hudson.plugins.ws__cleanup.WsCleanup plugin" in job_config and "<cleanWhenSuccess>" in job_config:
                delete_post = True
            if not delete_post:
                print "job: %s" % job['name']
                if job['name'] in ('prova-pipeline','prova_pipeline','test depe 1', 'test lmmm', 'test-lmmm-2'):
                    continue
                new_job_config = CleanWorkSpaceService.add_post_build_clean_workspace(job_config)
                self.jenkins.reconfig_job(job['name'], new_job_config)

    @staticmethod
    def die(msg):
        sys.stderr.write(msg + "\n")
        sys.exit(1)
