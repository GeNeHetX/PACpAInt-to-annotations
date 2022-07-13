#!/usr/bin/env bash

RED='\033[0;31m'
BLUE='\033[0;36m'
GREEN='\033[0;32m'
NC='\033[0m'

CHEMIN=$(dirname "$0")
cd $CHEMIN
CHEMIN=$(realpath .)

chmod +x programmes/generateurs/generateur_geojson.py programmes/generateurs/generateur_groovy.py

echo -e "${BLUE} IMAGES TRAITEES :${NC}"
let "nb_erreurs = 0"
if [ "$'(ls ./Images)" != "" ]
then
    for i in Images/*
    do
	if programmes/generateurs/generateur_geojson.py $CHEMIN/$i
	then
	    echo -e "$i : ${GREEN}OK${NC}"
	else
	    let "nb_erreurs = nb_erreurs + 1"
	    echo -e "$i : ${RED}ERREUR${NC}"
	fi
    done
else
    echo -e "${RED}PAS D'IMAGES DANS LE DOSSIER${NC}"
fi

if [ $nb_erreurs == 0 ]
then
    echo -e "${GREEN}Toutes les images ont été traitées${NC}"
    if programmes/generateurs/generateur_groovy.py $CHEMIN
    then
	echo -e "${GREEN}Génération des fichiers groovy effectuée"
    else
	echo -e "${RED}Erreur lors de la génération des fichiers grrovy"
    fi
else
    echo -e "${RED}$nb_erreurs erreurs sont survenues${NC}"
fi

