#!/usr/bin/python

from config import Config
from simple_salesforce import Salesforce
from utils import get_number_term

import time

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import smtplib


def send_email(to, name, task_id, account_name, instance):
    msg = MIMEMultipart()

    print "To = %s" % to
    print "From = %s" % Config.SalesForce.USERNAME
    print "Name = %s" % name
    print "TaskId = %s" % task_id
    print "Account_name = %s" % account_name

    msg['Subject'] = 'Your call with ' + account_name + '.'
    msg['From'] = Config.SalesForce.USERNAME
    msg['To'] = to

    body = "Hi " + name +\
           ",\nyou have just finished a call which" +\
           "has been logged in SalesForce.\n\nPlease update" +\
           "the entry with details about the call: http://" +\
           instance + "/" + task_id + "/e.\n\n----" +\
           "THIS IS AN AUTOMATICALLY GENERATED MESSAGE. ----"

    msg.attach(MIMEText(body, 'plain'))
    s = smtplib.SMTP('mail.brandwatch.com')

    s.sendmail(Config.SalesForce.USERNAME, to, msg.as_string())
    s.quit()


class SalesForceHandler(object):

    def __init__(self,
                 instance=Config.SalesForce.INSTANCE,
                 username=Config.SalesForce.USERNAME,
                 password=Config.SalesForce.PASSWORD,
                 token=Config.SalesForce.TOKEN):

        self.__sf = Salesforce(instance=instance,
                               username=username,
                               password=password,
                               security_token=token)

    def get_user_id(self, name):
        query = "SELECT Id FROM User WHERE Name LIKE '" + name + "'"
        result = self.__sf.query_all(query)

        if 'records' in result:
            result = self.__sf.query_all(query)["records"]

        if (len(result) == 1):
            return result[0]['Id']
        return None

    def get_shared_users(self, phone):
        shared_users = Config.SalesForce.SHARED

        print shared_users, type(phone)
        for i in shared_users:
            if phone in shared_users[i]:
                return i
        return None

    def get_number_contacts(self, phone):
        term = get_number_term(phone)
        query = "SELECT AccountId FROM Contact WHERE Phone LIKE '" + term +\
                "' OR MobilePhone LIKE '" + term + "'"

        results = self.__sf.query_all(query)
        if 'records' in results:
            results = self.__sf.query_all(query)["records"]

        return len(results)

    def get_number_accounts(self, phone):

        term = get_number_term(phone)
        query = "SELECT Id FROM Account WHERE Phone LIKE '" + term + "'"

        results = self.__sf.query_all(query)
        if 'records' in results:
            results = self.__sf.query_all(query)["records"]

        return len(results)

    def create_task(self, info):
        print "Creating task"
        task = self.__sf.Task.create({
            'Type': 'Called',
            'WhatId': info['AccountId'],
            'OwnerID': info['UserId'],
            'Subject': 'Call',
            'Status': 'Completed',
            'WhoId': info['ContactId'],
            'Description': 'A call has been logged automagically.',
            'Status': 'Completed',
            'Priority': 'Normal',
            'Summary__c': info['Summary'],
            'ActivityDate': time.strftime('%Y-%m-%d')
        })

        name = self.__sf.User.get(info['UserId'])['FirstName']
        to = self.__sf.User.get(info['UserId'])['Email']
        task_id = self.__sf.Task.get(task['id'])

        account_name = self.__sf.Account.get(task_id['WhatId'])['Name']

        send_email(to, name, task['id'], account_name,
                   Config.SalesForce.INSTANCE)

    def get_account_id_from_account(self, phone):
        term = get_number_term(phone)

        query_account = "SELECT Id FROM Account WHERE Phone LIKE '"\
                        + term + "'"

        accounts = self.__sf.query_all(query_account)
        if 'records' in accounts:
            accounts = self.__sf.query_all(query_account)["records"]

        if (len(accounts) == 1):
            return accounts[0]['Id']
        else:
            return None

    def get_account_id_from_contact(self, phone):
        term = get_number_term(phone)

        query_contact = "SELECT AccountId FROM Contact WHERE Phone LIKE '"\
                        + term + "'"

        accounts = self.__sf.query_all(query_contact)
        if 'records' in accounts:
            accounts = self.__sf.query_all(query_contact)["records"]

        if (len(accounts) == 1):
            return accounts[0]['AccountId']
        elif (len(accounts) > 1):
            account_id = accounts[0]['AccountId']
            for account in accounts:
                if account['AccountId'] != account_id:
                    return None
            return account_id
        else:
            return None

    def get_account_id_from_mobile(self, phone):
        term = get_number_term(phone)

        query_mobile = "SELECT AccountId FROM Contact WHERE MobilePhone LIKE '"\
                       + term + "'"

        accounts = self.__sf.query_all(query_mobile)
        if 'records' in accounts:
            accounts = self.__sf.query_all(query_mobile)["records"]

        if (len(accounts) == 1):
            return accounts[0]['AccountId']
        elif (len(accounts) > 1):
            account_id = accounts[0]['AccountId']
            for account in accounts:
                if account['AccountId'] != account_id:
                    return None
            return account_id
        else:
            return None

    def get_account_id(self, phone):

        account_id = self.get_account_id_from_account(phone)
        if (account_id):
            return account_id
        account_id = self.get_account_id_from_contact(phone)
        if (account_id):
            return account_id
        account_id = self.get_account_id_from_mobile(phone)
        if (account_id):
            return account_id

    def get_contact_id(self, phone):

        term = get_number_term(phone)

        query = "SELECT Id FROM Contact WHERE Phone LIKE '" + term +\
                "' OR MobilePhone LIKE '" + term + "'"

        results = self.__sf.query_all(query)
        if 'records' in results:
            results = self.__sf.query_all(query)["records"]

        if (len(results) == 1):
            return results[0]['Id']
        return None
