from dotenv import load_dotenv
import os
import json
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import pprint
import streamlit as st
from moralis import sol_api
import gspread

# load_dotenv()
# MORALIS_API_KEY = os.getenv('MORALIS_API_KEY')
# CMC_API_KEY = os.getenv('CMC_API_KEY')

MORALIS_API_KEY = st.secrets['MORALIS_API_KEY']
CMC_API_KEY = st.secrets['CMC_API_KEY']



def get_wallet_portfolio(adress):
    params = {
    "network": "mainnet",
    "address": adress
    }

    result = sol_api.account.get_portfolio(
    api_key=MORALIS_API_KEY,
    params=params,
    )

    return result

def get_coin_price(adress):
    params = {
        "network": "mainnet",
        "address": adress
    }

    try:
        result = sol_api.token.get_token_price(
            api_key=MORALIS_API_KEY,
            params=params
        )
        return result['usdPrice']
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        return e


def convert_solana_to_usd(amount):
    url = 'https://pro-api.coinmarketcap.com/v2/tools/price-conversion'

    parameters = {
    'amount': amount,
    'symbol': 'SOL',
    'convert': 'USD',
    }

    headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': CMC_API_KEY,
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        usd_price = data['data'][0]['quote']['USD']['price']
        return round(usd_price, 2)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        return e


def get_solana_price():
    url = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest'

    parameters = {
    'symbol': 'SOL',
    }

    headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': CMC_API_KEY,
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        sol_usd_price = data['data']["SOL"][1]['quote']['USD']['price']
        sol_change_percent = data['data']["SOL"][1]['quote']['USD']['percent_change_24h']


        return round(sol_usd_price, 2), round(sol_change_percent, 1)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        return 0


gc = gspread.service_account_from_dict(st.secrets["google"])
sh = gc.open("Crypto Wallets")
worksheet = sh.sheet1

def upload_wallet(name, value, address):
    worksheet.append_row([name, value, address])

def get_wallet_names():
    addresses = worksheet.col_values(1)
    addresses = addresses[1:]
    return addresses

def get_wallet_address(name):
    names = worksheet.col_values(1)[1:]
    addresses = worksheet.col_values(3)[1:]
    try:
        index = names.index(name)
        return addresses[index]
    except ValueError:
        return "Address not found for the given name"