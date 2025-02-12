import getpass
import json
import sqlite3
import time
from pathlib import Path

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
            response = json_data
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

            response = request_retry(4, api, headers, json_data)
            if response is not None and not isinstance(response,dict):
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
                print(f"[bold red] {keyword_list_item} page {page} added to unscraped list. [/bold red]")

            json_string = json.dumps(item_list)
            with open( f"data/item_list_{i}.json", "w",) as f:
                f.write(json_string)

            json_string_time = json.dumps(timeout_dict)
            with open( "data/time_out.json", "w",) as f:
                f.write(json_string_time)



def sql_uploader():
    username = getpass.getuser()

    conn = sqlite3.connect(
        f"/Users/{username}/Projects/market-price/data/database.db"
    )
    cursor = conn.cursor()

    try:
        with conn as connection:
            connection.execute("DROP TABLE market_data")


    except sqlite3.OperationalError:
        print("Tables do not exist")

    cursor.execute(
        """
    CREATE TABLE market_data (
        id ,
        title text,
        brand TEXT
    )
    """
    )


    conn.commit()
    conn.close()

# ## Create the table in the database (if not exists)
# id_list= []
# for item in item_list:
#     segment_range = Path(
#         f"/Users/{username}/iCloud/Research/Data_Science/Projects/data/strava/{grand_tour}_pickles"
#     )
#     for year in years:
#         # Define the regex pattern
#         print(f'[bold yellow] ----------------{grand_tour}, {year}-------------- [/bold yellow]')
#         pattern = re.compile(rf"segment_\d+_{year}_{grand_tour}\.pkl\.gz")
#         # Use glob to find files and filter with regex
#         matching_files = [
#             file for file in segment_range.glob("*") if pattern.match(file.name)
#         ]
#         for file in matching_files:
#             json_data = json.loads(jsonisers.segment_jsoniser(file,logger))
#
#             for activity in json_data:
#                 if (
#                     activity["activity_id"] not in id_list_segment
#                     and activity["athlete_id"] != "no id"
#                     and activity["distance"] != "No distance"
#                 ):
#                     cursor.execute(
#                         """ INSERT INTO segments_data (activity_id, athlete_id, date, tour_year, distance, segment) VALUES (?, ?, ?, ?, ?, ?) """,
#                         (
#                             int(activity["activity_id"]),
#                             int(activity["athlete_id"]),
#                             str(activity["date"])
#                             .replace("June", "Jun")
#                             .replace("July", "Jul")
#                             .replace("August", "Aug")
#                             .replace("September", "Sep"),
#                             str(f"{grand_tour}-{year}"),
#                             float(activity["distance"]),
#                             json.dumps(activity["segments"]),
#                         ),
#                     )
#                     id_list_segment.append(activity["activity_id"])
#                     # print(f"{j} segment {grand_tour} {year} uploaded")
#                 else:
#                     pass
#
#             json_data = json.loads(jsonisers.stat_jsoniser(file,logger))
#
#             for activity in json_data:
#                 if (
#                     activity["activity_id"] not in id_list_stat
#                     and activity["athlete_id"] != "no id"
#                 ):
#                     cursor.execute(
#                         """ INSERT INTO stats_data (activity_id, athlete_id, tour_year , stat) VALUES (?,?, ?, ? ) """,
#                         (
#                             int(activity["activity_id"]),
#                             int(activity["athlete_id"]),
#                             str(f"{grand_tour}-{year}"),
#                             json.dumps(dict(list(activity.items())[2:])),
#                         ),
#                     )
#                     id_list_stat.append(activity["activity_id"])
#                     # print(f"{j} stats {grand_tour} {year} uploaded")
#                 else:
#                     pass
#
#     # for j in range(
#     #    1,
#     #    len(sorted(details_range.glob(f"segment_details_{year}_{grand_tour}_*")))
#     #    + 1,
#     # ):
#     #    with open(
#     #        f"/Users/{username}/iCloud/Research/Data_Science/Projects/tdf_data_fin/strava/mapping/segment_details_{year}_{grand_tour}_{j}.json",
#     #        "r",
#     #    ) as f:
#     #        json_data = json.loads(f.read())
#
#     #    for segment in json_data:
#     #        if segment["segment_no"] not in id_list_details:
#     #            try:
#     #                segment["category"]
#     #            except KeyError:
#     #                segment["category"] = None
#
#     #            cursor.execute(
#     #                """ INSERT INTO segment_details_data  (segment_id, activity_id, segment_name, category, hidden, end_points) VALUES (?, ?, ?, ?, ?, ? ) """,
#     #                (
#     #                    str(segment["segment_no"]),
#     #                    str(segment["activity_no"]),
#     #                    segment["segment_name"],
#     #                    str(segment["category"]),
#     #                    str(segment["hidden"]),
#     #                    json.dumps(segment["end_points"]),
#     #                ),
#     #            )
#     #            id_list_details.append(segment["segment_no"])
#     #            print(f"{j} segment_details {grand_tour} {year} uploaded")
#     #        else:
#     #            pass
# print("JSON data uploaded successfully.")
#
# # with open(
# #    f"/Users/deniz/Projects/tdf_results/data_tools/data_cleaning/jsoniser_test_2.json",
# #    "r",
# # ) as f:
# #
# #    json_data = json.loads(f.read())
# #
# # id_list_json = []
# # for activity in json_data:
# #    if activity["activity_id"] not in id_list_json:
# #        cursor.execute(
# #            """ INSERT INTO segments_json (activity_id, athlete_id, date, distance, segments) VALUES (?, ?, ?, ?, ?) """,
# #            (
# #                str(activity["activity_id"]),
# #                str(activity["athlete_id"]),
# #                str(activity["date"])
# #                .replace("June", "Jun")
# #                .replace("July", "Jul")
# #                .replace("August", "Aug")
# #                .replace("September", "Sep"),
# #                float(activity["distance"]),
# #                json.dumps(activity["segments"]),
# #            ),
# #        )
# #        id_list_json.append(activity["activity_id"])
# #        # print(f"{j} segment {grand_tour} {year} uploaded")
# #    else:
# #        pass
