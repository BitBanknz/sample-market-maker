import requests

def get_estimated_future_price(currency_pair='btc_eth'):
    request = requests.get('https://bitbank.nz/api/forecasts/' + currency_pair + '?secret=YOUR_API_KEY')
    if request.status_code != 200:
        print("request error code: {}, {}".format(request.status_code, request.text))
    featureset = request.json()['results']
    return float(featureset['estimated_future_wavg_5'])

def get_buy_below_sell_above_percents(currency_pair='btc_eth'):
    request = requests.get('https://bitbank.nz/api/forecasts/' + currency_pair + '?secret=YOUR_API_KEY')
    if request.status_code != 200:
        print("request error code: {}, {}".format(request.status_code, request.text))
    featureset = request.json()['results']
    buy_below_percent = float(featureset['recommended_buy']) / float(featureset['best_bid_price'])
    sell_above_percent = float(featureset['recommended_sell']) / float(featureset['best_ask_price'])
    return buy_below_percent, sell_above_percent
