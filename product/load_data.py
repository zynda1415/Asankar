import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials


@st.cache_data(ttl=300)  # Auto refresh every 5 minutes (300 seconds)
def load_data():
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]

    creds = Credentials.from_service_account_info(
        st.secrets["service_account"],
        scopes=scope,
    )

    client = gspread.authorize(creds)

    sheet_id = st.secrets["service_account"]["sheet_id"]
    sheet = client.open_by_key(sheet_id).sheet1

    data = sheet.get_all_records()
    return pd.DataFrame(data)
