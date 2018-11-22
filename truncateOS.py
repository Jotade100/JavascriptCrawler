from fileSearch import lectura 
from fileParser import lexeo
import yaml
import os.path

def imprimir(cadena):
    return print(cadena.encode('utf-8'))

with open("config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

listaArchivos = [[cfg['inicializador']['archivo'], ["INICIO"]]]

# rootFile = cfg['inicializador']['pathBase']+"\\"+cfg['inicializador']['archivo'] # si no funcionara docker, se puede usar esto para definir el path del archivo main sin copiar todo al dir

lectura(listaArchivos)

imprimir("---- Archivos leídos ----")
for i in listaArchivos:
    if (os.path.exists(i[0])):
        lexeo(i)
