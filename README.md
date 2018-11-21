# Python Crawler
> Este sistema es un crawler que permite indexar y buscar objetos en Python ( > v3.6.x). Esto lo hace a través de la inspección del código fuente e identifica las relaciones entre archivos por medio de expresiones  ```import``` en el código para ubicar los demás archivos a parsear e ir creando un path de recorrido en el grafo. Luego de parsear el código fuente, se almacenan las variables, funciones y clases identificadas en una base de datos mongo, para luego facilitar las consultas personalizadas de la data clasificada de los archivos. 

## Instalación e implementación
### Requerimientos
* Docker (Linux, MacOS, Docker for Windows ToolBox, etc.)

### Librerías utilizadas
* Pygments: Lexer for Python
* Pymongo

Clonar el repositorio, o el tag release más reciente:

`$ git clone https://github.com/Jotade100/JavascriptCrawler.git`

Acceder al directorio clonado:

`$ cd JavascriptCrawler/`

Agregar en este directorio los archivos y carpetas python a inspeccionar con el crawler:

`cp -R path_to_sourceFiles JavascriptCrawler/`

Modificar en el archivo de configuración `config.yml` el valor de la llave `archivo` al nombre del archivo python que se va a utilizar como el archivo root: (el archivo root debe estar a nivel del directorio Ej. JavascriptCrawler/nombreArchivo.py )

`$ nano config.yml`

`archivo: nombreArchivo.py`  

(Guardar los cambios realizados)

Construir imagen a partir del Dockerfile en el directorio JavascriptCrawler/:

`docker build -t pythonCrawler . `

Levantar el container a partir de la imagen con nombre `pythonCrawler`:

`docker run -it pythonCrawler`

En este punto, el programa inicia con el parseo del código fuente especificado, almacenando la información útil en la base de datos y continua con el recorrido de los demás archivos utilizando los imports.

## Información de la Base de Datos (MongoDB)
