from datetime import timedelta

import logging
import requests

from utils.timehelper import timehelper

logger = logging.getLogger('root')

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
    time_to_ignore_forecasts = timehelper.to_posix(timehelper.now() - timedelta(minutes=3))
    if featureset['date'] < time_to_ignore_forecasts:
        logger.info("BitBank.nz returning out of date forecasts for {}".format(currency_pair))
        return 1.01, 1.01

    estimated_future_price = (float(featureset['estimated_future_wavg_5']) + float(featureset['estimated_future_wavg_30']) + float(featureset['estimated_future_wavg_60'])) / 3.
    buy_below_percent = estimated_future_price * .995
    sell_above_percent = estimated_future_price * 1.005
    #take % off
    buy_below_percent = min(.998, buy_below_percent)
    sell_above_percent = max(1.002, sell_above_percent)
    return buy_below_percent, sell_above_percent
