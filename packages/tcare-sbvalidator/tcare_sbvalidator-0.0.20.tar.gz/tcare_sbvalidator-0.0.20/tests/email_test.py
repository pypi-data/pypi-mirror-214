import asyncio, sys
from dotenv import dotenv_values
config = dotenv_values(".env")

sys.path.append("..")
from src.tcare_sbvalidator.email_handler import Email

NAMESPACE = config['NAMESPACELOCAL']
CONNECTION_STRING = config['CONNECTION_STRING']
SENDER = config['TEST_EMAIL_SENDER']
RECIPIENT = config['TEST_EMAIL_RECIPIENT']

async def main():
    handler = Email()
    handler.connectWithCred(NAMESPACE)

    await handler.publish_message(
        handler.build_json(
            id="123",
            sender=SENDER,
            recipient=RECIPIENT,
            email_subject="test_subject",
            content="Helloo!",
        )
    )

asyncio.run(main())