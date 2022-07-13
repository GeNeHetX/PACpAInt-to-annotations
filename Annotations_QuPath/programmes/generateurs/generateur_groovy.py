#!/usr/bin/env python3

import sys
import os.path


def ecriture_groovy(fichier):
    chemin_geojson =  os.path.abspath(sys.argv[0])[:-43] + "geojson/"
    fichier.write("def entry = getProjectEntry()\n")
    fichier.write('importObjectsFromFile("' + chemin_geojson + 'tumeurs/" + entry.getImageName() + ".geojson")')


def main():

    chemin_groovy = os.path.abspath(sys.argv[0])[:-32] + "groovy/"
    groovy_tumeurs = open(chemin_groovy + "import_tumeurs.groovy", "w")
    ecriture_groovy(groovy_tumeurs)
    groovy_tumeurs.close()


if __name__ == "__main__":
    main()
