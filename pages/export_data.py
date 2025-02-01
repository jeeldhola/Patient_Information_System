import streamlit as st
import pandas as pd
import math
from datetime import datetime
from dateutil.relativedelta import relativedelta
import json
import io
from io import BytesIO

from google.oauth2 import service_account
from googleapiclient.discovery import build

credentials_info = st.secrets["connections"]
credentials = service_account.Credentials.from_service_account_info(credentials_info)

# Google Sheets API setup
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
#SERVICE_ACCOUNT_FILE = 'streemlit-ed54095f0814.json'  # Update this path
# Authenticate and create the service

service = build('sheets', 'v4', credentials=credentials)

# The ID and range of the spreadsheet
SPREADSHEET_ID = '1Eb3pnP1MYlDaBCzz0pTc3h1yNBpslxfGI4QiAQEDAiw'  # Update this with your spreadsheet ID
RANGE_NAME = 'Sheet1'  # Update this with your target range


def fetch_data_from_google_sheet():
    try:
        result = service.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=RANGE_NAME
        ).execute()

        values = result.get('values', [])

        if not values:
            st.warning("No data found in the specified range.")
            return pd.DataFrame()

        # Extract headers (First row)
        headers = values[0]
        
        if len(values) < 2:  # No data rows available
            st.warning("Only headers found, no data available.")
            return pd.DataFrame(columns=headers)

        # Process data rows safely, padding if needed
        data_rows = [row + [""] * (len(headers) - len(row)) for row in values[1:]]

        # Create DataFrame
        df = pd.DataFrame(data_rows, columns=headers)
        df = df.loc[:, ~df.columns.duplicated()]
        # Ensure MRN or any required column exists
        required_columns = ["MRN"]  # Add more required columns if needed
        for col in required_columns:
            if col not in df.columns:
                st.error(f"Column '{col}' not found in Google Sheets.")
                return pd.DataFrame()

        return df

    except Exception as e:
        st.error(f"Error fetching data from Google Sheets: {str(e)}")
        return pd.DataFrame()

def to_excel(df):
    """Convert DataFrame to Excel and return as byte stream."""
    to = io.BytesIO()
    with pd.ExcelWriter(to, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False)
    to.seek(0)
    return to


if __name__ == "__main__":



    df = fetch_data_from_google_sheet()
    butt = st.button("🔙 Back")
    if butt:
            st.switch_page("main.py")
    st.markdown(
        """
        <style>
        .st-emotion-cache-yw8pof {
            width: 100%;
            padding: 6rem 1rem 10rem;
            max-width: 72rem;
        }
        .stColumn.st-emotion-cache-1vj2wxa.eiemyj2 .st-emotion-cache-b95f0i.eiemyj4>div div:nth-child(2) .st-emotion-cache-b95f0i.eiemyj4{
            overflow-y: auto;
            height: 300px;
            overflow-x: hidden;
        }
        .st-emotion-cache-j7qwjs.e1dbuyne3{
            display: none !important;
        }
        .stSidebar  {display: none !important;}
        .st-emotion-cache-1i55tjj.e1obcldf18 {display: none !important;}
        </style>
        """,
        unsafe_allow_html=True,
    )
    if "selected_columns" not in st.session_state:
        st.session_state.selected_columns = {col: False for col in df.columns}

    # **Layout: Two columns (Left for selection, Right for Table)**
    col1, col2 = st.columns([1, 3])

    # **Left Column: Scrollable Column Selection**
    with col1:
        st.subheader("Select Columns")
        with st.container():
            for col in df.columns:
                st.session_state.selected_columns[col] = st.checkbox(col, st.session_state.selected_columns[col])

    # **Right Column: Show Selected Data Table**
    selected_columns = [col for col, selected in st.session_state.selected_columns.items() if selected]
    filtered_df = df[selected_columns] if selected_columns else pd.DataFrame()

    with col2:
        st.write("### Selected Columns Data Table")
        st.dataframe(filtered_df, use_container_width=True)

    # **Function to create Excel file**
    col3, col4 = st.columns([1, 3])
    with col3:
        
        if selected_columns:
            to = to_excel(filtered_df)
            st.download_button(
                label="Download Selected Data",
                data=to,
                file_name="filtered_columns.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.warning("Please select column to download.")
    with col4:
       
        to1 = to_excel(df)  # Export the entire DataFrame
        st.download_button(
            label="Download Entire Data",
            data=to1,
            file_name="entire_file.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )