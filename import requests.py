import requests

url = "https://www.currys.co.uk/gbuk/rtx-3080/components-upgrades/graphics-cards/324_3091_30343_xx_ba00013562-bv00313767/xx-criteria.html"

payload={}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
