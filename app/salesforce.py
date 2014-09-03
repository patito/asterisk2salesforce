#!/usr/bin/python

from config import Config
from simple_salesforce import Salesforce
from utils import get_number_term


class SalesForceHandler(object):

    def __init__(self, 
                 instance = Config.SalesForce.INSTANCE,
                 username = Config.SalesForce.USERNAME,
                 password = Config.SalesForce.PASSWORD,
                 token = Config.SalesForce.TOKEN):

        self.__sf = Salesforce(instance=instance,
                               username=username, 
                               password=password, 
                               security_token=token)


    def get_user_id(self, name):
        print name
        query = "SELECT Id FROM User WHERE Name LIKE '" + name + "'"
        result = self.__sf.query_all(query)["records"]
        if (len(result) == 1):
            print result[0]['Id']


    def get_number_contacts(self, phone):
        term = get_number_term(phone)
    
        print "Term = %s" % term
        query = "SELECT AccountId FROM Contact WHERE Phone LIKE '" + term +\
                "' OR MobilePhone LIKE '" + term + "'"

        results = self.__sf.query_all(query)["records"]

        return len(results)


    def get_number_accounts(self, phone):

        term = get_number_term(phone)
        query = "SELECT Id FROM Account WHERE Phone LIKE '" + term + "'"
        results = self.__sf.query_all(query)["records"]
       
        return len(results)


    def create_task(self):

        task = self.__sf.Task.create({
            'Type':'Called',
            'WhatId':accountId,
            'OwnerID':userId,
            'Subject':subject,
            'Status':'Completed',
            'WhoId':contactId,
            'Description':'A call has been logged automagically.',
            'Status':'Completed',
            'Priority':'Normal',
            'Summary__c':summary,
            'ActivityDate':time.strftime('%Y-%m-%d')
        })

    def get_account_id_from_account(self, phone):
        term = get_number_term(phone)

        query_account = "SELECT Id FROM Account WHERE Phone LIKE '" + term + "'"    
        accounts = self.__sf.query_all(query_account)["records"]
        
        if (len(accounts) == 1):
            return accounts[0]['Id']
        else:
            return None


    def get_account_id_from_contact(self, phone):
        term = get_number_term(phone)

        query_contact = "SELECT AccountId FROM Contact WHERE Phone LIKE '" + term + "'"
        contacts = self.__sf.query_all(query_contact)["records"]

        if (len(contacts) == 1):
            return contacts[0]['AccountId']
        elif (len(contacts) > 1):
            account_id = results[0]['AccountId']
            for contact in results:
                if contact['AccountId'] != account_id:
                    return None
            return account_id    
        else:
            return None


    def get_account_id_from_mobile(self, phone):
        term = get_number_term(phone)

        query_mobile = "SELECT AccountId FROM Contact WHERE MobilePhone LIKE '" + term + "'"
        mobiles = self.__sf.query_all(query_mobile)["records"]

        if (len(mobiles) == 1):
            return mobiles[0]['AccountId']
        elif (len(mobiles) > 1):
            account_id = results[0]['AccountId']
            for contact in results:
                if contact['AccountId'] != account_id:
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
        results = self.__sf.query_all(query)["records"]
        
        if (len(results) == 1):
            return results[0]['Id']
        return None
         
