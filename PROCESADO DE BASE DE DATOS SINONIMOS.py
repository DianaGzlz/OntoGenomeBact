#IMPORT
import csv
from tqdm import tqdm
import re
import random


#ARCHIVO DE TRABAJO
archivo = "Datos completos.csv"
proteinas = []
with open(archivo, newline='') as File:  
    reader = csv.reader(File)
    for row in tqdm(reader):
        proteinas.append(row[1]) #secuencia de proteina
proteinas.pop(0) #Eliminar header de archivo


#DICCIONARIO DE RETROTRADUCCION
dicc_amino_DNA = {
    'A' : ['GCT', 'GCC', 'GCA', 'GCG'], #Ala Alanina
    'C' : ['TGT', 'TGC'], #Cys Cisteina
    'D' : ['GAC', 'GAT'], #Asp Acido Aspártico
    'E' : ['GAA', 'GAG'], #GlT Acido GlTtámico
    'F' : ['TTT', 'TTC'], #Phe Fenilalanina
    'G' : ['GGT','GGC', 'GGA', 'GGG'], #Gly Glicina
    'H' : ['CAT', 'CAC'], #His Histidina
    'I' : ['ATT', 'ATC', 'ATA'], #Ile IsoleTcina
    'K' : ['AAA', 'AAG'], #Lys Lisina
    'L' : ['TTA', 'TTG', 'CTT', 'CTC', 'CTA', 'CTG'], #LeT LeTcina
    'M' : ['ATG'], #Met Metionina
    'N' : ['AAC', 'AAT'], #Asn Asparagina
    'P' : ['CCT', 'CCC', 'CCA', 'CCG'], #Pro Prolina
    'Q' : ['CAA', 'CAG'], #Gln GlTtamina
    'R' : ['AGA', 'AGG', 'CGA', 'CGC', 'CGG', 'CGT'], #Arg Arginina
    'S' : ['TCT', 'TCC', 'TCA', 'TCG', 'AGT', 'AGC'], #Ser Serina
    'T' : ['ACT', 'ACC', 'ACA', 'ACC'], #Thr Treonina
    #selenocisteina, codon de paro
    'U' : ['TGA'], #Sec Selenocisteina, codon normalmente interpretado como codon de paro
    'V' : ['GTT', 'GTC', 'GTA', 'GTG'], #Val Valina
    'W' : ['TGG'], #Trp Triptófano
    #Xxx Aminácido no determiando
    'X' : ['GCT', 'GCC', 'GCA', 'GCG', 'TGT', 'TGC', 'GAC', 'GAT', 'GAA', 'GAG', 'TTT', 'TTC',
    'GGT', 'GGC', 'GGA', 'GGG', 'CAT', 'CAC', 'ATT', 'ATC', 'ATA', 'AAA', 'AAG', 'TTA', 'TTG', 
    'CTT', 'CTC', 'CTA', 'CTG', 'ATG', 'AAC', 'AAT', 'CCT', 'CCC', 'CCA', 'CCG', 'CAA', 'CAG',
    'AGA', 'AGG', 'CGA', 'CGC', 'CGG', 'CGT', 'TCT', 'TCC', 'TCA', 'TCG', 'AGT', 'AGC', 'ACT',
    'ACC', 'ACA', 'ACC', 'GTT', 'GTC', 'GTA', 'GTG', 'TGG', 'TAT', 'TAC'], #TODAS ALS OPCIONES POSIBLES
    'Y' : ['TAT', 'TAC'], #Tyr Tirosina
    'Z' : ['GAA', 'GAG'], #Glx GlTtamina T otro GlTtámico 
    #PONGO LO MISMO EN Z QTE EN E
}


#FUNCIONES
def orden_secuencia(prot): #SECUENCIA LIMPIA DE PROTEINA
    if '\r' in prot:
        cadenas = prot.split('\r\n')
    else:
        cadenas = prot.split('\n')
    cadenas.pop(0) #titulo
    cadena_aminoac = ''
    for cad in cadenas:
        cad.replace(' ','')
        cad.replace('\r','')
        re.sub(r" \r", "", cad)
        cadena_aminoac = cadena_aminoac + cad
        
    return cadena_aminoac

def palabras (secuencia): # GENERACION DE PALABRAS POR PROTEINAS
    tam = len(secuencia)
    c1 = 0
    c2 = 5
    palabras = []
    for i in range(tam):
        if c2<tam:
            palabras.append(secuencia[c1:c2])
        if c2==tam:
            palabras.append(secuencia[c1:])
        c1 = c1+1
        c2 = c2+1 
    return palabras #contar palabras por proteinas (dicc de conteos)

def trad_inv(palabra): #RETROTRADUCCIONES POR PALABRA
    lista_pal = list(palabra)
    try:
        cadenas = dicc_amino_DNA[lista_pal[0]] #inicial
        for i in range(1,len(lista_pal)): #no contamos el 0, 5 PORQUE SON PALABRAS DE TAMANO 5
            comb = dicc_amino_DNA[lista_pal[i]]
            lista_temp = [] #vacio
            for cad in cadenas: #por cada cadena existente
                for co in comb: #por combinacion posible
                    lista_temp.append(cad + co)
            cadenas = lista_temp
        return cadenas #lista de traducciones por palabra
    except:
        pass

def kmeros(traducc): #KMEROS POR RETROTRADUCCION
    lista_km = []
    lista_km.append(traducc[0:13])
    lista_km.append(traducc[1:14])
    lista_km.append(traducc[2:])
    return lista_km #guardar equivalencias en diccionario

def guardar_prot_pal(palabra, Lote): #GUARDADO DE KMEROS EN ARCHIVO
    with open('archivos_NN/vector_nn'+Lote+'.txt', 'a') as f:
        f.write(palabra)


#PROCESADO DE BASE DE DATOS Y GENERACION DE ARCHIVOS DE TRAINING Y TESTING POR SINONIMOS
c1 = 0
for prot in tqdm(proteinas):
    vector = []
    c1+=1
    secuencia = orden_secuencia(prot)
    words = palabras(secuencia)
    for pal in words:
        traduccs = trad_inv(pal)
        traduccs = list(set(traduccs))
        sin1 = ''
        sin2 = ''
        sin3 = ''
        for trad in traduccs:
            ksecs = kmeros(trad)
            sin1 += ksecs[0] + ','
            sin2 += ksecs[1] + ','
            sin3 += ksecs[2] + ','
        
        sin1 = sin1[0:-1] + '.' + str(c1) + '-'
        sin2 = sin2[0:-1] + '.' + str(c1) + '-'
        sin3 = sin3[0:-1] + '.' + str(c1) + '-'
        vector.append(sin1)
        vector.append(sin2)
        vector.append(sin3)
    random.shuffle(vector)
    tot_km = len(vector)

    #GUARDADO DE ARCHIVOS
    training = tot_km*0.91 #91% dtos totales
    tr1 = int(1*(training/10)) #10% datos training
    tr2 = int(2*(training/10)) #10% datos training
    tr3 = int(3*(training/10)) #10% datos training
    tr4 = int(4*(training/10)) #10% datos training
    tr5 = int(5*(training/10)) #10% datos training
    tr6 = int(6*(training/10)) #10% datos training
    tr7 = int(7*(training/10)) #10% datos training
    tr8 = int(8*(training/10)) #10% datos training
    tr9 = int(9*(training/10)) #10% datos training
    tr10 = int(training) #10% datos training
    #TRAINING
    train1 = ''
    for kmr in (range(0,tr1)):
        train1+=vector[kmr]
    guardar_prot_pal(train1, '_tr1')
    train2 = ''
    for kmr in (range(tr1,tr2)):
        train2+=vector[kmr]
    guardar_prot_pal(train2, '_tr2')
    train3 = ''
    for kmr in (range(tr2,tr3)):
        train3+=vector[kmr]
    guardar_prot_pal(train3, '_tr3')
    train4 = ''
    for kmr in (range(tr3,tr4)):
        train4+=vector[kmr]
    guardar_prot_pal(train4, '_tr4')
    train5 = ''
    for kmr in (range(tr4,tr5)):
        train5+=vector[kmr]
    guardar_prot_pal(train5, '_tr5')
    train6 = ''
    for kmr in (range(tr5,tr6)):
        train6+=vector[kmr]
    guardar_prot_pal(train6, '_tr6')
    train7 = ''
    for kmr in (range(tr6,tr7)):
        train7+=vector[kmr]
    guardar_prot_pal(train7, '_tr7')
    train8 = ''
    for kmr in (range(tr7,tr8)):
        train8+=vector[kmr]
    guardar_prot_pal(train8, '_tr8')
    train9 = ''
    for kmr in (range(tr8,tr9)):
        train9+=vector[kmr]
    guardar_prot_pal(train9, '_tr9')
    train10 = ''
    for kmr in (range(tr9,tr10)):
        train10+=vector[kmr]
    guardar_prot_pal(train10, '_tr10')
    #TESTING
    test_vec = ''
    for kmr in (range(tr10, tot_km)):
        test_vec += vector[kmr]
    guardar_prot_pal(test_vec, '_testing')

