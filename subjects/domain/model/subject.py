from pydantic import BaseModel, Field

class Subject(BaseModel):
  career: str
  plan: str
  level: int
  key: str
  name: str
  required: bool
  credits_required: float
