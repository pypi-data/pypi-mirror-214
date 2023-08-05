import json
from datetime import datetime
from .models.sms import SmsServiceBusMessage
from azure.servicebus import ServiceBusMessage
from .base_handler import BaseHandler

class Sms(BaseHandler):
    messageSchema = SmsServiceBusMessage
    topic = "send-sms"

    # Building the standard JSON format for the message and publishing the message are separated
    # But could be combined into a single method later
    def build_json(self, id, recipient, sender, content, options=None):
        try:
            return json.dumps({
                "specversion": "1.0.0",
                "type": "servicebusevent",
                "id": id,
                "time": datetime.now(),
                "datacontenttype": "application/json",
                "data": {
                    "type": "sms",
                    "content": content,
                    "recipient": recipient,
                    "sender": sender
                },
                "options": options,
            }, default=str)
        except Exception as e:
            print(e)

    @BaseHandler.cleanupCred
    async def publish_message(self, message_json):
       async with self.client:
            async with self.client.get_topic_sender(self.topic) as sender:
                msg = ServiceBusMessage(message_json)
                await sender.send_messages(msg)
                print(f"message sent with content: {message_json}")

