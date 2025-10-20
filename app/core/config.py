from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MONGO_CONNECTION_STRING: str
    MONGO_DB_NAME: str
    FINNHUB_API_KEY: str

    class Config:
        env_file = ".env"


settings = Settings()
