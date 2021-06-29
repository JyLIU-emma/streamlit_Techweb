# -*- coding: utf-8 -*-
# Auteur: Jianying LIU
# pour lancer ce script:
# python3 .\scrapying_ntealan.py

from bs4 import BeautifulSoup
from selenium import webdriver
import selenium.webdriver.support.ui as ui
import time
import json

# Paramétrer le driver
    ################################
    # chemin à remplacer si besoin #
    ################################
driver = "./chromedriver.exe"
browser = webdriver.Chrome(executable_path = driver)
wait = ui.WebDriverWait(browser,10)


lans = ["yb_fr_3031","ful_fr_2020"]
url = "https://ntealan.net/dictionaries/content/fr-af/"
login_flag = False
for lan in lans:
    print(f"Dictionnaire aspiré : {lan}")
    # scraping la 1ère page
    browser.get(url+lan)
    time.sleep(2)
    # fermer la fenêtre auto-ouvrante et se connecter
    close_button = browser.find_element_by_css_selector("#dialInfo div div div.modal-bottom button")
    close_button.click()
    time.sleep(2)
    if not login_flag:
        login = browser.find_element_by_xpath('//*[@id="page"]/div[1]/div/app-bar-top/div[3]/div/span[6]')
        login.click()
        time.sleep(2)
        browser.find_element_by_id("pseudo").send_keys("emmaliu")
        browser.find_element_by_id("password").send_keys("emmaliu")
        browser.find_element_by_css_selector("#myModalLoggin div div div.modal-footer button").click()

    # aspirer la liste des mots, avec leurs catégorie grammaticale et leurs traductions et le nombre de views
    word_list = []
    compteur = 1
    echec_count = 0
    
    # essayer d'aspirer les 2000 premiers mots
    # condition d'arrêt: 1) plus de 2000 mots; 2) echouer d'aspirer le mots sans arrêt pour 15 fois
    while compteur < 2000 and echec_count < 15:
        xpath = f'//app-bar-left/div/div[2]/div[1]/div/ul/li[{compteur}]'
        dico = {}
        try:
            result = browser.find_element_by_xpath(xpath)
            # scrolling la page, pour permêtre à cliquer l'élément
            if compteur > 13:
                browser.execute_script("arguments[0].scrollIntoView(false);",result)
            result.click()
            time.sleep(0.6)
            print(f'En train de traiter : {compteur}e mot', end="\r")
            word = result.find_element_by_tag_name("div").text
            cat = browser.find_element_by_css_selector(".cat_part").text

            # focaliser à la partie traduction
            wait.until(lambda driver: driver.find_element_by_css_selector(".translation"))
            traduction = browser.find_element_by_css_selector(".translation")
            trans = traduction.find_elements_by_css_selector(".group_equiv")
            sens_groupe = []
            for each in trans:
                num = each.find_element_by_css_selector(".number").text[:-1]
                sens = each.find_element_by_css_selector(".equivalent").text
                sens_groupe.append(sens)
            views = browser.find_element_by_css_selector("#contenu ul li:nth-child(4) span button span").text
            dico["forme"] = word
            dico["catégorie"] = cat
            dico["sens"] = sens_groupe
            dico["views"] = views
            word_list.append(dico)
            echec_count = 0
        except:
            print(f'Aspiration échouée: {compteur}e mot', end="\r")
            echec_count += 1
            time.sleep(1.5)
        finally:
            compteur += 1

    # écrire le résultat dans un fichier
    json_text = json.dumps(word_list,indent=4)
    with open(f"scrapying_results/langues/dico_{lan}.json","w",encoding="utf8") as f:
        f.write(json_text)

browser.quit()