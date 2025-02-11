from curl_cffi import requests
from curl_cffi.requests.exceptions import Timeout


def get_req(api, headers, json_data):
    return requests.post(api, headers=headers, json=json_data)


def request_retry(max_retries, api, headers, json_data):
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
