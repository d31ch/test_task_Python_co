import requests

response = requests.get("https://opentdb.com/api.php?amount=10")
print(response.status_code)
print(response.text)