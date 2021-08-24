import requests
import pandas as pd
import sys

# get_price takes in a list of cryptocurrencies and returns a dataframe of their names and current prices
def get_price(cryptos, exchange='bitfinex'):
    # make lists of all of the prices and their names
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
    
    # pass that array into pandas
    df = pd.DataFrame(prices, index=names, columns=['Price'])
    df.index.name = 'Name'
    
    # return the data frame
    return df


if __name__=="__main__":
    # read in the names of the cryptocurrencies from the arguments
    if len(sys.argv) == 2:
        cryptos = sys.argv[1].split(',')
        try:
            prices = get_price(cryptos)
            print(prices)
        except requests.exceptions.HTTPError:
            print("An error occured finding cryptocurrency prices. Please be sure that the correct abbreviation was used for each currency")
    # print a concerned warning if nothing or more than one argument is passed in
    else:
        print("Please pass in the names of the cryptocurrencies to check as comma separate values with no spaces in between.")
        print("For example, 'btc,eth,doge' or just 'btc")