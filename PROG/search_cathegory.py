# -*- PipEnv -*-
# -*- coding: Utf-8 -*-

# -tc- Attention aux noms de fichiers: un seul mot, en minuscule et category, pas cathegory

import requests as req

from pprint import pprint

# CONSTANTS #

# -tc- S'il y a plusieurs catégories, il serait plus logique de nommer cette liste au pluriel, soit CATEGORIES
CATEGORY = ["Viandes",
            "Boissons",
            "Diététique",
            "Produits_laitiers",
            "Produits_de_la_mer",
            "Biscuiterie"
            ]


class ApiCall:
    """ CALL THE API OPEN FOOD FACT """

    def __init__(self):
        """  """
        pass

    # -tc- Pourquoi écrits-tu tes docstrings en majuscules?
    # -tc- Utiliser des verbes d'action pour nommer les méthodes
    def connecting(self):  # -> Pourquoi PyCharm me suggère d'utiliser la méthode static? # -tc- parce que tu n'as pas d'attributs. Pas écouter pycharm
        """ USE THE CONFIGURATION FOR THE CONNECTING """
        
        # -tc- Ne JAMAIS utiliser global, sauf en des cas très exceptionnels que tu ne rencontreras probablement pas durant 
        # -tc- durant ta carrière
        global api, config

        for category in CATEGORY:
            # -tc- les commentaires ne sont pas des docstrings. Ils s'écrivent avec des dièses, pas des guillemets
            """ Ma boucle qui collect mes produits de chaque categories ne fonctionne plus, 
            pourtant avant la création de ma classe celle-ci marchait trés bien^^ """

            api = "https://fr.openfoodfacts.org/cgi/search.pl"             # Address OpenFooFact.org the API FR locating
            config = {"action": "process",                                         # This config for  for connecting API
                      "tagtype_0": "categories",                                            # Get the result by category
                      'tag_0': category,                                         # the tag represents the article search
                      "tag_contains_0": "contains",
                      "page_size": 50,                                                     # Number of articles per page
                      "json": 1}                                                              # The API response in JSON

        # -tc- Cette méthode connecting() ne fait pas ce que tu veux
        return api, config

    def api_response(self):  # -> Pourquoi PyCharm me suggère d'utiliser la méthode static?
        """ USE THE RESPONSE THE API """

        # -tc- éliminer global
        global products

        # -tc- config n'existe pas et global n'est pas la bonne solution pour partager des données entres plusieurs
        # -tc- méthodes. 
        # -tc- requests n'est pas un nom de variable très bien choisi ici, response serait plus adapté
        requests = req.get(api, params=config)                               # Uses the configuration for the connection
        response = requests.json()                                                         # Return the response in JSON
        products = response['products']                                                          # Finally result of API

        return products                                                                    # Return the finally response

    def final_product(self):  # -> Pourquoi PyCharm me suggère d'utiliser la méthode static?
        """ FORMATTED THE RESPONSE JUST HARVEST THE CATEGORY'S SELECTED """

        pos = 0
        print(len(products))

        product_final = []

        for product in products:
            # -tc- ceci est un commentaire, pas un docstring
            """ J'ai supprimé le dictionnaire pour mes champs, et a opter 
            pour le nomage de mes champ afin de pouvoir les manipuler """

            try:
                # -tc- les catégories ne t'intéresse à priori pas, tu les as sélectionnées en amont
                categories = product['categories']
                name = product['product_name_fr']
                grade = product['nutrition_grade_fr']
                website = product['url']
                store = product['stores']
                keys = (categories, name, grade, website, store)
                # A tuple that organizes and respect the order of the fields

                # -tc- préférer l'utilisation de la fonction enumerate() plutot que d'incrémenter pos à chaque fois. S'il y a une erreur
                # -tc- pos n'est pas incrémenté
                pos += 1

                refactor = sorted(keys)
                product_final.append(refactor)
                pprint(product_final)

            except KeyError:
                print("KeyError", "POSITION ACTUEL :", pos)
                continue     # Tester si le 'continue' termine le travail
            # -tc- On n'a à priori aucune raison d'avoir une IndexError ici
            except IndexError:
                print("IndexError", "POSITION ACTUEL :", pos)

        print(pos)

        return product_final


def main():
    """ A cette heure ma classe marche bien, sauf la boucle
    d'entrè, puis mes champs vide qui arrete le receuil des donnèes """

    """Mes variables 'global' me servent juste à fonctionnner ma classe, elle seront remplacer et organiser
     par le constructeur """

    call = ApiCall()
    connect = call.connecting()
    formated = call.api_response()
    final = call.final_product()


if __name__ == "__main__":
    main()
