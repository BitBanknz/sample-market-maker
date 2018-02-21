from datetime import timedelta

import logging
import requests

# from utils.timehelper import timehelper
from market_maker.utils.timehelper import timehelper

logger = logging.getLogger('root')

def get_estimated_future_price(currency_pair='btc_eth'):
    request = requests.get('https://bitbank.nz/api/forecasts/' + currency_pair + '?secret=YOUR_API_KEY')
    if request.status_code != 200:
        logger.info("request error code: {}, {}".format(request.status_code, request.text))
    featureset = request.json()['results']
    return float(featureset['estimated_future_wavg_5'])

def set_sell_mode(mode):
    with open('/tmp/sellmode.txt', 'w') as f:
        f.write(str(mode))


set_sell_mode(None)
def get_sell_mode():
    with open('/tmp/sellmode.txt', 'r') as f:
        readline = f.readline()
        if readline == "None":
            return None
        return readline == "True"


def get_buy_below_sell_above_percents(currency_pair='btc_eth'):
    global sell_mode
    try:
        request = requests.get('https://bitbank.nz/api/forecasts/' + currency_pair + '?secret=YOUR_API_KEY')
        if request.status_code != 200:
            logger.info("request error code: {}, {}".format(request.status_code, request.text))
        featureset = request.json()['results']
    except Exception as e:
        logger.info(e)
        return 1 - .03, 1.03
    time_to_ignore_forecasts = timehelper.to_posix(timehelper.now() - timedelta(minutes=3))
    if featureset['date'] < time_to_ignore_forecasts:
        logger.info("BitBank.nz returning out of date forecasts for {}".format(currency_pair))
        return 1 - .03, 1.03

    # estimated_future_price = (float(featureset['estimated_future_wavg_5']) + float(featureset['estimated_future_wavg_30']) + float(featureset['estimated_future_wavg_60'])) / 3.
    # buy_below_percent = estimated_future_price * .995
    # sell_above_percent = estimated_future_price * 1.005
    # #take % off
    # buy_below_percent = min(.998, buy_below_percent)
    # sell_above_percent = max(1.002, sell_above_percent)
    buy_below_percent = 1 - .03
    sell_above_percent = 1.03
    # should buy?

    if (float(featureset['estimated_future_wavg_5']) > 1 and
    float(featureset['power_imbalance']) > 1 and
    float(featureset['wavg_distance_to_midpoint_percent60min']) > 0
        ):
        # buy_below_percent = 1
        set_sell_mode(False)
        logger.info('buying! at ' + str(featureset['best_bid_price']))
    if (float(featureset['estimated_future_wavg_5']) < 1 and
    float(featureset['power_imbalance']) < 1 and
    float(featureset['wavg_distance_to_midpoint_percent60min']) < 0
        ):
        # sell_above_percent = 1
        set_sell_mode(True)
        logger.info('selling! at ' + str(featureset['best_ask_price']))
    sell_mode = get_sell_mode()
    if sell_mode == True:
        sell_above_percent = 1.0018
    if sell_mode == False:
        buy_below_percent = 1 - .0018

    return buy_below_percent, sell_above_percent
