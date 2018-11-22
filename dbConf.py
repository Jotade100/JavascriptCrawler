# Si no tenes el engine de mongo en tu compu, descarga este link:
#   https://fastdl.mongodb.org/win32/mongodb-win32-x86_64-2008plus-ssl-4.0.4-signed.msi
# Community edition version 4.0.4 para Windows 64-bit x64 (64 bits)
# Si tu compu no es de 64 bits descarga Community Edition para los bits 
# https://www.mongodb.com/download-center/community

# linea de comando para inicializar la db con persistencia en la dir --dbPath
''' "C:\Program Files\MongoDB\Server\4.0\bin\mongod.exe" --dbpath="D:\geord\Docs\Analisis_complejidad\JavascriptCrawler\data"   '''

from pymongo import MongoClient

def imprimir(cadena):
    return print(cadena.encode('utf-8'))

class dataBase():

    def __init__(self, puerto=27017):
        try: 
            self.client = MongoClient('mongodb://localhost', puerto) #27017
            self.client.drop_database('pythonParser')
            self.data = self.client['pythonParser']   # creo/acceso la base de datos
            self.variables_db = self.data['variables']  # creo la coleccion variables en la db pythonParser
            self.functions_db = self.data['functions'] # creo la coleccion functions en la db pythonParser
            self.classes_db = self.data['classes'] # creo la coleccion classes en la db pythonParser
            self._parametros = {"var":self.variables_db, "function":self.functions_db, "class":self.classes_db}
            imprimir("Conectado a la DB ;)")
            #print('Parametros aceptados en colecciones: ', self._parametros)
            #return client
        except:   
            imprimir("error en conexión")

    def registrar(self, collection, dictionary2save):
        if collection == "var":
            self._parametros["var"].insert(dictionary2save)
        if collection == "fx":
            self._parametros["function"].insert(dictionary2save)
        if collection == "class":
            self._parametros["class"].insert(dictionary2save)
        #print('Guardado', dictionary2save)
    
    def imprimir(self, collection):
        if collection == "var":
            _vars = self.variables_db.find() 
            for record in _vars: 
                print(record)
        if collection == "fx":
            _functions = self.functions_db.find()
            for f in _functions:
                print(f)
        if collection == "class":
            _classes = self.classes_db.find()
            for c in _classes:
                print(c)

    def reset(self, collection="all"):
        if collection == "var":
            self.variables_db.drop()
            #print('variables dropeado')
        if collection == "fx":
            self.functions_db.drop()
        if collection == "class":
            self.classes_db.drop()
        if collection == "all":
            self.classes_db.drop()
            self.functions_db.drop()
            self.variables_db.drop()
        
    def query(self, collection, value2search): #class_name
        if collection == "class":
            self.classes_db.find({'inherits_class':value2search})

    
    #print(myDB)

    # estas son las colecciones creadas
    

#record2saveTEST = {'function': 'primeraFuncion', 'params': ['token', 'text'], 'createdAt': 'unitTesting.py', 'importedAt': []}
    #record2saveTEST = myDB.functions.insert(record2saveTEST)

    # imprimo todos los registros en la coleccion de functions
#functions = functions_db.find() 
#for record in functions: 
#    print(record)