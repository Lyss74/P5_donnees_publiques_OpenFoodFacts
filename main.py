# -*- PipEnv -*-
# -*- coding: Utf-8 -*-

from time import sleep
import csv
import random

from Config.constants import *
from Database.database_user import DataBaseUser


class Main:

    def __init__(self):
        """ Connect to Mysql database from the class DataBaseUser() """
        self.favorite = []
        self.database = DataBaseUser()
        self.db = self.database.connect_mysql()

    def home_menu(self):
        print('\n', DECO, '\n', "***  Bonjour et bienvenue au °Substitute Factory° ***", '\n', DECO)
        print("tapez:", '\n',
              "*'R': pour effectuer une Recherche" '\n',
              "*'F': pour consulter les Favoris" '\n',
              '\n', DECO, '\n', SPACE_ADJUST, "*** °DATABASE CONTROL° ***", '\n', DECO, '\n',
              "*'G' pour Consulter les bases de donnèes disponnible", '\n',
              "*'C' pour Choisir une base de donnèes existante", '\n',
              "*'D' pour Dupprimer une base de donnèes existante", '\n',
              "*'N' pour crèer une Nouvelle base de donnèes", '\n',
              "*'Q' pour Quiter", '\n')
        user = input()
        key_list = ["R", "F", "G", "C", "D", "N", "Q"]
        # -tc- utilise des elifs. Je ne comprends pas pourquqoi toutes ces options
        if user not in key_list:
            self.home_menu()
        elif user == 'R':
            self.step_1()
        elif user == 'F':
                # self.database.get_favorites(user)
            self.home_menu()
        elif user == 'G':
                # self.database.get_databases()
            self.home_menu()
        elif user == 'C':
            # self.database.use_database(user)
            self.home_menu()
        elif user == 'D':
            # self.database.drop_database(user)
            self.home_menu()
        elif user == 'N':
            # self.database.create_database(user)
            self.home_menu()
            for base in enumerate(SEASON_DATABASES):
                print(base)
        elif user == 'Q':
            quit()

    def step_1(self):
        """ Choice Category """
        select_1 = self.value_error(self.step_1_action)
        print(" |*** vous avez choisis ***| :  ", select_1.capitalize())
        # -tc- Pourquoi ralentir le programme?
        sleep(0.5)
        self.step_2(select_1)

    def step_1_action(self):
        for get in enumerate(CATEGORIES):
            print("*", get)
        user = input(" |*** Pour choisir une categorie, tapez le chiffre associé et appuyer sur ENTREE ***| ")
        return CATEGORIES[int(user)]

    def step_2(self, select_1):
        # -tc- ajouter select_1 dans l'appel à self.value_error
        select_2 = self.value_error(self.step_2_action, select_1)
        print(" |*** vous avez choisis ***| :  ", select_2['name_product'].capitalize())
        # -tc- sleep() à éliminer
        sleep(0.5)
        # -tc- Pourquoi ne passer uniquement select_2[1] au step suivant?
        # -tc- C'est une bonne idée de passer select_1 et select_2 à step_3
        self.step_3(select_1, select_2)

    def step_2_action(self, select_1):
        products = self.database.get_all_products_per_category(str(select_1))
        for i, select in enumerate(products):
            print(f"* ({i+1}, {select['name_product']})")
        user = input(" |*** Pour choisir un produit, tapez le chiffre associé et appuyer sur ENTREE ***| ")
        if '0' in user:
            raise IndexError()
        return products[int(user)-1]

    def step_3(self, select_1, select_2):
        # -tc- ajouter select_1 dans l'appel à self.value_error
        print("STEP 3")
        select_3 = self.value_error(self.step_3_action, select_1, select_2)
        # -tc- Afficher tout le détail du product sélectionné
        self.final_use(select_1, select_2, select_3)


    def step_3_action(self, select_1, select_2):
        substitutes = self.database.get_healthier_product_in_category(select_1, select_2)
        for i, select in enumerate(substitutes):
            print(f"* ({i+1}, {select['name_product']})")
        user = input(" |*** Pour choisir un substitut, tapez le chiffre associé et appuyer sur ENTREE ***| ")
        if '0' in user:
            raise IndexError()
        return substitutes[int(user)-1]


    def step_3_back(self, select_1, select_2):
        """ Substitute research """
        print("STEP 3")
        compare = self.database.get_product_in_category(str(select_2))
        for select in compare:
            print(select)
        user = input("Vous pouvez choisir un produits" '\n' "tapez le chiffre associé et appuyer sur ENTREE" '\n' 
                     "'Q' pour Quitter" '\n'
                     "'H' retour au Menu")

        start = select[0]
        for choice in range(start):
            print(choice)

        if user.isdigit():
            select_3 = compare[int(user)]
            print("Vous avez choisis: ", select_3, '\n' "Souhaitez-vous sauvegarder ce produit?")
            self.final_use(select_2, select_3)
        else:
            key_list = ["C", "H", "Q"]
            if user not in key_list:
                self.step_3(select_2)
            elif user == 'C':
                self.step_3(select_2)
            elif user == 'H':
                self.home_menu()
            elif user == 'Q':
                quit()

    def final_use(self, select_1, select_2, select_3):
        print("FINAL USE")
        user = input("tapez:" '\n' 
                     "'O': pour Oui" '\n'
                     "'N': pour Non" '\n' 
                     "'C': pour Choisir un nouveau produit" '\n' 
                     "'H': retour au Menu" '\n'
                     "'Q': pour Quitter, valider avec ENTREE")
        if user.isdigit():
            print("IndexError - Veuillez faire un choix parmi la liste")
            self.final_use(select_2, select_3)
        else:
            key_list = ["O", "N", "C", "H", "Q"]
            if user not in key_list:
                self.final_use(select_2, select_3)
            if user == 'O':
                self.favorite.extend(select_3)
                print("Ajout du produits:", select_3, "successful")
                self.step_3(select_2)
                self.save_data(self.favorite, 'Save_favorites')
            elif user == 'N':
                self.step_3(select_2)
                self.home_menu()
            elif user == 'C':
                self.step_3(select_2)
                self.home_menu()
            elif user == 'H':
                self.home_menu()
            elif user == 'Q':
                quit()

    def value_error(self, select_function, *args):
        """ Control the ValueError """
        try:
            return select_function(*args)
        except ValueError:
            print("ValueError - |*** /!\ Tapez le chiffre associé à votre choix dans la liste /!\ ***|")
            return self.value_error(select_function, *args)
        except IndexError:
            print("IndexError - |*** /!\ Tapez le chiffre associé à votre choix dans la liste /!\ ***|")
            return self.value_error(select_function, *args)

    def save_data(self, outlist, filename):
        with open(filename, 'w', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=';')                                           # Import the data in file
            for e in outlist:
                writer.writerow(e)
        return filename


def main():

    init = Main()
    ini = init.home_menu()
    # step1 = init.step_3()
    # init.step_2_action()


if __name__ == "__main__":
    main()

