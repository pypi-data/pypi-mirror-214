import json
from datetime import datetime
from .models.email import EmailServiceBusMessage
from azure.servicebus import ServiceBusMessage
from .base_handler import BaseHandler

class Email(BaseHandler):
    messageSchema = EmailServiceBusMessage
    topic = "send-email"

    def build_json(self, id, sender, recipient, email_subject, content, options=None):
        try:
            return json.dumps({
                "specversion": "1.0.0",
                "type": "servicebusevent",
                "id": id,
                "time": datetime.now(),
                "datacontenttype": "application/json",
                "data": {
                    "type": "email",
                    "sender": sender,
                    "recipient": recipient,
                    "email_subject": email_subject,
                    "content": content,
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

