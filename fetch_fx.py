import requests
import pandas as pd
import sqlalchemy as sa
from sqlalchemy.exc import IntegrityError
import os
from time import sleep

postgres_conn_str = os.environ.get(
    "POSTGRES_CONN_STR", "postgresql://admin:password@0.0.0.0:5432/admin"
)
# Heroku: https://help.heroku.com/ZKNTJQSK/why-is-sqlalchemy-1-4-x-not-connecting-to-heroku-postgres
if postgres_conn_str.startswith("postgres://"):
    postgres_conn_str = postgres_conn_str.replace("postgres://", "postgresql://", 1)
postgres_engine = sa.create_engine(postgres_conn_str)


def main():
    api_key = os.environ.get("EXCHANGE_RATE_API_KEY")
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/USD"
    print("Fetching data")
    response = requests.request("GET", url)
    if response.status_code == 200:
        result = response.json()
        if result["result"] == "success":
            last_updated_at = result["time_last_update_unix"]
            rates = result["conversion_rates"]
            usd = rates["USD"]
            cad = rates["CAD"]
            inr = rates["INR"]
            _data = {
                "last_updated_at": pd.Timestamp(last_updated_at, unit="s"),
                "usd": usd,
                "cad": cad,
                "inr": inr,
            }
            df = pd.DataFrame([_data])
            if not df.empty:
                print(df)
                try:
                    df.to_sql(
                        "fx",
                        con=postgres_engine,
                        if_exists="append",
                        index=False,
                    )
                    print("Exported")
                except IntegrityError:
                    print("Data already exists.")


if __name__ == "__main__":
    main()