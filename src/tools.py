import json
import time

from curl_cffi import requests
from curl_cffi.requests.exceptions import Timeout
from rich import print


def get_req(api, headers, json_data):
    return requests.post(api, headers=headers, json=json_data)


def request_retry(max_retries, api, headers, json_data):
    retry_count = 0
    while retry_count < max_retries:
        try:
            response = get_req(api, headers, json_data)
            break  # Exit loop on success
        except Timeout:
            print("[bold yellow] Timeout while waiting for the page to load. Reloading... [/bold yellow]")
            retry_count += 1
            if retry_count >= max_retries:
                print("[bold red] Max retries reached. Exiting. [/bold red]")
                response = None  # Handle case where all retries fail
        except Exception as e:
            print(f"An error occurred: {e}")
            response = None
            break  # Exit loop on unexpected errors

    return response

def scraper(keyword_list,ApiOptions):
    timeout_dict = {}
    for i,keyword_list_item in enumerate(keyword_list):
        print(keyword_list_item)
        item_list = []
        for page in range(300):
            time.sleep(3)
            api_options = ApiOptions(keyword_list_item,page) 
            api = api_options.api
            headers = api_options.headers
            json_data = api_options.json_data

            response = request_retry(3, api, headers, json_data)
            if response is not None:
                zero_test = []
                for item in response.json()["content"]:
                    zero_test.append(item)
                    item_list.append(item)
                    print("Scraped page", page)

                if len(zero_test)==0:
                    print("End of page.")
                    break
            else:
                timeout_dict.update({'keyword':keyword_list_item,'page':page})

            json_string = json.dumps(item_list)
            with open( f"item_list_{i}.json", "w",) as f:
                f.write(json_string)

    json_string_time = json.dumps(timeout_dict)
    with open( "time_out.json", "w",) as f:
        f.write(json_string_time)


