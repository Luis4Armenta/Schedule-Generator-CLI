import os
import requests
from lxml import etree
from typing import List
from bs4 import BeautifulSoup
from datetime import datetime
from subjects.domain.model.subject import Subject
from subjects.application.subject_service import SubjectService
from subjects.infrastructure.mongo_subjects_repository import MongoSubjectsRepository

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
    
  def _upload_schedule(self, file_path: str):
    with open(file_path, 'r') as file:
      contenido: str = file.read()
      
      subjects: List[Subject] = []
    
      dom = etree.HTML(str(BeautifulSoup(contenido, 'html.parser', from_encoding='utf8')))
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
      
      
      subjects_database = MongoSubjectsRepository()
      subjects_database.connect()
      subject_service = SubjectService(subjects_database)
      subject_service.upload_subjects(subjects)
      subjects_database.disconnect()

      print(f'Se ha cargado el horario {file_path[-10:][:-5]}.')
      
      
  def _upload_subject(self, file_path: str):
    with open(file_path, 'rb') as file:
      files = {'file': (os.path.basename(file_path), file)}
      respuesta = requests.post('http://localhost:3000/subjects', files=files)
      
      if respuesta.status_code == 202:
        c, p, s = file_path.split('/')[-3:]
        print(f'Se ha cargado el periodo {s[:-5]} del plan {p} de la carrera {c}.')
      else:
        print(f'Ha ocurrido un error... {respuesta.content}')

  def _upload_availability(self, file_path: str):
    with open(file_path, 'rb') as file:
      files = {'file': (os.path.basename(file_path), file)}
      respuesta = requests.post('http://localhost:3000/courses/occupancy', files=files)
      
      if respuesta.status_code == 200:
        c, p = file_path.split('/')[-2:]
        print(f'Se ha actualizado la disponibilidad de la carrera {c}, plan {p[:-5]}.')
      else:
        print(f'Ha ocurrido un error... {respuesta.content}')