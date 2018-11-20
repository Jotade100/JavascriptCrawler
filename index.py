from flask import Flask
app = Flask("Ricolino")

@app.route("/")
def principal():
    return "Probando... 1,2,3, probando..."

@app.route("/consulta",methods = ['POST', 'GET'])
def consulta():
    consulta = request.form['consulta']
    if conexion.get(consulta) != None:
        # Si el parámetro no es vacío
        return ""
    else:
        # El parámetro es vacío
        return ""

app.run(host="localhost",port=5000)