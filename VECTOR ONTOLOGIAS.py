#IMPORT
import csv
from tqdm import tqdm




# ARCHIVO DE ONTOLOGIAS COMPLETAS 43558
dicc_onto_compl = {}
with open ('ontologias_completas.csv', 'r') as f:
    reader = csv.reader(f)
    for row in tqdm(reader):
        dicc_onto_compl[row[0]] = row[1]


#DE BASE DE DATOS GENERACION DE DICCIONARIO DE ETIQUETAS ONTOLOGICAS POR PROTEINA 3920
dicc_prot_onto = {}
c1 = 0
characters = "' "
with open ('Datos completos.csv', 'r') as d:
    reader = csv.reader(d)
    for row in tqdm(reader):
        cadena = row[2]
        cadena = row[2][3:-3]
        cadena = ''.join( x for x in cadena if x not in characters)
        cadenas = cadena.split(',')
        dicc_prot_onto[c1] = cadenas
        c1+=1
del dicc_prot_onto[0] #BORRAR HEADER DE DICCIONARIO


#GENERACION DE VECTOR DE ONTOLOGIAS POR PROTEINA
dicc_vectorY = {}

for key in tqdm(dicc_prot_onto):
    valores = dicc_prot_onto[key]
    vectory = []
    for clave in dicc_onto_compl.keys():
        if clave not in valores:
            vectory.append(0)
        if clave in valores:
            vectory.append(1)
    dicc_vectorY[key] = vectory


#GUARDADO DE VECTORES DE ONTOLOGIAS DE PROTEINAS
with open('vectory_ontologias.csv', 'w') as f:
    for key in dicc_vectorY.keys():
        f.write("%s, %s\n" % (key, dicc_vectorY[key]))