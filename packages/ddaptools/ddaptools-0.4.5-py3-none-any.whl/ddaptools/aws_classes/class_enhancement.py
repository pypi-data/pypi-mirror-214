
from abc import ABC, abstractmethod
from ddaptools.aws_classes.class_helpers import *
from ddaptools.dda_constants import *
from typing import List
from ddaptools.aws_classes.config_mapper_df import ConfigMapper
import pandas as pd
from ddaptools.dda_models import *
utils = Utils()


class SourceAdapter(ABC):
    """Transformation for Status Types Interfaces, 
    some might come in json or have different namings, the idea is to convert them
    into the standard interfaces.
    """
    @abstractmethod
    def adapt(staging_events: dict)->dict:
        pass

class StatusAdapter(SourceAdapter):
    """Transformation for Status Types Interfaces
    """

    def adapt(staging_events: dict)->dict:
        pass

class MockAdapter(SourceAdapter):
    """Mock Adaptation to be used until the other interfaces work.
    """

    # I will be mocking a standard interface with evertything one could have?
    def __init__(self) -> None:
        super().__init__()
        self.mock_adapt_result ={'guid':'a08f815f-12fa-47fb-9f6d-5c3d7fe53eff','version':'1.0','connector_guid':'365_MANAGEMENT','activity':'','organization_guid':'74d25673-b01c-4211-a7c4-9930610fb7eb','actor':'<CY5PR05MB9143EE143E6008D69C9391F5DD319@CY5PR05MB9143.namprd05.prod.outlook.com>','operation':2,'item_count':5,'details':[{'event_guid':'74d25673-b01c-4211-a7c4-9930610fb7eb','user_guid':'ab3c-asd1-100G','timestamp_utc':'2022-10-24T18:23:36','loadbatch_id':'a08f815f-12fa-47fb-9f6d-5c3d7fe53eff','raw_details':{'CreationTime':'2022-10-24T18:23:36','Id':'c878338a-15ff-4986-8bd3-5d6eac071b4a','Operation':'MipLabel','OrganizationId':'74d25673-b01c-4211-a7c4-9930610fb7eb','RecordType':43,'UserKey':'c397ec65-e71e-493f-94f2-2e53cdd9b02e','UserType':4,'Version':1,'Workload':'Exchange','ObjectId':'<CY5PR05MB9143EE143E6008D69C9391F5DD319@CY5PR05MB9143.namprd05.prod.outlook.com>','UserId':'nelson@o365.devcooks.com','ApplicationMode':'Standard','ItemName':'HelloThere','LabelAction':'None','LabelAppliedDateTime':'2022-10-25T18:23:32','LabelId':'defa4170-0d19-0005-0004-bc88714345d2','LabelName':'AllEmployees(unrestricted)','Receivers':['nwang@ddapfilings.com','wangnelson2@gmail.com'],'Sender':'nelson@o365.devcooks.com'},'application':'Exchange','operation':'MipLabel','version_source_uri':{'id':'','uri':'','file_type':'','file_extension':'','size':0},'source_uri':{'id':'','uri':'','file_type':'','file_extension':'','size':0}},{'event_guid':'74d25673-b01c-4211-a7c4-9930610fb7eb','user_guid':'ab3c-asd1-100G','timestamp_utc':'2022-10-25T18:23:36','loadbatch_id':'a08f815f-12fa-47fb-9f6d-5c3d7fe53eff','raw_details':{'CreationTime':'2022-10-25T18:23:36','Id':'c17eedb7-6977-4169-b625-bb26e0ede079','Operation':'MipLabel','OrganizationId':'74d25673-b01c-4211-a7c4-9930610fb7eb','RecordType':13,'UserKey':'c397ec65-e71e-493f-94f2-2e53cdd9b02e','UserType':4,'Version':1,'Workload':'Exchange','ObjectId':'<CY5PR05MB9143EE143E6008D69C9391F5DD319@CY5PR05MB9143.namprd05.prod.outlook.com>','UserId':'nelson@o365.devcooks.com','IncidentId':'11bb1d67-ae3d-d176-4000-08dab6b85275','PolicyDetails':[{'PolicyId':'00000000-0000-0000-0000-000000000000','Rules':[{'Actions':[],'ConditionsMatched':{'ConditionMatchedInNewScheme':True,'OtherConditions':[{'Name':'SensitivityLabels','Value':'defa4170-0d19-0005-0004-bc88714345d2'}]},'RuleId':'defa4170-0d19-0005-0004-bc88714345d2','RuleMode':'Enable','RuleName':'defa4170-0d19-0005-0004-bc88714345d2','Severity':'Low'}]}],'SensitiveInfoDetectionIsIncluded':False,'ExchangeMetaData':{'BCC':[],'CC':[],'FileSize':17579,'From':'nelson@o365.devcooks.com','MessageID':'<CY5PR05MB9143EE143E6008D69C9391F5DD319@CY5PR05MB9143.namprd05.prod.outlook.com>','RecipientCount':2,'Sent':'2022-10-25T18:23:33','Subject':'HelloThere','To':['nwang@ddapfilings.com','wangnelson2@gmail.com'],'UniqueID':'fe03264d-a22d-4c70-57b1-08dab6b60675'}},'application':'Exchange','operation':'MipLabel','version_source_uri':{'id':'','uri':'','file_type':'','file_extension':'','size':0},'source_uri':{'id':'','uri':'','file_type':'','file_extension':'','size':0}},{'event_guid':'74d25673-b01c-4211-a7c4-9930610fb7eb','user_guid':'ab3c-asd1-100G','timestamp_utc':'2022-10-25T18:23:33','loadbatch_id':'a08f815f-12fa-47fb-9f6d-5c3d7fe53eff','raw_details':{'CreationTime':'2022-10-25T18:23:33','Id':'e01bd1fb-a635-4f09-57b1-08dab6b60675','Operation':'Send','OrganizationId':'74d25673-b01c-4211-a7c4-9930610fb7eb','RecordType':2,'ResultStatus':'Succeeded','UserKey':'10032002359E261F','UserType':0,'Version':1,'Workload':'Exchange','ClientIP':'68.160.247.154','UserId':'nelson@o365.devcooks.com','AppId':'00000002-0000-0ff1-ce00-000000000000','ClientIPAddress':'68.160.247.154','ClientInfoString':'Client=OWA;Action=ViaProxy','ExternalAccess':False,'InternalLogonType':0,'LogonType':0,'LogonUserSid':'S-1-5-21-3007612343-326144747-4028531239-4420872','MailboxGuid':'bd6abed2-5d3b-4206-aada-31ca71605e63','MailboxOwnerSid':'S-1-5-21-3007612343-326144747-4028531239-4420872','MailboxOwnerUPN':'nelson@o365.devcooks.com','OrganizationName':'devcooks.onmicrosoft.com','OriginatingServer':'CY5PR05MB9143(15.20.4200.000)\r\n','SessionId':'e01c84f0-8db1-439e-87bc-5ee52fdf90d4','Item':{'Id':'Unknown','InternetMessageId':'<CY5PR05MB9143EE143E6008D69C9391F5DD319@CY5PR05MB9143.namprd05.prod.outlook.com>','ParentFolder':{'Id':'LgAAAAALcWhVmnTeRJS8qp8HxA25AQC/yWJ3KK0XQJ7UyikjUZtEAAAAAAEPAAAB','Path':'\\Drafts'},'SizeInBytes':3991,'Subject':'HelloThere'}},'application':'Exchange','operation':'Send','version_source_uri':{'id':'','uri':'','file_type':'','file_extension':'','size':0},'source_uri':{'id':'','uri':'','file_type':'','file_extension':'','size':0}},{'event_guid':'74d25673-b01c-4211-a7c4-9930610fb7eb','user_guid':'ab3c-asd1-100G','timestamp_utc':'2022-10-25T18:23:04','loadbatch_id':'a08f815f-12fa-47fb-9f6d-5c3d7fe53eff','raw_details':{'CreationTime':'2022-10-25T18:23:04','Id':'daf566de-6581-486c-b9f7-f8df1d07457f','Operation':'MailItemsAccessed','OrganizationId':'74d25673-b01c-4211-a7c4-9930610fb7eb','RecordType':50,'ResultStatus':'Succeeded','UserKey':'10032002359E261F','UserType':0,'Version':1,'Workload':'Exchange','UserId':'nelson@o365.devcooks.com','AppId':'00000002-0000-0ff1-ce00-000000000000','ClientIPAddress':'68.160.247.154','ClientInfoString':'Client=OWA;Action=ViaProxy','ExternalAccess':False,'InternalLogonType':0,'LogonType':0,'LogonUserSid':'S-1-5-21-3007612343-326144747-4028531239-4420872','MailboxGuid':'bd6abed2-5d3b-4206-aada-31ca71605e63','MailboxOwnerSid':'S-1-5-21-3007612343-326144747-4028531239-4420872','MailboxOwnerUPN':'nelson@o365.devcooks.com','OperationProperties':[{'Name':'MailAccessType','Value':'Bind'},{'Name':'IsThrottled','Value':'False'}],'OrganizationName':'devcooks.onmicrosoft.com','OriginatingServer':'CY5PR05MB9143(15.20.4200.000)\r\n','SessionId':'e01c84f0-8db1-439e-87bc-5ee52fdf90d4','Folders':[{'FolderItems':[{'InternetMessageId':'<ceafc3fa-fd0a-46ba-9754-e033ee56ce75@az.westcentralus.production.microsoft.com>'},{'InternetMessageId':'<ae042a57-4cd4-466a-adf0-417549c30a96@az.westeurope.production.microsoft.com>'},{'InternetMessageId':'<abccdb15-1bd4-476f-88f8-0bde5349cb61@az.westus2.production.microsoft.com>'},{'InternetMessageId':'<5c06433f-d7f6-48c7-8752-72f5cf93011c@az.westus.production.microsoft.com>'}],'Id':'LgAAAAALcWhVmnTeRJS8qp8HxA25AQC/yWJ3KK0XQJ7UyikjUZtEAAAAAAEMAAAB','Path':'\\Inbox'},{'FolderItems':[{'InternetMessageId':'<CY5PR05MB91439309823940F866A9629EDD2E9@CY5PR05MB9143.namprd05.prod.outlook.com>'},{'InternetMessageId':'<CY5PR05MB9143FB7EF878879EED5FC05CDD2D9@CY5PR05MB9143.namprd05.prod.outlook.com>'},{'InternetMessageId':'<CY5PR05MB91439292F10817DCB3DE6FC6DD2D9@CY5PR05MB9143.namprd05.prod.outlook.com>'},{'InternetMessageId':'<CY5PR05MB91436B02DD20921A28720BA4DD2D9@CY5PR05MB9143.namprd05.prod.outlook.com>'}],'Id':'LgAAAAALcWhVmnTeRJS8qp8HxA25AQC/yWJ3KK0XQJ7UyikjUZtEAAAAAAEJAAAB','Path':'\\SentItems'}],'OperationCount':8},'application':'Exchange','operation':'MailItemsAccessed','version_source_uri':{'id':'','uri':'','file_type':'','file_extension':'','size':0},'source_uri':{'id':'','uri':'','file_type':'','file_extension':'','size':0}},{'event_guid':'74d25673-b01c-4211-a7c4-9930610fb7eb','user_guid':'ab3c-asd1-100G','timestamp_utc':'2022-10-25T18:23:41','loadbatch_id':'a08f815f-12fa-47fb-9f6d-5c3d7fe53eff','raw_details':{'CreationTime':'2022-10-25T18:23:41','Id':'0d77eaad-2ddd-4e39-8ce1-469113caf263','Operation':'MailItemsAccessed','OrganizationId':'74d25673-b01c-4211-a7c4-9930610fb7eb','RecordType':50,'ResultStatus':'Succeeded','UserKey':'10032002359E261F','UserType':0,'Version':1,'Workload':'Exchange','UserId':'nelson@o365.devcooks.com','AppId':'13937bba-652e-4c46-b222-3003f4d1ff97','ClientAppId':'13937bba-652e-4c46-b222-3003f4d1ff97','ClientIPAddress':'2603:10b6:930:3d::7','ClientInfoString':'Client=REST;Client=RESTSystem;;','ExternalAccess':False,'InternalLogonType':0,'LogonType':0,'LogonUserSid':'S-1-5-21-3007612343-326144747-4028531239-4420872','MailboxGuid':'bd6abed2-5d3b-4206-aada-31ca71605e63','MailboxOwnerSid':'S-1-5-21-3007612343-326144747-4028531239-4420872','MailboxOwnerUPN':'nelson@o365.devcooks.com','OperationProperties':[{'Name':'MailAccessType','Value':'Bind'},{'Name':'IsThrottled','Value':'False'}],'OrganizationName':'devcooks.onmicrosoft.com','OriginatingServer':'CY5PR05MB9143(15.20.4200.000)\r\n','Folders':[{'FolderItems':[{'InternetMessageId':'<CY5PR05MB9143EE143E6008D69C9391F5DD319@CY5PR05MB9143.namprd05.prod.outlook.com>'}],'Id':'LgAAAAALcWhVmnTeRJS8qp8HxA25AQC/yWJ3KK0XQJ7UyikjUZtEAAAAAAEJAAAB','Path':'\\SentItems'}],'OperationCount':1},'application':'Exchange','operation':'MailItemsAccessed','version_source_uri':{'id':'','uri':'','file_type':'','file_extension':'','size':0},'source_uri':{'id':'','uri':'','file_type':'','file_extension':'','size':0}}],'hash_1':'','hash_2':''}

    def adapt(self, staging_events: dict)->dict:
        return self.mock_adapt_result



class SalesforceAdapter(SourceAdapter):

    def __init__(self, organizationQuerier: OrganizationalQuerier):
        self.organizationQuerier = organizationQuerier
        self.platform_id = 1

    def adapt(self, staging_events: dict)->dict:
        """Staging event (with 365 details into 365 adapted source.)
        Args:
            staging_events (dict): Converted Staging event.
        """

        management_api = StagingModel()
        management_api.populate_properties_from_dict(staging_events)
        
        # Get the organizations profile per Actor as key for the information
        # {__actor_nelson: {user_id: 1, user_organization_id: ..,  }}
        organization_params_salesforce  = self.organizationQuerier.getOrganizationParameters_salesforce(
            orgnaization_guid_salesforce=management_api.organization_guid
        )


        # Building the right interface
        new_details = []
        
        for event in management_api.details:
            user_key_salesforce = Utils.NoneSafe(event, "Actor__c")
            user_profile = organization_params_salesforce[user_key_salesforce]
            
            # Repeated variables
            timestamp = Utils.NoneSafe(event, "ActionDate__c")

            fileEvent = EventData(
                user_id=Utils.NoneSafe(user_profile, "user_id"),
                organization_guid=management_api.organization_guid,
                application="SALESFORCE",
                app="SALESFORCE",
                app_type=None,
                operation=Utils.NoneSafe(event, "Activity__c"),
                operation_type=None,
                staging_details_guid=Utils.NoneSafe(event, "Id"),
                staging_guid=management_api.guid,
                platform_id=self.platform_id,
                organization_id=None,
                local_timezone=None,
                timestamp=timestamp,
                end_time=None,
                timestamp_local=None,
                end_time_local=None,
                duration=None,
                description=Utils.NoneSafe(event, "Description__c"),
                title=Utils.NoneSafe(event, "Object__c"),
                url=Utils.NoneSafe(event, "URL__c"),
                site=None,
                url_domain=Utils.NoneSafe(event, "Record_Link__c"),
                files=None,
                file_count=None,
                action_type="ACTIVE",
                geolocation=None,
                ipv4=None,
                local_ipv4=None,
                size=None,
                sha2=None,
                email_subject=None,
                from_address=None,
                to_address=None,
                email_bcc=None,
                email_cc=None,
                email_imid=None,
                phone_result=None,
                record_url=Utils.NoneSafe(event, "Record_Link__c"),
                recording_url=None,
                record_id=Utils.NoneSafe(event, "RecordId__c")
            )
            new_details.append(fileEvent)
        management_api.details = new_details
        return management_api.to_dict()


class ChromeAdapter(SourceAdapter):
    
    def __init__(self, organizationQuerier: OrganizationalQuerier):
        self.organizationQuerier = organizationQuerier
        self.platform_id = 2

    def adapt(self, staging_events: dict)->dict:
        
        management_api = StagingModel()
        management_api.populate_properties_from_dict(staging_events)
        
        # Get the organizations profile per Actor as key for the information
        # {__actor_nelson: {user_id: 1, user_organization_id: ..,  }}
        organization_and_user_params  = self.organizationQuerier.getOrganizationParameters_connectorguid(
            management_api.connector_guid
        )
        # print("organization_and_user_params", organization_and_user_params)

        # Building the right interface
        new_details = []
        
        for event in management_api.details:
            user_profile = organization_and_user_params["user_profile"]
            
            # Repeated variables
            timestamp = Utils.NoneSafe(event, "timestamp")
            files = Utils.NoneSafe(event, "files")

            def aggregateFileSizes(files):
                
                if(files is None):
                    return 0
                
                total_size = 0
                for file in files:
                    total_size += Utils.NoneSafe(file, "size", 0)
                return total_size
            
            def eventActiveStatus(event):
                """Determines if the event ACTIVITY Status for Chrome Extension if the type it will return ACTIVE unless the event type is idle
                Passive if it is download or upload

                Args:
                    event (str): Event  should contain type key.

                Returns:
                    str: ACTIVE | IDLE | PASSIVE
                """
                # if the type is idle, then it is IDLE
                event_type = Utils.NoneSafe(event, "type")

                if(event_type == "idle"): return "IDLE"
                if(event_type == "download"): return "PASSIVE"
                if(event_type == "upload"): return "PASSIVE"
                return "ACTIVE"
                
            def getSumFeats(dictObject, *args):
                """
                Get the sum of numeric values for the specified keys from the dictionary.
                """
                total = 0
                for key in args:
                    value = dictObject.get(key)
                    if isinstance(value, (int, float)):
                        total += value
                return total
                

            fileEvent = EventData(
                user_id=Utils.NoneSafe(user_profile, "user_id"),
                organization_guid=management_api.organization_guid,
                application="CHROME",
                app=Utils.NoneSafe(event, "domain"),
                app_type=None,
                operation=Utils.NoneSafe(event, "type"),
                operation_type=None,
                staging_details_guid=Utils.NoneSafe(event, "guid"),
                staging_guid=management_api.guid,
                platform_id=self.platform_id,
                organization_id=Utils.NoneSafe(user_profile, "user_organization_id"),
                local_timezone=Utils.NoneSafe(user_profile, "user_timezone"),
                timestamp=timestamp,
                end_time=Utils.NoneSafe(event, "endTime"),
                timestamp_local=None,
                end_time_local=None,
                duration=None,
                description=Utils.NoneSafe(event, "interactions"),
                title=Utils.NoneSafe(event, "title"),
                url=Utils.NoneSafe(event, "url"),
                site=Utils.NoneSafe(event, "domain"),
                url_domain=Utils.NoneSafe(event, "domain"),
                files=files,
                file_count= len(files) if files is not None else 0,
                action_type=eventActiveStatus(event),
                geolocation=None,
                ipv4=None,
                local_ipv4=None,
                size=aggregateFileSizes(files),
                sha2=None,
                email_subject=None,
                from_address=None,
                to_address=None,
                email_bcc=None,
                email_cc=None,
                email_imid=None,
                phone_result=None,
                record_url=None,
                recording_url=None,
                record_id=None,
                keystrokes=getSumFeats(event, "keyboard"),
                mouse_clicks=getSumFeats(event, " auxclick", "click", ", dbclick")

            )
            new_details.append(fileEvent)
        management_api.details = new_details
        return management_api.to_dict()

class WindowsAdapter(SourceAdapter):
    """
    Adapter for windows events
    """
    
    def __init__(self, organizationQuerier: OrganizationalQuerier):
        self.organizationQuerier = organizationQuerier
        self.platform_id = 3

    def adapt(self, staging_events: dict)->dict:
        
        management_api = StagingModel()
        management_api.populate_properties_from_dict(staging_events)
        
        # Get the organizations profile per Actor as key for the information
        # {__actor_nelson: {user_id: 1, user_organization_id: ..,  }}
        organization_and_user_params  = self.organizationQuerier.getOrganizationParameters_connectorguid(
            management_api.connector_guid
        )

        # Building the right interface
        new_details = []


        # Some custom functions
        def aggregateFileSizes(files):
            
            if(files is None):
                return 0
            
            total_size = 0
            for file in files:
                total_size += Utils.NoneSafe(file, "size", 0)
                
            return total_size
        
        def createDescription(event):
            """Adds keypress and mouseclicks """
            return Utils.NoneSafe("keypress", event) + Utils.NoneSafe("mouseclick", event)
        
        def eventActiveStatus(event):
            """Determines if the event ACTIVITY Status for Chrome Extension

            Args:
                event (str): Event Active Status

            Returns:
                str: ACTIVE | PASSOVE
            """
            keypresses = Utils.NoneSafe(event, "keypress")
            mouseclicks = Utils.NoneSafe(event, "mouseclick")

            
            count_activity = keypresses + mouseclicks

            # if the keys are more than 0, then it is active
            if count_activity > 0:
                return "ACTIVE"
            else:
                return "PASSIVE"
        
        for event_raw_str in management_api.details:

            try:
                user_profile = organization_and_user_params["user_profile"]
                # It seems that each event is a string here => Convert into json
                event = json.loads(event_raw_str)
                
                # Repeated variables
                timestamp = Utils.NoneSafe(event, "event_date")
                files = Utils.NoneSafe(event, "files")

                network_interface_json = Utils.NoneSafe(event, "network_interface")
                network_interface_dict = json.loads(network_interface_json) if network_interface_json is not None else {}
                
                # print("event individual =>", type(event), event)

                fileEvent = EventData(
                    user_id=Utils.NoneSafe(user_profile, "user_id"),
                    organization_guid=management_api.organization_guid,
                    application=Utils.NoneSafe(event, "process"),
                    app=Utils.NoneSafe(event, "process"),
                    app_type=None,
                    operation=Utils.NoneSafe(event, "event_type"),
                    operation_type=None,
                    staging_details_guid=Utils.NoneSafe(event, "guid"),
                    staging_guid=management_api.guid,
                    platform_id=self.platform_id,
                    organization_id=Utils.NoneSafe(user_profile, "organization_id"),
                    local_timezone=Utils.NoneSafe(user_profile, "user_timezone"),
                    timestamp=timestamp,
                    end_time=Utils.NoneSafe(event, "event_end_date"),
                    timestamp_local=None,
                    end_time_local=None,
                    duration=None,
                    description=None, #createDescription(event),
                    title=Utils.NoneSafe(event, "title"),
                    url=None,
                    site=None, 
                    url_domain=None,
                    files=None,
                    file_count= None,
                    action_type=None, # eventActiveStatus(event),
                    geolocation=Utils.NoneSafe(event, "location"),
                    ipv4=None, #Utils.NoneSafe(network_interface_dict, "ipv4"),
                    local_ipv4=None,
                    size=None,
                    sha2=None,
                    email_subject=None,
                    from_address=None,
                    to_address=None,
                    email_bcc=None,
                    email_cc=None,
                    email_imid=None,
                    phone_result=None,
                    record_url=None,
                    recording_url=None,
                    record_id=None,
                    keystrokes=Utils.NoneSafe(event, "keypress", 0),
                    mouse_clicks=Utils.NoneSafe(event, "mouseclicks", 0)
                )
                new_details.append(fileEvent)
            except Exception as e:
                # print(e)
                # print("Error in Windows Adapter")
                # print(event)
                continue
        management_api.details = new_details
        return management_api.to_dict()


class TransformationStrategy(ABC):
    """Transformation Strategy to be implemented
    """
    
    @abstractmethod
    def publish(self, enhanced_events: List[dict]):
        pass


    @abstractmethod
    def transform(self, staging_events_events: List[dict]) -> List[dict]: 
        pass

class BasicEnhancement(TransformationStrategy):
    """
    Basic Enhancemnts involves the following:
    (1) Update based on the appropriate source
    (2) Enhance it using the specific business specifications
    (3) Publish it into the events database
    """
    
    def __init__(self, source_adapter, organizationDBProvider: OrganizationalQuerier, publishingDBProvider: DatabaseProvider):
        

        self.organizationDBProvider = organizationDBProvider
        self.publishingDBProvider = publishingDBProvider
        self.default_source_adapter = source_adapter
        
        self.businessRules = {} # To be populated when enhancements is requested.
        


    def transform(self, staging_events_events: List[dict]) -> dict["events": List[Event], "timeslots": List[Timeslot]]: 
        standarized_events:StagingModel = self.adapt(staging_events_events)
        enhanced_events: dict["events": List[Event], "timeslots": List[Timeslot]] = self.businessEnhancements(standarized_events)

        return enhanced_events
    
    def separateEvent(self, events: List[dict]) -> dict:
        """
            produce two list of events:
            (1) events mapped
            (2) timeslot mappedimage.png
            In the future there is another process that also cretes the timeslots separated on between.
            @param events: List of events in format of dict with the same properties of EventData model.
            @return: dict of events and timeslots: dict{event: List[Event], timeslot: List[Timeslot]}
        """
        events_list = []
        timeslots_list = []

        for event in events:
            # If there is duration not None and more than 0 then it means that it can produce a timeslot
            # if(event["duration"] is not None and event["duration"] > 0):
                # new_timeslot = Timeslot.from_dict(event)
            eventData = Utils.eventDataIntoTimeSlots(event)
            timeslots_list.extend(eventData)
            
            # Always create an event based event.
            new_event = Event.from_dict(event)
            events_list.append(new_event.to_dict())

        # print("1 | events_list", len(events_list), "timeslots_list", len(timeslots_list))
        return {
            "events": events_list,
            "timeslots": timeslots_list
        }


    def businessEnhancements(self, events: StagingModel) -> dict["events": List[Event], "timeslots": List[Timeslot]]:
        """
        Args:
            events (dict): events of the business enhancment.

        Returns:
            @return: dict of events and timeslots: dict{event: List[Event], timeslot: List[Timeslot]}
        """
        # TODO Business Enhancments (Import the tested and proven business enhancements)
        # Basic Enhancemnets (Assume they it had been already denormalized. )
        normalized_events: List[dict] = ConfigMapper.event_normalization(events)

        # organization_params: List[dict] = self.organizationDBProvider.getOrganizationParameters(normalized_events[0]['user_guid'])
        organization_params: List[dict] = self.organizationDBProvider.getOrganizationParametersByOrganizationID(normalized_events[0]["organization_id"])
        joint_events = ConfigMapper.join_organization_fields(
            normalized_events=normalized_events,
            user_information_table=organization_params
        )
        date_mapped_events = ConfigMapper.date_related_population(join_events=joint_events)
        

        # Convert into pandas first.
        # date_mapped_events_df = pd.DataFrame(date_mapped_events)
        processed_events = ConfigMapper.categorization_jobs(date_mapped_events=date_mapped_events)
        # processed_events = classified_events_df
        
        # Have the separatation between events and timeslots
        # print("2 | events_list", len(processed_events["evemts"]), "timeslots_list", len(processed_events["timeslots"]))
        return self.separateEvent(processed_events)



    def adapt(self, staging_events: dict) -> dict:
        return self.default_source_adapter.adapt(staging_events = staging_events)

    
    def publish(self, enhanced_events: List[dict], table_name=""):
        self.publishingDBProvider.publish(enhanced_events, table_name=table_name)

    def fetchBusinessRules():
        """Using the self.organizationDBProvider it receives and updates the Dataset
        """
        pass

class CommonProcessor():
    """
    v1 of the Common processor for enhancements, basic transformations into specific interfaces.
    using what it knows about the job type. Receives job parameters from SQS to run those jobs
    
    """
    
    def __init__(self, publishingDBProvider: DatabaseProvider, organization_provider: OrganizationalQuerier, job_parameters: dict):
            
        self.publishingDBProvider = publishingDBProvider
        self.job_parameters = job_parameters
        self.organization_provider = organization_provider
        self.transformation_strategy: TransformationStrategy = self.getTransformationStrategy()

    def runJobs(self):
        """Runs the jobs it was instantiated with.
        """
        events: List[dict] = self.getStagingEvents()
        enhanced_events: List[dict] = self.transformation_strategy.transform(events)
        assert(isinstance(enhanced_events, List))
        self.transformation_strategy.publish(enhanced_events=enhanced_events)

    def getStagingEvents(self) -> List[dict]:
        """Depending on the job parameters it receives the events from either The Provider and either Table.
        I am as
        """
        credentials = {}
        settings = {}
        map_staging_events_source_db = {
            "MOCK_EVENTS": MockStagingDatabaseProviderPrePopulated
        }
        sourceDBProvider = map_staging_events_source_db[self.job_parameters[STAGING_EVENTS_SOURCE]](credentials=credentials, settings=settings)
        staging_event_body = sourceDBProvider.getOne(key_value=self.job_parameters[EVENT_GUID])
        return staging_event_body[DETAILS]


    def getTransformationStrategy(self) -> TransformationStrategy:
        """Understands what type of job to perform depending on the event's type
        """
        
        map_enhancemnettype_TransformationStrategy = {
            'MOCK': BasicEnhancement,
        } #Careful, only one that shouldnt be initialized

        map_source_to_sourceadapter = {
            "MOCK_ADAPTER": MockAdapter,
        }


        transformationStrategyClass = map_enhancemnettype_TransformationStrategy[self.job_parameters[ENHANCEMENT_TYPE]]
        source_adapter_to_use = map_source_to_sourceadapter[self.job_parameters[SOURCE]]
        transformationStrategy = transformationStrategyClass(
            organizationDBProvider=self.organization_provider,
            publishingDBProvider=self.publishingDBProvider,
            source_adapter=source_adapter_to_use()
        )
        return transformationStrategy


    def getTransformationStrategy(self, staging_event) -> TransformationStrategy:
        """Understanding the transformation that is provided by the item. We want to make the transformation later on.
        The idea is toreceive the getTransformationStrategy on the project.

        Returns:
            TransformationStrategy: _description_
        """
        if(staging_event.type == ""):
            pass
        
class BetterCommonProcessor():
    """
    v2 of the common processor.
    Fixes:
    - Now it can predict whether is a chrome adapter required or the another by reading teh start of the connector guid. It should actually work
    duty: Receives a simple database provider, and querier. the job parameter accepted is as follows Map<String, String>{event_guid: string}
    """
    def __init__(self, publishingDBProvider: DatabaseProvider, organization_provider: OrganizationalQuerier, job_parameters: dict):
        self.publishingDBProvider = publishingDBProvider
        self.job_parameters = job_parameters

        # Because we dont know how it will look on the future, it would look like { event_guid }
        self.organization_provider = organization_provider

    def runJobs(self):
        """Runs the jobs it was instantiated with. by analizing first which is the job type required
        """
        specific_staging_event: List[dict] = self.getStagingEvent()
        transformationStrategy = self.getTransformationStrategy(specific_staging_event)
        enhanced_events: List[dict] = transformationStrategy.transform(specific_staging_event)
        transformationStrategy.publish(enhanced_events=enhanced_events)

    def getStagingEvent(self) -> List[dict]:
        """Depending on the job parameters it receives the events from either The Provider and either Table.
        I am as
        """
        staging_event_body = self.publishingDBProvider.getOne(key_value=self.job_parameters[EVENT_GUID]) # Gets the first one with that GUID
        return staging_event_body
    
    def getTransformationStrategy(self, staging_event) -> TransformationStrategy:
        """Understanding the transformation that is provided by the item. We want to make the transformation later on.
        The idea is toreceive the getTransformationStrategy on the project.
        """

        # For now I can dummy return Chrom Basic enhancer
        # If connector guid starts with chrome then use Chrome adapter
        
        adapter = ChromeAdapter(organizationQuerier=self.organization_provider)

        if(staging_event[CONNECTOR_GUID].startswith("chrome")):
            adapter = ChromeAdapter(organizationQuerier=self.organization_provider)
        else:
            adapter = SalesforceAdapter(organizationQuerier=self.organization_provider)

        basic_enhancment = BasicEnhancement(
            organizationDBProvider=self.organization_provider,
            publishingDBProvider=self.publishingDBProvider,
            source_adapter=adapter
        )

        return basic_enhancment

        
class PlatformIDBasedCommonProcessor():
    """v3 of the common processor
    Fixes:
    - Now it lookups the platformId and a basic dictionary to pickup the right adapter 
    """
    def __init__(self, publishingDBProvider: DatabaseProvider, organization_provider: OrganizationalQuerier, job_parameters: dict):
        self.publishingDBProvider = publishingDBProvider
        self.job_parameters = job_parameters

        # Because we dont know how it will look on the future, it would look like { event_guid }
        self.organization_provider = organization_provider

    def runJobs(self):
        """Runs the jobs it was instantiated with. by analizing first which is the job type required
        """
        specific_staging_event: List[dict] = self.getStagingEvent()
        transformationStrategy = self.getTransformationStrategy(specific_staging_event)
        enhanced_events: List[dict] = transformationStrategy.transform(specific_staging_event)
        transformationStrategy.publish(enhanced_events=enhanced_events)

    def getStagingEvent(self) -> List[dict]:
        """Depending on the job parameters it receives the events from either The Provider and either Table.
        I am as
        """
        staging_event_body = self.publishingDBProvider.getOne(key_value=self.job_parameters[EVENT_GUID]) # Gets the first one with that GUID
        return staging_event_body
    
    def getTransformationStrategy(self, staging_event) -> TransformationStrategy:
        """Understanding the transformation that is provided by the item. We want to make the transformation later on.
        The idea is toreceive the getTransformationStrategy on the project.
        """

        # For now I can dummy return Chrom Basic enhancer
        # If connector guid starts with chrome then use Chrome adapter
        adapter_map = {
            1: SalesforceAdapter,
            2: ChromeAdapter,
            3: WindowsAdapter
        }
        PLATFORM_ID = "platformId"
        
        adapter = ChromeAdapter(organizationQuerier=self.organization_provider) # Default adapter
        
        adapter_id = staging_event[PLATFORM_ID]
        if (adapter_id in adapter_map):
            adapter = adapter_map[adapter_id](organizationQuerier=self.organization_provider)
            

        basic_enhancment = BasicEnhancement(
            organizationDBProvider=self.organization_provider,
            publishingDBProvider=self.publishingDBProvider,
            source_adapter=adapter
        )

        return basic_enhancment


 
class ConnecToGUIDHarcodedDictBasedCommonProcessor():
    """v4 of the common processor
    Fixes:
    - Now it lookups the connectorGUID on the basic hardcoded dictionary and a basic dictionary to pickup the right adapter 
    """
    def __init__(self, publishingDBProvider: DatabaseProvider, organization_provider: OrganizationalQuerier, job_parameters: dict):
        self.publishingDBProvider = publishingDBProvider
        self.job_parameters = job_parameters

        # Because we dont know how it will look on the future, it would look like { event_guid }
        self.organization_provider = organization_provider

    def runJobs(self):
        """Runs the jobs it was instantiated with. by analizing first which is the job type required
        """
        specific_staging_event: List[dict] = self.getStagingEvent()
        transformationStrategy = self.getTransformationStrategy(specific_staging_event)
        enhanced_events: List[dict] = transformationStrategy.transform(specific_staging_event)
        transformationStrategy.publish(enhanced_events=enhanced_events)

    def getStagingEvent(self) -> List[dict]:
        """Depending on the job parameters it receives the events from either The Provider and either Table.
        I am as
        """
        staging_event_body = self.publishingDBProvider.getOne(key_value=self.job_parameters[EVENT_GUID]) # Gets the first one with that GUID
        return staging_event_body
    
    def getTransformationStrategy(self, staging_event) -> TransformationStrategy:
        """Understanding the transformation that is provided by the item. We want to make the transformation later on.
        The idea is toreceive the getTransformationStrategy on the project.
        """

        # For now I can dummy return Chrom Basic enhancer
        # If connector guid starts with chrome then use Chrome adapter
        adapter_map = {
            "salesforce-connector": SalesforceAdapter,
            "chrome-extension-ddap-1": ChromeAdapter,
            3: WindowsAdapter
        }
        
        adapter = ChromeAdapter(organizationQuerier=self.organization_provider) # Default adapter
        print("staging_event => ", staging_event)
        adapter_id = staging_event[CONNECTOR_GUID]
        if (adapter_id in adapter_map):
            adapter = adapter_map[adapter_id](organizationQuerier=self.organization_provider)
            

        basic_enhancment = BasicEnhancement(
            organizationDBProvider=self.organization_provider,
            publishingDBProvider=self.publishingDBProvider,
            source_adapter=adapter
        )

        return basic_enhancment













