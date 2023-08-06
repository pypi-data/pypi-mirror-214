import json
from azure.identity.aio import DefaultAzureCredential
from azure.servicebus.aio import ServiceBusClient
from azure.servicebus import ServiceBusMessage
from azure.servicebus.exceptions import ServiceBusAuthenticationError

# def cleanupCred(func):
#     async def wrapper(*args, **kwargs):
#         await func(*args, **kwargs)
#         if args[0].cred:
#             await args[0].cred.close()
#     return wrapper

class BaseHandler:
    client = None
    messageSchema = None
    
    def validate_json(self, message):
        if not self.messageSchema:
            raise Exception("A class inheriting from BaseHandler is trying to validate without a messageSchema property.")
        parsed_json = json.loads(message)
        return self.messageSchema(**parsed_json)

    def connectWithCred(self, namespace):
        cred = DefaultAzureCredential()
        self.client = ServiceBusClient(namespace, cred)

    def connectWithString(self, connection_string):
        self.client = ServiceBusClient.from_connection_string(connection_string)
    
    # @cleanupCred
    async def publish_message(self, message_json):
        try:
            sender = self.client.get_topic_sender(self.topic)
            msg = ServiceBusMessage(message_json)
            await sender.send_messages(msg)
            print(f"message sent with content: {message_json}")
        except ServiceBusAuthenticationError as e:
            print(f"Make sure that {self.topic} is a valid topic.", e)
        except Exception as e:
            print(f"There was a problem publishing message: {e}")
        finally:
            return self.client
