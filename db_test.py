import motor.motor_asyncio as db
from dotenv import load_dotenv
import os
import asyncio


async def main():
    load_dotenv()

    db_pass = os.environ.get("DB_PASS")
    db_user = os.environ.get("DB_USER")
    db_client = db.AsyncIOMotorClient(
        f"mongodb+srv://{db_user}:{db_pass}@cluster0.xutksl2.mongodb.net/?retryWrites=true&w=majority"
    )

    async with await db_client.start_session() as session:
        cursor = session.client.roosterbot.playlist.find()
        """         for document in await cursor.to_list(length=100):
            print(document) """

        print(await cursor.to_list(length=100))


asyncio.run(main())
