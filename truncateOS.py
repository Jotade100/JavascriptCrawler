from fileSearch import lectura 
from fileParser import lexeo
import yaml
import os.path


with open("config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)
# lista con los archivos usados
listaArchivos = [[cfg['inicializador']['archivo'], ["INICIO"]]]
# rootFile = cfg['inicializador']['pathBase']+"\\"+cfg['inicializador']['archivo'] # si no funcionara docker, se puede usar esto para definir el path del archivo main sin copiar todo al dir
lectura(listaArchivos)
# Probando la lectura
#print(listaArchivos)
#lexeo(listaArchivos[0])
for i in listaArchivos:
    #print(i)
    #print(i[0], os.path.exists(i[0]))
    if (os.path.exists(i[0])):
        lexeo(i)
