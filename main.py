from api_opt import ApiOptions
from tools import scraper

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
    keyword_list = keyword_list[4:]
    scraper(keyword_list, ApiOptions)




