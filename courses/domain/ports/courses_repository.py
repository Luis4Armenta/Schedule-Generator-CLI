from typing import Optional
from abc import ABC, abstractmethod

from courses.domain.model.course import Course

class CourseRepository(ABC):
  @abstractmethod
  def connect(self, options) -> None:
    pass
    
  @abstractmethod
  def get_course(self, sequence: str, subject: str) -> Optional[Course]:
    pass
  
  @abstractmethod
  def add_course(self, course: Course) -> None:
    pass
  
  @abstractmethod
  def add_course(self, course: Course) -> None:
    pass
  
  @abstractmethod
  def update_availability(self, sequence: str, subject: str, new_availability: int) -> None:
    pass
  
  @abstractmethod
  def disconnect(self) -> None:
    pass

