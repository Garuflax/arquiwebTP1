# arquiwebTP1

## Requerimientos

### Frontend

* Node y npm: se puede descargar [acá](https://nodejs.org/en/download/)
* Angular: correr `npm install -g @angular/cli` en terminal

### Backend

* Python3
* redis-server: correr `sudo apt install redis-server` en terminal
* venv: correr `sudo apt install python3-venv` en terminal
* flask_cors: `pip install flask-cors` en ambiente virtual
* flask_jwt_extended: `pip install Flask-JWT-Extended` en ambiente virtual
* flask_qrcode: `pip install flask_qrcode` en ambiente virtual
* flask_mail: `pip install Flask-Mail` en ambiente virtual
* redis: `pip install redis` en ambiente virtual
* pytest: `pip install pytest` en ambiente virtual
* coverage: `pip install coverage` en ambiente virtual

## Comandos útiles

### Frontend

* `ng version` para ver versión de angular
* `ng serve --open` para correrlo

### Backend

* `python3 -m venv venv` crear ambiente virtual (hacerlo solo una vez)
* `. venv/bin/activate` activar ambiente virtual
* `pip install -e .` instalar proyecto en modo editable (hacerlo en el ambiente virtual)
* `pytest` para correr tests
* `coverage run -m pytest` para correr tests y analizar cobertura
* `coverage report` para ver el reporte del análisis de cobertura

## Tutoriales

### Frontend

* [Angular](https://angular.io/tutorial/toh-pt0)

### Backend

* [Flask](https://flask.palletsprojects.com/en/1.1.x/tutorial/)
