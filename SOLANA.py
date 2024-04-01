'''
- Building a Solana Wallet Tracker using Python and the modules Streamlit and Moralis
- https://www.webfx.com/tools/emoji-cheat-sheet/ Use this page for picking emoji
- API for Portfolio Analysis from here: https://admin.moralis.io/settings
- API for Crypto Price Checking from here: https://pro.coinmarketcap.com/account/

streamlit run f:/Programmieren/Python/SolanaTracker/SOLANA.py
'''

import api_handler
import streamlit as st
import time

time.sleep(2)

total_portfolio_value_usd = 0

sol_blc = "0.00"
usd_blc = "0.00"

solana_price, solana_24h_change = api_handler.get_solana_price()

st.set_page_config(page_title="SolanaTracker", page_icon=":zany_face:", layout="wide")

st.metric("Solana-Price",f"${solana_price}",f"{solana_24h_change}%")

st.title("Solana Wallet Tracker")

wallet = st.text_input(label="Wallet-Adress",placeholder="e.g. 71WDyyCsZwyEYDV91Qrb212rdg6woCHYQhFnmZUBxiJ6", max_chars=50, disabled=False)
button = st.button("Search 🔍")

if button:
    if wallet != "" and len(wallet) >= 5:
        result = api_handler.get_wallet_portfolio(wallet)
        solana_balance = result["nativeBalance"]
        tokens = result["tokens"]
        sol_blc = solana_balance['solana']
        #Sol Balance to USD
        usd_blc = api_handler.convert_solana_to_usd(sol_blc)

col1, col2= st.columns(2)
with col1:
   st.subheader("Solana:")
   st.header(f"{sol_blc}SOL")

with col2:
   st.subheader("USD:")
   st.header(f"${usd_blc}")

st.divider()
st.subheader("Tokens:")

if button:
    if wallet != "" and len(wallet) >= 5:
        with st.spinner('Wait for it...'):
         for token in tokens:
            formatted_amount = '{:,}'.format(round(float(token['amount'])))
            coin_value = api_handler.get_coin_price(token['mint'])
            position_value_usd = float(token['amount']) * coin_value

            # Fügen Sie den Wert des aktuellen Tokens zur Gesamtsumme hinzu
            total_portfolio_value_usd += position_value_usd

            with st.container(border=True):
               col1, col2 = st.columns([3, 1])
               with col1:
                  st.header(f"{token['name']} - ${round(position_value_usd, 2)}")
                  st.write(f'{formatted_amount} {token["symbol"]}')
               with col2:
                  st.write(f"[DexScreener](https://dexscreener.com/solana/{token['mint']})")
               st.write('<span class="red-frame"/>', unsafe_allow_html=True)

         st.toast(body="Portfolio Sucessfully loaded...", icon="✅") 

st.subheader("USD:")
st.header(f"${round(total_portfolio_value_usd, 2)}")

st.divider()
st.subheader("Total Value")
st.header(f"${total_portfolio_value_usd + float(usd_blc)}")


st.write("""
  <style>
    div[data-testid="stVerticalBlockBorderWrapper"]:has(
      >div>div>div[data-testid="element-container"] 
      .red-frame
    ) {
      outline: 2px solid white;
      border-radius: 12px;
      padding: 15px;
      background: #0d0d0d; 
    }
  </style>
  """, unsafe_allow_html=True)