import os

from pymongo import MongoClient
from typing import TypedDict, Optional

from subjects.domain.model.subject import Subject
from subjects.domain.ports.subjects_repository import SubjectRepository

def singleton(cls):
    instances = {}

    def wrapper(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return wrapper

class MongoConfig(TypedDict):
  host: str
  port: int
  database: str

@singleton
class MongoSubjectsRepository(SubjectRepository):
 
  def connect(self) -> None:
    self.mongo_client = MongoClient(os.environ['MONGODB_CONNECTION_STRING'])
    self.database = self.mongo_client[os.environ['MONGODB_DATABASE']]
    self.subjects_collection = self.database['subjects']
  
  
  def add_subject(self, subject: Subject) -> None:
    self.subjects_collection.insert_one(subject).inserted_id
  
  def get_subject(self, career: str, name: str) -> Optional[Subject]:
    subject = self.subjects_collection.find_one({'career': career, 'name': name})

    if subject:
      return Subject(
        career=subject['career'],
        key=subject['key'],
        level=subject['level'],
        name=subject['name'],
        plan=subject['plan'],
        required=subject['required'],
        credits_required=subject['credits_required']
      )
    else:
      return None

  def disconnect(self) -> None:
    self.mongo_client.close()
    