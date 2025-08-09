import requests
import json
import os

def get_weather_data(small_area):
    base_dir = os.path.dirname(__file__)
    area_file_path = os.path.join(base_dir, "weather_web_api.area.json")

    with open(area_file_path, "r", encoding="utf-8") as area_json:
        area_dict = json.load(area_json)

    small_area_id = None
    for inner_dict in area_dict:
        for cities_dict in inner_dict['cities']:
            if small_area == cities_dict['title']:
                small_area_title = cities_dict['title']
                small_area_id = cities_dict['id']
                break
        if small_area_id is not None:
            break

    if small_area_id is None:
        return {"error": "City not found"}

    url = f"https://weather.tsukumijima.net/api/forecast?city={small_area_id}"
    response = requests.get(url)

    if response.status_code != 200:
        return {"error": f"Failed to fetch data: {response.status_code}"}

    weather_data = response.json()

    try:
        with open(os.path.join(base_dir, "weather_web_api.json"), "w", encoding="utf-8") as file:
            json.dump(weather_data, file, ensure_ascii=False, indent=4)
    except Exception as error_message:
        return {"error": f"Failed to save data: {error_message}"}

    return weather_data
 