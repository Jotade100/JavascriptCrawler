from pygments import highlight
from pygments.lexers.python import PythonLexer
from pygments.formatters.html import HtmlFormatter

#from pygments import lex
import json

def read():
    tmpFile = open('testFile.py', 'r').read()
    return tmpFile

code = read()
#print(code)
array = list(PythonLexer().get_tokens(code))
def convertToJson(token, text):
    return {"token": str(token)[6:], "text": text}
#print(array[2][0]) # lee las tuplas
File2Json =  json.dumps({"tokens": [convertToJson(*token) for token in array]}, indent=2) # creo un multi-string con el formato de un json
tmpFileJson = json.loads(File2Json) #creo un diccionario en base al string json anterior
tmpTokens = tmpFileJson["tokens"]
for obj in tmpTokens:
    if obj["token"] == "Name.Class":
        print(obj["text"])
    #print(token)
    
#print(array)
#print(tmpFileJson["tokens"])

#for tupla in array:
