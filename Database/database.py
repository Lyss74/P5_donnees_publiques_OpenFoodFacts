# -*- PipEnv -*-
# -*- coding: Utf-8 -*-

# C:\Users\Admin\GoogleDrive\DATA_OPEN_PROG\OPENCLASSROOMS\MyProjectOC\PROJET_05\MySQL\bin

import records as rec

from Config import constants as conf
from Database.database_user import DataBaseUser
from Api.search_category import ApiCollectingData


class DataBaseCreator:
    """
        This class has the responsibility of structuring the database, and inserting the data collection of the API
    """

    def __init__(self, db):
        """ Connect to Mysql database from the class DataBaseUser() """
        self.db = db
        self.database = DataBaseUser(self.db)

    def drop_tables(self):
        """ Delete existing tables, to collect new data  """

        # -tc- attention, ta base ne se nomme pas nécessairement purbeurre
        # -tc- attention, utiliser if exists pour le cas où c'est la première
        # -tc- création des tables
        self.db.query(""" 
                        DROP TABLE if exists
                        Categories, 
                        Categories_summary, 
                        Products,
                        Products_categories_key,
                        Products_categories_summary_key,
                        Products_stores,
                        Stores;
                      """)

    def create_table_product(self):
        """ Create table Products """
        self.db.query("""
                        CREATE TABLE IF NOT EXISTS Products (
                        barcode BIGINT UNIQUE PRIMARY KEY,
                        name_product VARCHAR(150),
                        grade CHAR(1),
                        web_site VARCHAR(255));
                       """)

    def create_table_category(self):
        """ Create table category """
        self.db.query("""
                        CREATE TABLE IF NOT EXISTS Categories (
                        id BIGINT PRIMARY KEY AUTO_INCREMENT,
                        category VARCHAR(125) UNIQUE);
                      """)

        self.db.query("""
                        CREATE TABLE IF NOT EXISTS Categories_summary (
                        id BIGINT PRIMARY KEY AUTO_INCREMENT,
                        c_category VARCHAR(125) UNIQUE); 
                      """)

    def create_table_store(self):
        """ Create table stores """
        self.db.query("""
                        CREATE TABLE IF NOT EXISTS Stores (
                        id MEDIUMINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
                        store VARCHAR(150) UNIQUE);
                      """)

    def create_table_subkey(self):
        """ Creating to the associate index table """
        self.db.query("""
                        CREATE TABLE IF NOT EXISTS Products_categories_key ( 
                        id MEDIUMINT PRIMARY KEY AUTO_INCREMENT,
                        product_id BIGINT REFERENCES Products(barcode),
                        category_id MEDIUMINT REFERENCES Category(id));
                       """)

        self.db.query("""
                        CREATE TABLE IF NOT EXISTS Products_categories_summary_key (
                        id MEDIUMINT PRIMARY KEY AUTO_INCREMENT,
                        product_id BIGINT REFERENCES Products(barcode),
                        c_category_id MEDIUMINT REFERENCES Categories_summary(id));
                      """)

        self.db.query("""                                                           
                        CREATE TABLE IF NOT EXISTS Products_stores (
                        id MEDIUMINT PRIMARY KEY AUTO_INCREMENT,
                        product_id BIGINT REFERENCES Products(barcode),
                        store_id MEDIUMINT REFERENCES Stores(id));               
                      """)

    def create_favorites_table(self):
        """ Create the favorites table """
        self.db.query("""
                        CREATE TABLE IF NOT EXISTS Favorites (
                        product_id BIGINT REFERENCES Products(barcode), 
                        substitute_id BIGINT REFERENCES Products(barcode),
                        PRIMARY KEY(product_id, substitute_id));                       
                      """)

    def insert_product(self, id, name, grade, url, *args):
        """ Insert the product data in the table"""
        self.db.query("""                        
                        INSERT INTO Products (barcode, name_product, grade, web_site) 
                        VALUES 
                        (:id, :name, :grade, :url) 
                        ON DUPLICATE KEY UPDATE barcode=:id;
                      """, id=id, name=name, grade=grade, url=url)

    def insert_category(self, id, name, grade, url, categories, sub_category, stores, *args):
        """ Insert the category list data in the table"""
        for category in categories:
            self.db.query("""
                            INSERT INTO Categories(category) 
                            VALUES 
                            (:category)
                            ON DUPLICATE KEY UPDATE category=:category;                          
                          """, category=category)

            self.db.query("""
                            INSERT INTO Categories_summary(c_category) 
                            VALUES 
                            (:c_category)
                            ON DUPLICATE KEY UPDATE c_category=:c_category;                          
                          """, c_category=sub_category)

            self.db.query("""
                            INSERT INTO Products_categories_key (product_id, category_id)
                            VALUES (:barcode,
                            (SELECT id FROM Categories WHERE category=:category_id));
                          """, barcode=id, category_id=category)

            self.db.query("""
                            INSERT INTO Products_categories_summary_key (product_id, c_category_id)
                            VALUES (:barcode,
                            (SELECT id FROM Categories_summary WHERE c_category=:category_id));
                          """, barcode=id, category_id=sub_category)

    def insert_stores(self, id, name, grade, url, categories, sub_category, stores, *args):
        """ Insert the store list data in the table"""
        for store in stores:
            self.db.query("""
                            INSERT INTO Stores(store)
                            VALUES (:store)
                            ON DUPLICATE KEY UPDATE store=:store;
                          """, store=store)

            self.db.query("""
                            INSERT INTO Products_stores (product_id, store_id)
                            VALUES (:barcode,
                            (SELECT id FROM Stores WHERE store=:store_id));
                          """, barcode=id, store_id=store)

    def create_tables(self):
        """ Execute the creating table """
        self.drop_tables()
        print('\n', conf.DECO, '\n', conf.SPACE_ADJUST, "**** Deleting tables success ****", '\n', conf.DECO, '\n')
        self.create_table_product()
        self.create_table_category()
        self.create_table_store()
        self.create_table_subkey()
        # self.create_favorites_table()
        print('\n', conf.DECO, '\n', conf.SPACE_ADJUST, "**** Creating table success ****", '\n', conf.DECO, '\n')
        return True

    def insert_rows(self, products):
        """ Completion the data row per row """
        for product in products:
            self.insert_product(*product)
            self.insert_category(*product)
            self.insert_stores(*product)
        print('\n', conf.DECO, '\n', conf.SPACE_ADJUST, "**** Insert data success *****", '\n', conf.DECO, '\n')
        return True


def main():
    """ Initialize the connection """
    db = rec.Database(f"mysql+mysqlconnector://{conf.USER}:{conf.PASSWORD}@localhost/"
                      f"{conf.DATABASE}?charset=utf8mb4")
    creating = DataBaseCreator(db)

    # Connecting in the API
    downloader = ApiCollectingData()                                                                # Load the API class
    connect = downloader.connect_and_harvest()                                                  # Load the API connexion
    final_products = downloader.format_final_response(connect)                                  # Harvest OPFF's request

    # Create table
    creating.create_tables()                                                             # Creating the necessary tables

    # Insert data
    creating.insert_rows(final_products)


if __name__ == "__main__":
    main()
