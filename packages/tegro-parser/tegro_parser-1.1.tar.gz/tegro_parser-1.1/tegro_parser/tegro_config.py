from pydantic import BaseModel

class TegroConfig(BaseModel):
    api_url: str = "https://tegro.money/api/"
    shop_id: str
    api_key: str