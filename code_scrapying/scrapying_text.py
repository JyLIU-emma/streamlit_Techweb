# -*- coding: utf-8 -*-
# Auteur: Jianying LIU

from bs4 import BeautifulSoup
import json
from MPAscraper import MPA_Scrapper

# scraping de la page
################################
# chemin à remplacer si besoin #
################################
driver = '.\chromedriver.exe'
url_nhhome = "https://www.nh-hotels.fr"
url_requete = url_nhhome + "/corporate/fr/salle-de-presse/nouvelles/nh-hotel-group-reconnu-pour-sa-strategie-durable-contre-le-changement"
scrapper = MPA_Scrapper(url_nhhome,driver)
scrapper.setCookies()
html = scrapper.getHTMLText(url_requete)

# parsing de la page
html_parser = BeautifulSoup(html, 'html.parser')
node_body = html_parser.find('body')

title = node_body.find('h1').string
main_content = node_body.find('div', {'class': 'content node-ultimas-noticias'})
sous_titre = main_content.find("div",{"class": "field-name-field-news-subtitle"}).text
date = main_content.find("div",{"class": "field-name-field-news-date"}).string
texte = main_content.find("div",{"class": "field-name-field-txt-ulnoticias"}).strings
texte = "\n".join([para for para in texte])

#écrire le contenu dans un fichier
contenu = {"Titre":title, "Sous-titre":sous_titre, "Date":date, "Texte":texte}
json_contenu = json.dumps(contenu, indent=4)
with open("scrapying_results/logement_eco/intro_eco_nh-hotels.json", "w", encoding="utf-8") as f:
    f.write(json_contenu)