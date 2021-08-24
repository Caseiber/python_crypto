import requests
import pandas as pd
import sys

def get_price(cryptos, exchange='bitfinex'):
    # make an dict of all of the prices and their names
    names = []
    prices = []

    # for everything in the list, find the price
    for crypto in cryptos:
        if crypto == " " or crypto == "":
            continue

        url = 'https://api.cryptowat.ch/markets/{exchange}/{crypto}usd/price'.format(
            crypto = crypto, exchange = exchange)

        resp = requests.get(url)
        resp.raise_for_status()

        data = resp.json()

        names.append(crypto)
        prices.append(data['result']['price'])
        # prices[crypto] = data['result']
    
    data = {
        'name': names,
        'price': prices
    }
    # pass that array into pandas
    df = pd.DataFrame.from_dict(data)
    
    # return the data frame
    return df


if __name__=="__main__":
    # read in the names of the cryptocurrencies from the arguments
    if len(sys.argv) == 2:
        cryptos = sys.argv[1].split(',')
        prices = get_price(cryptos)
        print(prices)
    # print a concerned warning if nothing or more than one argument is passed in
    else:
        print("Please pass in the names of the cryptocurrencies to check as comma separate values with no spaces in between.")
        print("For example, 'btc,eth,doge' or just 'btc")