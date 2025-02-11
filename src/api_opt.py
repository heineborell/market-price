class ApiOptions():
    """docstring for ApiOptions."""
    def __init__(self,keyword_item:str,page:int):
        
        self.api = "https://api.marketfiyati.org.tr/api/v2/searchByCategories"

        self.json_data = {
            "keywords": f"{keyword_item}",
            "pages": page,
            "size": 24,
            "menuCategory": True,
        }
        
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:134.0) Gecko/20100101 Firefox/134.0",
            "Accept": "application/json",
            "Accept-Language": "en-US,en;q=0.9",
            # 'Accept-Encoding': 'gzip, deflate, br, zstd',
            "Content-Type": "application/json",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
            "Timeout": "20000",
            "Expires": "0",
            "WithCredentials": "true",
            "Origin": "https://marketfiyati.org.tr",
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
        }



