from pydantic import BaseModel, HttpUrl
from typing import List
from comments.domain.comment import Comment

class Teacher(BaseModel):
  name: str
  url: str
  positive_score: float
  comments: List[Comment]