import gspread
import streamlit as st

gc = gspread.service_account_from_dict({
    "type": st.secrets["google"]["type"],
    "project_id": st.secrets["google"]["project_id"],
    "private_key_id": st.secrets["google"]["private_key_id"],
    "private_key": st.secrets["google"]["private_key"],
    "client_email": st.secrets["google"]["client_email"],
    "client_id": st.secrets["google"]["client_id"],
    "auth_uri": st.secrets["google"]["auth_uri"],
    "token_uri": st.secrets["google"]["token_uri"],
    "auth_provider_x509_cert_url": st.secrets["google"]["auth_provider_x509_cert_url"],
    "client_x509_cert_url": st.secrets["google"]["client_x509_cert_url"],
    "universe_domain": st.secrets["google"]["universe_domain"]
})
sh = gc.open("Crypto Wallets")
sh = gc.open("Crypto Wallets")

st.write(sh.sheet1.get('A1'))
