#!/usr/bin/python

from salesforce import SalesForceHandler


class CDRFields(object):
    """
    Store all fields of event CDR (Asterisk event).
    """
    # Fields available
    ACCOUNT_CODE = 'AccountCode'
    DESTINATION_CONTEXT = 'DestinationContext'
    DURATION = 'Duration'
    CALLER_ID = 'CallerID'
    LAST_DATA = 'LastData'
    DESTINATION = 'Destination'
    AMA_FLAGS = 'AMAFlags'
    DISPOSITION = 'Disposition'
    DESTINATION_CHANNEL = 'DestinationChannel'
    SOURCE = 'Source'
    ANSWER_TIME = 'AnswerTime'
    LAST_APPLICATION = 'LastApplication'
    START_TIME = 'StartTime'
    BILLABLE_SECONDS = 'BillableSeconds'
    PRIVILEGE = 'Privilege'
    USER_FIELD = 'UserField'
    END_TIME = 'EndTime'
    EVENT = 'Event'
    CHANNEL = 'Channel'
    UNIQUE_ID = 'UniqueID'

    @classmethod
    def get_account_code(cls, event):
        return event[cls.ACCOUNT_CODE]

    @classmethod
    def get_destination_context(cls, event):
        return event[cls.DESTINATION_CONTEXT]

    @classmethod
    def get_duration(cls, event):
        return event[cls.DURATION]

    @classmethod
    def get_caller_id(cls, event):
        return event[cls.CALLER_ID]

    @classmethod
    def get_last_data(cls, event):
        return event[cls.LAST_DATA]

    @classmethod
    def get_destination(cls, event):
        return event[cls.DESTINATION]

    @classmethod
    def get_ama_flags(cls, event):
        return event[cls.AMA_FLAGS]

    @classmethod
    def get_disposition(cls, event):
        return event[cls.DISPOSITION]

    @classmethod
    def get_destination_channel(cls, event):
        return event[cls.DESTINATION_CHANNEL]

    @classmethod
    def get_source(cls, event):
        return event[cls.SOURCE]

    @classmethod
    def get_answer_time(cls, event):
        return event[cls.ANSWER_TIME]

    @classmethod
    def get_last_application(cls, event):
        return event[cls.LAST_APPLICATION]

    @classmethod
    def get_start_time(cls, event):
        return event[cls.START_TIME]

    @classmethod
    def get_billable_seconds(cls, event):
        return event[cls.BILLABLE_SECONDS]

    @classmethod
    def get_privilege(cls, event):
        return event[cls.PRIVILEGE]

    @classmethod
    def get_user_field(cls, event):
        return event[cls.USER_FIELD]

    @classmethod
    def get_end_time(cls, event):
        return event[cls.END_TIME]

    @classmethod
    def get_channel(cls, event):
        return event[cls.CHANNEL]

    @classmethod
    def get_unique_id(cls, event):
        return event[cls.UNIQUE_ID]


class CDREvent(object):
    """
    Handle CDR event (Asterisk Event).
    """

    def __init__(self):
        self.__sf = SalesForceHandler()

    def handle_internal(self):

        print "============================================================="
        print "from-internal"
        if self.source in self.__extensions:
            name = self.__extensions[self.source]
            user_id = self.__sf.get_user_id(name)
            contacts = self.__sf.get_number_contacts(self.destination)
            accounts = self.__sf.get_number_accounts(self.destination)
            print "Id = %s | Name = %s | Contacts = %d | Accounts = %d" %\
                  (user_id, name, contacts, accounts)
            if (contacts != 1):
                if (accounts == 1):
                    contact_id = self.__sf.get_contact_id(self.destination)
                    account_id = self.__sf.get_account_id(self.destination)
                    print "Contact ID = %s" % contact_id
                    print "Account ID = %s" % account_id
            else:
                contact_id = self.__sf.get_contact_id(self.destination)
                account_id = self.__sf.get_account_id(self.destination)
                print "Contact ID = %s" % contact_id
                print "Account ID = %s" % account_id
        else:
            print "Number does not exist!"
        print "============================================================="

    def handle_external(self):

        print "============================================================="
        print "from-did-direct"
        if self.destination in self.__extensions:
            name = self.__extensions[self.destination]
            user_id = self.__sf.get_user_id(name)
            contacts = self.__sf.get_number_contacts(self.source)
            accounts = self.__sf.get_number_accounts(self.source)
            print "Id = %s | Name = %s | Contacts = %d | Accounts = %d" %\
                  (user_id, name, contacts, accounts)
            if contacts != 1:
                if accounts == 1:
                    contact_id = self.__sf.get_contact_id(self.source)
                    account_id = self.__sf.get_account_id(self.source)
                    print "Contact ID = %s" % contact_id
                    print "Account ID = %s" % account_id
            else:
                contact_id = self.__sf.get_contact_id(self.source)
                account_id = self.__sf.get_account_id(self.source)
                print "Contact ID = %s" % contact_id
                print "Account ID = %s" % account_id
        else:
            print "Number does not exist!"
        print "============================================================="

    def callback(self, event, manager):
        self.duration = self.get_field(event, CDRFields.DURATION)
        self.source = self.get_field(event, CDRFields.SOURCE)
        self.destination = self.get_field(event, CDRFields.DESTINATION)
        self.start_time = self.get_field(event, CDRFields.START_TIME)
        self.end_time = self.get_field(event, CDRFields.END_TIME)
        self.destination_context = self.get_field(
            event,
            CDRFields.DESTINATION_CONTEXT
        )
        self.disposition = self.get_field(event, CDRFields.DISPOSITION)
        print "Disposition = %s" % self.disposition
        if ((self.destination_context == "from-internal") and
           (len(self.destination) > 4) and (self.disposition != "NO ANSWER")):
            self.handle_internal()
        elif (self.destination_context == "from-did-direct"):
            self.handle_external()
        else:
            print "nothing"

    def debug(self, event):
        print ("Received event[%s]" % event.name)
        print "Duration    = %s" % self.get_field(event, CDRFields.DURATION)
        print "Source      = %s" % self.get_field(event, CDRFields.SOURCE)
        print "Destination = %s" % self.get_field(event, CDRFields.DESTINATION)
        print "StartTime   = %s" % self.get_field(event, CDRFields.START_TIME)
        print "EndTime     = %s" % self.get_field(event, CDRFields.END_TIME)
        print "DestinationContext = %s" % self.get_field(
            event,
            CDRFields.DESTINATION_CONTEXT
        )

    def get_field(self, event, field):
        return event[field]

    def set_extensions(self, extensions):
        self.__extensions = extensions
