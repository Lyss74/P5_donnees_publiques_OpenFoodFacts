#!/usr/bin/env python3
# -*- coding: Utf-8 -*-


import records


# DB_CONNECT = records.Database("""mysql+mysqlconnector://OPFF:OCP5@localhost/?charset=utf8mb4""")


class DataBaseCreator:

    def __init__(self):
        pass

    # -tc-utiliser des verbes d'action pour les méthodes, comme create_category_table, create_store_table, 
    # -tc- create_product_store_table(), create_database(), drop_database(), etc.
    def c_table(self):
        pass

    def store(self):
        pass

    def product_store(self):
        pass

    def c_link(self):
        pass

    def fav_like(self):
        pass


#  QUERY_INSERT = """()"""
#  QUERY_ALTER = """()"""
#  QUERY_MODIFY = """()"""
#  QUERY_INSERT = """(INSERT IN TO Product(product_name, generic_name, url, nutrition_grade_fr, store)
#                     VALUES(:product_name, :generic_name, :url, :nutrition_grade_fr, :store))"""
