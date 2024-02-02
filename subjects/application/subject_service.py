from typing import List, Optional
from abc import ABC, abstractmethod
from subjects.domain.model.subject import Subject
from subjects.domain.ports.subjects_repository import SubjectRepository

class ISubjectService(ABC):
  @abstractmethod
  def upload_subjects(self, subjects: List[Subject]):
    pass
  
  @abstractmethod
  def get_subject(self, career: str, name: str) -> Optional[Subject]:
    pass

class SubjectService(ISubjectService):
  def __init__(self, subject_repository: SubjectRepository):
    self.subject_repository = subject_repository
  
  def upload_subjects(self, subjects: List[Subject]) -> None:
    for subject in subjects:
      subject_exists: bool = True if self.subject_repository.get_subject(subject.career, subject.name) else False
      
      if subject_exists:
        continue
      else:
        self.subject_repository.add_subject(subject.dict())
        
  def get_subject(self, career: str, name: str) -> Optional[Subject]:
    return self.subject_repository.get_subject(career, name)


