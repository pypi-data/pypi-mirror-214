from .tcare_cloud_event import TcareCloudEvent
from pydantic import BaseModel

class CampaignEventData(BaseModel):
  source: str # i.e. assist - this will be useful for analytics
  campaign: str
  case_id: str
  caregiver_id: str
  first_name: str
  last_name: str
  action: str # i.e. start, stop
  email: str
  phone: str

class CampaignEventServiceBusMessage(TcareCloudEvent):  
  data: CampaignEventData