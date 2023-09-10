from pydantic import BaseModel


class Scroll(BaseModel):
    user_id: int
