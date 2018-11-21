from fileSearch import lectura 
from fileParser import lexeo
import yaml

with open("config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)
# lista con los archivos usados
listaArchivos = [cfg['inicializador']['archivo']]
lectura(listaArchivos)
# Probando la lectura
#print(listaArchivos)
#lexeo(listaArchivos[0])
for i in listaArchivos:
    lexeo(i)
