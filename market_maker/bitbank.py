import requests

def get_estimated_future_price(currency_pair='btc_eth'):
    request = requests.get('https://bitbank.nz/api/forecasts/' + currency_pair + '?secret=YOUR_API_KEY')
    if request.status_code != 200:
        print("request error code: {}, {}".format(request.status_code, request.text))
    featureset = request.json()['results']
    return float(featureset['estimated_future_wavg_5'])

def get_buy_below_sell_above_percents(currency_pair='btc_eth'):
    try:
        request = requests.get('https://bitbank.nz/api/forecasts/' + currency_pair + '?secret=YOUR_API_KEY')
        if request.status_code != 200:
            print("request error code: {}, {}".format(request.status_code, request.text))
        featureset = request.json()['results']
    except Exception as e:
        print(e)
        return 1.01, 1.01
    buy_below_percent = float(featureset['recommended_buy']) / float(featureset['best_bid_price'])
    sell_above_percent = float(featureset['recommended_sell']) / float(featureset['best_ask_price'])
    #take .4% off
    buy_below_percent = min(1, buy_below_percent + .006)
    sell_above_percent = max(1, sell_above_percent - .006)
    return buy_below_percent, sell_above_percent
