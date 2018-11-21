# Python Crawler
> Este sistema es un crawler que permite indexar y buscar objetos en Python ( > v3.6.x). Esto lo hace a través de la inspección del código fuente e identifica las relaciones entre archivos por medio de expresiones  ```import``` en el código para ubicar los demás archivos a parsear e ir creando un path de recorrido en el grafo. Luego de parsear el código fuente, se almacenan las variables, funciones y clases identificadas en una base de datos mongo, para luego facilitar las consultas personalizadas de la data clasificada de los archivos. 

## Instalación
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

Modificar en el archivo de configuración `config.yml` el valor de `archivo` al nombre del archivo python que se va a utilizar como el archivo root:  

Levantar container a partir de la imagen (Dockerfile) en el directorio:
``
