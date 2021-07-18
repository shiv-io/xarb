import requests
import pandas as pd
import sqlalchemy as sa
from sqlalchemy.exc import IntegrityError
import os
from time import sleep
from datetime import datetime

from fetch_wazirx import postgres_conn_str

postgres_engine = sa.create_engine(postgres_conn_str)

def main():
    url = "https://api.coinbase.com/v2/prices/spot?currency=USD"
    print("Fetching data")
    response = requests.request("GET", url)
    unix_time = datetime.utcnow()
    if response.status_code == 200:
        result = response.json()
        _data = result["data"]
        _data["amount"] = float(_data["amount"])
        _data["created_at"] = pd.Timestamp(unix_time)
        _data["type"] = 'spot'
        df = pd.DataFrame([_data])
        if not df.empty:
            print(df)
            try:
                df.to_sql(
                    "cb_ticker",
                    con=postgres_engine,
                    if_exists="append",
                    index=False,
                )
                print("Exported")
            except IntegrityError:
                print("Data already exists.")
    else:
        print(response.text)

if __name__ == "__main__":
    main()