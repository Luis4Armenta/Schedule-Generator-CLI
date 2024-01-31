import click
import json
from downloader import Downloader

STATE_FILE = 'state.json'
def load_state():
    try:
        with open(STATE_FILE, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_state(state):
    with open(STATE_FILE, 'w') as file:
        json.dump(state, file)

@click.group()
def main():
    pass


@main.group()
def download():
    pass


@main.group()
def upload():
    pass

@main.command()
@click.option('--sessionid', '-s', required=True)
@click.option('--token', '-t', required=True)
@click.option('--domain', '-d', required=True)
def login(sessionid, token, domain):
  state = load_state()
  state['session_id'] = sessionid
  state['token'] = token
  state['domain'] = domain
  
  save_state(state)
  print("Las credenciales de acceso al SAES han sido cargadas...")

@download.command(name='subjects')
@click.argument('carrera', required=False)
@click.argument('plan', required=False)
@click.argument('periodo', required=False)
def download_subjects(carrera, plan, periodo):
    """
    Descarga las asignaturas de las carreras.
    """
    click.echo(f'Descargando asignaturas{"..." if carrera == None else ""} ', nl=False if carrera != None else True)
    if carrera:
        click.echo(f'de la carrera {carrera}{"..." if plan == None else ","} ', nl=False if plan != None else True)
    if plan:
        click.echo(f'plan {plan}{"..." if periodo == None else ","} ', nl=False if periodo != None else True)
    if periodo:
        click.echo(f'periodo {periodo}...')
    
    state = load_state()
    assert state['session_id']
    assert state['token']
    assert state['domain']

    downloader = Downloader(state['session_id'], state['token'], state['domain'])
    downloader.download_subjects(carrera, plan, periodo)
    
    print("Las asignatruas han sido descargadas")
    

@download.command(name='courses')
@click.argument('carrera', required=False)
@click.argument('plan', required=False)
@click.argument('periodo', required=False)
def download_courses(carrera, plan, periodo):
    """
    Descarga las unidades de aprendizaje.
    """
    click.echo(f'Descargando unidades de aprendizaje{"..." if carrera == None else ""} ', nl=False if carrera != None else True)
    if carrera:
        click.echo(f'de la carrera {carrera}{"..." if plan == None else ","} ', nl=False if plan != None else True)
    if plan:
        click.echo(f'plan {plan}{"..." if periodo == None else ","} ', nl=False if periodo != None else True)
    if periodo:
        click.echo(f'periodo {periodo}...')

@upload.command(name='courses')
@click.argument('carrera', required=False)
@click.argument('plan', required=False)
@click.argument('periodo', required=False)
def upload_courses(carrera, plan, periodo):
    """
    Sube información de unidades de aprendizaje.
    """
    click.echo('Subiendo información para courses...')
    if carrera:
        click.echo(f'Carrera: {carrera}')
    if plan:
        click.echo(f'Plan de estudios: {plan}')
    if periodo:
        click.echo(f'Periodo: {periodo}')

if __name__ == '__main__':
    main()
