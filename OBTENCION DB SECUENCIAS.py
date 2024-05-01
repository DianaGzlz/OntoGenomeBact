#IMPORT
import uniprot #https://github.com/boscoh/uniprot
import urllib.request
import pandas as pd

#Archivo descargado
archivo = 'ecocyc.gaf'

texto = [] 
with open(archivo) as File:
    for linea in File:
        if '!' in linea:
            pass
        else:
            texto.append(linea)
#Acomodo de registros, ID UNIPROT & GO ID
uniprot_id = []
ontologia = []
for elem in texto:
    contenido = elem.split('\t')
    uniprot_id.append(contenido[1]) #posicion 2
    ontologia.append(contenido[4]) #posicion 5

print(len(uniprot_id), len(ontologia))


#DICCIONARIO UniprotID : [GO IDS]
ids_ontos = {} #3921

for i in range(len(uniprot_id)):
    if uniprot_id[i] in ids_ontos:
        ids_ontos[uniprot_id[i]] += ', ' + ontologia[i]
    else:
        ids_ontos[uniprot_id[i]] = ontologia[i]


#OBTENCION DE SECUENCIAS POR UNIPROT ID
secuencias1 = [] #3886
exito = []
errores = []
for line in ids_ontos.keys(): #fuente: https://gist.github.com/JoaoRodrigues/afe11985e4cab4c0002eebae2213e0a8
    line = line.strip() #elimina espacios en blanco y signos de puntuacion
    if not line:
        continue
    try:
        url = f'https://www.uniprot.org/uniprot/?query={line}&format=fasta'
        with urllib.request.urlopen(url) as r:
            fasta = r.read().decode('utf-8').strip()
            secuencias1.append(fasta)
            exito.append(line)
    except:
        errores.append(line)
print(secuencias1) #, file=ostream

#AJUSTE DE ONTOLOGIAS PARA GUARDADO
ontos = [] #3920 

for elem in exito:
    texto = ids_ontos[elem]
    contenido = texto.split(',')
    ontologias = []
    for eti in contenido:
        ontologias.append(eti)
    onts = list(set(ontologias))
    ontos.append(onts)
len(ontos)

#GUARDADO

array = pd.DataFrame([exito, secuencias1, ontos])
arrayT = array.T
arrayT.to_csv('Datos completos.csv', index=False)