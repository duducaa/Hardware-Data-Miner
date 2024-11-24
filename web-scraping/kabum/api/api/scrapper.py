from bs4 import BeautifulSoup
import requests
import json


headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

def scraping(product_name):
    url = f"https://www.kabum.com.br/busca/{product_name}"
    
    response = requests.get(url, headers=headers)
    
    soup = BeautifulSoup(response.content, "html.parser")
    
    page_json = json.loads(soup.find(id="__NEXT_DATA__").text)
    
    products = page_json["props"]["pageProps"]["data"]["catalogServer"]["data"]
    
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
    
    return {
        "cheaper": {
            "credit": minor_price, 
            "debit": minor_discount_price
        }
    }