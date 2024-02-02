import os

from pymongo import MongoClient
from typing import TypedDict, Optional

from teachers.domain.model.teacher import Teacher
from teachers.domain.ports.teachers_repository import TeacherRepository

from comments.domain.comment import Comment

def singleton(cls):
    instances = {}

    def wrapper(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return wrapper

@singleton
class MongoTeachersRepository(TeacherRepository):
  def connect(self) -> None:
    str_connection = f'mongodb://{os.environ["MONGODB_USER"]}:{os.environ["MONGODB_PASSWORD"]}@{os.environ["MONGODB_HOST"]}/'

    self.mongo_client = MongoClient(host=str_connection, port=int(os.environ['MONGODB_PORT']))
    self.database = self.mongo_client[os.environ['MONGODB_DATABASE']]
    self.teachers_collection = self.database['teachers']
    
  def get_teacher(self, teacher_name: str) -> Optional[Teacher]:
    teacher = self.teachers_collection.find_one({'name': teacher_name})
    
    
    if teacher:
      return Teacher(
        name=teacher['name'],
        url=teacher['url'],
        comments=teacher['comments'],
        positive_score=teacher['positive_score']
      )
    else:
      return None
  
  def add_teacher(self, teacher: Teacher) -> None:
    print('Trantando..........')
    print(f'Agregando profesor {teacher.name}')
    print(f'Sus comentarios {teacher.comments}')
    print(f'Su url {teacher.url}')
    self.teachers_collection.insert_one(teacher.dict())

  def disconnect(self) -> None:
    self.mongo_client.close()
    