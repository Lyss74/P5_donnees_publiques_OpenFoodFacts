# -*- PipEnv -*-
# -*- coding: Utf-8 -*-


import records as rec

import Config.constants as cons
from Api.search_category import ApiCollectingData


class DataBaseCreator:

    def __init__(self):
        self.db = None

    def connect_mysql(self):
        """ Connecting in the database """
        self.db = rec.Database(
            f"mysql+mysqlconnector://{cons.USER}:{cons.PASSWORD}@localhost/"
            f"{cons.DATABASE}?charset=utf8mb4"
        )
        return self.db

    def show_database(self):
        """ Control the datanase """
        databases = self.db.query("SHOW DATABASES;")
        for row in databases:
            print(row['Database'])
        return databases

    def show_table(self):
        """"""
        tables = self.db.query("SHOW TABLES;")
        for table in tables:
            print(table)
        return tables

    def use_database(self):
        """"""
        pass

    def create_table_product(self):
        """ Create table """
        self.db.query("""
            CREATE TABLE Products_10k_Table (
                Barre_code BIGINT PRIMARY KEY,
                Name_product VARCHAR(255),
                Grade CHAR(1),
                Web_site VARCHAR(255))
        """)

    def create_table_categories(self, connect):
        """"""
        self.db.query("""CREATE TABLE Categories (
                                Categories VARCHAR(15));""")

    def create_table_stores(self, connect):
        """"""
        self.db.query("""CREATE TABLE Stores (
                                Stores VARCHAR(50));""")

    def create_favorites_table(self):
        pass

    def create_tables(self):
        """ Execute the creating table """
        self.create_table_product()
        self.create_table_categories()
        self.create_table_stores()

    def get_all_products(self):
        return self.db.query("""
            SELECT * FROM Products_10k_Table""",
            fetchall=True
        ).as_dict()


    def insert_product(self, id, name, grade, url, *args):
        self.db.query("""
                        INSERT INTO Products_10k_Table (
                        Barre_code,
                        Name_product,
                        Grade,
                        Web_site) 
                        VALUES 
                        (:id, :name, :grade, :url) 
                        ON DUPLICATE KEY UPDATE Barre_code = :id
            """,
                       id=id,
                       name=name,
                       grade=grade,
                       url=url)

    def insert_products(self, products):
        for product in products:
            self.insert_product(*product)

    def insert_categories(self, connect):
        response_api = Search()
        insert_categories = """
                            INSERT INTO Categories ( 
                            categories) 
                            VALUES 
                            (:format_categories);
                            """
        pass

    def insert_stores(self, connect):
        response_api = Search()
        insert_stores = """
                        INSERT INTO Stores (
                        stores) 
                        VALUES 
                        (:stores);
                        """
        pass


def main():
    """ Connecting in the database """
    databases = DataBaseCreator()
    databases.connect_mysql()
    #databases.show_database()
    databases.create_table_product()

    downloader = ApiCollectingData()
    connect = downloader.bring_out()
    final_products = tuple(downloader.format_final_response(connect))

    databases.insert_products(final_products)

    """ Control the database """
    # show_base = databases.show_database(connecting)
    # show_table = databases.show_table(connecting)
    # choose = databases.choose_database(connecting)

    """ Create table """
    # categories = databases.create_table(connecting)

    """ Insert data """
    #insert_p = databases.insert_product(connecting)
    # insert_c = databases.insert_categories(connecting)
    # insert_s = databases.insert_stores(connecting)


if __name__ == "__main__":
    main()
