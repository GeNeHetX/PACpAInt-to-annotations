#!/usr/bin/env python3

import girder_client as gc
from skimage import io
import sys
import csv
import json
from math import floor


def creation_dossier(client, id_collection, nom_dossier):
    reponse = client.createFolder(id_collection, nom_dossier, parentType="collection", reuseExisting=True)
    id_dossier = str(reponse)[28:]
    pos_id = 1
    while id_dossier[pos_id] != "'":
        pos_id += 1
    id_dossier = id_dossier[:pos_id]
    return id_dossier


def creation_image(client, id_dossier, nom_image):
    chemin_image = "../" + nom_image 
    reponse = client.uploadFileToFolder(id_dossier, nom_image)
    id_image = str(reponse)[218:]
    pos_id = 1
    while id_image[pos_id] != "'":
        pos_id += 1
    id_image = id_image[:pos_id]
    return id_image


def generation_annotations(client, id_image, nom_image):
    chemin_csv = "pacpaint results/" + nom_image[7:] + "/tile_scores.csv"
    corps_tumeurs = '{"description": "", "elements": ['
    corps_stromas = '{"description": "", "elements": ['
    corps_cell_tum = '{"description": "", "elements": ['
    corps_classiques = '{"description": "", "elements": ['
    corps_basal = '{"description": "", "elements": ['
    corps_actifs = '{"description": "", "elements": ['
    corps_inactifs = '{"description": "", "elements": ['
    fichier_csv = open(chemin_csv)
    lecture_csv = csv.reader(fichier_csv, delimiter=',')
    compteur_lignes = 0
    for ligne in lecture_csv:
        if compteur_lignes == 0:
            compteur_lignes += 1
        else:
            
            if float(ligne[4]) >= 0.5:
                tuile = '{"fillColor":"rgba(255, 0, 0, 0.5)","lineColor":"rgba(255, 0, 0, 0.5)","lineWidth":1,"rotation":0,"normal":[0,0,1],"type":"rectangle","center":[%i,%i,0],"width":452,"height":452},' % (floor((int(ligne[2])*112+56)/0.2479), floor((int(ligne[3])*112+56)/0.2479))
                corps_tumeurs = "".join([corps_tumeurs, tuile])

                if float(ligne[5]) >= 0.5:
                     tuile = '{"fillColor":"rgba(255, 0, 0, 0.5)","lineColor":"rgba(255, 0, 0, 0.5)","lineWidth":1,"rotation":0,"normal":[0,0,1],"type":"rectangle","center":[%i,%i,0],"width":452,"height":452},' % (floor((int(ligne[2])*112+56)/0.2479), floor((int(ligne[3])*112+56)/0.2479))
                     corps_cell_tum  = "".join([corps_cell_tum, tuile])

                     if float(ligne[6]) > float(ligne[7]):
                         tuile = '{"fillColor":"rgba(255, 150, 0, 0.5)","lineColor":"rgba(255, 150, 0, 0.5)","lineWidth":1,"rotation":0,"normal":[0,0,1],"type":"rectangle","center":[%i,%i,0],"width":452,"height":452},' % (floor((int(ligne[2])*112+56)/0.2479), floor((int(ligne[3])*112+56)/0.2479))
                         corps_classiques  = "".join([corps_classiques, tuile])

                     else:
                         tuile = '{"fillColor":"rgba(150, 0, 0, 0.5)","lineColor":"rgba(150, 0, 0, 0.5)","lineWidth":1,"rotation":0,"normal":[0,0,1],"type":"rectangle","center":[%i,%i,0],"width":452,"height":452},' % (floor((int(ligne[2])*112+56)/0.2479), floor((int(ligne[3])*112+56)/0.2479))
                         corps_basal  = "".join([corps_basal, tuile])
                else:
                    tuile = '{"fillColor":"rgba(50, 200, 50, 0.5)","lineColor":"rgba(50, 200, 50, 0.5)","lineWidth":1,"rotation":0,"normal":[0,0,1],"type":"rectangle","center":[%i,%i,0],"width":452,"height":452},' % (floor((int(ligne[2])*112+56)/0.2479), floor((int(ligne[3])*112+56)/0.2479))
                    corps_stromas  = "".join([corps_stromas, tuile])

                    if float(ligne[8]) > float(ligne[9]):
                        tuile = '{"fillColor":"rgba(0, 150, 0, 0.5)","lineColor":"rgba(0, 150, 0, 0.5)","lineWidth":1,"rotation":0,"normal":[0,0,1],"type":"rectangle","center":[%i,%i,0],"width":452,"height":452},' % (floor((int(ligne[2])*112+56)/0.2479), floor((int(ligne[3])*112+56)/0.2479))
                        corps_actifs  = "".join([corps_actifs, tuile])

                    else:
                        tuile = '{"fillColor":"rgba(0, 255, 0, 0.5)","lineColor":"rgba(0, 255, 0, 0.5)","lineWidth":1,"rotation":0,"normal":[0,0,1],"type":"rectangle","center":[%i,%i,0],"width":452,"height":452},' % (floor((int(ligne[2])*112+56)/0.2479), floor((int(ligne[3])*112+56)/0.2479))
                        corps_inactifs  = "".join([corps_inactifs, tuile])

    corps_tumeurs = corps_tumeurs[:-1]
    corps_tumeurs = "".join([corps_tumeurs, '], "name": "annotations_tumeurs"}'])
    corps_cell_tum = corps_cell_tum[:-1]
    corps_cell_tum = "".join([corps_cell_tum, '], "name": "annotations_cellules_tumorales"}'])
    corps_stromas = corps_stromas[:-1]
    corps_stromas = "".join([corps_stromas, '], "name": "annotations_stromas"}'])
    corps_classiques = corps_classiques[:-1]
    corps_classiques = "".join([corps_classiques, '], "name": "annotations_classiques"}'])
    corps_basal = corps_basal[:-1]
    corps_basal = "".join([corps_basal, '], "name": "annotations_basal"}'])
    corps_actifs = corps_actifs[:-1]
    corps_actifs = "".join([corps_actifs, '], "name": "annotations_actifs"}'])
    corps_inactifs = corps_inactifs[:-1]
    corps_inactifs = "".join([corps_inactifs, '], "name": "annotations_inactifs"}'])
    postStr = "annotation?itemId=%s" % (id_image)
    client.post(postStr, data=corps_tumeurs)
    client.post(postStr, data=corps_cell_tum)
    client.post(postStr, data=corps_stromas)
    client.post(postStr, data=corps_classiques)
    client.post(postStr, data=corps_basal)
    client.post(postStr, data=corps_actifs)
    client.post(postStr, data=corps_inactifs)

    return 0


def main():
    if len(sys.argv) != 5:
        print("Veuillez préciser un nom de dossier de dépôt")
        sys.exit(1)
    
    client = gc.GirderClient(apiUrl="http://34.76.208.101:8080/api/v1")
    client.authenticate(sys.argv[1], sys.argv[2])

    id_collection = "62d51a3357e5cb919e96d219"
    id_dossier = creation_dossier(client, id_collection, sys.argv[3])
    id_image = creation_image(client, id_dossier, sys.argv[4])
    generation_annotations(client, id_image, sys.argv[4])
    return  0

if __name__ == "__main__":
    main()
