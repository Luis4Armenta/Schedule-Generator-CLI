import os
from pymongo import MongoClient
from typing import Optional

from courses.domain.model.course import Course
from courses.domain.ports.courses_repository import CourseRepository


def singleton(cls):
    instances = {}

    def wrapper(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return wrapper


@singleton
class MongoCourseRepository(CourseRepository):
  def connect(self) -> None:
    str_connection = f'mongodb://{os.environ["MONGODB_USER"]}:{os.environ["MONGODB_PASSWORD"]}@{os.environ["MONGODB_HOST"]}/'

    self.mongo_client = MongoClient(host=str_connection, port=int(os.environ['MONGODB_PORT']))
    self.database = self.mongo_client[os.environ['MONGODB_DATABASE']]
    self.course_collection = self.database['courses']

  def get_course(self, sequence: str, subject: str) -> Optional[Course]:
    course = self.course_collection.find_one({
      'sequence': sequence,
      'subject': subject
    })
    
    if course:
      return Course(
        plan=course['plan'],
        level=course['level'],
        career=course['career'],
        shift=course['shift'],
        semester=course['semester'],
        sequence=course['sequence'],
        teacher=course['teacher'],
        subject=course['subject'],
        course_availability=course['course_availability'],
        teacher_positive_score=course['teacher_positive_score'],
        required_credits=course['required_credits'],
        schedule=course['schedule'],
      )
    else:
      None
    
  def add_course(self, course: Course) -> None:
    print(f'Agregando {course.sequence}, {course.subject}')
    self.course_collection.insert_one(course.dict())
    
  def disconnect(self) -> None:
     self.mongo_client.close()
    