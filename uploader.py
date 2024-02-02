import os
import requests
from lxml import etree
from typing import List
from bs4 import BeautifulSoup
from datetime import datetime
from subjects.domain.model.subject import Subject
from courses.domain.model.course import CourseAvailability
from courses.application.course_service import CourseService
from courses.domain.model.course import Course, ScheduleCourse
from teachers.application.teacher_service import TeacherService
from comments.application.comment_service import CommentService
from subjects.application.subject_service import SubjectService
from comments.infrastructure.azure_text_analyzer import AzureTextAnalyzer
from teachers.infrastructure.mongo_teachers_repository import MongoTeachersRepository
from courses.infrastructure.mongo_courses_repository import MongoCourseRepository
from comments.infrastructure.bs4_comments_web_scraper import BS4CommentsWebScraper
from subjects.infrastructure.mongo_subjects_repository import MongoSubjectsRepository
from courses.infrastructure.mongo_courses_repository import MongoCourseRepository
class Uploader:
  
  def upload_subjects(
    self,
    career: str = None,
    plan: str = None,
    period: str = None
  ):
    start_scan_in = f'downloads/subjects'
    if career:
      start_scan_in = start_scan_in + f'/{career}'
    if plan:
      start_scan_in = start_scan_in + f'/{plan}'
      
    for root, dirs, files in os.walk(start_scan_in):   
      for file in files:
        if period:
          if not file.startswith(period):
            continue
          
        if file.endswith('.html'):
          file_path = os.path.join(root, file)
          self._upload_subject(file_path)


  def upload_availability(
    self,
    career: str = None,
    plan: str = None
  ):
    start_scan_in = f'downloads/availability'
    if career:
      start_scan_in = start_scan_in + f'/{career}'
    if plan:
      start_scan_in = start_scan_in + f'/{plan}'
      
    for root, dirs, files in os.walk(start_scan_in):   
      if len(files) != 0:
        datetimes = [ datetime.strptime(file[:-5], '%Y-%m-%d %H:%M:%S.%f') for file in files]
        
        current_availibility = str(max(datetimes))
        print(current_availibility)
        
        for file in files:
          if file.startswith(current_availibility):
            file_path = os.path.join(root, file)
            self._upload_availability(file_path)
          
          
  def upload_schedules(
      self,
      career: str = None,
      plan: str = None,
      period: str = None,
      shift: str = None,
      sequence: str = None
    ):
    
    start_scan_in = f'downloads/schedules'
    if career:
      start_scan_in = start_scan_in + f'/{career}'
    if plan:
      start_scan_in = start_scan_in + f'/{plan}'
    if period:
      start_scan_in = start_scan_in + f'/{period}'
    if shift:
      start_scan_in = start_scan_in + f'/{shift}'
    
    for root, dirs, files in os.walk(start_scan_in):   
      for file in files:
        if sequence:
          if sequence not in file:
            continue
          
        if file.endswith('.html'):
          file_path = os.path.join(root, file)
          self._upload_schedule(file_path)
    
  def _upload_subject(self, file_path: str):
    subjects_database = MongoSubjectsRepository()
    subjects_database.connect()
    subject_service = SubjectService(subjects_database)
    
    with open(file_path, 'r') as file:
      contenido: str = file.read()
      
      subjects: List[Subject] = []
    
      dom = etree.HTML(str(BeautifulSoup(contenido,'html.parser')))
      props = dom.xpath('//select/option[@selected="selected"]/@value')
      raw_subjects = dom.xpath('//table[@id="ctl00_mainCopy_GridView1"]//tr')[1:]
      
      career: str = props[0]
      plan: str = props[1]
      
      for raw_subject in raw_subjects:        
        fields = raw_subject.xpath('./td/text()')
        
        level: int = int(fields[0])
        key: str = fields[1]
        name: str = fields[2]
        required: bool = True if fields[3].strip().upper() == 'OBLIGATORIA' else False
        credits_required: float = float(fields[4])
        
        subject = Subject(
          career=career,
          plan=plan,
          level=level,
          key=key,
          name=name,
          required=required,
          credits_required=credits_required
        )
        
        subjects.append(subject)
      
      
      
      subject_service.upload_subjects(subjects)

      c, p, n = file_path.split('/')[-3:]
      print(f'Se han cargado las asignaturas de la carrera {c}, plan {p}, nivel {n[:-5]}.')
      
    subjects_database.disconnect()
      
  def _upload_schedule(self, file_path: str):
    course_repository = MongoCourseRepository()
    subjects_repository = MongoSubjectsRepository()
    teachers_repository = MongoTeachersRepository()
    
    course_repository.connect()
    subjects_repository.connect()
    teachers_repository.connect()
    
    web_scraper = BS4CommentsWebScraper()
    text_analyzer = AzureTextAnalyzer()
    comment_service = CommentService(web_scraper, text_analyzer)
    
    teacher_service = TeacherService(teachers_repository, comment_service)
    courses_service = CourseService(course_repository, teacher_service, subjects_repository)
    with open(file_path, 'rb') as file:
      content = file.read()
      courses: List[Course] = []

      dom = etree.HTML(str(BeautifulSoup(content, 'html.parser')))
      raw_courses = dom.xpath('//table[@id="ctl00_mainCopy_dbgHorarios"]//tr')[1:]
      props = dom.xpath('//select/option[@selected="selected"]/@value')
      
      career: str = props[0]
      plan: str = props[2]
      level: str = props[3]
      seq: str = props[4].strip()


      for raw_course in raw_courses:
        sequence = raw_course.xpath('./td/text()')[0].strip().upper()
        level = sequence[0]
        shift = sequence[2]
        semester = sequence[3]
        teacher_name = raw_course.xpath('./td/text()')[2].strip().upper()

        if sequence != seq:
          continue

        schedule_course: ScheduleCourse = get_sessions(raw_course)
        
        course = Course(
          semester=semester,
          career=career,
          level=level,
          plan=plan,
          shift=shift,
          sequence=sequence,
          subject=raw_course.xpath('./td/text()')[1],
          teacher=teacher_name,
          schedule=schedule_course,
          course_availability=40,
          required_credits=None,
          teacher_positive_score=None,
        )

        courses.append(course)

      courses_service.upload_courses(courses)
      
      s = file_path.split('/')
      print(f'Se ha cargado los cursos de la secuencia {s[-1][:-5]}')

    course_repository.disconnect()
    subjects_repository.disconnect()
    teachers_repository.disconnect()

  def _upload_availability(self, file_path: str):
    course_repository = MongoCourseRepository()
    subjects_repository = MongoSubjectsRepository()
    teachers_repository = MongoTeachersRepository()
    
    course_repository.connect()
    subjects_repository.connect()
    teachers_repository.connect()
    
    web_scraper = BS4CommentsWebScraper()
    text_analyzer = AzureTextAnalyzer()
    comment_service = CommentService(web_scraper, text_analyzer)
    
    teacher_service = TeacherService(teachers_repository, comment_service)
    courses_service = CourseService(course_repository, teacher_service, subjects_repository)
      
    with open(file_path, 'rb') as file:
      content = file.read()
      availabilities: List[CourseAvailability] = []
    
      dom = etree.HTML(str(BeautifulSoup(content, 'html.parser')))
      raw_courses = dom.xpath('//table[@id="ctl00_mainCopy_GrvOcupabilidad"]//tr')[1:]
      
      for raw_course in raw_courses:
        sequence: str = raw_course.xpath('./td/text()')[0].strip().upper()
        subject: str = raw_course.xpath('./td/text()')[2].strip().upper()
        course_avalibility = int(raw_course.xpath('./td/text()')[6].strip())
      
      
        a = CourseAvailability(
          sequence=sequence,
          subject=subject,
          course_availability=course_avalibility
        )
        availabilities.append(a)
        
      
      
      courses_service.update_course_availability(availabilities)
      

      c, p = file_path.split('/')[-2:]
      print(f'Se ha actualizado la disponibilidad de la carrera {c}, plan {p[:-5]}.')
    
    course_repository.disconnect()
    subjects_repository.disconnect()
    teachers_repository.disconnect()

def get_sessions(raw_course) -> ScheduleCourse:
  sessions: ScheduleCourse = []
  
  days = raw_course.xpath('./td/text()')[5:-1]
  for session, day in zip(days, ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']):
    session: str = session.strip()
    if session:
      start_time, end_time = session.split('-')
      sessions.append({
        'day': day,
        'start_time': start_time,
        'end_time': end_time,
      })
      
  return sessions