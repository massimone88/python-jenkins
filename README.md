## Python Jenkins
Python Jenkins is wrapper of CLI python-jenkins(https://github.com/openstack/python-jenkins) with extended commands.

## Requirements
* Python (of course). 
* python-jenkins: [python-jenkins](https://python-jenkins.readthedocs.org/en/latest/).

## Bugs reports
Please report bugs and feature requests at [https://github.com/massimone88/python-jenkins/issues](https://github.com/massimone88/python-jenkins/issues).

## Command line tool
### to install
For libraries dependences is better that you have **pip** installed.

* clone the repo in your pc (`git clone https://github.com/massimone88/python-jenkins.git python-jenkins`).
* run the command in the repo folder `pip install -r requirements.txt` to install libraries dependences.
* run the command in the repo folder `python setup.py install` to install the jenkins CLI.
* make sure that you have the python scripts folder in the **PATH** (For Windows is `C:\Python27\Scripts`).

### usage
To use the command line tool, you need to define which Jenkins server(s) can be
accessed. this can be done in 2 files:

* /etc/python-jenkins.cfg
* ~/.python-jenkins.cfg

Here's an example of the syntax:

`````
[global]
default = local
ssl_verify = true
timeout = 5

[local]
url = http://10.0.3.2:8080
username = nickN@me
gitlab_url = gitlab.com
gitlab_namespace = group1

[distant]
url = https://some.whe.re
username = nickN@me2
gitlab_url = gitlab.com
gitlab_namespace = group2
ssl_verify = false
`````

The [global] section define which server is accesed by default.
Each other section defines how to access a server. Only private token
authentication is supported (not user/password).

The `ssl_verify` option defines if the server SSL certificate should be
validated (use false for self signed certificates, only useful with https).

The `timeout` option defines after how many seconds a request to the Gitlab
server should be abandoned.

The `username` defines the username for jenkins login. For store the password in cypertext please run the command `jenkins set_jenkins_password`.

### set_jenkins_password
Typing the command `jenkins set_jenkins_password` will be asked a password of your jenkins credential. After all will be store in the configuration files the following option:
* **pwd_key**
* **pwd_iv**
* **pwd_enc**
If you don't want to store the password of you configuration file, it will be asked in every command.

The `gitlab_url` option defines the IP address or the hostname of the Gitlab server in order to create Jenkins job with Gitlab SCM. **WARNING**: you have to write the hostname or the IP address of ssh connection, not the HTTP address.

The `gitlab_namespace` defines the namespace of the gitlab repositories.

Choosing a different server than the default one can be done at run time:

`````
jenkins --jenkins=distant [command]
`````

for all command type `jenkins --help`.

For help of a specific command type `jenkins <command> --help`.
