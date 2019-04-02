#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time :  15:00
# @Author : cold
# @File : python_mysql.py




from configparser import ConfigParser
import os


class MySQLConfig(ConfigParser):
    def __init__(self, config, **kwargs):
        # ConfigParser.__init__(self,allow_no_value=True)
        super(MySQLConfig, self).__init__(allow_no_value=True)
        self.config = config
        self.mysql_vars = {}
        if os.path.exists(self.config):
            self.read(self.config)
            self.get_mysqld_vars()
        else:
            self.get_default_vars()
        self.set_mysqld_vars(kwargs)


    def set_mysqld_vars(self, kwargs):
        for k, v in kwargs.items():
            setattr(self,k,v)
            self.mysql_vars[k] = str(v)


    def get_mysqld_vars(self):
        rst = {}
        options = self.options('mysqld')
        for o in options:
            rst[o] = self.get('mysqld', o)
        self.set_mysqld_vars(rst)

    def get_default_vars(self):
        default = {
            'port':'3306',
            'socket': '/tmp/mysql.sock',
            'log-bin':'mysql-bin',
            'basedir': '/usr/local/mysql',
            'datadir':'/data/mysql',
            'binlog_format':'mixed',
            'server-id':'1',
            'user':'mysql',
        }
        self.set_mysqld_vars(default)

    def set_vars(self,k,v):
        self.mysql_vars[k] = v

    def save(self):
        if not self.has_section('mysqld'):
            self.add_section('mysqld')
        for k,v in self.mysql_vars.items():
            # print(k,v)
            self.set('mysqld', k ,v)


        with open(self.config,'w') as fd:
            # print(fd)
            self.write(fd)

if __name__ == '__main__':
    mc = MySQLConfig(r'C:\Users\cold\Desktop\my3.cnf', mx=1360)
    mc.set_vars('skip-grant1', None)
    mc.save()

    print(mc.port)
    print(mc.socket)