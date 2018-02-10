from datetime import timedelta

import logging
import requests

# from utils.timehelper import timehelper
from market_maker.utils.timehelper import timehelper

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
        return 1.03, 1.03
    time_to_ignore_forecasts = timehelper.to_posix(timehelper.now() - timedelta(minutes=3))
    if featureset['date'] < time_to_ignore_forecasts:
        logger.info("BitBank.nz returning out of date forecasts for {}".format(currency_pair))
        return 1.03, 1.03

    # estimated_future_price = (float(featureset['estimated_future_wavg_5']) + float(featureset['estimated_future_wavg_30']) + float(featureset['estimated_future_wavg_60'])) / 3.
    # buy_below_percent = estimated_future_price * .995
    # sell_above_percent = estimated_future_price * 1.005
    # #take % off
    # buy_below_percent = min(.998, buy_below_percent)
    # sell_above_percent = max(1.002, sell_above_percent)
    buy_below_percent = 1
    sell_above_percent = 1
    # should buy?

    if (float(featureset['estimated_future_wavg_5']) > 1 and
                float(featureset['estimated_future_wavg_30']) > 1 and
    float(featureset['estimated_future_wavg_60']) > 1 and
    float(featureset['estimated_future_wavg_120']) > 1 and
    float(featureset['power_imbalance']) > 1 and
    float(featureset['wavg_distance_to_midpoint_percent30min']) > 0 and
    float(featureset['wavg_distance_to_midpoint_percent5min']) > 0 and
    float(featureset['wavg_distance_to_midpoint_percent60min']) > 0
        ):
        buy_below_percent = 1
        print('buying! at ' + str(featureset['best_bid_price']))
    if (float(featureset['estimated_future_wavg_5']) < 1 and
                float(featureset['estimated_future_wavg_30']) < 1 and
    float(featureset['estimated_future_wavg_60']) < 1 and
    float(featureset['estimated_future_wavg_120']) < 1 and
    float(featureset['power_imbalance']) < 1 and
    float(featureset['wavg_distance_to_midpoint_percent30min']) < 1 and
    float(featureset['wavg_distance_to_midpoint_percent5min']) < 1 and
    float(featureset['wavg_distance_to_midpoint_percent60min']) < 1
        ):
        sell_above_percent = 1
        print('selling! at ' + str(featureset['best_ask_price']))

    return buy_below_percent, sell_above_percent
