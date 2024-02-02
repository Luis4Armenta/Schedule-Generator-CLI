from pydantic import BaseModel, Field
from typing import Optional, List
from typing_extensions import TypedDict

class Session(TypedDict):
  day: str
  start_time: str
  end_time: str

ScheduleCourse = List[Session]

class CourseAvailability(BaseModel):
  sequence: str
  subject: str
  course_availability: int


class Course(BaseModel):
  plan: str 
  level: str
  career: str
  shift: str
  semester: str
  sequence: str
  teacher: str 
  subject: str
  course_availability: Optional[int] = Field(default=40)
  teacher_positive_score: Optional[float]
  
  required_credits: Optional[float]
  schedule: ScheduleCourse

  