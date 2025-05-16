import requests

headers = {
    'Accept': 'application/json',  # Specify that you want JSON
}

response = requests.get('http://buy4u.3utilities.com:8000/api/products/', headers=headers)

print(response.json())