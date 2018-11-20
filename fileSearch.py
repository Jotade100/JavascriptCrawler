from pygments import highlight
from pygments.lexers.python import PythonLexer
from pygments.formatters.html import HtmlFormatter
from pygments.token import String, string_to_tokentype

# # # # # # # # Métodos # # # # # # # #
def readFile(archivo):
    tmpFile = open(archivo, 'r').read()
    return tmpFile

def agregar(item, lista):
    if item not in lista:
        lista.append(item)


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
                    agregar(cadena, archivos)
        except:
            # variable de broma XD
            variable = 0
            # El archivo no existe, de seguro es una librería general 
            #print("El archivo " + archivo + " no existe")


# # # # # # # # Código de prueba # # # # # # # #
#lectura(resultados)
#print(resultados)