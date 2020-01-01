import requests, pandas as pd
from datetime import datetime

def getWeatherAsJSON(zipcode):
    with open("model/open_weather_api_key.txt", 'r') as api_file:
        key = api_file.read()
    headers = {'X-API-KEY': key}
    params = {"zip": zipcode, "mode": "json"}
    open_weather_api_url = 'http://api.openweathermap.org/data/2.5/forecast'
    req = requests.post(open_weather_api_url, headers=headers, params=params)

    req_data = req.json()
    # print(req_data)
    # print(zipcode)

    weather_data_list = []

    for entry in (req_data['list']):
        posix_time = int(entry['dt'])
        record = {
            'year': datetime.utcfromtimestamp(posix_time).year,
            'month': datetime.utcfromtimestamp(posix_time).month,
            'day': datetime.utcfromtimestamp(posix_time).day,
            'hour': datetime.utcfromtimestamp(posix_time).hour,
            "humidity": entry['main']['humidity'],
            "temperature": entry['main']['temp'],
            "cloudiness_percent": entry['clouds']['all'],
            "wind_speed": entry['wind']['speed']
        }


        if 'rain' in entry.keys():
            record["rain_mm"] = entry['rain']['3h']
        else:
            record["rain_mm"] = 0
        # for weather_condition in entry['weather']:
        #     # weather_data_dict.append({""})
        #     print(weather_condition['main'])
        #     print(weather_condition['description'])
        weather_data_list.append(record)

    # print(weather_data_list)
    weather_df = pd.DataFrame.from_records(weather_data_list)[:len(weather_data_list)-13]
    # function to save to database when user "Favorited" a view
    weather_data_json = weather_df.to_json(orient='columns')
    print(weather_df.tail(10))
    return weather_data_json