from pygments import highlight
from pygments.lexers.python import PythonLexer
from pygments.formatters.html import HtmlFormatter
from pygments.token import String, string_to_tokentype

# # # # # # # # Métodos # # # # # # # #
def readFile(archivo):
    tmpFile = open(archivo, 'r').read()
    return tmpFile

def agregar(item, lista):
    comodin = True
    for elemento in lista:
        if elemento[0] == item[0]:
            comodin = False

    if comodin:
        lista.append(item)


def lectura(archivos):
    for archivo in archivos:
        try:
            # archivo[0] es la ruta del archivo
            # archivo[1] es la ruta seguida para encontrar el archivo
            code = readFile(archivo[0])
            lista = list(PythonLexer().get_tokens(code))
            for item in lista:
                if item[0] == string_to_tokentype('Token.Name.Namespace'):
                    cadena = item[1]
                    cadena = cadena.replace(".", "/")
                    cadena = cadena + ".py"
                    ruta = archivo[1].copy()
                    ruta.append(archivo[0])
                    objeto = [cadena, ruta]
                    agregar(objeto, archivos)
        except:
            # variable de broma XD
            variable = 0
            # El archivo no existe, de seguro es una librería general 
            #print("El archivo " + archivo + " no existe")


# # # # # # # # Código de prueba # # # # # # # #
#lectura(resultados)
#print(resultados)