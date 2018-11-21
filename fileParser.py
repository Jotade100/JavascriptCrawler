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
#db.registrar("var",record2saveTEST)
#db.imprimirVariables()
#db.imprimir(FX)
#db.reset()
#db.imprimir(FX)
#db.reset()



def extractParams(tmpFileJsonArray, indice): # indice primer parentesis
    indice = indice + 1 # esto es para empezar a evaluar el primer parametro.
    params = []
    while tmpFileJsonArray[indice]["value"] != ")":
        if tmpFileJsonArray[indice]["token"] == "Name":
            params.append(tmpFileJsonArray[indice]["value"])
        indice += 1
    return params

def extractInherits(tmpFileJsonArray, indice): # indice primer parentesis
    indice = indice + 1 # esto es para empezar a evaluar el primer parametro.
    while tmpFileJsonArray[indice]["value"] != ")":
        if tmpFileJsonArray[indice]["token"] == "Name":
            inheritedClass = tmpFileJsonArray[indice]["value"]
        indice += 1
    return inheritedClass

def readFile(archivo):
    tmpFile = open(archivo, 'r').read()
    return tmpFile

def convertToJson(token, text):
    return {"token": str(token)[6:], "value": text}

def lexeo(archivo):
    importedFilesInFile = []
    queue4scrawler = []
    classesInFile = []
    variablesInFile = [] #aqui se guardan los objetos json
    tmpVariables = [] #aqui se guarda solo el nombre de las variables en el archivo para validar que no se guarden en variablesInFile vars repetidas
    functionsInFile = []
    try:
        code = readFile(archivo) 
        tokenObjects = tuple(PythonLexer().get_tokens(code))
        File2Json =  json.dumps([convertToJson(*token) for token in tokenObjects], indent=2) # creo un multi-string con el formato de un json
        tmpFileJsonArray = json.loads(File2Json)
        #print(tmpFileJsonArray)
        for i in range(0, (len(tmpFileJsonArray)-1)):
            if (tmpFileJsonArray[i]["token"] == "Keyword.Namespace" and tmpFileJsonArray[i]["value"] == "from") or (tmpFileJsonArray[i]["token"] == "Keyword.Namespace" and tmpFileJsonArray[i]["value"] == "import" and tmpFileJsonArray[i-4]["value"] != "from"): #esta ultima condicion valida que el formato sea: from x import y || import x  
                if tmpFileJsonArray[i+2]["value"] not in importedFilesInFile: #valido que el valor no se encuentre ya en el array (luego voy a validar que no este en la db)
                    tmpImported = {"file":tmpFileJsonArray[i+2]["value"], "importedAt": [archivo], "discovered":1}
                    importedFilesInFile.append(tmpImported) 
            if tmpFileJsonArray[i]["token"] == "Name.Class":
                if tmpFileJsonArray[i]["value"] not in classesInFile:
                    tmpInherits = extractInherits(tmpFileJsonArray,i)
                    tmpClass = {"class_name":tmpFileJsonArray[i]["value"], "definedAt": archivo, "inherits_class":tmpInherits}
                    classesInFile.append(tmpClass)

                    db.registrar(C,tmpClass) # Base de datos


            if tmpFileJsonArray[i]["token"] == "Name":
                if tmpFileJsonArray[i]["value"] not in tmpVariables and tmpFileJsonArray[i-1]["value"]!= '.' and tmpFileJsonArray[i-2]["value"]!= 'import' :
                    tmpVariables.append(tmpFileJsonArray[i]["value"])
                    tmpVariable = {"variable":tmpFileJsonArray[i]["value"], "declaredAt":archivo}
                    variablesInFile.append(tmpVariable)
                    db.registrar(VAR,tmpVariable) # Base de datos

            if tmpFileJsonArray[i]["token"] == "Name.Function":
                tmpParams = extractParams(tmpFileJsonArray,i)
                #if tmpFileJsonArray[i+1]["token"] == "Token.Punctuation":
                tmpFunction = {"function":tmpFileJsonArray[i]["value"], "params": tmpParams,"createdAt":archivo, "paramsNumber": len(tmpParams) ,"importedAt":[]}
                functionsInFile.append(tmpFunction)
                db.registrar(FX,tmpFunction) # Base de datos
        # Terminado de leer el archivo
        #print(classesInFile)
        #print(variablesInFile)
        #print(functionsInFile)

    except:
        variable = 0

#db.imprimir(FX)

#db.imprimir(FX)
#cursor = db.classes_db.find({"inherits_class": "data"})
#for d in cursor:
#    pprint(d["class_name"])
#db.reset()
# # # # # # # # # # # # # # Código de prueba # # # # # # # # # # # # # # # # #

# importedFilesInFile = [] #archivos a parsear
# classesInFile = []
# variablesInFile = [] #aqui se guardan los objetos json
# tmpVariables = [] #aqui se guarda solo el nombre de las variables en el archivo para validar que no se guarden en variablesInFile vars repetidas
# functionsInFile = []
# queue4scrawler = [] #se va a hacer enqueue a los archivos que no hayan sido descubiertos tras validar en la db (que no se ha creadp)

# currentFile = 'brewTesting.py' #convertir a variable dinamica al momento de convertir este bloque a funcion
# code = readFile(currentFile) 
# #print(currentFile)
# tokenObjects = tuple(PythonLexer().get_tokens(code))
# File2Json =  json.dumps([convertToJson(*token) for token in tokenObjects], indent=2) # creo un multi-string con el formato de un json
# tmpFileJsonArray = json.loads(File2Json) #creo un diccionario en base al string json anterior

# for i in range(0, (len(tmpFileJsonArray)-1)):
#     if (tmpFileJsonArray[i]["token"] == "Keyword.Namespace" and tmpFileJsonArray[i]["value"] == "from") or (tmpFileJsonArray[i]["token"] == "Keyword.Namespace" and tmpFileJsonArray[i]["value"] == "import" and tmpFileJsonArray[i-4]["value"] != "from"): #esta ultima condicion valida que el formato sea: from x import y || import x  
#         if tmpFileJsonArray[i+2]["value"] not in importedFilesInFile: #valido que el valor no se encuentre ya en el array (luego voy a validar que no este en la db)
#             tmpImported = {"file":tmpFileJsonArray[i+2]["value"], "importedAt": [currentFile], "discovered":1}
#             importedFilesInFile.append(tmpImported) 
#     if tmpFileJsonArray[i]["token"] == "Name.Class":
#         if tmpFileJsonArray[i]["value"] not in classesInFile:
#             tmpClass = {"class_name":tmpFileJsonArray[i]["value"], "definedAt": currentFile}
#             classesInFile.append(tmpClass)
#     if tmpFileJsonArray[i]["token"] == "Name":
#         if tmpFileJsonArray[i]["value"] not in tmpVariables and tmpFileJsonArray[i-1]["value"]!= '.' and tmpFileJsonArray[i-2]["value"]!= 'import' :
#             tmpVariables.append(tmpFileJsonArray[i]["value"])
#             tmpVariable = {"variable":tmpFileJsonArray[i]["value"], "declaredAt":currentFile}
#             variablesInFile.append(tmpVariable)
#     if tmpFileJsonArray[i]["token"] == "Name.Function":
#         tmpParams = extractParams(i)
#         #if tmpFileJsonArray[i+1]["token"] == "Token.Punctuation":
#         tmpFunction = {"function":tmpFileJsonArray[i]["value"], "params": tmpParams,"createdAt":currentFile, "paramsNumber": len(tmpParams) ,"importedAt":[]}
#         functionsInFile.append(tmpFunction)


# #print(tmpFileJsonArray)
# #print(importedFilesInFile)
# #print("Clases en archivo leído: ",classesInFile)
# #print("Variables en archivo leído: ",variablesInFile)
# #print("Funciones en archivo leído: ", functionsInFile)

# def lecturaLimpiaClases(classesArray):
#     print("--------------------------- Clases en el archivo -----------------------------------\n")
#     for clase in classesArray:        
#         print(clase["class_name"])
#     print('\n')
# def lecturaLimpiaVariables(variablesArray):
#     print("--------------------------- Variables en el archivo -----------------------------------\n")
#     for var in variablesArray:
#         print(var["variable"])
#     print('\n')
# def lecturaLimpiaFunciones(functionsArray):
#     print("--------------------------- Funciones en el archivo -----------------------------------\n")
#     for func in functionsArray:
#         print(func["function"])
#     print('\n')

#lecturaLimpiaClases(classesInFile)
#lecturaLimpiaVariables(variablesInFile)
#lecturaLimpiaFunciones(functionsInFile)

#for pyFile in pyFiles:
#    registerFile = {"file":pyFile}
#    db_archivosLeidos.insert_one(registerFile)

#for x in db_archivosLeidos.find():
  #print(x)
#print(tokenObjects)
#print(tmpFileJsonArray)
#print(functionsInFile)