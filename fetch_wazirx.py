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
        eth_inr = result.get("ethinr")

        df = pd.DataFrame()

        str_keys = [
            "low",
            "high",
            "last",
            "open",
            "volume",
            "sell",
            "buy"
        ]
        for x in [btc_inr, eth_inr]:
            if x is not None:
                for k, v in x.items():
                    if k in str_keys:
                        x[k] = float(v)

        if btc_inr is not None:
            df = df.append([btc_inr])
        if eth_inr is not None:
            df = df.append([eth_inr])
        

        print(df)

        if not df.empty:
            df.to_sql(
                "ticker",
                con=postgres_engine,
                if_exists="append",
                index=False,
            )
            print("Exported")


if __name__ == "__main__":
    print("Fetching data")
    main()
