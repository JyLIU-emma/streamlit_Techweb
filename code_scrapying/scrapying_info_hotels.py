# -*- coding: utf-8 -*-
# Auteur: Jianying LIU
# pour lancer ce script
# python3 scrapying_info_hotels.py

from bs4 import BeautifulSoup
from MPAscraper import MPA_Scrapper
import re
import csv

def parsing_country_page(country_url, id_hotel, list_hotels, cont_name, country_name):
    """
    trouver les liens vers chaque hôtel, ensuite en intégrant la fonction parsing_hotel_page, aspirer les infos

    Args: 
        country_url(str): l'url de la page à aspirer dans cette fonction
        id_hotel(int): compteur de l'aspiration de page hôtel
        cont_name(str): le nom du continent de ce pays
        country_name(str): nom du pays
    Returns: 
        id_hotel(int) nombre total des hôtels aspirés
        list_hotels(list) une liste regroupe les dico_info de chaque hôtel
    """
    html = scrapper.getHTMLText(country_url)
    html_parser = BeautifulSoup(html, 'html.parser')
    block_liste = html_parser.html.body.find('div', {'class': 'group-block'})
    cities = [city for city in block_liste.select(".grid-item")]
    for city in cities:
        city_name = city.h2.text[10:]
        hotels = city.select("li")
        for hotel in hotels:
            id_hotel += 1
            hotel_name = hotel.a.text.strip()
            hotel_url = hotel.a['href']
            hotel_info_dico = parsing_hotel_page(hotel_name, url_nhhome+hotel_url)
            hotel_info_dico['city'] = city_name
            hotel_info_dico['id'] = id_hotel
            hotel_info_dico['continent'] = cont_name
            hotel_info_dico['country'] = country_name
            list_hotels.append(hotel_info_dico)
    return id_hotel, list_hotels

def parsing_hotel_page(hotel_name,url_hotel):
    """
    aspirer les infos de l'hôtêls à partir du url donné

    Args:
        hotel_name(str): nom de l'hôtel
        url_hotel(str): l'url vers la page de cette hôtel
    Returns:
        dico_info_hotel(dict): un dico contien les infos de nom, adresse, services, marque écologique de l'hôtel
    """
    html = scrapper.getHTMLText(url_hotel)
    html_parser = BeautifulSoup(html, 'html.parser')
    address = html_parser.find('a', {'data-target': '#modal-hotel-map-detail'}).text
    services = [service.string for service in html_parser.select("div #services li p")]
    eco_mark = False
    if "Eco-friendly" in services:
        eco_mark = True
    dico_info_hotel = {"name":hotel_name, "address":address,"services":services,"eco_mark":eco_mark}
    return dico_info_hotel

if __name__ == "__main__":
    # scraping de la page
    
    ################################
    # chemin à remplacer si besoin #
    ################################
    driver = "./chromedriver.exe"

    url_nhhome = "https://www.nh-hotels.fr"
    url_requete = url_nhhome + "/hotels"
    id_hotel = 0
    scrapper = MPA_Scrapper(url_nhhome,driver)
    scrapper.setCookies()
    html = scrapper.getHTMLText(url_requete)

    # trouver les urls de pays
    html_general = BeautifulSoup(html, 'html.parser')
    block_liste = html_general.html.body.find('div', {'class': 'group-block'})
    list_hotels = []
    continents = [continent for continent in block_liste.select(".grid-item")]
    for cont in continents:
        cont_name = cont.h2.text[10:]
        countries = cont.select("li")
        for country in countries:
            country_name = country.strong.string
            country_url = country.a['href']
            id_hotel, list_hotels = parsing_country_page(country_url, id_hotel, list_hotels, cont_name, country_name)

    # écrire du fichier json pour stocker info
    with open("scrapying_results/logement_eco/hotels_info.csv", "w", encoding="utf8") as f:
        fieldnames = ["id","hotel_name","continent","country","city","address","services","eco_mark"]
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=",", quoting=csv.QUOTE_ALL)
        writer.writeheader()
        for i in list_hotels:
            row = {"id":i["id"], 
                "hotel_name":i["name"],
                "continent":i["continent"],
                "country":i["country"],
                "city":i["city"],
                "address":i["address"],
                "services":"|".join(i["services"]),
                "eco_mark":i["eco_mark"]
                }
            writer.writerow(row)