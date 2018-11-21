from fileSearch import lectura 
from fileParser import lexeo
<<<<<<< HEAD
import yaml

with open("config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)
# lista con los archivos usados
listaArchivos = [cfg['inicializador']['archivo']]
=======


# lista con los archivos usados
listaArchivos = ['testFile.py']
>>>>>>> f7e958528f10052a952b4d52e593442f75d65435
lectura(listaArchivos)
# Probando la lectura
#print(listaArchivos)
#lexeo(listaArchivos[0])
for i in listaArchivos:
<<<<<<< HEAD
    lexeo(i)
=======
    lexeo(i)

>>>>>>> f7e958528f10052a952b4d52e593442f75d65435
