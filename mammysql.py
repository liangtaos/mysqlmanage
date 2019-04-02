#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time :  10:43
# @Author : cold
# @File : mammysql.py

import time
from optparse import OptionParser
import os
import glob
import sys
from python_mysql import MySQLConfig
from subprocess import Popen,PIPE
import shlex

MYSQL_DATA_DIR = r'C:\Users\cold\Desktop\data'
MYSQL_CONF_DIR = r'C:\Users\cold\Desktop\conf'
# MYSQL_CONF_DIR = '/data/conf'


def opt():
    parser = OptionParser()
    parser.add_option(
        "-n", "--name",
        dest = "name",
        action = "store",
        default = "myinstance"
    )
    parser.add_option(
        "-p", "--port",
        dest = "port",
        action = "store",
        default = "3306",
    )
    parser.add_option(
        "-c","--command",
        dest = "command",
        default = "check",
    )

    options , args = parser.parse_args()
    return options, args


def _init():
    if not os.path.exists(MYSQL_DATA_DIR):
        os.makedirs(MYSQL_DATA_DIR)
    if not os.path.exists(MYSQL_CONF_DIR):
        os.makedirs(MYSQL_CONF_DIR)

def readConf():
    confs = glob.glob(MYSQL_CONF_DIR+'\*.cnf')
    return confs


def checkPort(conf,port):
    mc = MySQLConfig(conf)
    if mc.mysql_vars['port'] == port:
        return True
    else:
        return False

def getCNF(name):
    cnf = os.path.join(MYSQL_CONF_DIR, '{0}.cnf'.format(name))
    return cnf


def _getDict(name,port):
    return {
        'pid-file': os.path.join(MYSQL_DATA_DIR,name,'{0}.pid'.format(name)),
        'socket':'/tmp/{0}.sock'.format(name),
        'port':port,
        'datadir': os.path.join(MYSQL_DATA_DIR, name),
        'log-error': os.path.join(MYSQL_DATA_DIR,name,'{0}.log'.format(name))
    }

def mysql_install(name):
    cmd = "/usr/local/mysql/scripts/mysql_install_db --default-file={0}".format(getCNF(name))
    p = Popen(shlex.split(cmd), stdout=PIPE,stderr=PIPE)
    p.communicate()
    p.returncode

def setOwner(datadir):
    os.system('chown -R mysql.mysql {0}'.format(datadir))



def mysql_run(name):
    cmd = 'mysqld_safe --defaults-file={0} &'.format(getCNF(name))
    p = Popen(cmd, shell=True,stdout=PIPE, stderr=PIPE)
    time.sleep(2)
    p.returncode



def createInstance(name, port):
    name = name.strip()
    exists_confs = readConf()
    # print(exists_confs)
    for conf in exists_confs:
        if conf.split('\\')[-1][:-4] == name:
            print("%s is exists"% name)
            sys.exit(-1)
        if checkPort(conf, port):
            print('%s is exist'% port)
            sys.exit(-1)
    cnf = getCNF(name)

    if not os.path.exists(cnf):
        c = _getDict(name, port)
        mc = MySQLConfig(cnf, **c)
        mc.save()
    datadir = os.path.join(MYSQL_DATA_DIR,name)
    if not os.path.exists(datadir):
        mysql_install(name)
        setOwner(datadir)


if __name__ == '__main__':
    _init()
    options, args = opt()
    instance_name = options.name
    instance_port = options.port
    instance_cmd = options.command
    createInstance(instance_name,instance_port)
