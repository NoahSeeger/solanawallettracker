import gspread
import streamlit as st

gc = gspread.service_account_from_dict(st.secrets["google"])
sh = gc.open("Crypto Wallets")
worksheet = sh.sheet1

first_names = ["John", "Emma", "Mark"]
last_names = ["Doe", "Smith", "Johnson"]

for i in range(len(first_names)):
    row = [first_names[i], last_names[i]]
    worksheet.append_row(row)

st.write("Daten wurden erfolgreich hinzugefügt!")