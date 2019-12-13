import requests
import json
import pandas as pd
from datetime import datetime, timedelta

headers = {
    'Connection': 'keep-alive',
    'Accept': '*/*',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Referer': 'https://www.bud.hu/en/departures',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-GB,en;q=0.9,hu-HU;q=0.8,hu;q=0.7,en-US;q=0.6',
}

params_depart = (
    ('mode', 'list'),
    ('lang', 'eng'),
    ('dir', '0'),
    ('flightdate_custom_from_date', 'yesterday'),
    ('flightdate_custom_from_time', '00:00'),
    ('onlyday', '1'),
)

params_arrival = (
    ('mode', 'list'),
    ('lang', 'eng'),
    ('dir', '1'),
    ('flightdate_custom_from_date', 'yesterday'),
    ('flightdate_custom_from_time', '00:00'),
    ('onlyday', '1'),
)

response_list = []
for direction in [params_depart, params_arrival]:
    response = requests.get('https://www.bud.hu/api/ajaxFlights/', headers=headers, params=direction)
    response_list.append(pd.DataFrame(response.json()))

df = pd.concat(response_list).reset_index(drop = True)
stamp = (datetime.today() - timedelta(days = 1)).strftime("%Y_%m_%d")
df.to_pickle(f".\\data\\BUD_{stamp}.pkl")
