# %%
from get_auth import get_auth
import requests
import json
token = get_auth()
headers = {'Authorization': f'Bearer {token}'}

request = "messages?$select=sender,subject"
# request = "messages?"
request += "&$count=true"
request += "&$top=100"
# request = ""


def get_request(request):
    url = "https://graph.microsoft.com/v1.0/me/" + request
    response = requests.get(url, headers=headers)
    return response.json()


senders = set()
# while
data = get_request(request)
value = data['value']
senders.update(i['sender']['emailAddress']['address']
               for i in value if 'sender' in i)
print(senders)
# %%
