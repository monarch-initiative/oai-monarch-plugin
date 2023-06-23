import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    monarch_api_url: str = (
        os.getenv("MONARCH_API_URL")
        if os.getenv("MONARCH_API_URL")
        else "https://api-v3.monarchinitiative.org/v3/api"
    )

    monarch_ui_url: str = (
        os.getenv("MONARCH_UI_URL")
        if os.getenv("MONARCH_UI_URL")
        else "https://monarchinitiative.org"
    )

    monarch_api_v2_url: str = (
        os.getenv("MONARCH_API_V2_URL")
        if os.getenv("MONARCH_API_V2_URL")
        else "https://api.monarchinitiative.org/api"
    )

settings = Settings()
