import streamlit as st
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials

def load_data():
    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=[
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
    )

    client = gspread.authorize(creds)
    sheet = client.open("asankar_product_images").sheet1
    data = sheet.get_all_records()
    return pd.DataFrame(data)
