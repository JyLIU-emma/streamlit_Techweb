# -*- coding: utf-8 -*-
# Auteur: Jianying LIU

from bs4 import BeautifulSoup
from MPAscraper import MPA_Scrapper
import re
import json

URL_ROOT = 'https://fr.wikipedia.org/wiki/'

def scrapy_langues_info(dico_langue):
    langues_info = []
    for id_lang, lang in dico_langue.items():
        url = URL_ROOT + lang
        print(f"Scrapy en cours: {url}")
        driver = "None"
        scrapper = MPA_Scrapper(url,driver)
        html = scrapper.getHTMLText(url)
        html_parser = BeautifulSoup(html, 'html.parser')
        table = html_parser.find('table', {'class': 'infobox_v2'})
        rows = table.select('tr')

        for r in rows:
            if r.th:
                # print(r.th.text.strip())
                if r.th.text.strip() == "Pays":
                    pays = r.td.text.strip()
                    pays_count = len(pays.split(","))
                    # langues_info[id_lang]["pays"] = pays
                if r.th.text.strip() == "Nombre de locuteurs":
                    nbre_locuteurs = r.td.text.strip()
                    nbre_locuteurs = re.sub(r"\[.+\]", "", nbre_locuteurs)
                    chiffre_loc = re.sub(r"\(.+\)", "", nbre_locuteurs)
                    chiffre_loc = re.sub(r'millions.*$', '000000', chiffre_loc)
                    chiffre_loc = re.sub(r"[^0-9]", "", chiffre_loc)
                    chiffre_loc = re.sub(u"\u00a0", "", chiffre_loc)
                    chiffre_loc = int(chiffre_loc.strip())
                    # langues_info[id_lang]["nbre_locuteurs"] = nbre_locuteurs
        langues_info.append({"id":id_lang, "url": url, "pays":pays, "pays_count":pays_count, "nbre_locuteurs":nbre_locuteurs, "chiffre": chiffre_loc})
    return langues_info

def main():
    dico_langue = {'gb':'Ngiemboon', 'ful':'Peul', 'med':'Medumba', 'swh':'Swahili', 'yb':'Yemba',
               'so':'Sonink%C3%A9_(langue)', 'bu':'Boulou_(langue)', 'gho':'Ghomala%CA%BC', 'mbo':'Mbo_(langue_du_Cameroun)',
               'ma':'Mafa_(langue)', 'dl':'Douala_(langue)', 'bs':'Bassa_(langue_bantoue)', 'fe':'Nufi',
               'et':'Eton_(langue_bantoue)', 'mu':'Moussey_(langue)', 'ok':'Oku_(langue)', 'ŋg':'Ngemba_(langue)'}
    lang_info = scrapy_langues_info(dico_langue)
    json_text = json.dumps(lang_info, indent=4)
    with open(f"scrapying_results/langues/lang_info.json","w",encoding="utf8") as f:
        f.write(json_text)

if __name__ == "__main__":
    main()
