# -*- PipEnv -*-
# -*- coding: Utf-8 -*-


import requests as req
import csv
from pprint import pprint

from Config import constants as cons


class ApiCollectingData:
    """ Call the Api Open Food Fact """

# self.key = (barre_code, name, grade, website, format_categories.upper(), store)

    def bring_out(self):
        """ Use the configuration for the connecting interface """
        all_products = []
        api = "https://fr.openfoodfacts.org/cgi/search.pl"                 # Address OpenFooFact.org the API FR locating

        for category in cons.CATEGORIES:
            config = {"action": "process",                                         # This config for  for connecting API
                      "tagtype_0": "categories",                                            # Get the result by category
                      'tag_0': category,                                         # the tag represents the article search
                      "tag_contains_0": "contains",
                      "page_size": 50,                                                     # Number of articles per page
                      "json": 1}                                                              # The API response in JSON

            response = req.get(api, params=config)                           # Uses the configuration for the connection
            results = response.json()                                                      # Return the response in JSON
            products_section = results['products']                                               # Finally result of API

            for product in products_section:
                product['main_category'] = category
            all_products.extend(products_section)
        # pprint(all_products)
        return all_products

    def validate_the_data(self, keys, products_section):
        """ Validate the complete fields """
        for key in keys:
            if key not in products_section or not products_section[key]:
                return False
        return True

    def format_final_response(self, all_products):
        """ Formatted the response just harvest the categories selected """
        product_final = []
        keys = ['id', 'product_name_fr', 'nutrition_grade_fr', 'url', 'categories', 'stores']

        print(len(all_products))
        for product in all_products:
            if self.validate_the_data(keys, product):
                barre_code = product['id']
                format_categories = product['main_category'].upper()
                name = product['product_name_fr']
                grade = product['nutrition_grade_fr']
                website = product['url']
                categories = product['categories']
                stores = product['stores']
                key = (barre_code, name, grade, website, format_categories, stores)
                formatting = key
                product_final.append(formatting)
        pprint(product_final)
        # print(type(product_final))
        return product_final

    def convert_type_final(self, convert_type):
        convert = tuple(convert_type)
        pprint(convert)
        return convert

    def save_data(self, product_final, filename):
        with open(filename, 'w', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=';')
            for e in product_final:
                writer.writerow(e)
        return filename


def main():

    downloader = ApiCollectingData()
    connect = downloader.bring_out()
    final = tuple(downloader.format_final_response(connect))

    pprint(final)
    print(f"Nous avons récupéré {len(final)} produits")

    #convert = name.convert_type_final(final)
    # save_in_file = call.save_data(final , 'output_data_save.csv')


if __name__ == "__main__":
    main()
