import asyncio, sys
from dotenv import dotenv_values
config = dotenv_values(".env")

sys.path.append("..")
from src.tcare_sbvalidator.email_handler import Email

NAMESPACE = config['NAMESPACELOCAL']
CONNECTION_STRING = config['CONNECTION_STRING']

async def main():
    handler = Email()
    handler.connectWithCred(NAMESPACE)

    await handler.publish_message(
        handler.build_json(
            id="123",
            sender="elijah.kennedy@tcare.ai",
            recipient="elijahclimbs@gmail.com",
            email_subject="test_subject",
            content="Helloo!",
        )
    )

asyncio.run(main())