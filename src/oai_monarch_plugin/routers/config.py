import os

from pydantic import BaseSettings
from dotenv import load_dotenv

load_dotenv()

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

    ncbi_api_key: str = (
        os.getenv("NCBI_API_KEY")
        if os.getenv("NCBI_API_KEY")
        else None
    )

settings = Settings()
