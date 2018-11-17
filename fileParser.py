from pygments import highlight
from pygments.lexers.python import PythonLexer
from pygments.formatters.html import HtmlFormatter
import json
import pymongo
import os, fnmatch

# representar colecciones en db como matrices de adyacencia para los archivos y funciones

#myclient = pymongo.MongoClient("mongodb://localhost:27017/")
#db = myclient["filesParser"]
#db_funciones = db["funciones"]
#db_variablesInFile = db["variablesInFile"]
#db_archivosLeidos = db["archivos"]

def eliminarColeccionesDB():
    db_funciones.drop()
    db_variablesInFile.drop()
    db_archivosLeidos.drop()

importedFilesInFile = [] #archivos a parsear
classesInFile = []
variablesInFile = []
functionsInFile = []
#from pygments import lex


def readFile(archivo):
    tmpFile = open(archivo, 'r').read()
    return tmpFile

code = readFile('testFile.py')
tokenObjects = tuple(PythonLexer().get_tokens(code))
def convertToJson(token, text):
    return {"token": str(token)[6:], "value": text}
File2Json =  json.dumps([convertToJson(*token) for token in tokenObjects], indent=2) # creo un multi-string con el formato de un json
tmpFileJsonArray = json.loads(File2Json) #creo un diccionario en base al string json anterior

for i in range(0, (len(tmpFileJsonArray)-1)):
    if (tmpFileJsonArray[i]["token"] == "Keyword.Namespace" and tmpFileJsonArray[i]["value"] == "from") or (tmpFileJsonArray[i]["token"] == "Keyword.Namespace" and tmpFileJsonArray[i]["value"] == "import" and tmpFileJsonArray[i-4]["value"] != "from"): #esta ultima condicion valida que el formato sea: from x import y || import x  
        if tmpFileJsonArray[i+2]["value"] not in importedFilesInFile: #valido que el valor no se encuentre ya en el array (luego voy a validar que no este en la db)
            importedFilesInFile.append(tmpFileJsonArray[i+2]["value"]) 
    if tmpFileJsonArray[i]["token"] == "Name.Class":
        if tmpFileJsonArray[i]["value"] not in classesInFile:
            classesInFile.append(tmpFileJsonArray[i]["value"])
    if tmpFileJsonArray[i]["token"] == "Name":
        if tmpFileJsonArray[i]["value"] not in variablesInFile and tmpFileJsonArray[i-1]["value"]!= '.':
            variablesInFile.append(tmpFileJsonArray[i]["value"])
    if tmpFileJsonArray[i]["token"] == "Name.Function":
        functionsInFile.append(tmpFileJsonArray[i]["value"])
#print(tmpFileJsonArray)
print(importedFilesInFile)
print("Clases en archivo leído: ",classesInFile)
print("Variables en archivo leído: ",variablesInFile)
print("Funciones en archivo leído: ", functionsInFile)

listOfFiles = os.listdir()
pyFiles = []
py = "*.py"
for f in listOfFiles:
    if fnmatch.fnmatch(f, py):
        pyFiles.append(f)
print(" Archivos Python: ",pyFiles)

#for pyFile in pyFiles:
#    registerFile = {"file":pyFile}
#    db_archivosLeidos.insert_one(registerFile)

#for x in db_archivosLeidos.find():
  #print(x)