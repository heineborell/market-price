from curl_cffi import requests
from curl_cffi.requests.exceptions import Timeout

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
    'keywords': f"{keyword_list[0]}",
    'pages':10,
    'size': 24,
    'menuCategory': True,
}

api = 'https://api.marketfiyati.org.tr/api/v2/searchByCategories'

def get_req(api, headers, json_data):
    return requests.post(api, headers=headers, json=json_data)


def request_retry(max_retries,api,headers,json_data):
    retry_count = 0
    while retry_count < max_retries:
        try:
            response = get_req(api, headers, json_data)
            break  # Exit loop on success
        except Timeout:
            print("Timeout while waiting for the page to load. Reloading...")
            retry_count += 1
            if retry_count >= max_retries:
                print("Max retries reached. Exiting.")
                response = None  # Handle case where all retries fail
        except Exception as e:
            print(f"An error occurred: {e}")
            response = None
            break  # Exit loop on unexpected errors

    return response

response=request_retry(3,api,headers,json_data)
if response is not None:
    for item in response.json()['content']:
        print(item)

