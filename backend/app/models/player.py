from typing import Optional
from sqlmodel import Field, SQLModel

# Define the Player model with SQLModel. table=True indicates this model should be mapped to a database table.
# SQLModel in parantheses inherits from sqlalchemy (for database interaction) and pydantic (for data validation and serialization).
class Player(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    age: int
    height: str = Field(max_length=10)  # e.g., "6'7"
    position: str = Field(max_length=20)
    bio: Optional[str] = Field(default=None, max_length=500)
    image_url: Optional[str] = Field(default=None, max_length=200)