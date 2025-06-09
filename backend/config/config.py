from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    BASE_URL: str = "https://api.spacexdata.com/v4"

settings = Settings()