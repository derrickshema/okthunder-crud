from typing import Optional
from sqlmodel import Field, SQLModel

class Player(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    age: int
    height: float
    position: str = Field(max_length=20)
    bio: Optional[str] = Field(default=None, max_length=500)
    image_url: Optional[str] = Field(default=None, max_length=200)