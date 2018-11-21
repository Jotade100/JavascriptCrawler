import yaml
def primeraFuncion(token, text):
    final = token + text
    return final

with open("config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)
cfg['inicializador']['archivo']