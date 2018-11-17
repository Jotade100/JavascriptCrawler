from pygments import highlight
from pygments.lexers.python import PythonLexer
from pygments.formatters.html import HtmlFormatter
import json
import pymongo
import os, fnmatch, sys

# representar colecciones en db como matrices de adyacencia para los archivos y funciones

#myclient = pymongo.MongoClient("mongodb://localhost:27017/")
#db = myclient["filesParser"]
#db_funciones = db["funciones"]
#db_variablesInFile = db["variablesInFile"]
#db_archivosLeidos = db["archivos"]

#basePath, currentFile = os.path.split(__file__)
#print(currentFile)

def eliminarColeccionesDB():
    db_funciones.drop()
    db_variablesInFile.drop()
    db_archivosLeidos.drop()

importedFilesInFile = [] #archivos a parsear
classesInFile = []
variablesInFile = [] #aqui se guardan los objetos json
tmpVariables = [] #aqui se guarda solo el nombre de las variables en el archivo para validar que no se guarden en variablesInFile vars repetidas
functionsInFile = []
queue4scrawler = [] #se va a hacer enqueue a los archivos que no hayan sido descubiertos tras validar en la db (que no se ha creadp)

#from pygments import lex


def readFile(archivo):
    tmpFile = open(archivo, 'r').read()
    return tmpFile
currentFile = 'testFile.py' #convertir a variable dinamica al momento de convertir este bloque a funcion
code = readFile(currentFile) 
print(currentFile)
tokenObjects = tuple(PythonLexer().get_tokens(code))
def convertToJson(token, text):
    return {"token": str(token)[6:], "value": text}
File2Json =  json.dumps([convertToJson(*token) for token in tokenObjects], indent=2) # creo un multi-string con el formato de un json
tmpFileJsonArray = json.loads(File2Json) #creo un diccionario en base al string json anterior

for i in range(0, (len(tmpFileJsonArray)-1)):
    if (tmpFileJsonArray[i]["token"] == "Keyword.Namespace" and tmpFileJsonArray[i]["value"] == "from") or (tmpFileJsonArray[i]["token"] == "Keyword.Namespace" and tmpFileJsonArray[i]["value"] == "import" and tmpFileJsonArray[i-4]["value"] != "from"): #esta ultima condicion valida que el formato sea: from x import y || import x  
        if tmpFileJsonArray[i+2]["value"] not in importedFilesInFile: #valido que el valor no se encuentre ya en el array (luego voy a validar que no este en la db)
            tmpImported = {"file":tmpFileJsonArray[i+2]["value"], "importedAt": [currentFile], "discovered":1}
            importedFilesInFile.append(tmpImported) 
    if tmpFileJsonArray[i]["token"] == "Name.Class":
        if tmpFileJsonArray[i]["value"] not in classesInFile:
            tmpClass = {"class_name":tmpFileJsonArray[i]["value"], "definedAt": currentFile}
            classesInFile.append(tmpClass)
    if tmpFileJsonArray[i]["token"] == "Name":
        if tmpFileJsonArray[i]["value"] not in tmpVariables and tmpFileJsonArray[i-1]["value"]!= '.' and tmpFileJsonArray[i-2]["value"]!= 'import' :
            tmpVariables.append(tmpFileJsonArray[i]["value"])
            tmpVariable = {"variable":tmpFileJsonArray[i]["value"], "declaredAt":currentFile}
            variablesInFile.append(tmpVariable)
    if tmpFileJsonArray[i]["token"] == "Name.Function":
        tmpFunction = {"function":tmpFileJsonArray[i]["value"], "createdAt":currentFile, "importedAt":[]}
        functionsInFile.append(tmpFunction)
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
        f2save = {'file':f, 'discovered':0}
        pyFiles.append(f2save)
print(" Archivos Python: ",pyFiles)

def lecturaLimpiaClases(classesArray):
    print("--------------------------- Clases en el archivo -----------------------------------\n")
    for clase in classesArray:        
        print(clase["class_name"])
    print('\n')
def lecturaLimpiaVariables(variablesArray):
    print("--------------------------- Variables en el archivo -----------------------------------\n")
    for var in variablesArray:
        print(var["variable"])
    print('\n')
def lecturaLimpiaFunciones(functionsArray):
    print("--------------------------- Funciones en el archivo -----------------------------------\n")
    for func in functionsArray:
        print(func["function"])
    print('\n')

lecturaLimpiaClases(classesInFile)
lecturaLimpiaVariables(variablesInFile)
lecturaLimpiaFunciones(functionsInFile)
#for pyFile in pyFiles:
#    registerFile = {"file":pyFile}
#    db_archivosLeidos.insert_one(registerFile)

#for x in db_archivosLeidos.find():
  #print(x)