import json
from azure.identity.aio import DefaultAzureCredential
from azure.servicebus.aio import ServiceBusClient

class BaseHandler:
    client = None
    cred = None
    messageSchema = None
    
    def validate_json(self, message):
        if not self.messageSchema:
            raise Exception("A class inheriting from BaseHandler is trying to validate without a messageSchema property.")
        parsed_json = json.loads(message)
        return self.messageSchema(**parsed_json)

    def connectWithCred(self, namespace):
        if self.client == None:
            self.cred = DefaultAzureCredential()
            self.client = ServiceBusClient(namespace, self.cred)

    def connectWithString(self, connection_string):
        if self.client == None:
            self.client = ServiceBusClient.from_connection_string(connection_string)

    def cleanupCred(func):
        async def wrapper(*args, **kwargs):
            await func(*args, **kwargs)
            if args[0].cred:
                await args[0].cred.close()
        return wrapper