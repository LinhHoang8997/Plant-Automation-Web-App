import requests
import timeit
import pandas as pd
import io  #important and useful


def zipToCoord(zipcode):
    US_zip = pd.read_csv('model/US_zip_code.csv', usecols=['Postal Code', 'Estimated Lat', 'Estimated Long'], dtype={"Postal Code": str, 'Estimated Lat': float,  'Estimated Long': float})
    # US_zip['z'].apply(lambda x: 1 if zipcode in US_zip['Postal Code'] else 0)
    lat = None
    long = None

    for index, row in US_zip.iterrows():
        # print(zipcode)
        # print(row['Postal Code'])
        if zipcode in row['Postal Code']:
            lat = row['Estimated Lat']
            long = row['Estimated Long']
            return (lat, long)

def getDataFromNSRDB(zipcode):
    (lat, long) = zipToCoord(zipcode)
    print(lat)
    print(long)
    with open('model/NSRDB_api_key.txt', 'r') as api_file: #Have to add model/ back to link
        key = api_file.read()
    NREL_psm3_url = "http://developer.nrel.gov/api/solar/nsrdb_psm3_download.csv?"

    # payload = "names=2012&leap_day=false&interval=60&utc=false&full_name=Honored%2BUser&email=honored.user%40gmail.com&affiliation=NREL&mailing_list=true&reason=Academic&attributes=dhi%2Cdni%2Cwind_speed%2Cair_temperature&wkt=MULTIPOINT(-106.22%2032.9741%2C-106.18%2032.9741%2C-106.1%2032.9741)"

    params = {
        'api_key': key
    }

    data = {
        "names": 2018,
        'utc': "true",
        'email': 'linhdanghoang@gmail.com',
        'wkt': "POINT({} {})".format(long, lat), #latitude is the wide axis, and longtitude is the x axis. https://gis.stackexchange.com/questions/11626/does-y-mean-latitude-and-x-mean-longitude-in-every-gis-software
        'attributes': 'dni,ghi,clearsky_ghi,solar_zenith_angle',
        'interval': 60
    }

    headers = {
        'content-type': "application/x-www-form-urlencoded",
        'cache-control': "no-cache"
    }

    response = requests.post(NREL_psm3_url, headers=headers, data=data, params = params)
    csv_data = response.content
    solar_df = pd.read_csv(io.StringIO(csv_data.decode('utf-8')), skiprows=2)

    solar_df_by_month = solar_df.drop(['Day', 'Hour'], axis=1).groupby("Month", as_index= False).mean().round(3)
    data_in_json = solar_df_by_month.to_json(orient='columns')
    return data_in_json