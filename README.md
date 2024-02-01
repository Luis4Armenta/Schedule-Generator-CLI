# Schedule Generator CLI

Esta es una herramienta para gestionar la data que necesita mi sistema generador de horarios.

## Instalación

1. Haz la [instalación de Selenium](https://selenium-python.readthedocs.io/installation.html).
2. Crea un entorno virtual:

```bash
  python -m venv .venv
```
3. Activa el entorno virtual:
```bash
  source .venv/bin/activate
```
4. Instala los requerimientos del proyecto:
```bash
  pip install -r requirements.txt
```
5. Prueba el CLI:
```bash
  python main.py
```
6. Carga el dominio de tu SAES, el session id y web token de un login hecho con tu cuenta.
```bash
  python main.py login -s <ASP.NET_SessionId> -t <.ASPXFORMSAUTH> -d <saes domain>
```
7. Disfruta del programa. Utilizando el siguiente comando podrás descargar el mapa curricular del periodo 2 perteneciente al plan 21 en la carrera C:
```bash
  python main.py download subjects C 21 2
```
8. Podrás visualizar tus descargas en la carpeta "downloads":
```bash
  tree downloads
```

    