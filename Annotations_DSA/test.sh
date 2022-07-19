#!/usr/bin/env bash

RED='\033[0;31m'
BLUE='\033[0;36m'
GREEN='\033[0;32m'
NC='\033[0m'

echo -n "Login or email : "
read UTILISATEUR
echo  -n "Password for $UTILISATEUR : "
read -s MOTDEPASSE
echo ""


CHEMIN=$(dirname "$0")
cd $CHEMIN
CHEMIN=$(realpath .)

chmod +x dsa/authenticate.py

if [ "$'(ls ./Images)" != "" ]
then
    if dsa/authenticate.py $UTILISATEUR $MOTDEPASSE
    then
	echo -e "${GREEN}Authentification réussie${NC}"
	echo -n "Dossier de dépôt : "
	read DOSSIER
	let "nb_erreurs = 0"
	for i in Images/*
	do
	    if dsa/complet_dsa.py $UTILISATEUR $MOTDEPASSE $DOSSIER $i
	    then
		echo -e "$i : ${GREEN}OK${NC}"
	    else
		let "nb_erreurs = nb_erreurs + 1"
		echo -e "$i : ${RED}ERREUR${NC}"
	    fi
	done
	if [ $nb_erreurs == 0 ]
	then
	    echo -e "${GREEN}Toutes les images ont été traitées${NC}"
	else
	    echo -e "${RED}$nb_erreurs erreurs sont survenues${NC}"
	fi
    else
	echo -e "${RED}Erreur d'authentification ${NC}"
    fi
fi
