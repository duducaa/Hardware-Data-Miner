from flask import Flask, request
from flask_cors import CORS
import json

from routes.scrapingRoute import app_scraping

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "http://smartshopper-scraping-gateway:5000/*"}})

app.register_blueprint(app_scraping)

if __name__ == "__main__":
    app.run(host="kabum-scraping", debug=True)