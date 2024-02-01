import os
import requests

class Uploader:
  
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
    with open(file_path, 'rb') as file:
      files = {'file': (os.path.basename(file_path), file)}
      respuesta = requests.post('http://localhost:3000/courses', files=files)
      
      if respuesta.status_code == 202:
        print(f'Se ha cargado el horario {file_path[-10:][:-5]} correctamente.')
      else:
        print(f'Ha ocurrido un error... {respuesta.content}')