from pydantic import BaseModel, Field
from typing import Optional

class Comment(BaseModel):
  subject: str
  text: str
  date: str
  likes: int = Field(e=0)
  dislikes: int = Field(ge=0)
  positive_score: Optional[float] = None
  neutral_score: Optional[float] = None
  negative_score: Optional[float] = None
  