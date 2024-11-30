import sys, os

root = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
sys.path.append(root)
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), 'data/models')))
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), 'data')))

from flask import Blueprint, request
from flask_cors import cross_origin
import json

from scrapper import Scrapper

app_scraping = Blueprint("scraping", __name__)

@app_scraping.route("/product_name")
@cross_origin()
def products(product_name):
    if request.method == "GET":
        try:
            scrapper = Scrapper()
            
            url = "/".join([scrapper.base_urls["product"], product_name])
            get_page_data = scrapper.get_page_data(url)
            products = get_page_data["catalogServer"]["data"]
            
            minor_price = 0
            minor_discount_price = 0
            for product in products:
                name: str = product["name"]
                if name.lower().find(product_name) == -1:
                    continue
                
                price = product["price"]
                price_with_discount = product["priceWithDiscount"]
                
                if minor_price == 0 or minor_price > price:
                    minor_price = price
                    
                if minor_discount_price == 0 or minor_discount_price > price_with_discount:
                    minor_discount_price = price_with_discount
            
            product_data = {
                "cheaper": {
                    "credit": minor_price, 
                    "debit": minor_discount_price
                }
            }
                
            return json.dumps(product_data), 200
        except Exception as err:
            return json.dumps({"Error": f"{err}"}), 501
    else:
        return "Wrong method. Only GET allowed", 405

@app_scraping.route("/categories")
@cross_origin()
def get_categories():
    if request.method == "GET":
        try:
            scrapper = Scrapper()
            categories = scrapper.get_categories()
            return json.dumps(categories), 200
        except Exception as err:
            return json.dumps({"Error": f"{err}"}), 501
    else:
        return "Wrong method. Only GET allowed", 405
    
@app_scraping.route("/test")
@cross_origin()
def test():
    if request.method == "GET":
        try:
            scrapper = Scrapper()
            return json.dumps(scrapper.next_data(scrapper.base_urls["categories"])), 200
        except Exception as err:
            return json.dumps({"Error": f"{err}"}), 501
    else:
        return "Wrong method. Only GET allowed", 405