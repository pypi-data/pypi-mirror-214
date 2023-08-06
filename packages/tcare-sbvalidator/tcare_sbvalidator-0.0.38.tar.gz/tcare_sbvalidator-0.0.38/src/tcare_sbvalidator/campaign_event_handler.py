import json
from datetime import datetime
from .models.campaign_event import CampaignEventServiceBusMessage
from .base_handler import BaseHandler

class Campaign(BaseHandler):
    messageSchema = CampaignEventServiceBusMessage
    topic = "campaign-event"

    def build_json(self, id, trigger, action, campaign_id, case_id, user_id, phone, email, options=None):
        try:
            return json.dumps({
                "specversion": "1.0.0",
                "type": "servicebusevent",
                "id": id,
                "time": datetime.now(),
                "datacontenttype": "application/json",
                "data": {
                    "type": "campaign-event",
                    "trigger": trigger, # i.e 'assist'
                    "action": action, # i.e. 'start'
                    "campaign_id": campaign_id, # i.e. "elevance-1" 
                    "case_id": case_id, # JUST case_id or user_id is probably going to be enough to kick things off
                    "user_id": user_id, # both are likely unecessary
                    "phone": phone,
                    "email": email,
                },
                "options": options,
            }, default=str)
        except Exception as e:
            print(e)

    async def send_campaign_event(self, id, recipient, sender, content, options=None):
        msg = self.build_json(id, recipient, sender, content, options)
        await self.publish_message(msg)