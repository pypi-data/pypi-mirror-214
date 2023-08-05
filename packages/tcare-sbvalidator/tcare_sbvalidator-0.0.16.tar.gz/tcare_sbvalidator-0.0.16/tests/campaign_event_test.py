import asyncio, sys
from dotenv import dotenv_values
config = dotenv_values(".env")

sys.path.append("..")
from src.tcare_sbvalidator.campaign_event_handler import Campaign

NAMESPACE = config['NAMESPACELOCAL']
# CONNECTION_STRING = config['CONNECTION_STRING']

async def main():
    handler = Campaign()
    handler.connectWithCred(NAMESPACE)
    await handler.publish_message(
        handler.build_json(
            id="123",
            trigger="assist",
            action="start",
            campaign_id="elevance-1",
            case_id="1",
            user_id="1"
        )
    )

asyncio.run(main())