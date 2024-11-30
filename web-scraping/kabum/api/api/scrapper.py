from bs4 import BeautifulSoup
import requests
import json

class Scrapper():
    def __init__(self):
        self.num_categories = 0
        self.categories = {}
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        self.base_urls = {
            "product": "https://www.kabum.com.br/busca/",
            "categories": "https://www.kabum.com.br/hardware"
        }
        
    def get_page_data(self, url):
        with requests.Session() as session:
            session.headers.update(self.headers)
            response = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(response.content, "html.parser")
            next_data = json.loads(soup.find(id="__NEXT_DATA__").text)
            return json.loads(next_data["props"]['pageProps']["data"])
    
    def find_data(self, url: str):
        try:
            data = self.get_page_data(url)
            categories: list = data["categories"]["list"]
            return list(map(lambda x: x["slug"], categories))
        except Exception:
            return []
        
    def get_categories(self):
        self.categories_recursive(self.base_urls["categories"])
        return self.categories
    
    def categories_recursive(self, url: str, previous_cats: list = []):            
        categories = self.find_data(url)
        
        parent_id = self.num_categories
        for cat in categories:
            if cat in previous_cats:
                break
            self.num_categories = self.num_categories + 1
            with open("categories.txt", 'a') as f:
                f.write(f"{self.num_categories} - {cat} - {parent_id}\n")
            self.categories_recursive("/".join([url, cat]), categories)
