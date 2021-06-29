# -*- coding: utf-8 -*-
# Auteur: Jianying LIU

import requests
import json

url = "https://apis.ntealan.net/ntealan/dictionaries/metadata"
try:
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    metadata = response.json()
except Exception:
    print("echec de téléchargement : %s"%(url))
    print("HTTP-Code :", response.status_code)

liste_meta = []
for i in metadata['metadata']:
    liste_meta.append({'id_dico': i['id_dico'],
                       'abbr_name': i['abbr_name'],
                       'long_name': i['long_name'],
                       'review_year': i['review_year'],
                       'nbre_articles': i['statistics']['articles'],
                       'nbre_view': i['statistics']['article_viewers']})

json_text = json.dumps(liste_meta, indent=4)
with open(f"scrapying_results/langues/dico_meta.json","w",encoding="utf8") as f:
    f.write(json_text)