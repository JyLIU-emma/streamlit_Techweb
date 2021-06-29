# -*- coding: utf-8 -*-
# Auteur: Jianying LIU

from bs4 import BeautifulSoup
import json
from MPAscraper import MPA_Scrapper

# scraping de la page
url = "https://www.laclefverte.org/recherche/?types="
driver = "None"
scrapper = MPA_Scrapper(url,driver)
cat_liste = [("Campings",0),("Hôtels",1),("Chambres d'hôtes",3),("Résidences de tourisme",5),("Villages et centres de vacances", 7),("Auberges de jeunesse",4),("Restaurants",6),("Gîtes et Meublés",2)]

type_nombre = []
for i in cat_liste:
    url_requete = url + str(i[1])
    html = scrapper.getHTMLText(url_requete)
    html_parser = BeautifulSoup(html, 'html.parser')
    nombre = html_parser.find('div', {'class': 'count pull-left'}).text.strip()
    nombre = nombre.split(" résultats ")[0]
    type_nombre.append({"cat": i[0], "nombre": int(nombre)})

#écrire le contenu dans un fichier
json_contenu = json.dumps(type_nombre, indent=4)
with open("scrapying_results/logement_eco/calcul_nombre.json", "w", encoding="utf-8") as f:
    f.write(json_contenu)