#IMPORT
import csv
from tqdm import tqdm
import numpy as np
import sys
import re
import random
import collections


#BASE DE DATOS
archivo = "Datos completos.csv"
ontos = []
with open(archivo, newline='') as File:  
    reader = csv.reader(File)
    for row in tqdm(reader):
        ontos.append(row[2])
ontos.pop(0) #ELIMINAR HEADER


#GENERACION DE DICCIONARIO DE ETIQUETAS POR PROTEINA
ontologias = [] #vector de cada bacteria
characters = "'[ ] "
for on in tqdm(ontos):
    for x in range(len(characters)):
        on = on.replace(characters[x],"")
    ontologias.append(on)


etiquetas = [] 
dicc_onto_bact = {} #4 206
for o in ontologias:
    labels = o.split(',')
    labels = list(set(labels))
    etiquetas.append(labels)
    for lab in labels:
        dicc_onto_bact[lab] = 1

dic_bact = dict(sorted(dicc_onto_bact.items()))


#GENERACION DE VECTOR DE ONTOLOGIAS BACTERIANAS POR PROTEINA
dicc_vec_bact = {}
c = 0
for vector in ontologias:
    c = c+1
    y = [] #vector y
    for bac in dic_bact.keys():
        if bac in vector:
            y.append(1)
        else:
            y.append(0)
    dicc_vec_bact[c] = y


#GIARDADO DE VECTOR DE ONTOLOGIAS BACTERIANAS POR PROTEINA
with open('vector_ONTO_BAC.csv', 'w') as f:
    for key in dicc_vec_bact.keys():
        f.write("%s, %s\n" % (key, dicc_vec_bact[key]))
