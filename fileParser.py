from pygments import highlight
from pygments.lexers.python import PythonLexer
from pygments.formatters.html import HtmlFormatter
import json
import pymongo
import os, fnmatch, sys
import dbConf as db
from pprint import pprint
# ----------------------------- Variables para funciones de la base de datos ---------------------------------------------------------------

VAR, FX, C = "var","fx","class"

# -----------------------------------------------------------------------------------------------------------------------------------------

# -------------------------------------- Instanciacion de Base De Datos ------------------------------------------------------------------
db = db.dataBase()
#record2saveTEST = {'function': 'primeraFuncion', 'params': ['token', 'text'], 'createdAt': 'unitTesting.py', 'importedAt': []}
#db.imprimirVariables()
#db.imprimir(FX)
#db.reset()

def imprimir(cadena):
    return print(cadena.encode('utf-8'))


def extractParams(tmpFileJsonArray, indice): # indice primer parentesis
    indice, params = indice + 1, [] # esto es para empezar a evaluar el primer parametro.

    while tmpFileJsonArray[indice]["value"] != ")":
        if tmpFileJsonArray[indice]["token"] == "Name":
            params.append(tmpFileJsonArray[indice]["value"])
        indice += 1
    return params

def extractInherits(tmpFileJsonArray, indice): # indice primer parentesis
    indice, inheritedClass = indice + 1, "" # esto es para empezar a evaluar el primer parametro.
    
    while tmpFileJsonArray[indice]["value"] != ")":
        if tmpFileJsonArray[indice]["token"] == "Name":
            inheritedClass = tmpFileJsonArray[indice]["value"]
        indice += 1
    return inheritedClass

def readFile(archivo):
    imprimir(archivo)
    tmpFile = open(archivo, 'r', encoding = "utf-8").read()
    return tmpFile

def convertToJson(token, text):
    return {"token": str(token)[6:], "value": text}

def lexeo(archivo):
    importedFilesInFile, classesInFile, variablesInFile, tmpVariables, functionsInFile = [], [], [], [], []
    code = readFile(archivo[0])
    tokenObjects = tuple(PythonLexer().get_tokens(code))
    File2Json =  json.dumps([convertToJson(*token) for token in tokenObjects], indent=2) # creo un multi-string con el formato de un json
    tmpFileJsonArray = json.loads(File2Json)
    #print(tmpFileJsonArray)
    for i in range(0, (len(tmpFileJsonArray)-1)):
        if (tmpFileJsonArray[i]["token"] == "Keyword.Namespace" and tmpFileJsonArray[i]["value"] == "from") or (tmpFileJsonArray[i]["token"] == "Keyword.Namespace" and tmpFileJsonArray[i]["value"] == "import" and tmpFileJsonArray[i-4]["value"] != "from"): #esta ultima condicion valida que el formato sea: from x import y || import x  
            if tmpFileJsonArray[i+2]["value"] not in importedFilesInFile: #valido que el valor no se encuentre ya en el array (luego voy a validar que no este en la db)
                tmpImported = {"file":tmpFileJsonArray[i+2]["value"], "importedAt": [archivo[0]], "route": [archivo[1]] , "discovered":1}
                importedFilesInFile.append(tmpImported) 
        if tmpFileJsonArray[i]["token"] == "Name.Class":
            if tmpFileJsonArray[i]["value"] not in classesInFile:
                tmpInherits = extractInherits(tmpFileJsonArray,i)
                isParent = 1
                if len(tmpInherits)>0:
                    isParent = 0
                tmpClass = {"className":tmpFileJsonArray[i]["value"], "definedAt": archivo[0], "route": [archivo[1]] , "inheritsClass":tmpInherits, "isParentClass": isParent}
                classesInFile.append(tmpClass)
                db.registrar(C,tmpClass) # Base de datos
        if tmpFileJsonArray[i]["token"] == "Name":
            if tmpFileJsonArray[i]["value"] not in tmpVariables and tmpFileJsonArray[i-1]["value"]!= '.' and tmpFileJsonArray[i-2]["value"]!= 'import' :
                tmpVariables.append(tmpFileJsonArray[i]["value"])
                tmpVariable = {"variable":tmpFileJsonArray[i]["value"], "declaredAt":archivo[0], "route": archivo[1]}
                variablesInFile.append(tmpVariable)
                db.registrar(VAR,tmpVariable) # Base de datos
        if tmpFileJsonArray[i]["token"] == "Name.Function":
            tmpParams = extractParams(tmpFileJsonArray,i)
            tmpFunction = {"function":tmpFileJsonArray[i]["value"], "params": tmpParams,"createdAt":archivo[0], "route": archivo[1], "paramsNumber": len(tmpParams) ,"importedAt":[]}
            functionsInFile.append(tmpFunction)
            db.registrar(FX,tmpFunction) # Base de datos
