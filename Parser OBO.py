#IMPORT
import obonet 
import csv #para el archivo de excel


url = 'http://purl.obolibrary.org/obo/go/go-basic.obo'
graph = obonet.read_obo(url) 
#EXTRACCION DE IDS Y NOMBRES DE ETIQUETAS ONTOLOGICAS
id_to_name = {id_: data.get('name') for id_, data in graph.nodes(data=True)}
name_to_id = {data['name']: id_ for id_, data in graph.nodes(data=True) if 'name' in data}

#GENERACION DE DICCIONARIO DE ONTOLOGIAS
dicc_onto = {} #id : descrip
for nombre in graph: #extraer nombres de oontologias
    descrip = id_to_name[nombre]
    id_onto = name_to_id[descrip]
    dicc_onto[id_onto] = descrip
    #nombres.append(id_to_name[nombre])

#GENERACION DE ARCHIVO DE ONTOLOGIAS COMPLETAS
with open('ontologias_completas.csv', 'w') as f:
    for key in dicc_onto.keys():
        f.write("%s, %s\n" % (key, dicc_onto[key]))