import requests

response = requests.get("http://localhost:5031/")

print(response.json())