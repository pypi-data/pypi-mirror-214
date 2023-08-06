import json
from datetime import datetime
from .models.email import EmailServiceBusMessage
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

    async def send_email(self, id, recipient, sender, content, options=None):
        msg = self.build_json(id, recipient, sender, content, options)
        await self.publish_message(msg)