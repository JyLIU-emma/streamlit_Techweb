# -*- coding: utf-8 -*-
# Auteur: Jianying LIU

import streamlit as st
import numpy as np 
import pandas as pd
import json
import re
import time
import plotly.express as px
import plotly.graph_objs as go


# ----------------------------Page de présentation-------------------------------------------------

def presentation():
    st.success("Bienvenue dans notre monde de stats!")
    st.markdown(
        """
        # Présentation du projet


        Ce projet est réalisé dans le cadre du devoir final du cours Rechniques web.

        Le but de ce projet est de pratiquer les techniques scrapying sur site MPA et SPA, ainsi qu'apprendre à visualiser les données aspirées.

        ### Thématiques principales
        - **Logement écologique**  
            Depuis le site de l'entreprise [NH HOTELS GROUP](https://www.nh-hotels.fr), aspirer les informations liées à l'écologie, et puis la visualiser pour montrer le besoin d'un plateforme de recherche du logement écologique.
        - **Langues africaines**  
            Depuis le site [ntealan](https://ntealan.net), aspirer les données pour montrer la nécessité de soutenir ce genre de projet.
        """
    )

# ----------------------------Page de partie logement écologique-------------------------------------------------
def color_ecologique(data, nbr_col, color="lightgreen"):
    """
    surligner les hôtels verts dans Dataframe
    """
    attr = f'background-color: {color}'
    if data.ndim == 1:
        is_eco = data["eco_mark"]
        return [attr if is_eco else '']*nbr_col

def logement_eco():

    ###############################################
    # loader les fichiers ressources, texte intro #
    ###############################################

    with open("scrapying_results/logement_eco/intro_eco_nh-hotels.json", "r", encoding="utf8") as f:
        texte_nhhotel = json.load(f)
    with open("scrapying_results/logement_eco/calcul_nombre.json", "r", encoding="utf8") as f:
        liste_type_nombre = json.load(f)

    st.markdown(
        """
        # Logement écologique


        Depuis la fin des années 1990s, le changement climatique a attiré nos attentions et nous commençons à chercher une vie plus écologique, plus "verte".

        De ce fait, la préférence des logements écologiques deviennent une mode, une tendance de plus en plus évidente. Ici, nous prenons l'exemple d'une entreprise hôtelière pour montrer le grand marché derrière cette tendance.

        ## Tableau des hôtels
        """
    )


    ################################
    # imprimer les infos de hôtels #
    ################################

    df = pd.read_csv('scrapying_results/logement_eco/hotels_info.csv',encoding='utf-8')
    continent = np.insert(df["continent"].unique(), 0, "non spécifié")
    continent_choisi = st.selectbox("Choisissez un/plusieurs continents", continent)
    pays = np.insert((df["country"] + "(" + df["continent"] + ")" ).unique(), 0, "non spécifié")
    pays_choisi = st.selectbox("Choisissez un/plusieurs pays", pays)
    pays_choisi = re.sub(r"\(.+\)", "", pays_choisi)
    df_selected = df
    if continent_choisi != "non spécifié":
        df_selected = df_selected[(df_selected.continent == continent_choisi)]
    if pays_choisi != "non spécifié":
        df_selected = df_selected[(df_selected.country == pays_choisi)]
    nbr_col = df_selected.shape[1]
    st.write("### Tables des hôtel (Les hôtels écologiques sont surlignés en vert)", df_selected.style.apply(color_ecologique, nbr_col=nbr_col, axis=1))
    
    #######################################################################################
    # graphre de barre pour  montrer le nombre de leurs hôtels dans différents continents #
    #######################################################################################

    st.write("#### La répartition des hôtels")
    hotel_count = df["continent"].value_counts()
    hotel_count = pd.DataFrame({"Continent":hotel_count.index, "Hotêls":hotel_count.values})
    bargram = px.bar(hotel_count, x="Continent", y="Hotêls", color="Hotêls", height=500)
    st.plotly_chart(bargram)

    hotel_eco_count = df.loc[df.eco_mark == True]["continent"].value_counts()
    hotel_eco_count = hotel_eco_count.to_dict()
    hotel_noeco_count = df.loc[df.eco_mark == False]["continent"].value_counts()
    hotel_noeco_count = hotel_noeco_count.to_dict()
    list_continent = ["Europe", "Amérique", "Médio Oriente", "Afrique"]
    trace_1 = go.Bar(
        x = list_continent,
        y = [hotel_eco_count.get(cont, 0) for cont in list_continent],
        name = "écologique"
    )

    trace_2 = go.Bar(
        x = list_continent,
        y = [hotel_noeco_count.get(cont, 0) for cont in list_continent],
        name = "non_écologique"
    )

    trace = [trace_1, trace_2]
    layout = go.Layout(title="Répartition des hôtels écologiques dans différents continents", barmode="stack")
    fig = go.Figure(data=trace, layout=layout)
    st.plotly_chart(fig)
    st.write("**Nous voyons bien un essor de l'hôtellerie écologique en Europe.**")

    ####################################################################################
    # camenbert pour montrer les proportions des hôtels écologiques et non écologiques #
    ####################################################################################

    st.write("#### État global des hôtels écologiques")
    hotel_eco = df["eco_mark"].value_counts()
    hotel_eco = pd.DataFrame({"Oui/Non écologique":hotel_eco.index, "Hotêls":hotel_eco.values})
    hotel_eco.loc[0,'Oui/Non écologique'] = "Hôtels écologique"
    hotel_eco.loc[1,'Oui/Non écologique'] = "Hôtels non écologique"
    piegram = px.pie(hotel_eco, names="Oui/Non écologique", values="Hotêls")
    st.plotly_chart(piegram)
    st.write("**On voit bien que les logements écologiques l'emportent sur les non écologiques.**")

    #############################################################################
    # graphre de barre pour  montrer de nombreux logements de ce type en France #
    #############################################################################

    st.markdown(
        """
        #### Nombre de différents type de logements écologiques

        À partir du site de [laclefverte](https://www.laclefverte.org/), une organisation qualifiant les logements écologiques, on trouve des listes de différents types de logements écologiques. 
        Le nombre total de chaque type est utilisé ici pour démonstrer l'essor de ce domaine.
        """
    )
    st.write("#### Différents type de logements écologiques")
    nombre_df = pd.DataFrame({"Type":[i["cat"] for i in liste_type_nombre], "Nombre":[i["nombre"] for i in liste_type_nombre]})
    nombre_total = nombre_df.Nombre.sum()
    st.write(f"**Nombre total des hôtels écologiques en France :{nombre_total}**")
    nombre_bargram = px.bar(nombre_df, x="Type", y="Nombre", color="Nombre", height=500)
    st.plotly_chart(nombre_bargram)
    
    ##############################################
    # la démonstration d'un texte aspiré du site #
    ##############################################

    st.markdown(
        """
        ## Efforts du groupe NH HOTEL GROUP sur ce domaine

        Un rapport sur leur site présente bien leur contribution sociale par rapport à ce sujet.
        """
    )
    st.header(texte_nhhotel['Titre'])
    st.subheader(texte_nhhotel['Sous-titre'])
    st.markdown(f"***{texte_nhhotel['Date']}***")
    if st.button("Texte complet"):
        st.markdown(texte_nhhotel['Texte'])
    else:
        st.markdown(texte_nhhotel['Texte'][:500] + "...")
    

    #####################
    # Partie conclusion #
    #####################

    st.markdown(
        """
        # Conclusion

        À partir de ce qui est montré avant, nous constatons que les logements écologiques ont devient une tendence importante dans l'industrie hôtelière.

        Dans une seule entreprise, il a 201 hôtels écologiques, et seulement en France, 714 logements de tous les genres sont qualifiés comme écologiques.

        **Ce nombre est déjà énorme et ayant besoin d'un système de recherche.**

        En plus, jusqu'ici, nous ne trouvons pas une plate-forme pour englober toutes ces informations, c'est-à-dire un site qui comporte toutes les logements écologiques au niveau mondial et n'importe quelle entreprise qu'il appartienne.

        **En un mot, l'habitation écologique a un bel avenir en perspective, et les systèmes assistant ce domaine sont encore sous-développés, Donc beaucoup d'opportunités potentiels nous attendent.**
        """
    )




# ----------------------------Page de partie langues africaines-------------------------------------------------

def langues_africaines():

    ###############################################
    # loader les fichiers ressources, texte intro #
    ###############################################

    with open("scrapying_results/langues/dico_ful_fr_2020.json", "r", encoding="utf8") as ful:
        dico_fulfulde = json.load(ful)
    with open("scrapying_results/langues/dico_yb_fr.json", "r", encoding="utf8") as yb:
        dico_yemba = json.load(yb)

    st.markdown("# Dictionnaires des langues africaines")
    st.markdown(
        """
        Il y a environs 6000-7000 langues dans le  monde entier, l'Afrique est l'un des continent qui profite la plus de diversité des langues. Néanmoins, il y a aussi beaucoup de langues dans cette région qui est en train de mourir.
        
        [Ntealan](https://ntealan.net) est un dictionnaire multilingue en ligne qui nous permet de chercher les traductions des expressions de 24 langues africaines en français, anglais, italien et allemand.

        Mais les ressources ne sont pas encore assez complets. Ce projet a besoins de plus de participation et bénévoles.

        On a extrait tout d'abord les métadonnées des dictionnaires sur ce site, ainsi que certaines informations sur les langues concernées pour montrer la nécessité de les développer davantage.

        Ensuite, une partie des dictionnaire bilingue yemba-français et fulfulde-français sont extraite pour vous montrer comment cet outil peut nous aider.
        """
    )


    ###################################
    # Démonstration globale de l'état #
    ###################################

    with open("scrapying_results/langues/dico_meta.json", "r", encoding="utf8") as f_meta:
        dico_meta = json.load(f_meta)
    with open("scrapying_results/langues/lang_info.json", "r", encoding="utf8") as f_lang:
        dico_lang = json.load(f_lang)
    
    st.markdown("## État global sur les dictionnaires de Ntealan")

    trace_1 = go.Bar(
        x = [i["abbr_name"] for i in dico_meta],
        y = [i["nbre_articles"] for i in dico_meta],
        name = "nombre d'articles"
    )
    trace_2 = go.Bar(
        x = [i["abbr_name"] for i in dico_meta],
        y = [i["nbre_view"] for i in dico_meta],
        name = "nombre de vues"
    )
    trace = [trace_1, trace_2]
    layout = go.Layout(title="Nombres d'articles et de vues des dictionnaires")
    figure = go.Figure(data=trace, layout=layout)
    st.plotly_chart(figure)
    
    st.markdown(
        """
        Nous voyons bien dans la figure que seulement 4 langues ont plus de 3000 articles. Pour la plupart des langues, le nombre d'articles ne dépasse même pas 1000. En plus, pour l'instant, sauf un dictionnaire bilingue xx-anglais, tous les restes sont des dictionnaire français. 
        **Donc, il reste encore beaucoup de travail pour compléter les données.**

        En plus, si on regarde le nombre de vue, sauf la langue yemba, tous les autres dictionnaires sont peu consultés, certains ont même moins de consultation que le nombre d'articles.
        Même si pour la langue yemba, on peut voir plus tard que seulement les premiers articles ont plus de consultations, le reste de ce dictionnaire demeure toujours peu consulté.

        Nous imaginons que c'est plutôt parce que les ressources ne sont pas encore complètes et le site reste inconnu pour les chercheurs de ce domaine. Avec plus de travail et de diffusion, cela améliorera.

        """
    )

    st.markdown(
        """
        ## Info sur les langues concernées

        Après une petite recherche sur les 24 langues concernées, nous trouvons deux états principaux pour ces langues:

        - Certaines langues sont la langue maternelle/la langue seconde pour une population assez grande, **donc il a une valeur pour développer un tel site, afin de faciliter la comminication entre cette population et le monde occidental.**

        - Certaines langues ont peu d'information sur Internet (comme pour Yangben, ŋk̀ùnàbémbé, ndemli, Ejagham), on n'a même rien trouvé. Et ce sont souvent des langues en danger. **De ce fait, il nous faut travailler dessus pour sauver ces patrimoines linguistiques.**

        Le tableau et la figure suivants démonstrent plus clairs ces infos.
        """
    )

    langues_df = pd.DataFrame({"Langue_id":[i["id"] for i in dico_lang], "Nombre_pays_utilise":[i["pays_count"] for i in dico_lang],
                               "pays":[i["pays"] for i in dico_lang], "Nombre_locuteurs":[i["nbre_locuteurs"] for i in dico_lang],
                               "Nombre_locuteurs_chiffre":[i["chiffre"] for i in dico_lang], "page_wiki":[i["url"] for i in dico_lang]})
    st.table(langues_df)

    st.write("#### Nombres de locuteurs")
    nombre_bargram = px.bar(langues_df, x="Langue_id", y="Nombre_locuteurs_chiffre", color="Nombre_locuteurs_chiffre", height=500)
    st.plotly_chart(nombre_bargram)


    ##############################
    # Extraits des dictionnaires #
    ##############################

    st.markdown(
        """
        ## Extraits des dictionnaires

        """
    )

    #################################
    # démonstration des traductions #
    #################################

    st.markdown(
        """
        ## Utilisation de ce dictionnaire

        Vous pouvez consulter la traduction du français vers la langue choisie, à partir de données scrapying dans le site Ntealan
        """
    )

    # choisissez la langue, qui sert au traitement suivant
    langue_choisi = st.selectbox("Choisissez une langue", ["yemba","fulfulde"])
    if langue_choisi == "yemba":
        dico = dico_yemba
    else:
        dico = dico_fulfulde

    # création d'une liste d'indice de traductions
    index_traduction = []
    for entree in dico:
        for trans in entree["sens"]:
            index_traduction.append((trans, entree["forme"], entree["catégorie"]))
    

    word_query = st.text_input("Entrez un mot français", "il")
    trouvee = []
    for entree in index_traduction:
        if word_query.lower() in entree[0].lower().split():
            trouvee.append(entree)

    # transformer la sous-liste trouvee à un dataframe, pour la démonstration
    index_df = pd.DataFrame(trouvee, columns=['français',langue_choisi, 'catégorie gramaticale'])
    
    # imprimer résultat
    if not trouvee:
        st.write("Rien est trouvée!")
    else:
        st.write(f"La traduction du mot ***{word_query}*** est :", index_df)
    
    
    ######################################################
    # graphe animée démonstre le nombre de consultations #
    ######################################################

    st.header(f"Nombre de consultation des mots(les {len(dico)} premiers) :")

    liste_views = [int(mot["views"]) for mot in dico]

    # afficher le progrès
    progress_bar = st.sidebar.progress(0)
    status_text = st.sidebar.empty()

    # état inital
    total_views = np.array([[liste_views[0]]])
    run = st.empty()
    chart = st.line_chart(total_views)
    views = st.empty()

    if run.button("Run"):
        # ajout un par un du nombre de views de chaque mot dans le graphe
        for i in range(1,len(dico)):
            new_row = np.array([[liste_views[i]]])
            percent = round(i/len(dico), 2)
            status_text.text(f"{percent}% Complete")
            chart.add_rows(new_row)
            progress_bar.progress(percent)
            total_views = total_views[-1, :] + np.array([[liste_views[i]]]).cumsum(axis=0)
            views.text(f"Nombre de consultations total : {total_views[0]}")
        progress_bar.empty()

    st.markdown("***On constate clairement que le nombre de consultations baisse très vite dans la première dizaine d'entrées, et puis prèsque 0 pour la plupard d'entrées. Donc, il reste encore beaucoup de travail à faire.***")


    ##############
    # Conclusion #
    ##############

    st.markdown(
        """
        # Conclusion

        En un mot, au contraire du nombre assez élevé de locuteurs de ces langues africaines, l'état actuel du site Ntealan et le manque des ressouces linguistiques au près de ces langues se révèle bien la nécessité d'investir à ce domaine.

        Il a non seulement des intérêts économiques, mais aussi des intérêts culturels et scientifiques.

        """
    )

def main():
    st.sidebar.header("Techniques web -- Projet personel")
    st.sidebar.info("Auteur: Jianying")
    choix = st.sidebar.radio(label="Table de matières : ", options=["Présentation du projet", "Logement écologique", "Langues africaines"])

    if choix == "Présentation du projet":
        presentation()
    elif choix == "Logement écologique":
        logement_eco()
    elif choix == "Langues africaines":
        langues_africaines()


if __name__ == "__main__":
    main()