from flask import Flask, request
from flask_cors import CORS
import json

from scrapper import scraping

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "http://smartshopper-scraping-gateway:5000/*"}})

@app.route("/")
def start():
    if request.method == "GET":
        try:
            return json.dumps(scraping("rtx 4070")), 200
        except Exception as err:
            return json.dumps({"Error": f"{err}"}), 501
    else:
        return "Wrong method. Only GET allowed", 405

if __name__ == "__main__":
    app.run(host="kabum-scraping", debug=True)