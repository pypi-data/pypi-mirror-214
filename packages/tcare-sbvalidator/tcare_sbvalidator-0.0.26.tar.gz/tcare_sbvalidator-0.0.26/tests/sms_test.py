import asyncio, sys
from dotenv import dotenv_values
config = dotenv_values(".env")

sys.path.append("..")
from src.tcare_sbvalidator.sms_handler import Sms

NAMESPACE = config['NAMESPACELOCAL']
CONNECTION_STRING = config['CONNECTION_STRING']
SENDER = config['TEST_SMS_SENDER']
RECIPIENT = config['TEST_SMS_RECIPIENT']

async def main():
    handler = Sms()
    handler.connectWithCred(NAMESPACE)

    await handler.publish_message(
        handler.build_json(
            id="123",
            sender=SENDER,
            recipient=RECIPIENT,
            content="Helloo!"
        )
    )

asyncio.run(main())