import json
from datetime import datetime
from .models.sms import SmsServiceBusMessage
from .base_handler import BaseHandler

class Sms(BaseHandler):
    messageSchema = SmsServiceBusMessage
    topic = "send-sms"

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
    
    async def send_sms(self, id, recipient, sender, content):
        msg = self.build_json(self, id, recipient, sender, content)
        self.publish_message(msg)