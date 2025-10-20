import motor.motor_asyncio
from app.core.config import settings

client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGO_CONNECTION_STRING)
database = client[settings.MONGO_DB_NAME]


def get_trades_collection():
    return database.get_collection("trades")


def get_setups_collection():
    return database.get_collection("setups")
