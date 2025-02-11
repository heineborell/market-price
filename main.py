from curl_cffi import requests
from rich import print

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:134.0) Gecko/20100101 Firefox/134.0',
    'Accept': 'application/json',
    'Accept-Language': 'en-US,en;q=0.9',
    # 'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Content-Type': 'application/json',
    'Cache-Control': 'no-cache',
    'Pragma': 'no-cache',
    'Timeout': '20000',
    'Expires': '0',
    'WithCredentials': 'true',
    'Origin': 'https://marketfiyati.org.tr',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
}

keyword_list = ['Temel Gıda','Meyve ve Sebze',"Et, Tavuk ve Balık","Süt Ürünleri ve Kahvaltılık","İçecek","Atıştırmalık ve Tatlı","Temizlik ve Kişisel Bakım Ürünleri"]
json_data = {
    'keywords': 'Temel Gıda',
    'pages':89,
    'size': 24,
    'menuCategory': True,
}

response = requests.post('https://api.marketfiyati.org.tr/api/v2/searchByCategories', headers=headers, json=json_data)


for item in response.json()['content']:
    print(item)
