# Xarb

## Getting started
Spin up Postgres backend and pgREST API:

```
docker-compose up -d
```

Initalize the db:

```
docker exec -it postgres bash
PGPASS=password psql -U admin -d admin -a -f init_db.sql
```

Initialize python virtual environment, install dependencies:

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Run modules:
```
python fetch.py # Fetch WazirX data
python fetch_cb.py # Fetch coinbase data
python fetch_fx.py # Fetch exchange rates
```

Set up cronjobs. For example:
```
# FX rates - fetch at 00:10 UTC
10 0 * * * /home/pi/wazirx/venv/bin/python3 /home/pi/wazirx/fetch_fx.py >> /home/pi/wazirx/fx.log 2>&1

## Wazirx - every 5 minutes
*/5 * * * * /home/pi/wazirx/venv/bin/python3 /home/pi/wazirx/fetch.py >> /home/pi/wazirx/fetch.log 2>&1

## Coinbase - every 5 minutes
*/5 * * * * /home/pi/wazirx/venv/bin/python3 /home/pi/wazirx/fetch_cb.py >> /home/pi/wazirx/fetch_cb.log 2>&1
```

You can spin up the frontend through the following.
```
source venv/bin/activate
cd xarb
python -m http.server 8000
```
Then, navigate to [localhost:8000](http://localhost:8000).

## Contributing
Create an issue or open up a branch and PR.
