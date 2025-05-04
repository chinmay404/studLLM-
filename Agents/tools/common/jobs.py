import requests

payload = { 'api_key': 'a4b3d551', 'query': 'Software' }
r = requests.get('https://api.scraperapi.com/structured/google/jobs', params=payload)
print(r.text)
