# White port 5800
# Black port 5801

import requests
import sys
import socket

url = sys.argv[1]
port = sys.argv[2]

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((url, port))

"""
data = {
    "data": "test_data"
}

r = requests.post(url, json=data)
print(r.status_code)
"""

while True:
    print(client_socket.accept())
