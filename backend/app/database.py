import os
from sqlalchemy.ext.asyncio import create_async_engine

from dotenv import load_dotenv
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_async_engine(DATABASE_URL, echo=True)

async def test_connection():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(lambda _: None)
        print("✅ Successfully connected to the database!")
    except Exception as e:
        print("❌ Failed to connect to the database:")
        print(e)