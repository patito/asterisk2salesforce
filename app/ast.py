#!/usr/bin/python

import sys
import re

import asterisk.manager

from config import Config as config
from cdr import CDREvent


class AsteriskHandler(object):
    """
    Handle Asterisk management, events, connection.
    """
    def __init__(self, host=config.Asterisk.HOST,
                 login=config.Asterisk.LOGIN,
                 password=config.Asterisk.PASSWORD):
        self.__host = host
        self.__login = login
        self.__password = password
        self.__manager = asterisk.manager.Manager()

    def connect(self):

        try:
            self.__manager.connect(self.__host)
            self.__manager.login(self.__login, self.__password)
        except asterisk.manager.ManagerSocketException as err:
            errno, reason = err
            print ("Error connecting to the manager: %s" % reason)
            sys.exit(1)
        except asterisk.manager.ManagerAuthException as reason:
            print ("Error logging in to the manager: %s" % reason)
            sys.exit(1)
        except asterisk.manager.ManagerException as reason:
            print ("Error: %s" % reason)
            sys.exit(1)

    def subscribe_cdr_event(self):
        cdr = CDREvent()
        cdr.set_extensions(self.get_all_extensions())
        self.__manager.register_event('Cdr', cdr.callback)

    def loop(self):
        self.__manager.message_loop()

    def logoff(self):
        self.__manager.logoff()

    def get_all_extensions(self):
        """
        Save extensions and full name in a dictionary.
        extensions[ext] = fullname
        """
        command = self.__manager.command('database showkey cidname')
        lines = command.data.split('\n')
        self.__extensions = {}

        for line in lines:
            splited_line = re.split('(\W+)', line)
            if (len(splited_line) > 10):
                ext = splited_line[4]
                fullname = splited_line[8] + " " + splited_line[10]
                self.__extensions[ext] = fullname

        return self.__extensions
