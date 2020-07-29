import requests
import json
import sys


args = sys.argv
port = args[1]
new_password = args[2]
token = args[3]

url = 'http://localhost:' + port + '/api/reset_superadmin_password'
json_headers = {'Content-type': 'application/json'}

data = {
    'token': token,
    'new_password': new_password
}

print(requests.post(url, data=json.dumps(data), headers=json_headers).json())
