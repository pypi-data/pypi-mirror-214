from .tcare_cloud_event import TcareCloudEvent
from pydantic import BaseModel

# SMS
class SmsData(BaseModel):
    type: str
    sender: str
    recipient: str
    content: str

class SmsServiceBusMessage(TcareCloudEvent):
    data: SmsData