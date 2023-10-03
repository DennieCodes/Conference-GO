from .keys import PEXELS_API_KEY, OPEN_WEATHER_API_KEY
import json
import requests


def get_picture(city, state):
    # url = f"https://api.pexels.com/v1/search?query='{city},{state}'"

    url = "https://api.pexels.com/v1/search"

    params = {
        "query": city + " " + state,
        "per_page": 1,
    }

    headers = {"Authorization": PEXELS_API_KEY}

    response = requests.get(url, headers=headers, params=params)
    result = json.loads(response.content)

    picture = result["photos"][0]["src"]["original"]

    return picture


def get_weather(city, state):
    # Geo Location
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={city},{state},001&limit=1&"
    api = f"appid={OPEN_WEATHER_API_KEY}"

    response = requests.get(url + api)
    result = json.loads(response.content)
    lat = result[0]["lat"]
    lon = result[0]["lon"]

    url = (
        f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&"
    )

    response = requests.get(url + api)
    result = json.loads(response.content)

    return result["weather"][0]["main"]

    # print("Weather is: ", result["weather"][0]["main"])
