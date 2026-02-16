import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

SHEET_ID = "1I9X2swZuDwxuuRlUituBojqKmwjomVr-K9kLeTWjtUU"
SHEET_NAME = "asankar_product_images"

@st.cache_data(ttl=60)
def load_data():
    credentials = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"]
    )
    client = gspread.authorize(credentials)
    sheet = client.open_by_key(SHEET_ID).worksheet(SHEET_NAME)
    data = sheet.get_all_records()
    return pd.DataFrame(data)
