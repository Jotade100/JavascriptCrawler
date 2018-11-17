from pygments import highlight
from pygments.lexers.python import PythonLexer
from pygments.formatters.html import HtmlFormatter
import json

files = [] #archivos a parsear
classes = []
variables = []
functions = []
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

for i in range(0, (len(tmpFileJsonArray)-1)):
    if (tmpFileJsonArray[i]["token"] == "Keyword.Namespace" and tmpFileJsonArray[i]["value"] == "from") or (tmpFileJsonArray[i]["token"] == "Keyword.Namespace" and tmpFileJsonArray[i]["value"] == "import" and tmpFileJsonArray[i-4]["value"] != "from"): #esta ultima condicion valida que el formato sea: from x import y || import x  
        if tmpFileJsonArray[i+2]["value"] not in files: #valido que el valor no se encuentre ya en el array (luego voy a validar que no este en la db)
            files.append(tmpFileJsonArray[i+2]["value"]) 
    if tmpFileJsonArray[i]["token"] == "Name.Class":
        classes.append(tmpFileJsonArray[i]["value"])
    if tmpFileJsonArray[i]["token"] == "Name":
        variables.append(tmpFileJsonArray[i]["value"])
    if tmpFileJsonArray[i]["token"] == "Name.Function":
        functions.append(tmpFileJsonArray[i]["value"])
#print(tmpFileJsonArray)
print(files)
#print(classes)
#print(variables)
#print(functions)