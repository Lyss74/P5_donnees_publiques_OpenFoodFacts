# -*- PipEnv -*-
# -*- coding: Utf-8 -*-

import records as rec

from Config import constants as conf
from Database.database_user import DataBaseUser


class Main:
    """
        This class has the responsibility of directing the user
    """

    def __init__(self):
        """ Connect to Mysql database from the class DataBaseUser() """
        self.favorites = []
        self.db = self.connect_mysql()
        self.database = DataBaseUser(self.db)

    def home_menu(self):
        """ This function allows to direct the user """
        print('\n', conf.DECO, '\n', "***  Bonjour et bienvenue au ° Substitute Factory ° ***", '\n', conf.DECO, '\n')
        print("Tapez:", '\n',
              " |-'1': Quel aliment souhaitez-vous remplacer ?" '\n',
              " |-'2': Retrouver mes aliments substitués" '\n',
              " |-'Q': Pour quitter", '\n')
        user = input()
        key_list = ["1", "2", "Q"]
        if user not in key_list:
            print('\n', conf.SPACE_ADJUST,  conf.INDEX_ERROR, '\n')
            self.home_menu()
        else:
            if user == '1':
                self.choice_category()
            elif user == '2':
                self.database.get_favorite_table()
            elif user == 'Q':
                self.quit()

    def choice_category(self):
        """ Choice Category """
        select_category = self.value_error(self.choice_category_action)
        print('\n', conf.SPACE_ADJUST, "|*** vous avez choisis ***| : ", select_category.capitalize(), '\n')
        self.choice_product(select_category)

    def choice_category_action(self):
        """ This function is linked with choice_category to control the user input """
        for i, get in enumerate(conf.CATEGORIES):
            print("*", i+1, get)
        user = input('\n' " |*** Pour choisir une catégorie, tapez le chiffre associé et appuyer sur ENTREE ***| " '\n')
        return conf.CATEGORIES[int(user) - 1]

    def choice_product(self, select_category):
        """ Choice product """
        select_product = self.value_error(self.choice_product_action, select_category)
        print('\n', conf.SPACE_ADJUST, "|*** Vous avez choisis ***| : ",
              select_product['name_product'].capitalize(), '\n')

        to_substitute = {'product_id': select_product['barcode']}
        self.favorites.append(to_substitute)                          # Temporarily saves the product to be substituted
        self.choice_substitute(select_category, select_product)

    def choice_product_action(self, select_category):
        """ This function is linked with choice_product to control the user input """
        products = self.database.get_all_products_per_category(str(select_category))
        for i, select in enumerate(products):
            print(f"* ({i+1}, {select['name_product']})")
        user = input('\n' " |*** Pour choisir un produit, tapez le chiffre associé et appuyer sur ENTREE ***| " '\n')
        if '0' in user:
            raise IndexError()
        return products[int(user) - 1]

    def choice_substitute(self, select_category, select_product):
        """ Choice the substitute """
        select_substitute = self.value_error(self.choice_substitute_action, select_category, select_product)
        self.choose_favorite_final(select_category, select_product, select_substitute)

    def choice_substitute_action(self, select_category, select_product):
        """ This function is linked with choice_substitute to control the user input """
        substitutes = self.database.choose_products_from_the_category(select_category, select_product)
        print("     | Code barre |,    | Nom Produits |,    | NutriScore |", '\n')
        for i, select in enumerate(substitutes):
            print(f"* ({i + 1}, {select['barcode']}, {select['name_product']}, {select['grade']})")
        user = input('\n' " | Vous pouvez choisir un produits" '\n'
                     " |-tapez le chiffre associé et appuyer sur ENTREE" '\n'
                     " |-'Q' pour quitter" '\n'
                     " |-'H' retour au Menu" '\n')
        if user.isdigit():
            select_substitute = substitutes[int(user) - 1]
            print('\n', conf.SPACE_ADJUST, "|*** Vous avez choisis ***|",
                  select_substitute['name_product'] + ",", "de grade : ", select_substitute['grade'], '\n', '\n',
                  "|*** Souhaitez-vous sauvegarder ce produit ? ***|", '\n')
            self.choose_favorite_final(select_category, select_product, select_substitute)
        else:
            key_list = ["C", "H", "Q"]
            if user not in key_list:
                # -tc- retour à choice_substitute, et non choice_substitute_action
                self.choice_substitute(select_category, select_product)
            elif user == 'C':
                # -tc- retour à choice_substitute, et non choice_substitute_action
                self.choice_substitute(select_category, select_product)
            elif user == 'H':
                self.home_menu()
            elif user == 'Q':
                self.quit()
        return substitutes[int(user)]

    def choose_favorite_final(self, select_category, select_product, select_substitute):
        """ Choose de products final substitue and save in the data base """
        user = input(" | tapez:" '\n' 
                     " |-'O': pour Oui" '\n'
                     " |-'N': pour Non" '\n' 
                     " |-'C': pour Choisir un nouveau produit" '\n' 
                     " |-'H': retour au Menu" '\n'
                     " |-'Q': pour quitter, valider avec ENTREE" '\n')
        if user.isdigit():
            print('\n', conf.SPACE_ADJUST,  conf.INDEX_ERROR, '\n')
            self.choose_favorite_final(select_category, select_product, select_substitute)
        else:
            key_list = ["O", "N", "C", "H", "Q"]
            if user not in key_list:
                print('\n', conf.SPACE_ADJUST, conf.VALUE_ERROR, '\n')
                self.choose_favorite_final(select_category, select_product, select_substitute)

            elif user == 'O':
                # -tc- pourquoi un ajout temporaire à une liste? Tu peux directement ajoute
                # -tc- à la base
                # -tc self.database.add_into_favorites(select_product, select_substitute)
                substitute = {'substitute_id': select_substitute['barcode']}
                self.favorites.append(substitute)            # Temporarily add to the list for insertion in the database
                print(conf.SPACE_ADJUST, " |*** Ajout du produit ***| ", '\n', conf.SPACE_ADJUST,
                      "|-Nom:", select_substitute['name_product'], '\n', conf.SPACE_ADJUST,
                      "|-Code barre:", substitute, '\n', conf.SPACE_ADJUST,
                      "|-Grade:", select_substitute['grade'], '\n', conf.SPACE_ADJUST,
                      "|-Site internet:", select_substitute['web_site'], '\n', conf.SPACE_ADJUST,
                      "|*** Successful ***|", '\n', '\n',
                      "|Contenu du casier favoris: ", '\n', '\n', self.favorites, '\n', '\n')
                # -tc- retour à choice_substitute, et non choice_substitute_action
                self.choice_substitute(select_category, select_product)

            elif user == 'N':
                print("|Contenu du casier favoris: ", '\n', '\n', self.favorites, '\n', '\n')
                self.choice_substitute_action(select_category, select_product)

            elif user == 'C':
                self.choice_substitute_action(select_category, select_product)
            elif user == 'H':
                self.home_menu()
            elif user == 'Q':
                self.quit()

    def add_favorites(self, object):
        pass

    def value_error(self, select_function, *args):
        """ This function will control the user's input """
        try:
            return select_function(*args)
        except ValueError:
            print('\n', conf.SPACE_ADJUST, conf.VALUE_ERROR, '\n')
            return self.value_error(select_function, *args)
        except IndexError:
            print('\n', conf.SPACE_ADJUST,  conf.INDEX_ERROR, '\n')
            return self.value_error(select_function, *args)

    def connect_mysql(self):
        """ Connecting in the database """
        self.db = rec.Database(f"mysql+mysqlconnector://{conf.USER}:{conf.PASSWORD}@localhost/"
                               f"{conf.DATABASE}?charset=utf8mb4")
        return self.db

    # -tc- ajouter une méthode quit()
    def quit(self):
        print("Au revoir")


def main():
    """ Initialize the main class """

    init = Main()
    init.home_menu()


if __name__ == "__main__":
    main()
