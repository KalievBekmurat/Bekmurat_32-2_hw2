import requests

url = "https://kinogo.biz/"

payload = {}
headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/116.0',
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
  'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)