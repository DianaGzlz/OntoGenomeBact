#IMPORT
from matplotlib import pyplot as plt
import tensorflow as tf
import numpy as np
import csv
import random
from tqdm import tqdm


#MODELO DE RED NEURONAL
############ insertar codigo acorde a arquitectura ##############
#ejemplo CNN A
batch_size = 10000
num_classes = 43558
epochs = 5
input_shape = (4, 13, 1)
#model
model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(1000, (5,5), padding='same', activation='relu', input_shape=input_shape),
    tf.keras.layers.MaxPool2D(),
    tf.keras.layers.Dropout(0.25),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(num_classes, activation='softmax')
])
#compilacion
model.compile(optimizer='Adam', loss='categorical_crossentropy', metrics=[tf.keras.metrics.AUC()])



#ARCHIVOS DE ALIMENTACION
#ontologias
vy1 = 'vectory_ontologias.csv' #'vector_ONTO_BAC.csv'
dicc_onto = {}

with open(vy1, 'r') as f:
    reader = csv.reader(f)
    for row in tqdm(reader):
        characters = "' []"
        cadena = row[1:]
        cadena = ''.join( x for x in cadena if x not in characters)
        cadenas = list(cadena)
        vectr = []
        for cad in cadenas:
            try:
                vectr.append(int(cad))
            except:
                pass
        dicc_onto[row[0]] = vectr

#kmeros
direc = 'folder1/vector_nn_tr1.txt'
arch = open(direc, 'r')
cont = arch.read()
texto = cont.split(',') #dividimos por conjunto de sinonimos
random.shuffle(texto)
cont = [] #vaciar para disminuir consumo de memoria
tam = len(texto) #368 444


#FUNCIONES
def OHE (kmeros): #convierte kmeros en OHE
    kmer = list(kmeros)
    vector = np.zeros((4,13), dtype=float)
    for i in range(13): #por cada letra del kmero
        if kmer[i] == 'A':
            vector[0][i] = 1
        if  kmer[i] == 'C':
            vector[1][i] = 1
        if  kmer[i] == 'T':
            vector[2][i] = 1
        if  kmer[i] == 'G':
            vector[3][i] = 1
    return vector

def vectores(texto): #reparte la informacion en lotes para entrenar
    kmeros_ohe = []
    ontos = []
    for tx in texto:
        if tx == '':
            pass
        else:
            partes = tx.split('.')
            ontos.append(dicc_onto[partes[1]])
            vec_ohe = OHE(partes[0])
            kmeros_ohe.append(vec_ohe)
            text = 0 #reemplazamos valor original por cero para usar menos memoria
    x_train = np.array(kmeros_ohe) 
    y_train = np.array(ontos)
    kmeros_ohe = [] #vaciamos el vector para usar menos memoria, ya convertido en array
    ontos = []
    return x_train, y_train


def correr_training(x_train, y_train): #Corre el lote de entrada en el modelo
    history = model.fit(x_train, y_train, batch_size=batch_size, epochs=epochs, validation_split=0.1)
                        #callbacks=[progbar])
    return history


def guardado(history, n1, n2):
    archivo = 'modelos/history_cnn_' + lot_ar + '.txt'
    cinco, seis = n1, n2
    losstrain,  lossval, auctrain, aucval = [], [], [], []
    for key in history.history.keys(): #cada key tiene una lsita de valores de cantidad de epocas
        if 'loss' in key[0:4]:
            losstrain += history.history[key] #asignar esa lista a un valor
        if 'val_loss' in key:
            lossval += history.history[key]
        if 'auc' in key[0:3]:
            auctrain += history.history[key]
        if 'val_auc' in key:
            aucval += history.history[key]
        clave = ''
    for i in range(epochs): #crear cadena de texto por epoca
        clave += str(losstrain[i]) + '\t' + str(lossval[i]) + '\t' + str(auctrain[i]) + '\t' + str(aucval[i]) + '\t' + str(n1) + '\t' + str(n2) + '\n'        
    m = open (archivo, 'a')  
    m.write(clave) #guardar el texto por lote
    m.close()
    mensaje = 'Se ha guardado lote ' + str(n1) + ' a ' + str(n2)
    return mensaje


def lotes(tam): #recibe tamano de archivo para generar vectores
    ciclos = int(tam/10000) #22,123,922.9 = 22,123,922 -> 22123 ciclos
    for e in tqdm(range(ciclos)):
        vector = texto[n1:n2] #por tamano de lote extraemos info
        vx, vy = vectores(vector) #convertir la inf a vectores
        record = correr_training(vx, vy) #mandar a training el vector
        msj = guardado(record, n1, n2)
        n1=+10000
        n2=+10000
    print('Ultimo ciclo')
    vector = texto[n2:] #n2=221230000, final=221239229, lote = 9229 datos
    vx, vy = vectores(vector) #convertir la inf a vectores
    record = correr_training(vx, vy) #mandar a training el vector
    msj = guardado(record, n1, n2)

    return print(msj)



#EJECUCION DE PROGRAMA
n1 = 0
n2 = 10000
vecs = lotes(tam)