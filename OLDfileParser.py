from pygments import highlight
from pygments.lexers.python import PythonLexer
from pygments.formatters.html import HtmlFormatter
import json
import pymongo
import os, fnmatch, sys
import dbConf as db

# ----------------------------- Variables para funciones de la base de datos ---------------------------------------------------------------

VAR, FX, C = "var","fx","class"

# -----------------------------------------------------------------------------------------------------------------------------------------

# -------------------------------------- Instanciacion de Base De Datos ------------------------------------------------------------------
db = db.dataBase()
#record2saveTEST = {'function': 'primeraFuncion', 'params': ['token', 'text'], 'createdAt': 'unitTesting.py', 'importedAt': []}
#db.registrar("var",record2saveTEST)
#db.imprimirVariables()
#db.imprimir(FX)
#db.reset()
#db.imprimir(FX)
db.reset()

  
def extractParams(indice): # indice primer parentesis
    indice = indice + 1 # esto es para empezar a evaluar el primer parametro.
    params = []
    while tmpFileJsonArray[indice]["value"] != ")":
        if tmpFileJsonArray[indice]["token"] == "Name":
            params.append(tmpFileJsonArray[indice]["value"])
        indice += 1
    return params


def readFile(archivo):
    tmpFile = open(archivo, 'r').read()
    return tmpFile

def convertToJson(token, text):
    return {"token": str(token)[6:], "value": text}


importedFilesInFile = [] #archivos a parsear
classesInFile = []
variablesInFile = [] #aqui se guardan los objetos json
tmpVariables = [] #aqui se guarda solo el nombre de las variables en el archivo para validar que no se guarden en variablesInFile vars repetidas
functionsInFile = []
queue4scrawler = [] #se va a hacer enqueue a los archivos que no hayan sido descubiertos tras validar en la db (que no se ha creadp)
currentFile = 'testFile.py' #convertir a variable dinamica al momento de convertir este bloque a funcion
code = readFile(currentFile)
tokenObjects = tuple(PythonLexer().get_tokens(code))
File2Json =  json.dumps([convertToJson(*token) for token in tokenObjects], indent=2) # creo un multi-string con el formato de un json
tmpFileJsonArray = json.loads(File2Json) #creo un diccionario en base al string json anterior


for i in range(0, (len(tmpFileJsonArray)-1)):
    if (tmpFileJsonArray[i]["token"] == "Keyword.Namespace" and tmpFileJsonArray[i]["value"] == "from") or (tmpFileJsonArray[i]["token"] == "Keyword.Namespace" and tmpFileJsonArray[i]["value"] == "import" and tmpFileJsonArray[i-4]["value"] != "from"): #esta ultima condicion valida que el formato sea: from x import y || import x  
        if tmpFileJsonArray[i+2]["value"] not in importedFilesInFile: #valido que el valor no se encuentre ya en el array (luego voy a validar que no este en la db)
            tmpImported = {"file":tmpFileJsonArray[i+2]["value"], "importedAt": [currentFile], "discovered":1}
            importedFilesInFile.append(tmpImported) 
            #db.registrar()
    if tmpFileJsonArray[i]["token"] == "Name.Class":
        if tmpFileJsonArray[i]["value"] not in classesInFile:
            tmpClass = {"class_name":tmpFileJsonArray[i]["value"], "definedAt": currentFile}
            classesInFile.append(tmpClass)
            db.registrar(C,tmpClass) # Base de datos
    if tmpFileJsonArray[i]["token"] == "Name":
        if tmpFileJsonArray[i]["value"] not in tmpVariables and tmpFileJsonArray[i-1]["value"]!= '.' and tmpFileJsonArray[i-2]["value"]!= 'import' :
            tmpVariables.append(tmpFileJsonArray[i]["value"])
            tmpVariable = {"variable":tmpFileJsonArray[i]["value"], "declaredAt":currentFile}
            variablesInFile.append(tmpVariable)
            db.registrar(VAR,tmpVariable) # Base de datos
    if tmpFileJsonArray[i]["token"] == "Name.Function":
        tmpParams = extractParams(i)
        tmpFunction = {"function":tmpFileJsonArray[i]["value"], "params": tmpParams,"createdAt":currentFile, "importedAt":[]}
        functionsInFile.append(tmpFunction)
        db.registrar(FX,tmpFunction) # Base de datos

listOfFiles = os.listdir()
pyFiles = []
py = "*.py"
for f in listOfFiles:
    if fnmatch.fnmatch(f, py):
        f2save = {'file':f, 'discovered':0}
        pyFiles.append(f2save)

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


