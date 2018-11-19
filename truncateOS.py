from fileSearch import lectura 
from fileParser import lexeo


# lista con los archivos usados
listaArchivos = ['testFile.py']
lectura(listaArchivos)
# Probando la lectura
#print(listaArchivos)
#lexeo(listaArchivos[0])
for i in listaArchivos:
    lexeo(i)

