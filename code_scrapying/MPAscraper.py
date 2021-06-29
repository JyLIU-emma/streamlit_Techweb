# -*- coding: utf-8 -*-
# Auteur: Jianying LIU

import requests
from selenium import webdriver

class MPA_Scrapper():
    """
    Classe sert à englober les étapes pour aspirer une page d'un site
    Pour l'initaliser:
    - l'url de la page d'accueil du site
    - path absolu vers le chromedriver
    """

    def __init__(self, index_url, driver_path):
        self.url = index_url
        self.driver = driver_path
        self.headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"}

    def setCookies(self):
        """
        Cette méthode va obtenir les cookies selon le site donné quand on initialise la classe
        """
        browser = webdriver.Chrome(executable_path = self.driver)
        browser.get(self.url)
        Cookie = browser.get_cookies()
        str_cookie =""
        for c in Cookie:
            str_cookie += f'{c["name"]}={c["value"]};'
        browser.quit()
        self.headers["Cookie"] = str_cookie

    def getHTMLText(self, url, img=False):
        """
        Cette méthode sert à aspirer une page html de MPA
        Args:
            url : l'url de la page à aspirer
        Returns: 
            renvoie un string du code html de la page si succès, si non imprime l'échec dans terminal
        """
        try:
            response = requests.get(url, headers = self.headers, timeout=30)
            response.raise_for_status()
            if img:
                return response.content
            return response.text
        except:
            print("echec de téléchargement : %s"%(url))
            print("HTTP-Code :", response.status_code)
            return ""