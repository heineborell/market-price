import time

from curl_cffi.requests import headers
from rich import print

from api_opt import ApiOptions
from tools import request_retry, scraper

if __name__ == "__main__":
    keyword_list = [
        "Temel Gıda",
        "Meyve ve Sebze",
        "Et, Tavuk ve Balık",
        "Süt Ürünleri ve Kahvaltılık",
        "İçecek",
        "Atıştırmalık ve Tatlı",
        "Temizlik ve Kişisel Bakım Ürünleri",
    ]
    keyword_list = [keyword_list[3],keyword_list[0]]
    scraper(keyword_list, ApiOptions)




