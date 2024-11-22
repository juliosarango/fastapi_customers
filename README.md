# FastAPI
![FastAPI](images/fastapi.png)

## Instalación  
```
pip install -r requirements.txt
```
Ejecutar la aplicación en modo desarrollo.
```
fastapi dev
```
![Run FastAPI](images/run_fastapi.png)

## Estructura de la aplicación
![Estructura proyecto](images/estructura.png)

## Diagrama de BD
![Diagrama DB](images/der.png)

## Midlewares
Permiten agregar funcionalidades a todos los requests y response de nuestra API


## Template de la comunidad 

La comunidad de FastAPI ha creado un template listo para su uso. Puedes encontrarlo en el siguiente [enlace](https://github.com/fastapi/full-stack-fastapi-template)
```
https://github.com/fastapi/full-stack-fastapi-template
```

## Reporte de pruebas unitarias
```
coverage run --source app/ -m pytest
coverage report
```
![Reporte pruebas unitarias](images/report_tests.png)