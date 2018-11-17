from pygments import highlight
from pygments.lexers.python import PythonLexer
from pygments.formatters.html import HtmlFormatter
import json
files = []
classes = []
variables = []
#from pygments import lex


def readFile():
    tmpFile = open('testFile.py', 'r').read()
    return tmpFile

code = readFile()
tokenObjects = tuple(PythonLexer().get_tokens(code))
def convertToJson(token, text):
    return {"token": str(token)[6:], "value": text}
File2Json =  json.dumps([convertToJson(*token) for token in tokenObjects], indent=2) # creo un multi-string con el formato de un json
tmpFileJsonArray = json.loads(File2Json) #creo un diccionario en base al string json anterior
for obj in tmpFileJsonArray:
    if obj["token"] == "Name.Class":
        classes.append(obj["value"])
    if obj["token"] == "Name":
        variables.append(obj["value"])
    #print(token)
print(classes)
print(variables)

#print(array)
#print(tmpFileJson["tokens"])

#for tupla in array:
