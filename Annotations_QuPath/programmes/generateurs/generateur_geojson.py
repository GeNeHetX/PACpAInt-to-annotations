#!/usr/bin/env python3

import csv
import json
from math import floor
import sys


def generateur_geojson_tumeurs(nom_fichier, lame):

    fichier_geojson_tumeurs = nom_fichier[:-(len(lame)+7)] + "geojson/tumeurs/"  + lame + ".geojson"
    ecriture_geojson_tumeurs = open(fichier_geojson_tumeurs, "w")
    
    body = '{"type":"FeatureCollection", "features":['

    fichier_csv = nom_fichier[:-(len(lame)+7)] + "/pacpaint results/" + lame + "/tile_scores.csv"
    lecture_csv = open(fichier_csv, "r")
    iterateur_csv = csv.reader(lecture_csv, delimiter=',')
    line_count = 0
    for row in iterateur_csv:
        if line_count == 0:
            line_count += 1
        else:
            if float(row[4]) >= 0.5:
                xcoin = floor((int(row[2]))*112/0.2479)
                ycoin = floor((int(row[3]))*112/0.2479)
                tuile = '{"type":"Feature","geometry":{"type":"Polygon","coordinates":[[[%i, %i],[%i, %i],[%i, %i],[%i, %i],[%i, %i]]]},"properties":{"object_type":"annotation","classification":{"name":"Tumor","colorRGB":-3670016},"isLocked":false}},' % (xcoin, ycoin, xcoin, ycoin + 452, xcoin + 452, ycoin + 452, xcoin + 452, ycoin, xcoin, ycoin)
                body = "".join([body, tuile])
    body = body[:-1]
    body = "".join([body, ']}'])
    ecriture_geojson_tumeurs.write(body)
    lecture_csv.close()

    ecriture_geojson_tumeurs.close()


def main():
    
    if len(sys.argv) != 2:
        print("Erreur lors du chargement des fichiers dans le dossier")
        sys.exit(1)

    lame = ""
    fin = 1
    nom_fichier = sys.argv[1]
    while nom_fichier[-fin] != "/":
        lame = nom_fichier[-fin] + lame
        fin += 1
    generateur_geojson_tumeurs(nom_fichier, lame)


if __name__ == "__main__":
    main()
