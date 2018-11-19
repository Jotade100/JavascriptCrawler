from pygments import highlight
from pygments.lexers.python import PythonLexer
from pygments.formatters.html import HtmlFormatter
from pygments.token import String, string_to_tokentype

def readFile(archivo):
    tmpFile = open(archivo, 'r').read()
    return tmpFile
#currentFile = 'testFile.py' #El archivo inicial desde donde se empieza a hacer el árbol de clases.
#code = readFile(currentFile) 
#print(code)
#print(list(PythonLexer().get_tokens(code)))
#lista = list(PythonLexer().get_tokens(code))
#resultados = []
#for item in lista:
    # Buscar todos los que contienen en su primer valor Token.Name.Namespace
    # En el segundo se vera como carpeta.carpeta2.archivo
    # print(type(item[0]))
#    if item[0] == string_to_tokentype('Token.Name.Namespace'):
#        # print(item[1])
#        cadena = item[1]
#        cadena = cadena.replace(".", "/")
#        cadena = cadena + ".py"
#        resultados.append(cadena)


# Aquí se debe de poner el archivo inicial desde donde se inicia el escaneo.
resultados = ['testFile.py']

def lectura(archivos):
    for archivo in archivos:
        try:
            code = readFile(archivo)
            lista = list(PythonLexer().get_tokens(code))
            for item in lista:
                if item[0] == string_to_tokentype('Token.Name.Namespace'):
                    cadena = item[1]
                    cadena = cadena.replace(".", "/")
                    cadena = cadena + ".py"
                    archivos.append(cadena)
        except:
            print("El archivo " + archivo + " no existe")


lectura(resultados)
print(resultados)