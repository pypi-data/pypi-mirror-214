from .cloudevents import TcareCloudEvent
from pydantic import BaseModel

# SMS
class SmsData(BaseModel):
    type: str
    sender: str
    recipient: str
    email_subject: str
    content: str

class SmsServiceBusMessage(TcareCloudEvent):
    data: SmsData