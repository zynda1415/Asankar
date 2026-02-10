import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets.readonly",
    "https://www.googleapis.com/auth/drive.readonly",
]

@st.cache_data
def load_data():
    credentials = Credentials.from_service_account_info(
        st.secrets["service_account"],
        scopes=SCOPES
    )

    client = gspread.authorize(credentials)

    # sheet_id is INSIDE [service_account] in your toml
    sheet_id = st.secrets["service_account"]["sheet_id"]

    sheet = client.open_by_key(sheet_id).sheet1
    return pd.DataFrame(sheet.get_all_records())
