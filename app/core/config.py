from pydantic_settings import BaseSettings
from pathlib import Path


# Get the project root directory (parent of app/)
PROJECT_ROOT = Path(__file__).parent.parent.parent
ENV_FILE = PROJECT_ROOT / ".env"


class Settings(BaseSettings):
    # Database
    MONGO_CONNECTION_STRING: str
    MONGO_DB_NAME: str
    
    # Price Service APIs
    FINNHUB_API_KEY: str
    EXCHANGE_RATE_API_KEY: str
    EXCHANGE_RATE_PROVIDER: str = "exchangerate-api"  # exchangerate-api, fixer, currencyapi
    USE_MOCK_PRICES: bool = False  # Default to real Finnhub

    # Pydantic v2 style model config
    model_config = {
        "env_file": str(ENV_FILE),
        "env_file_encoding": "utf-8",
        "extra": "ignore",
    }


settings = Settings()
