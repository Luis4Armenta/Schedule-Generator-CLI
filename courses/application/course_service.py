from typing import List

from courses.domain.model.course import Course
from courses.domain.ports.courses_repository import CourseRepository

from subjects.application.subject_service import SubjectService
from teachers.application.teacher_service import TeacherService

class CourseService:
  def __init__(
      self,
      course_repository: CourseRepository,
      teacher_service: TeacherService,
      subject_service: SubjectService
    ):
    self.course_repository = course_repository
    self.teacher_service = teacher_service
    self.subject_service = subject_service

  def upload_courses(self, courses: List[Course]):
    for course in courses:
      course_exists = self.course_repository.get_course(course.sequence, course.subject)
      if course_exists:
        continue
      
      teacher = self.teacher_service.get_teacher(course.teacher)
      sequence = course.sequence
      subject = self.subject_service.get_subject(sequence[1], course.subject)
      positive_score: float = 0.0
      if teacher:
        positive_score = teacher.positive_score
      else:
        positive_score = 0.5
      
      course.teacher_positive_score = positive_score
      course.required_credits = subject.credits_required
      self.course_repository.add_course(course)
