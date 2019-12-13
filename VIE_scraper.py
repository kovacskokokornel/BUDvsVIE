import requests
import json
import pandas as pd
from datetime import datetime, timedelta

headers = {
    'Connection': 'keep-alive',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-GB,en;q=0.9,hu-HU;q=0.8,hu;q=0.7,en-US;q=0.6',
}

params = (
    ('dummy', 'R08452f1Xc2dbb0c'),
)
### Departure data
response = requests.get('https://www.viennaairport.com/jart/prj3/va/data/flights/out.json', headers=headers, params=params)
df = pd.DataFrame(response.json()["monitor"]["departure"])

df["status"] = [status["description"] for status in df["status"]]
df["aircraft"] = [status["description"] for status in df["aircraft"]]
df["airline"] = [status["name"] for status in df["airline"]]
df["destinations"] = [status[0]["name"] for status in df["destinations"]]
df.drop(columns = ["checkin", "codeshares", "idx", "gate", "gateArea"], inplace = True)

df_dep = df.loc[df["status"] == "airborne"]

### Arrival data
response = requests.get('https://www.viennaairport.com/jart/prj3/va/data/flights/inc.json', headers=headers, params=params)
df = pd.DataFrame(response.json()["monitor"]["departure"])

df["status"] = [status["code"] for status in df["status"]]
df["aircraft"] = [status["description"] for status in df["aircraft"]]
df["airline"] = [status["name"] for status in df["airline"]]
df["origins"] = [status[0]["name"] for status in df["origins"]]
df.rename(columns = {"origins": "destinations"}, inplace = True)
df.drop(columns = ["belt", "codeshares", "idx"], inplace = True)

df_arr = df.loc[df["status"] == "BLI"]

df_final = pd.concat([df_arr, df_dep], sort = False).reset_index(drop = True)

print(len(df_final))
stamp = datetime.today().strftime("%Y_%m_%d_%H_%M")
df_final.to_pickle(f".\\data\\VIE_{stamp}.pkl")
