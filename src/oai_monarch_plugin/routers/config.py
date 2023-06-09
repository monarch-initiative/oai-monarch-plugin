import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    monarch_api_url: str = (
        os.getenv("MONARCH_API_URL")
        if os.getenv("MONARCH_API_URL")
        else "https://api-v3.monarchinitiative.org/v3/api"
    )


settings = Settings()
