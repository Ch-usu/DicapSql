import csv
import os

def leerVariablesUsuario():
    """"asume que exite un archivo de nombre variablesUsuario.csv
    y retorna un diccionario con las variables de usuario"""
    with open("variablesUsuario.csv") as f:
        variables = csv.DictReader(f ,delimiter=',')
        return list(variables)[0]

def escribirVariablesUsuario(variables):
    """Asume variables como un diccionario que contiene {"host": "", "user":"", "password":""}
    y retorna un strig que afirma que los cambios se han realizado"""
    with open("variablesUsuario.csv", "w") as f:
        escritor = csv.writer(f)
        escritor.writerow(variables.keys())
        escritor.writerow(variables.values())
    return leerVariablesUsuario()

def excelEnnumeration(name):
    distfiles = os.listdir()
    numberofexcelFile = 0
    for distfile in distfiles:
        if(name in distfile):
            numberofexcelFile += 1
    return numberofexcelFile

