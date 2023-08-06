import asyncio, sys
from dotenv import dotenv_values
config = dotenv_values(".env")

sys.path.append("..")
from src.tcare_sbvalidator.handlers import Campaign
from src.tcare_sbvalidator.models.campaign_event import CampaignEventData, CampaignContactData


NAMESPACE = config['NAMESPACELOCAL']
SMS_RECIPIENT = config['TEST_SMS_RECIPIENT']
EMAIL_RECIPIENT = config['TEST_EMAIL_RECIPIENT']

async def main():
    handler = Campaign()
    handler.connectWithCred(NAMESPACE)
    
    campaign_event_data = CampaignEventData(
      source="assist",
      campaign="elevance-1",
      case_id="1",
      caregiver_id="1",
      first_name="John",
      last_name="Doe",
      action="start",
      contact= [
        CampaignContactData(type="email", contact=EMAIL_RECIPIENT),
        CampaignContactData(type="sms", contact=SMS_RECIPIENT),
      ]
    )
    
    await handler.publish_message(campaign_event_data)

asyncio.run(main())