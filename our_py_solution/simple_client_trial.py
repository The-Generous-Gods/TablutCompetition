import requests
import sys

url = sys.argv[1]
data = {
    "data": "test_data"
}

r = requests.post(url, json=data)
print(r.status_code)
