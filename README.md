# Xarb

This is a simple webpage that allows you to monitor the spread in Bitcoin prices between Coinbase (large US-based crypto exchange) and WazirX (India-based crypto exchange).

![Screen Shot 2021-07-26 at 6 23 50 PM](https://user-images.githubusercontent.com/18354771/126991965-1f252c81-5311-4474-bc85-818eaf2d1b02.png)

## Getting started

Provision an API key from exchangerate-api.com. The free tier allows for 1000 requests/month. Then, export it:

```
export EXCHANGE_RATE_API_KEY=abc
```

Spin up Postgres backend and pgREST API:

```
docker-compose up -d
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
python fetch_cb.py # Fetch Coinbase data
python fetch_fx.py # Fetch exchange rates from exchangerate-api.com
```

Optionally, set up cronjobs. For example:
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
gunicorn app:server
```

## Contributing
Create an issue or open up a branch and PR.
