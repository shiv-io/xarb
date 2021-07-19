import requests
import pandas as pd
import sqlalchemy as sa
import os
from time import sleep

postgres_conn_str = os.environ.get(
    "POSTGRES_CONN_STR", "postgresql://admin:password@0.0.0.0:5432/admin"
)
postgres_engine = sa.create_engine(postgres_conn_str)


def main():
    url = "https://api.wazirx.com/api/v2/tickers"

    response = requests.request("GET", url)
    if response.status_code == 200:
        result = response.json()
        btc_inr = result.get("btcinr")

        df = pd.DataFrame()

        # The following keys are string-formatted, so we want to convert these
        # to floats
        str_keys = ["low", "high", "last", "open", "volume", "sell", "buy"]
        if btc_inr is not None:
            for k, v in btc_inr.items():
                if k in str_keys:
                    btc_inr[k] = float(v)
            df = df.append([btc_inr])

        if not df.empty:
            df["at"] = pd.to_datetime(df["at"], unit="s")
            print(df)
            df.to_sql(
                "wazirx_ticker",
                con=postgres_engine,
                if_exists="append",
                index=False,
            )
            print("Exported")


if __name__ == "__main__":
    print("Fetching data")
    main()
