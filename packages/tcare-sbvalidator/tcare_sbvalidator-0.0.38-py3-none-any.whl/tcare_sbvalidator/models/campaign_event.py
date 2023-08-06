from .tcare_cloud_event import TcareCloudEvent
from pydantic import BaseModel

# SMS
class CampaignEventData(BaseModel):
    type: str
    trigger: str
    action: str # i.e., start, end, etc.
    campaign_id: str
    case_id: str
    user_id: str
    phone: str
    email: str

class CampaignEventServiceBusMessage(TcareCloudEvent):
    data: CampaignEventData