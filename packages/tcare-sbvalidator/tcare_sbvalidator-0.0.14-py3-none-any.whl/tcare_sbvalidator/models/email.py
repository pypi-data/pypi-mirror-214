from .cloudevents import TcareCloudEvent
from pydantic import BaseModel

# SMS
class EmailData(BaseModel):
    type: str
    sender: str
    recipient: str
    content: str

class EmailServiceBusMessage(TcareCloudEvent):
    data: EmailData