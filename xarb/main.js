function getLatestData() {
    // HTTP GET
    fetch(url).then(function (result) {
        return result.json();
    }).then(function (json) {
        displayResults(json);
        console.log(json);
    });
}

function displayResults(json) {
    // If any results from the prior search exist, delete em'
    while (resultParas.firstChild) {
        resultParas.removeChild(resultParas.firstChild);
    }

    result = json[0];

    arbValue = document.createElement('li');
    arbValue.textContent = 'Current arbitrage value: USD ' + result.arbitrage_value_usd.toLocaleString();

    exchangeRate = document.createElement('li');
    exchangeRate.textContent = 'Assumes USD/INR at ' + result.inr.toFixed(2).toLocaleString();

    unixNow = Date.now()
    secondsAgo = Math.round(unixNow / 1000 - result.at);
    lastUpdated = document.createElement('li');

    if (secondsAgo < 60) {
        lastUpdated.textContent = 'WazirX spot price last updated ' + secondsAgo + ' seconds ago';
    } else if (secondsAgo >= 60 && secondsAgo < 3600) {
        minutesAgo = Math.round(secondsAgo / 60);
        lastUpdated.textContent = 'WazirX spot price last updated ' + minutesAgo + ' minutes ago';
    } else if (secondsAgo >= 3600) {
        hoursAgo = Math.round(secondsAgo / 3600);
        lastUpdated.textContent = 'WazirX spot price last updated ' + hoursAgo + ' hours ago';
    }

    coinbaseUpdatedSecondsAgo = Math.round(unixNow / 1000 - result.coinbase_updated_at);
    coinbaseLastUpdated = document.createElement('li');

    if (coinbaseUpdatedSecondsAgo < 60) {
        coinbaseLastUpdated.textContent = 'Coinbase spot price last updated ' + coinbaseUpdatedSecondsAgo + ' seconds ago';
    } else if (coinbaseUpdatedSecondsAgo >= 60 && coinbaseUpdatedSecondsAgo < 3600) {
        minutesAgo = Math.round(coinbaseUpdatedSecondsAgo / 60);
        coinbaseLastUpdated.textContent = 'Coinbase spot price last updated ' + minutesAgo + ' minutes ago';
    } else if (secondsAgo >= 3600) {
        hoursAgo = Math.round(coinbaseUpdatedSecondsAgo / 3600);
        coinbaseLastUpdated.textContent = 'Coinbase spot price last updated ' + hoursAgo + ' hours ago';
    }

    resultParas.appendChild(exchangeRate);
    resultParas.appendChild(lastUpdated);
    resultParas.appendChild(coinbaseLastUpdated);

    wazirXHeader = document.createElement('th');
    wazirXHeader.textContent = 'WazirX spot price, USD';
    wazirXValue = document.createElement('td');
    wazirXValue.textContent = result.wazirx_btc_usd.toLocaleString();

    dataTable.appendChild(document.createElement('tr'));
    dataTable.appendChild(wazirXHeader);
    dataTable.appendChild(wazirXValue);

    cbHeader = document.createElement('th');
    cbHeader.textContent = 'CB spot price, USD';
    cbValue = document.createElement('td');
    cbValue.textContent = result.coinbase_btc_usd.toLocaleString();
    cbValue.className = 'cbValue';

    dataTable.appendChild(document.createElement('tr'));
    dataTable.appendChild(cbHeader);
    dataTable.appendChild(cbValue);

    arbHeader = document.createElement('th');
    arbHeader.textContent = 'Spread, USD';
    arbValue = document.createElement('td');
    arbValue.textContent = result.arbitrage_value_usd.toLocaleString();

    dataTable.appendChild(document.createElement('tr'));
    dataTable.appendChild(arbHeader);
    dataTable.appendChild(arbValue);

    const pctReturn = (result.arbitrage_value_usd / result.coinbase_btc_usd) * 100
    returnHeader = document.createElement('th');
    returnHeader.textContent = 'Return on trade, %';
    returnValue = document.createElement('td');
    returnValue.textContent = Math.round(pctReturn * 100) / 100;

    dataTable.appendChild(document.createElement('tr'));
    dataTable.appendChild(returnHeader);
    dataTable.appendChild(returnValue);
}

function refreshPage() {
    location.reload();
}

function up(v, n) {
    return Math.ceil(v * Math.pow(10, n)) / Math.pow(10, n);
}

function calculateAndDisplay() {
    while (calculateResults.firstChild) {
        calculateResults.removeChild(calculateResults.firstChild);
    }

    const upfrontCapital = document.querySelector('.upfrontCapital').value;
    f = document.createElement('li');

    var cbValue = document.querySelector('.cbValue').textContent // e.g. 54,500.23 (string)
    cbValue = parseFloat(cbValue.replace(/[^0-9-.]/g, '')); // e.g. 54500.23 (float)
    btcOffUpfront = up(upfrontCapital / cbValue, 8); // BTC is divisible to 8 decimal places

    f.textContent = upfrontCapital + ' USD gets you ' + btcOffUpfront + ' BTC (doesn\'t account for fees)';
    calculateResults.appendChild(f);

}

const url = 'http://localhost:3001/last_arb'
const refreshBtn = document.querySelector('.refreshBtn');
const resultParas = document.querySelector('.resultParas');
const dataTable = document.querySelector('.dataTable');
const submitBtn = document.querySelector('.submit');
const calculateResults = document.querySelector('.calculateResults');

window.onload = getLatestData;
refreshBtn.addEventListener('click', refreshPage);
// submitBtn.addEventListener('click', calculateAndDisplay);
