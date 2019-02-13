# -*- PipEnv -*-
# -*- coding: Utf-8 -*-

import records as rec

from Config.constants import *


class DataBaseUser:

    def __init__(self):
        """  """
        self.db = None

    def connect_mysql(self):
        """ Connecting in the database """
        self.db = rec.Database(f"mysql+mysqlconnector://{USER}:{PASSWORD}@localhost/"
                               f"{DATABASE}?charset=utf8mb4")
        return self.db

    def get_databases(self):
        """ Control the database """
        databases = self.db.query("SHOW DATABASES;")
        for row in databases:
            print(row['Database'])

    def create_database(self, choose):
        self.db("""
                    CREATE DATABASE :choose;
                """, choose=choose)
        return True

    def use_database(self, use):
        using = self.db.query("USE :use;", use=use)

    def drop_database(self, drop):
        """ Drop the database """
        self.db.query("DROP DATABASES :drop;", drop=drop)
        return True

    def get_tables(self):
        """ Control the tables """
        table = self.db.query("SHOW TABLES;")

        for tables in enumerate(table):
            print(tables)
        return True

    def get_all_products(self):
        """ Control in the tables """
        return self.db.query("""
                                SELECT * FROM demo.Products;
                             """,  fetchall=True).as_dict()

    def get_all_products_per_category(self, category):
        """ Control in the tables """
        cat = self.db.query("""
                                SELECT * FROM Products AS product
                                JOIN products_categories_summary_key AS pc ON pc.product_id = product.barre_code  
                                JOIN Categories_summary AS c ON pc.c_category_id = c.id							
                                WHERE c.c_category = :user;	
                            """, user=category, fetchall=True).as_dict()

        return cat

    def get_product_in_category(self, select_2):
        prod = self.db.query("""
                                SELECT product.name_product, product.grade, product.barre_code FROM Products AS product
                                WHERE name_product LIKE :user;
                             """, user=select_2, fetchall=True).as_dict()

        return [(i, p['name_product'], p['grade'], p['barre_code']) for i, p in enumerate(prod)]

    def get_healthier_product_in_category(self, category, product):
        prod = self.db.query("""
                             SELECT * FROM Products AS product
                             JOIN Products_categories_summary_key AS pcsk ON pcsk.product_id = product.barre_code
                             JOIN Categories_summary AS cs ON cs.id = pcsk.c_category_id
                             WHERE product.grade < :grade AND cs.c_category = :category
                             """, 
                            grade=product['grade'], category=category, fetchall=True).as_dict()
        return prod


#        prod = self.db.query("""
#                                SELECT product.name_product, product.grade, product.barre_code FROM Products AS product
#                                WHERE name_product LIKE :user;
#                             """, user=select_2, fetchall=True).as_dict()
#
#        return [(i, p['name_product'], p['grade'], p['barre_code']) for i, p in enumerate(prod)]

def main():
    # Init the class, and Connecting in the database
    databases = DataBaseUser()                                                                 # Load the database class
    connecting = databases.connect_mysql()                                                    # Load the MySQL connexion

    # Control the database
    # c_data = databases.create_database(SEASON_DATABASES['Winter'])
    # use = databases.use_database(SEASON_DATABASES['Winter'])
    # drop = databases.drop_database(SEASON_DATABASES['Winter'])

    # get_bases = databases.get_databases()                                                      # Get the database list
    # get_tables = databases.get_tables()                                                           # Get the table list
    # get_products = databases.get_all_products_per_category()                                     # Get the insert list
    # get_products = databases.get_product_in_category()                                         # Get the insert list


if __name__ == "__main__":
    main()

