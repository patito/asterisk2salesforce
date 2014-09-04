#!/usr/bin/python

from salesforce import SalesForceHandler
import datetime


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
    def get_field(cls, event, field):
        if event.has_header(field):
            return event[field]
        else:
            return None

    @classmethod
    def get_account_code(cls, event):
        return cls.get_field(event, cls.ACCOUNT_CODE)

    @classmethod
    def get_destination_context(cls, event):
        return cls.get_field(event, cls.DESTINATION_CONTEXT)

    @classmethod
    def get_duration(cls, event):
        return cls.get_field(event, cls.DURATION)

    @classmethod
    def get_caller_id(cls, event):
        return cls.get_field(event, cls.CALLER_ID)

    @classmethod
    def get_last_data(cls, event):
        return cls.get_field(event, cls.LAST_DATA)

    @classmethod
    def get_destination(cls, event):
        return cls.get_field(event, cls.DESTINATION)

    @classmethod
    def get_ama_flags(cls, event):
        return cls.get_field(event, cls.AMA_FLAGS)

    @classmethod
    def get_disposition(cls, event):
        return cls.get_field(event, cls.DISPOSITION)

    @classmethod
    def get_destination_channel(cls, event):
        return cls.get_field(event, cls.DESTINATION_CHANNEL)

    @classmethod
    def get_source(cls, event):
        return cls.get_field(event, cls.SOURCE)

    @classmethod
    def get_answer_time(cls, event):
        return cls.get_field(event, cls.ANSWER_TIME)

    @classmethod
    def get_last_application(cls, event):
        return cls.get_field(event, cls.LAST_APPLICATION)

    @classmethod
    def get_start_time(cls, event):
        return cls.get_field(event, cls.START_TIME)

    @classmethod
    def get_billable_seconds(cls, event):
        return cls.get_field(event, cls.BILLABLE_SECONDS)

    @classmethod
    def get_privilege(cls, event):
        return cls.get_field(event, cls.PRIVILEGE)

    @classmethod
    def get_user_field(cls, event):
        return cls.get_field(event, cls.USER_FIELD)

    @classmethod
    def get_end_time(cls, event):
        return cls.get_field(event, cls.END_TIME)

    @classmethod
    def get_channel(cls, event):
        return cls.get_field(event, cls.CHANNEL)

    @classmethod
    def get_unique_id(cls, event):
        return cls.get_field(event, cls.UNIQUE_ID)


class CDREvent(object):
    """
    Handle CDR event (Asterisk Event).
    """

    def __init__(self):
        self.__sf = SalesForceHandler()

    def __register_call(self, account_id, contact_id, user_id, summary):
        info = {
            'AccountId': account_id,
            'ContactId': contact_id,
            'UserId': user_id,
            'Summary': summary
        }
        self.__sf.create_task(info)

    def make_summary(self):

        if self.disposition == "NO ANSWER":
            return "No Answer"

        billable_seconds = CDRFields.get_billable_seconds(self.event)
        if self.last_app == "VoiceMail":
            str_time = str(datetime.timedelta(seconds=int(billable_seconds)))
            return "Voicemail: " + str_time

        str_time = str(datetime.timedelta(seconds=int(billable_seconds)))
        return "Duration: " + str_time

    def handle_internal(self):

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
                    self.__register_call(account_id,
                                         contact_id,
                                         user_id,
                                         self.make_summary())
            else:
                contact_id = self.__sf.get_contact_id(self.destination)
                account_id = self.__sf.get_account_id(self.destination)
                self.__register_call(account_id,
                                     contact_id,
                                     user_id,
                                     self.make_summary())
        else:
            print "Number does not exist!"

    def handle_external(self):

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
                    self.__register_call(account_id,
                                         contact_id,
                                         user_id,
                                         self.make_summary())
            else:
                contact_id = self.__sf.get_contact_id(self.source)
                account_id = self.__sf.get_account_id(self.source)
                self.__register_call(account_id,
                                     contact_id,
                                     user_id,
                                     self.make_summary())
        else:
            print "Number does not exist!"

    def save_event_fields(self, event):
        klass = CDRFields
        self.event = event
        self.duration = klass.get_field(event, klass.DURATION)
        self.source = klass.get_field(event, klass.SOURCE)
        self.destination = klass.get_field(event, klass.DESTINATION)
        self.start_time = klass.get_field(event, klass.START_TIME)
        self.end_time = klass.get_field(event, klass.END_TIME)
        self.destination_context = klass.get_field(
            event,
            klass.DESTINATION_CONTEXT
        )
        self.last_app = klass.get_field(event, klass.LAST_APPLICATION)
        self.disposition = klass.get_field(event, klass.DISPOSITION)

    def callback(self, event, manager):
        self.save_event_fields(event)
        self.debug(event)
        if ((self.destination_context == "from-internal") and
           (len(self.destination) > 4) and (self.disposition != "NO ANSWER")):
            self.handle_internal()
        elif (self.destination_context == "from-did-direct"):
            self.handle_external()
        else:
            print "nothing"

    def debug(self, event):
        klass = CDRFields
        print "Received event[%s]" % event.name
        print "Duration    = %s" % klass.get_field(event, klass.DURATION)
        print "Source      = %s" % klass.get_source(event)
        print "Destination = %s" % klass.get_field(event, klass.DESTINATION)
        print "StartTime   = %s" % klass.get_field(event, klass.START_TIME)
        print "EndTime     = %s" % klass.get_field(event, klass.END_TIME)
        print "Disposition = %s" % klass.get_field(event, klass.DISPOSITION)
        print "DestinationContext = %s" % klass.get_field(
            event,
            klass.DESTINATION_CONTEXT
        )

    def set_extensions(self, extensions):
        self.__extensions = extensions
