import streamlit as st
import pandas as pd
import math
from datetime import datetime
from dateutil.relativedelta import relativedelta
import json

from google.oauth2 import service_account
from googleapiclient.discovery import build

credentials = st.secrets["connections"]
credentials_info = json.dumps(dict(credentials))
credentials = service_account.Credentials.from_service_account_info(credentials_info)
# Google Sheets API setup
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# Authenticate and create the service
service = build('sheets', 'v4', credentials=credentials)
# The ID and range of the spreadsheet
SPREADSHEET_ID = '1Eb3pnP1MYlDaBCzz0pTc3h1yNBpslxfGI4QiAQEDAiw'  
RANGE_NAME = 'Sheet1'  

def append_to_google_sheet(data):
    try:
        # Prepare the data to be appended
        values = [list(data.values())]
        body = {
            'values': values
        }
        # Call the Sheets API to append the data
        result = service.spreadsheets().values().append(
            spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME,
            valueInputOption='RAW', body=body).execute()
        st.success("Data successfully saved to Google Sheets.")
        return True
    except Exception as e:
        st.error(f"An error occurred while saving data to Google Sheets: {e}")
        return False

def fetch_data_from_google_sheet():
    try:
        
        result = service.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=RANGE_NAME
        ).execute()

        values = result.get('values', [])

        if not values:
            st.warning("No data found in the specified range.")
            return pd.DataFrame()  # or return None if preferred

        # Handle header and rows
        headers = values[0]  # Assume the first row is the header
        data_rows = [row + [""] * (len(headers) - len(row)) for row in values[1:]]  # Pad rows if needed
        df = pd.DataFrame(data_rows, columns=headers)
        return df

    except Exception as e:
        st.error(f"Error fetching data from Google Sheets: {str(e)}")
        return pd.DataFrame()

def update_google_sheet(data, mrn):
    try:
        df = fetch_data_from_google_sheet()
        if df.empty:
            st.error(f"No data found for MRN {mrn}.")
            return False
        if 'MRN' not in df.columns:
            st.error(f"MRN column not found in Google Sheets.")
            return False
        index = df[df['MRN'] == mrn].index[0]
        for key, value in data.items():
            if key in df.columns:
                df.at[index, key] = value
            else:
                st.error(f"Column {key} not found in Google Sheets.")
                return False
        values = [df.columns.tolist()] + df.values.tolist()
        body = {
            'values': values
        }
        result = service.spreadsheets().values().update(
            spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME,
            valueInputOption='RAW', body=body).execute()
        st.success("Data successfully updated in Google Sheets.")
        return True
    except Exception as e:
        st.error(f"An error occurred while updating data in Google Sheets: {e}")
        return False
st.markdown(
    """
    <style>
    
    .st-emotion-cache-1wqrzgl{
    min-width: auto;
    max-width: 212px}

    .st-emotion-cache-yw8pof{
        max-width: 1000px;
        padding: 0rem 0rem 00rem;
    }
    .st-emotion-cache-bm2z3a{
        padding-top: 20px;
    }
    .st-emotion-cache-1b50p5p{
    height: 100%;
    }
    .st-emotion-cache-1cvow4s h2 {
        font-size: 1.75rem;
    padding-top: 0.5rem;
    }
    .st-emotion-cache-qcpnpn{
    max-height: 500px;
    overflow-x: auto;
    margin-bottom: 75px;

    }
    
    .gdg-wmyidgi {
    max-height: 200px;
    }
    .stDataFrame.st-emotion-cache-6nrhu6.egqaslz0 >div:nth-child(2){
    max-height: 200px!important;
    }
    
    </style>
    """,
    
    unsafe_allow_html=True,
)
st.markdown(
    """
    <script>
        // Function to modify the aria-expanded attribute of the sidebar
        document.addEventListener("DOMContentLoaded", function() {
            const sidebar = document.querySelector('.stSidebar.st-emotion-cache-1wqrzgl.e1dbuyne0');
            if (sidebar) {
                // Remove the aria-expanded attribute
                sidebar.removeAttribute("aria-expanded");
            }
        });
    </script>
    """,
    unsafe_allow_html=True,
)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
username = "user"

def fetch_data_for_mrn(mrn):
    df = fetch_data_from_google_sheet()
    if df.empty:
        st.error(f"No data found in the Google Sheet.")
        return None
    if 'MRN' not in df.columns:
        st.error(f"MRN column not found in the Google Sheet.")
        return None
    if mrn not in df['MRN'].values:
        st.error(f"No data found for MRN {mrn}.")
        return None
    data = df[df['MRN'] == mrn]
    return data

if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(
        columns=["Name",
    "MRN",
    "Duplicate",
    "TAREdate",
    "PTech",
    "Tareage",
    "Gender",
    "Ethnicity",
    "PMHxHTN",
    "PMHxDM",
    "Hypercholesterolemia",
    "PMHxSmoking",
    "Obesity",
    "CirPMH_HBV",
    "CirPMH_HBVFT",
    "CirPMH_HBVART",
    "CirPMH_HCV",
    "CirPMH_HCVFT",
    "CirPMH_HCVART",
    "CirPMH_AUD",
    "CirPMH_AUDFT",
    "CirPMH_IVDU",
    "CirPMH_IVDUFT",
    "CirPMH_Liverfactors"
    "Cirdx_Dxdate",
    "Cirdx_Dxmethod",
    "Cirdx_HPIFT",
    "Cirdx_ImageemrFT",
    "Cirdx_Metavir",
    "Cirdx_Compatdx",
    "Cirdx_Compatdxbinary",
    "Cirdx_CompFT",
    "Cirdx_DateLabs",
    "Cirdx_AFP",
    "Cirdx_AFP L3",
    "Cirdx_AFPL3DateFT",
    "Cirdx_AscitesCTCAE",
    "Cirdx_AscitesCTCAEnumb",
    "Cirdx_AscitesFT",
    "HCCdx_HCCdxdate",
    "HCCdx_Methoddx",
    "HCCdx_Datelabs",
    "HCCdx_AFP",
    "HCCdx_AFP L3",
    "HCCdx_AFPL3dateFT",
    "HCCdx_Bilirubin",
    "HCCdx_Albumin",
    "HCCdx_INR",
    "HCCdx_Creatinine",
    "HCCdx_Sodium",
    "HCCdx_AscitesCTCAE",
    "HCCdx_AscitesCTCAEnumb",
    "HCCdx_Ascitesdiruetics",
    "HCCdx_Ascitesparacentesis",
    "HCCdx_Asciteshospitalization",
    "HCCdx_HEgrade",
    "HCCdx_ECOG",
    "HCCdx_LIRADS",
    "HCCdx_CPcalc",
    "HCCdx_CPclass",
    "HCCdx_MELD",
    "HCCdx_MELDNa",
    "HCCdx_Albiscore",
    "HCCdx_Albigrade",
    "HCCdx_BCLC",
    "PRVTHER_LDT",
    "PRVTHER_RFA",
    "PRVTHER_RFAdate",
    "PRVTHER_TARE",
    "PRVTHER_TAREdate",
    "PRVTHER_SBRT",
    "PRVTHER_SBRTdate",
    "PRVTHER_TACE",
    "PRVTHER_TACEdate",
    "PRVTHER_MWA",
    "PRVTHER_MWAdate",
    "PRVTHER_Resection",
    "PRVTHER_Resection date",
    "PRVTHER_Prevtxsum",
    "PRVTHER_NotesFT",
    "PRVTHER_Totalrecur",
    "PRVTHER_Locationprevtxseg",
    "PRVTHER_Location of Previous Tx Segments FT",
    "PRVTHER_RecurLocationFT",
    "PRVTHER_RecurDate",
    "PRVTHER_Recurrence Seg",
    "PRVTHER_NewHCCoutsideprevsite",
    "PRVTHER_NewHCCadjacentprevsite",
    "PRVTHER_ResidualHCCnoteFT",
    "PRVTHER_ResidualHCC",
    "PRVTHER_SystemictherapyFT",
    "PRVTHER_DateAFP",
    "PRVTHER_AFP",
    "PREY90_sx",
    "PREY90_Datelabs",
    "PREY90_AFP",
    "PRE90_AFPbinary",
    "PREY90_Bilirubin",
    "PREY90_Albumin",
    "PREY90_INR",
    "PREY90_Creatinine",
    "PREY90_Sodium",
    "PREY90_AST",
    "PREY90_ALT",
    "PREY90_Alkaline Phosphatase",
    "PREY90_Potassium",
    "PREY90_AscitesCTCAE",
    "PREY90_AscitesCTCAEnumb",
    "PREY90_AscitesFT",
    "PREY90_Ascitesdiruetics",
    "PREY90_Ascitesparacentesis",
    "PREY90_Asciteshospitalization",
    "PREY90_HEgrade",
    "PREY90_ECOG",
    "PREY90_CPcalc",
    "PREY90_CPclass",
    "PREY90_MELD",
    "PREY90_MELDNa",
    "PREY90_Albiscore",
    "PREY90_Albigrade",
    "PREY90_BCLC",
    "MY90_date",
    "MY90_Lung_shunt",
    "DAYY90_AFP",
    "DAYY90_AFP Binary",
    "PRE90_AFP BinaryDup",
    "DAYY90_Sodium",
    "DAYY90_Creatinine",
    "DAYY90_INR",
    "DAYY90_Albumin",
    "DAYY90_Bilirubin",
    "DAYY90_AST",
    "DAYY90_ALT",
    "DAYY90_Alkphos",
    "DAYY90_Leukocytes",
    "DAYY90_Platelets",
    "DAY90_Potassium",
    "Day90_AscitesCTCAE",
    "Day90_AscitesCTCAEnumb",
    "Day90_HEgrade",
    "Day90_ECOG",
    "DAYY90_CPcalc",
    "DAYY90_CPclass",
    "DAYY90_MELD",
    "DAYY90_MELDNa",
    "DAYY90_Albiscore",
    "DAYY90_Albigrade",
    "DAYY90_BCLC",
    "DAYY90_Sphere",
    "DAYY90_LTnoteFT",
    "ken_ChildPughscore",
    "ken_MELDpreTARE (MELDpreTARE)",
    "POSTY90_30DY_Datelabs",
    "POSTY90_30DY_AFP",
    "POSTY90_30DY_AFPdate",
    "POSTY90_30DY_Sodium",
    "POSTY90_30DY_Creatinine",
    "POSTY90_30DY_INR",
    "POSTY90_30DY_Albumin",
    "POSTY90_30DY_Bilirubin",
    "POSTY90_30DY_AST",
    "POSTY90_30DY_ALT",
    "POSTY90_30DY_ALP",
    "POSTY90_30DY_Leukocytes",
    "POSTY90_30DY_Platelets",
    "POSTY90_30DY_Potassium",
    "30DY_AE_AscitesCTCAE",
    "30DY_AE_AscitesCTCAEnumb",
    "30DY_AE_Ascitesdiruetics",
    "30DY_AE_Ascitesparacentesis",
    "30DY_AE_Asciteshospitalization",
    "30DY_AE_HEgrade",
    "30DY_AE_ascities_freetext",
    "POSTY90_30DY_ECOG",
    "POSTY90_30DY_CPcalc",
    "POSTY90_30DY_CPclass",
    "POSTY90_30DY_MELD",
    "POSTY90_30DY_MELDNa",
    "POSTY90_30DY_ALBIscore",
    "POSTY90_30DY_ALBIgrade",
    "POSTY90_30DY_BCLC",
    "Ken_BCLCStagepost90",
    "Ken_MELD_Stagepost90"
    "30DY_AE_Portalhtn",
    "30DY_AE_Vascularcomp",
    "30DY_AE_Fatigue",
    "30DY_AE_Diarrhea",
    "30DY_AE_Hypoalbuminemia",
    "30DY_AE_Hyperbilirubinemia",
    "30DY_AE_Increasecreatine",
    "30DY_AE_Abdominalpain",
    "30DY_AE_Sepsis",
    "30DY_AE_BacterialPer",
    "30DY_AE_Hemorrhage",
    "30DY_AE_Anorexia",
    "30DY_AE_Intrahepaticfistula",
    "30DY_AE_Constipation",
    "30DY_AE_Nausea",
    "30DY_AE_Vomiting",
    "30DY_AE_Cholecystitis",
    "30DY_AE_Gastriculcer",
    "30DY_AE_Hyperkalemia",
    "30DY_AE_Respfailure",
    "30DY_AE_AKI",
    "30DY_AE_Radiationpneumonitis",
    "30DY_AE_Other",
    "90DY_AE_DateofAE",
    "Additional Notes FT",
    "90DY_AE_Hosp3mo",
    "90DY_AE_Datehosp3mo",
    "90DY_AE_Hosp6mo",
    "90DY_AE_DeathduetoAE",
    "OC_Liver_transplant",
    "OC_Liver_transplant_date",
    "K_ken_ToxgtG3",
    "K_ken_ToxgtG2",
    "K_ken_AlbiPreTARERaw",
    "K_ken_AlbiPreTAREGrade",
    "K_ken_AlbiPostTARERaw",
    "K_ken_AliPostTAREGrade",
    "PREY90_prescan_modality",
    "PREY90_Imaging Date",
    "PREY90_total number of lesions",
    "PREY90_Number Involved Lobes",
    "PREY90_target_lesion_1_segments",
    "PREY90_TL1_LAD",
    "PREY90_Target Lesion 1 PAD",
    "PREY90_Target Lesion 1 CCD",
    "PREY90_Target Lesion 1 VOL",
    "PREY90_Target lesion 2 Segments",
    "PREY90_Target Lesion 2 LAD",
    "PREY90_Target Lesion 2 PAD",
    "PREY90_Target Lesion 2 CCD",
    "PREY90_Target Lesion 2 VOL",
    "PREY90_pretx targeted Lesion Dia Sum",
    "PREY90_Non-Target Lesion Location",
    "PREY90_Non-Target Lesion 2 LAD Art Enhanc",
    "PREY90_Non-Target Lesion 2 PAD Art Enhanc",
    "PREY90_Non-Target Lesion 2 CCD Art Enhanc",
    "PREY90_Non-targeted Lesion Dia Sum",
    "PREY90_Reviewers Initials",
    "PREY90_Pre Y90 Extrahepatic Disease",
    "PREY90_Pre Y90 Extrahepatic Disease Location",
    "PREY90_PVT",
    "PREY90_PVT Location",
    "PREY90_Features of cirrhosis",
    "1st_FU_Scan Modality",
    "1st_FU_Imaging Date",
    "1st_FU_Months Since Y90",
    "1st_FU_Total number of lesions",
    "1st_FU_Target Lesion 1 LAD Art Enhanc",
    "1st_FU_Target Lesion 1 PAD Art Enhanc",
    "1st_FU_Target Lesion 1 CCD Art Enhanc",
    "1st_FU_Target Lesion 2 Segments",
    "1st_FU_Target Lesion 2 LAD Art Enhanc",
    "1st_FU_Target Lesion 2 PAD Art Enhanc",
    "1st_FU_Target Lesion 2 CCD Art Enhanc",
    "1st_FU_Follow up 1 targeted Lesion Dia Sum",
    "1st_FU_Non-Target Lesion 2 LAD Art Enhanc",
    "1st_FU_Non-Target Lesion 2 PAD Art Enhanc",
    "1st_FU_Non-Target Lesion 2 CCD Art Enhanc",
    "1st_FU_Non-targeted Lesion Dia Sum",
    "1st_FU_Lesion Necrosis",
    "1st_FU_Reviewers Initials",
    "1st_FU_Non target lesion response",
    "1st_FU_New Lesions",
    "1st_FU_NEW Extrahepatic Disease",
    "1st_FU_NEW Extrahepatic Dz Location",
    "1st_FU_NEW Extrahepatic Dz Date",
    "1st_FU_% change non target lesion",
    "1st_FU_% Change Target Dia",
    "1st_FU_mRECIST LOCALIZED",
    "1st_FU_mRECIST Overall",
    "1st_FU_Free Text",
    "2nd_FU_Scan Modality",
    "2nd_FU_Imaging Date",
    "2nd_FU_Months Since Y90",
    "2nd_FU_Total number of lesions",
    "2nd_FU_Target Lesion 1 LAD Art Enhanc",
    "2nd_FU_Target Lesion 1 PAD Art Enhanc",
    "2nd_FU_Target Lesion 1 CCD Art Enhanc",
    "2nd_FU_Target Lesion 2 Segments",
    "2nd_FU_Target Lesion 2 LAD Art Enhanc",
    "2nd_FU_Target Lesion 2 PAD Art Enhanc",
    "2nd_FU_Target Lesion 2 CCD Art Enhanc",
    "2nd_FU_Follow up 2 targeted Lesion Dia Sum",
    "2nd_FU_Non-Target Lesion 1 LAD Art Enhanc",
    "2nd_FU_Non-Target Lesion 1 PAD Art Enhanc",
    "2nd_FU_Non-Target Lesion 1 CCD Art Enhanc",
    "2nd_FU_Non-targeted Lesion Dia Sum",
    "2nd_FU_Lesion Necrosis",
    "2nd_FU_Reviewers Initials",
    "2nd_FU_Non target lesion response",
    "2nd_FU_New Lesions",
    "2nd_FU_Extrahepatic Disease",
    "2nd_FU_NEW Extrahepatic Dz Location",
    "2nd_FU_NEW Extrahepatic Dz Date",
    "2nd_FU_% change non target lesion",
    "2nd_FU_% Change Target Dia",
    "2nd_FU_mRECIST LOCALIZED",
    "2nd_FU_mRECIST LOCALIZED with Follow UP",
    "2nd_FU_mRECIST Overall",
    "2nd_FU_Free Text",
    "3rd_FU_Scan Modality",
    "3rd_FU_Imaging Date",
    "3rd_FU_Months Since Y90",
    "3rd_FU_Total number of lesions",
    "3rd_FU_Target Lesion 1 LAD Art Enhanc",
    "3rd_FU_Target Lesion 1 PAD Art Enhanc",
    "3rd_FU_Target Lesion 1 CCD Art Enhanc",
    "3rd_FU_Target Lesion 2 Segments",
    "3rd_FU_Target Lesion 2 LAD Art Enhanc",
    "3rd_FU_Target Lesion 2 PAD Art Enhanc",
    "3rd_FU_Target Lesion 2 CCD Art Enhanc",
    "3rd_FU_Follow up 2 targeted Lesion Dia Sum",
    "3rd_FU_Non-Target Lesion 1 LAD Art Enhanc",
    "3rd_FU_Non-Target Lesion 1 PAD Art Enhanc",
    "3rd_FU_Non-Target Lesion 1 CCD Art Enhanc",
    "3rd_FU_Non-targeted Lesion Dia Sum",
    "3rd_FU_Lesion Necrosis",
    "3rd_FU_Reviewers Initials",
    "3rd_FU_Non target lesion response",
    "3rd_FU_New Lesions",
    "3rd_FU_Extrahepatic Disease",
    "3rd_FU_NEW Extrahepatic Dz Location",
    "3rd_FU_NEW Extrahepatic Dz Date",
    "3rd_FU_% change for non target lesion",
    "3rd_FU_% Change Target Dia",
    "3rd_FU_mRECIST LOCALIZED",
    "3rd_FU_mRECIST LOCALIZED with Follow UP",
    "3rd_FU_mRECIST Overall",
    "3rd_FU_Free Text",
    "4th_FU_Scan Modality",
    "4th_FU_Imaging Date",
    "4th_FU_Months Since Y90",
    "4th_FU_Total number of lesions",
    "4th_FU_Target Lesion 1 LAD Art Enhanc",
    "4th_FU_Target Lesion 1 PAD Art Enhanc",
    "4th_FU_Target Lesion 1 CCD Art Enhanc",
    "4th_FU_Target Lesion 2 Segments",
    "4th_FU_Target Lesion 2 LAD Art Enhanc",
    "4th_FU_Target Lesion 2 PAD Art Enhanc",
    "4th_FU_Target Lesion 2 CCD Art Enhanc",
    "4th_FU_Follow up 2 targeted Lesion Dia Sum",
    "4th_FU_Non-Target Lesion 1 LAD Art Enhanc",
    "4th_FU_Non-Target Lesion 1 PAD Art Enhanc",
    "4th_FU_Non-Target Lesion 1 CCD Art Enhanc",
    "4th_FU_Non-targeted Lesion Dia Sum",
    "4th_FU_Lesion Necrosis",
    "4th_FU_Reviewers Initials",
    "4th_FU_Non target lesion response",
    "4th_FU_New Lesions",
    "4th_FU_Extrahepatic Disease",
    "4th_FU_NEW Extrahepatic Dz Location",
    "4th_FU_NEW Extrahepatic Dz Date",
    "4th_FU_% change non target lesion",
    "4th_FU_% Change Target Dia",
    "4th_FU_mRECIST LOCALIZED",
    "4th_FU_mRECIST LOCALIZED with Follow UP",
    "4th_FU_mRECIST Overall",
    "4th_FU_Free Text",
    "5th_FU_Imaging Date",
    "5th_FU_Months Since Y90",
    "5th_FU_Total number of lesions",
    "5th_FU_Non-Target Lesion 1 LAD Art Enhanc",
    "5th_FU_Non-Target Lesion 1 PAD Art Enhanc",
    "5th_FU_Non-Target Lesion 1 CCD Art Enhanc",
    "5th_FU_Non-targeted Lesion Dia Sum",
    "5th_FU_Non target lesion response",
    "5th_FU_New Lesions",
    "5th_FU_Extrahepatic Disease",
    "5th_FU_NEW Extrahepatic Dz Location",
    "5th_FU_NEW Extrahepatic Dz Date",
    "5th_FU_% change non target lesion",
    "5th_FU_% Change Target Dia",
    "5th_FU_mRECIST LOCALIZED",
    "5th_FU_mRECIST LOCALIZED with Follow UP",
    "5th_FU_mRECIST Overall",
    "Dead",
    "Date of Death",
    "Time to Death",
    "OLT",
    "Date of OLT",
    "Time to OLT",
    "Repeat tx post Y90",
    "Date of Repeat tx Post Y90",
    "Time to Repeat Tx Post Y90",
    "Date of Localized Progression",
    "Time to localized progression",
    "Date of Overall (Local or systemic) Progression",
    "Time to Overall (Local or systemic) Progression",
    "Date of Last Follow up or last imaging date (if not OLT, Death, Repeat tx)",
    "GTV mean dose", "Tx vol mean dose", "Liver Vol Mean dose", "Healthy Liver mean dose", 
    "GTV Vol", "Tx vol", "Liver vol", "Healthy Liver Vol", "GTV/Liver", 
    "D98", "D95", "D90", "D80", "D70", 
    "V100", "V200", "V300", "V400", "ActivityBq", 
    "ActivityCi", "Tx vol Activity Density", "NEW", 
    "GTV < D95 Vol_ml", "GTV < D95 Mean Dose", "GTV < D95 Min Dose", 
    "GTV < D95 SD", "GTV < D95 Vol_1", "GTV < D95 Mean Dose_1", 
    "GTV < D95 Min Dose_1", "GTV < D95 SD_1", "GTV < D95 Vol_2", 
    "GTV < D95 Mean Dose_2", "GTV < D95 Min Dose_2", "GTV < D95 SD_2", 
    "GTV < 100 Gy Vol", "GTV < 100 Gy Mean Dose", "GTV < 100 Gy Min Dose", "GTV < 100 Gy SD",
    "1AFP Date", "1AFP", "2AFP Date", "2AFP", "3AFP Date", "3AFP", "4AFP Date", "4AFP",
    "5AFP Date", "5AFP", "6AFP Date", "6AFP", "7AFP Date", "7AFP", "8AFP Date", "8AFP",
    "9AFP Date", "9AFP", "10AFP Date", "10AFP", "11AFP Date", "11AFP", "12AFP Date", "12AFP",
    "13AFP Date", "13AFP", "14AFP Date", "14AFP", "15AFP Date", "15AFP", "16AFP Date", "16AFP",
    "17AFP Date", "17AFP", "18AFP DATE", "18AFP", "19AFP DATE", "19AFP", "20AFP DATE", "20AFP",
    "21AFP DATE", "21AFP", "22AFP DATE", "22AFP", "23AFP DATE", "23AFP", "24AFP DATE", "24AFP",
    "25AFP DATE", "25AFP", "26AFP DATE", "26AFP", "27AFP DATE", "27AFP", "28AFP DATE", "28AFP",
    "29AFP DATE", "29AFP", "30AFP DATE", "30AFP", "31AFP Date", "31AFP", "32AFP DATE", "32AFP",
    "33AFP DATE", "33AFP", "34AFP DATE", "34AFP",]
    )
# List of 11 tabs
def calculate_comorbidities_total(hypertension, diabetes, hypercholesterolemia, smoking, obesity):
    """Calculate total number of comorbidities"""
    conditions = [hypertension, diabetes, hypercholesterolemia, smoking, obesity]
    return sum(1 for condition in conditions if condition == 1)

def calculate_comorbidities_binary(total_count):
    """Convert total count to binary (1 if >=1, 0 if 0)"""
    return 1 if total_count >= 1 else 0
def get_variable_value(mrn, column_name):
    df = fetch_data_from_google_sheet()
    if df.empty:
        st.error(f"No data found in the Google Sheet.")
        return None
    if 'MRN' not in df.columns or column_name not in df.columns:
        st.error(f"Required columns not found in the Google Sheet.")
        return None
    if mrn not in df['MRN'].values:
        st.error(f"No data found for MRN {mrn}.")
        return None
    value = df.loc[df['MRN'] == mrn, column_name].values[0]
    return value
def login_page():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == "user" and password == "pass":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Invalid username or password.")

def add_new_data():
 
    
    df=fetch_data_from_google_sheet()
    st.dataframe(df)
    def calculatepoints(bilirubin, albumin, inr, ascites, encephalopathy):
                        if bilirubin < 2:
                            bilirubin_points = 1
                        elif 2 <= bilirubin <= 3:
                            bilirubin_points = 2
                        else:
                            bilirubin_points = 3

                        if albumin > 3.5:
                            albumin_points = 1
                        elif 2.8 <= albumin <= 3.5:
                            albumin_points = 2
                        else:
                            albumin_points = 3

                        if inr < 1.7:
                            inr_points = 1
                        elif 1.7 <= inr <= 2.3:
                            inr_points = 2
                        else:
                            inr_points = 3

            # Points for Ascites
                        if ascites == 'none':
                            ascites_points = 1
                        elif ascites == 'Asymptomatic' or ascites == 'Minimal ascities/Mild abd distension, no sx' or ascites == "Symptomatic" :
                            ascites_points = 2
                        else:  # 'moderate/severe'
                            ascites_points = 3

            # Points for Hepatic Encephalopathy
                        if encephalopathy == "1":
                            encephalopathy_points = 1
                        elif encephalopathy == "2":
                            encephalopathy_points = 2
                        else:
                            encephalopathy_points = 3
                             
                             

            # Total Child-Pugh score
                        total_score = (
                            bilirubin_points + albumin_points + inr_points + ascites_points + encephalopathy_points
                        )

                        return total_score

    def calculate_class(poin):
                        if 5 <= poin <= 6:
                            return 'A'
                        elif 7 <= poin <= 9:
                            return 'B'
                        elif 10 <= poin <= 15:
                            return 'C'
                        else:
                            return "Invalid points: must be between 5 and 15."
    
    def albi_calc(a,b):
                        a=int(a)*17.1
                        b=int(b)
                        t = math.log(a, 10)
                        answer = round((t * 0.66) + (b * -0.085))
                        return answer
    
    def albi_class(albi_score):
        if albi_score <= -2.60:
            return "Grade 1"
        elif albi_score > -2.60 and albi_score <= -1.39:
             return "Grade 2"
        else:
             return "Grade 3"

    def process_input(value):
                        
            # Handle the 'NA' case
                        if value.upper() == "NA":
                            return "NA"
            # Handle numeric cases
                        elif value.isdigit():
                            numeric_value = int(value)
                            return 1 if numeric_value < 200 else 2
                        else:
                            return "Invalid Input"
    
    def validate_input(value):
                        if value.isdigit() and 5 <= int(value) <= 15:
                            return value  # Valid number
                        elif value.upper() == "NA":
                            return "NA"  # Valid 'NA'
                        else:
                            return "NA" 
    def validate_input2(value):
                        if value.isdigit() and 6 <= int(value) <= 40:
                            return value  # Valid number
                        elif value.upper() == "NA":
                            return "NA"  # Valid 'NA'
                        else:
                            return "NA" 

    st.title("Patient Information System")

    tabs = ["Patient Info", "Patient Demographics", "Cirrhosis PMH","HCC Diagnosis", "Previous Therapy for HCC", "Pre Y90", "Day_Y90", "Post Y90 Within 30 Days Labs", "Other Post Tare","Imaging Date","Dosimetry Data","AFP"]

    col1, col2 = st.columns([0.3, 0.7],gap="small")

    # Left column for vertical tabs
    with col1:
        st.header("Patient Deatils")
        st.session_state.selected_tab = st.radio("", tabs)

    with col2:
        
        if st.session_state.selected_tab == "Patient Info":
            
            st.subheader("Patient_Info")
            with st.form("patient_info_form"):
                # Patient Info Section
                col1, col2 = st.columns(2)
                last_name = col1.text_input("Last Name")
                last_name = last_name.lower()
                first_name = col2.text_input("First Name")
                first_name = first_name.lower()
                
                mrn = st.text_input("MRN",help="Enter patient's Medical Record Number")
                
                duplicate_procedure_check = 0
                tare_date = st.date_input("TARE Tx Date", help="Select the treatment date")
                procedure_technique = st.selectbox(
                "Procedure Technique",
                options=["1", "2"],
                format_func=lambda x: {
                                    "1": "Lobar",
                                    "2": " Segmental",
                                }[x],
                index=None,  # No default selection
                placeholder="Choose an option",
                )

                age = st.number_input("Age at time of TARE", min_value=0, max_value=150, step=1)
            
                submit_tab1 = st.form_submit_button("Submit")
                if submit_tab1:
                        df = fetch_data_from_google_sheet()
                        if not df.empty and mrn in df['MRN'].values:
                            st.error(f"MRN {mrn} already exists. Please enter a unique MRN.")
                        else:
                            if hasattr(st.session_state, 'temp_mrn'):
                                # If temp_mrn exists, remove the old entry with the previous MRN
                                st.session_state.data = st.session_state.data[st.session_state.data["MRN"] != st.session_state.temp_mrn]
                                # Reset temp_mrn after clearing the previous entry
                                del st.session_state.temp_mrn
                            
                    
                            data = {
                                "Name": f"{last_name}, {first_name}",
                                "MRN": mrn,
                                "Duplicate" : duplicate_procedure_check,
                                "TAREdate": tare_date.strftime("%Y-%m-%d"),
                                "PTech": procedure_technique,
                                "Tareage": age
                                } 
                            st.session_state.temp_mrn = mrn
                            # Store the data in session state
                            st.session_state.patient_info = data
                            # Append the data to Google Sheets
                            append_to_google_sheet(data)
 
        elif st.session_state.selected_tab == "Patient Demographics":
            st.subheader("Patient_Demographics")
            with st.form("demographics_form"):
                #st.subheader("Patient Description")
                if "MRN" not in st.session_state.data:
                    st.warning("Please complete the Patient Information tab first.")
                else:
                    #try:
                        gender = st.selectbox(
                            "Gender",
                            options=["Male", "Female"],
                            index=None,  # No default selection
                            placeholder="Choose an option",
                        )

                        # Ethnicity dropdown
                        ethnicity = st.selectbox(
                            "Ethnicity",
                            options=["Black","White", "Asian", "Hispanic", "Other", "NA", "0"],
                            index=None,  # No default selection
                            placeholder="Choose an option",
                            
                        )

                        hypertension = st.selectbox(
                            "PMHx Hypertension",
                            options=["No", "Yes"],
                            index=None,  # No default selection
                            placeholder="Choose an option",
                        )

                        diabetes = st.selectbox(
                            "PMHx Diabetes (T1 or T2)",
                            options=["No", "Yes"],
                            index=None,  # No default selection
                            placeholder="Choose an option",
                        )

                        hypercholesterolemia = st.selectbox(
                            "Hypercholesterolemia",
                            options=["No", "Yes"],
                            index=None,  # No default selection
                            placeholder="Choose an option",
                        )

                        smoking = st.selectbox(
                            "Hx of Smoking",
                            options=["No", "Yes"],
                            index=None,  # No default selection
                            placeholder="Choose an option",
                        )

                        obesity = st.selectbox(
                            "Obesity",
                            options=["No", "Yes"],
                            index=None,  # No default selection
                            placeholder="Choose an option",
                        )

                        # Calculate comorbidities
                        total_count = calculate_comorbidities_total(
                            int(hypertension == "Yes"),
                            int(diabetes == "Yes"),
                            int(hypercholesterolemia == "Yes"),
                            int(smoking == "Yes"),
                            int(obesity == "Yes")
                        )
                        
                        binary_value = calculate_comorbidities_binary(total_count)

                        # Display calculated fields (read-only)
                        st.info(f"Comorbidities Total Count: {total_count}")
                        st.info(f"Comorbidities Binary Value: {binary_value}")
                        submit_tab2 = st.form_submit_button("Submit")
                        if submit_tab2:
                            #index = st.session_state.data[st.session_state.data["MRN"] == st.session_state.temp_mrn].index[0]
                            data1={
                                "Gender": gender,
                                "Ethnicity":ethnicity,
                                "PMHxHTN": hypertension,
                                "PMHxDM":diabetes,
                                "Hypercholesterolemia" : hypercholesterolemia,
                                "PMHxSmoking" : smoking,
                                "Obesity" : obesity,
                            }
                            if "patient_info" in st.session_state and st.session_state.patient_info["MRN"] == st.session_state.temp_mrn:
                                st.session_state.patient_info.update(data1)
                                # Update the data in Google Sheets
                                update_google_sheet(st.session_state.patient_info, st.session_state.temp_mrn)
                            else:
                                st.error(f"No patient information found for MRN {st.session_state.temp_mrn}")
                       
        elif st.session_state.selected_tab == "Cirrhosis PMH":
            st.subheader("Cirrhosis PMH")
            with st.form("cirrhosis_pmh_form"):
                
                if "MRN" not in st.session_state.data:
                    st.warning("Please complete the Patient Information tab first.")
                else:
                    try:
                    
                # Cirrhosis PMH Fields
                        cir_pmh_hbv_status = st.selectbox(
                            "Cir PMH HBV Status",
                            options=["Yes", "No"],
                            help="Select HBV Status",
                            index=None,  # No default selection
                            placeholder="Choose an option",
                        )

                        cir_pmh_hbv_free_text = "0" if cir_pmh_hbv_status == "No" else st.text_input(
                            "Cir PMH HBV Free Text"
                        )
                        
                        cir_pmh_hbv_art = "0" if cir_pmh_hbv_status == "No" else st.selectbox(
                            "Cir PMH HBV ART",
                            options=["Entecavir", "Tenofovir", "NA"],
                            index=None,  # No default selection
                            placeholder="Choose an option",
                        )

                        cir_pmh_hcv_status = st.selectbox(
                            "Cir_PMH_HCV Status",
                            options=["Yes", "No"],
                            index=None,  # No default selection
                            placeholder="Choose an option",
                        )

                        cir_pmh_hcv_free_text = "No" if cir_pmh_hcv_status == "No" else st.text_input(
                            "Cir_PMH_HCV Free Text",
                            help="Provide additional details for HCV Status",
                        )

                        cir_pmh_hcv_art = "No" if cir_pmh_hcv_status == "No" else st.selectbox(
                            "Cir_PMH_HCV ART",
                            options=["sofosbuvir/velpatasvir", "ledipasvir/sofosbuvir", "NA", "Glecaprevir/pibrentasvi"],
                            help="Select ART treatment for HCV",
                            index=None,  # No default selection
                            placeholder="Choose an option",
                    
                        )

                        cir_pmh_alcohol_use_disorder = st.selectbox( 
                            "Cir_PMH_Alcohol Use Disorder",
                            options=["Yes", "No"],
                            help="Select Alcohol Disorder",
                            index=None,  # No default selection
                            placeholder="Choose an option",
                        )

                        cir_pmh_alcohol_free_text = "0" if cir_pmh_alcohol_use_disorder == "No" else st.text_input(
                            "Cir_PMH_Alcohol Free Text",
                            help="Provide additional details for Alcohol Disorder",
                        )

                        cir_pmh_ivdu_status = st.selectbox(
                            "Cir_PMH_IVDU Status",
                            options=["Yes", "No"],
                            #format_func=lambda x: f"{x} ({1 if x == 'Yes' else 0})",
                            help="Select IVDU Status",
                            index=None,  # No default selection
                            placeholder="Choose an option",
                        )

                        cir_pmh_ivdu_free_text = "0" if cir_pmh_ivdu_status == "No" else st.text_input(
                            "Cir_PMH_IVDU Free Text",
                            help="Provide additional details for IVDU"
                    
                        )

                        cir_pmh_liver_addtional_factor = st.selectbox(
                            "Cir_PMH_Liver Additional Factors",
                            options=["NAFLD", "MAFLD", "NASH", "Autoimmune Hepatitis", "Hereditary Hemochromatosis","none"],
                            help="Select Other Contributing Factors",
                            index=None,  # No default selection
                            placeholder="Choose an option",
                        )
                
                        st.subheader("Cirrhosis Dx")
                        Cirrhosis_Dx_Diagnosis_Date = st.date_input("Cirrhosis Dx Diagnosis Date",help="Select Diagnosis date")

                        Cirrhosis_Dx_Diagnosis_Method = st.selectbox(
                            "Cirrhosis_Dx_Diagnosis Method",
                            options=["Biopsy", "Imaging"],
                            help="Select Diagnosis Method",
                            index=None,  # No default selection
                            placeholder="Choose an option",
                        ) 
                        Cirrhosis_Dx_HPI_EMR_Note_Free_Text = st.text_area(
                            "Cirrhosis_Dx_HPI EMR Note Free Text",
                            help="Provide details of HPI EMR"
                        )
                        Cirrhosis_Dx_Imaging_Findings_EMR_Note_Free_Text = st.text_area(
                            "Cirrhosis_Dx_Imaging Findings EMR Note Free Text",
                            help="Provide details of Imaging Findings"
                        )

                        Cirrhosis_Dx_Metavir_Score = st.selectbox (
                            "Cirrhosis_Dx_Metavir Score",
                            options=["F0/F1", "F2","F3","F4","NA"],
                            help="Select Metavir_score",
                            index=None,  # No default selection
                            placeholder="Choose an option",
                        ) 

                        Cirrhosis_Dx_Complications_at_Time_of_Diagnosis = st.multiselect(
                            "Cirrhosis_Dx_Complications at Time of Diagnosis",
                            options=["ascites", " ariceal hemorrhage","Hepatic encephalopathy","jaundice","SBP", "Hepatorenal Syndrome", "Coagulopathy", "Portal HTN", "PVT", "PVTT","Portal Vein Thrombosis" "none"],
                            help="Provide details of Compilications at time of Diagnosis",
                            placeholder="Select all that apply"
                        )
                        Cirrhosis_Dx_Complications_at_Time_of_Diagnosis_String = ", ".join(Cirrhosis_Dx_Complications_at_Time_of_Diagnosis)

                        Cirrhosis_Dx_Complications_at_Time_of_Diagnosis_Binary = st.selectbox(
                            "Cirrhosis_Dx_Complications at Time of Diagnosis Binary",
                            options=["0","1"],
                            format_func=lambda x: {
                                "1": " >1 ",
                                "0": "None",
                            }[x],
                            help="Provide details of Complications_at_Time_of_Diagnosis_Binary",
                            index=None,  # No default selection
                            placeholder="Choose an option",
                        )

                        Cirrhosis_Dx_Complications_Free_Text =  st.text_area(
                            "Cirrhosis_Dx_Complications Free Text",
                            help="Provide details of Complications"
                        )

                        Cirrhosis_Dx_Date_of_Labs_in_Window = st.date_input(" Cirrhosis_Dx_Date of Labs in Window",help="Select the date of lab test")

                        Cirrhosis_Dx_AFP = st.text_input(
                            "Cirrhosis_Dx_AFP",
                            help="Enter AFP value in ng/dl"
                            
                        )

                        Cirrhosis_Dx_AFP_L3 = st.text_input(
                            "Cirrhosis_Dx_AFP L3",
                            help="Enter AFP_L3 value in ng/dl"
                            
                        )
                        Cirrhosis_Dx_AFP_L3_Date_Free_Text = st.text_area("Cirrhosis_Dx_AFP L3 Date Free Text")

                        Cirrhosis_Dx_Ascites_CTCAE = st.selectbox (
                            "Cirrhosis_Dx_Ascites CTCAE",
                            options=["none", "Asymptomatic","Minimal ascities/Mild abd distension","Symptomatic","moderate ascities/Symptomatic medical intervention", "Severe symptoms, invasive intervention indicated", "Life Threatening: Urgent operation intervention indicated"],
                            format_func=lambda x: {
                            "none": "0. none",
                            "Asymptomatic": "1. Asymptomatic",
                            "Minimal ascities/Mild abd distension": "1. Minimal ascities/Mild abd distension",
                            "Symptomatic": "2. Symptomatic",
                            "moderate ascities/Symptomatic medical intervention" : " 2. moderate ascities/Symptomatic medical intervention",
                            "Severe symptoms, invasive intervention indicated": " 3. Severe symptoms, invasive intervention indicated",
                            "Life Threatening: Urgent operation intervention indicated" : "4. Life Threatening: Urgent operation intervention indicated",

                            }[x],
                            help="Select Metavir_score",
                            index=None,  # No default selection
                            placeholder="Choose an option",
                        ) 
                        def findascitesclass(score):
                            if score == "Asymptomatic" or score== "Minimal ascities/Mild abd distension":
                                 return 2
                            elif score == "Symptomatic" or score == "moderate ascities/Symptomatic medical intervention":
                                 return 3
                            elif score == "Severe symptoms, invasive intervention indicated" or score == "Life Threatening: Urgent operation intervention indicated" :
                                 return 3
                        
                        Cirrhosis_Dx_Ascites_Classification = 1 if Cirrhosis_Dx_Ascites_CTCAE == "none" else findascitesclass(Cirrhosis_Dx_Ascites_CTCAE)
                        st.write("Cirrhosis_Dx_Ascites Classification ",Cirrhosis_Dx_Ascites_Classification)
                        Cirrhosis_Dx_Ascites_Free_Text = "NA" if Cirrhosis_Dx_Ascites_CTCAE == "none" else st.text_area(
                            "Cirrhosis_Dx_Ascites Free Text",
                            
                        
                        )

                        submit_tab3 = st.form_submit_button("Submit")
                        if submit_tab3:

                            data2={
                            "CirPMH_HBV" : cir_pmh_hbv_status,
                            "CirPMH_HBVFT" : cir_pmh_hbv_free_text,
                            "CirPMH_HBVART" : cir_pmh_hbv_art,
                            "CirPMH_HCV" : cir_pmh_hcv_status,
                            "CirPMH_HCVFT" : cir_pmh_hcv_free_text,
                            "CirPMH_HCVART" : cir_pmh_hcv_art,
                            "CirPMH_AUD" : cir_pmh_alcohol_use_disorder,
                            "CirPMH_AUDFT" : cir_pmh_alcohol_free_text,
                            "CirPMH_IVDU" : cir_pmh_ivdu_status,
                            "CirPMH_IVDUFT" : cir_pmh_ivdu_free_text,
                            "CirPMH_Liverfactors" : cir_pmh_liver_addtional_factor,
                            "Cirdx_Dxdate" : Cirrhosis_Dx_Diagnosis_Date.strftime("%Y-%m-%d"),
                            "Cirdx_Dxmethod" : Cirrhosis_Dx_Diagnosis_Method,
                            "Cirdx_HPIFT" : Cirrhosis_Dx_HPI_EMR_Note_Free_Text,
                            "Cirdx_ImageemrFT" : Cirrhosis_Dx_Imaging_Findings_EMR_Note_Free_Text,
                            "Cirdx_Metavir" : Cirrhosis_Dx_Metavir_Score,
                            "Cirdx_Compatdx" : Cirrhosis_Dx_Complications_at_Time_of_Diagnosis_String,
                            "Cirdx_Compatdxbinary" : Cirrhosis_Dx_Complications_at_Time_of_Diagnosis_Binary,
                            "Cirdx_CompFT" : Cirrhosis_Dx_Complications_Free_Text,
                            "Cirdx_DateLabs" : Cirrhosis_Dx_Date_of_Labs_in_Window.strftime("%Y-%m-%d"),
                            "Cirdx_AFP" : Cirrhosis_Dx_AFP,
                            "Cirdx_AFP L3" : Cirrhosis_Dx_AFP_L3,
                            "Cirdx_AFPL3DateFT" : Cirrhosis_Dx_AFP_L3_Date_Free_Text,
                            "Cirdx_AscitesCTCAE" : Cirrhosis_Dx_Ascites_CTCAE,
                            "Cirdx_AscitesCTCAEnumb" : Cirrhosis_Dx_Ascites_Classification,
                            "Cirdx_AscitesFT" : Cirrhosis_Dx_Ascites_Free_Text,
                                 
                            }
                            if "patient_info" in st.session_state and st.session_state.patient_info["MRN"] == st.session_state.temp_mrn:
                                st.session_state.patient_info.update(data2)
                                # Update the data in Google Sheets
                                update_google_sheet(st.session_state.patient_info, st.session_state.temp_mrn)
                            else:
                                st.error(f"No patient information found for MRN {st.session_state.temp_mrn}")
                    except:
                        st.write("Please Fill Patient Information Page")

        elif st.session_state.selected_tab == "HCC Diagnosis":
            st.subheader("HCC Diagnosis")
            with st.form("hcc_dx_form"): 
                if "MRN" not in st.session_state.data:
                    st.warning("Please complete the Patient Information tab first.")
                else:
                    #try:
                        hcc_dx_hcc_diagnosis_date = st.date_input("HCC_Dx_HCC Diagnosis Date", help="Enter the HCC diagnosis date")

                        hcc_dx_method_of_diagnosis = st.selectbox(
                            "HCC_Dx_Method of Diagnosis",   
                            options=["Biopsy", "Imaging", "Unknown"],
                            index=None,  # No default selection
                            placeholder="Choose an option",
                            #format_func=lambda x: f"{x} ({1 if x == 'Biopsy' else 2 if x == 'Imaging' else 'NA'})"
                        )

                        hcc_dx_date_of_labs = st.date_input("HCC_Dx_Date of Labs in Window")

                        hcc_dx_afp = st.number_input("HCC_Dx_AFP", help="Enter AFP value in ng/dl", step=0.1)
                        hcc_dx_afp_l3 = st.number_input("HCC_Dx_AFP L3", help="Enter AFP L3 and date details",step=0.1)
                        hcc_dx_afp_l3_date_free_text = st.text_area("HCC_Dx_AFP L3 Date Free Text")

                        hcc_dx_bilirubin = st.number_input("HCC_Dx_Bilirubin", help="Enter the bilirubin value in mg/dl", min_value=1.0,step=0.1)
                        hcc_dx_albumin = st.number_input("HCC_Dx_Albumin", help="Enter the albumin value in g/dl",step=0.1)
                        hcc_dx_inr = st.number_input("HCC_Dx_INR", help="Enter the INR value",step=0.1)
                        hcc_dx_creatinine = st.number_input("HCC_Dx_Creatinine", help="Enter the creatinine value in mg/dl",step=0.1)
                        hcc_dx_sodium = st.number_input("HCC_Dx_Sodium", help="Enter the sodium value in mmol/L",step=0.1)

                        hcc_dx_ascites_CTCAE = st.selectbox (
                            "HCC_Dx_Ascites CTCAE",
                            options=["none", "Asymptomatic","Minimal ascities/Mild abd distension","Symptomatic","moderate ascities/Symptomatic medical intervention", "Severe symptoms, invasive intervention indicated", "Life Threatening: Urgent operation intervention indicated"],
                            format_func=lambda x: {
                            "none": "0. none",
                            "Asymptomatic": "1. Asymptomatic",
                            "Minimal ascities/Mild abd distension": "1. Minimal ascities/Mild abd distension",
                            "Symptomatic": "2. Symptomatic",
                            "moderate ascities/Symptomatic medical intervention": " 2. moderate ascities/Symptomatic medical intervention",
                            "Severe symptoms, invasive intervention indicated": " 3. Severe symptoms, invasive intervention indicated",
                            "Life Threatening: Urgent operation intervention indicated" : "4. Life Threatening: Urgent operation intervention indicated",

                        }[x],
                            help="Select Metavir_score",
                            index=None,  # No default selection
                            placeholder="Choose an option",
                        ) 
                        def findascitesclass(score):
                            if score == "Asymptomatic" or score== "Minimal ascities/Mild abd distension":
                                 return "Slight"
                            elif score == "Symptomatic" or score == "moderate ascities/Symptomatic medical intervention":
                                 return "Moderate"
                            elif score == "Severe symptoms, invasive intervention indicated" or score == "Life Threatening: Urgent operation intervention indicated" :
                                 return "Severe"
                        
                        hCC_dx_ascites_classification = "Absent" if hcc_dx_ascites_CTCAE == "none" else findascitesclass(hcc_dx_ascites_CTCAE)

                        hcc_dx_ascites_diruetics = 0 if hcc_dx_ascites_CTCAE == "none" else st.selectbox(
                            "HCC_Dx_Ascites Diruetics",
                            options = ["Yes","No"],
                            index=None,  # No default selection
                            placeholder="Choose an option",
            
                        )
                        hcc_dx_ascites_paracentesis = 0 if hcc_dx_ascites_CTCAE == "none" else st.selectbox(
                            "HCC_Dx_Ascites Paracentesis ",
                            options = ["Yes","No"],
                            index=None,  # No default selection
                            placeholder="Choose an option",
            
                        )
                        hcc_dx_ascites_hospitalization = 0 if hcc_dx_ascites_CTCAE == "none" else st.selectbox(
                            "HCC_Dx_Ascites Hospitalization",
                            options = ["Yes","No"],
                            index=None,  # No default selection
                            placeholder="Choose an option",
            
                        )

                        hcc_dx_he_grade = st.selectbox(
                            "HCC_Dx_HE Grade",
                            options=["1","2","3"],
                            format_func=lambda x: {
                            "1": "None",
                            "2": "Grade 1-2",
                            "3": "Grade 3-4",
                            
                        }[x],
                            index=None,  # No default selection
                            placeholder="Choose an option",

                        )
                       
                        hcc_dx_ecog_performance_status = st.selectbox("HCC_Dx_ECOG Performance Status", options=["0", "1", "2", "3", "4", "NA"],
                            index=None,  # No default selection
                            placeholder="Choose an option",)

                        hcc_dx_lirads_score = st.selectbox(
                            "HCC_Dx_LIRADS Score",
                            options=["LR-1", "LR-2", "LR-3", "LR-4", "LR-5", "LR-5V", "LR-M"],
                            index=None,  # No default selection
                            placeholder="Choose an option",
                        )

                        hcc_dx_child_pugh_points_calc = calculatepoints(hcc_dx_bilirubin,hcc_dx_albumin,hcc_dx_inr,hcc_dx_ascites_CTCAE,hcc_dx_he_grade)
                        hcc_dx_child_pugh_class_calc = calculate_class(hcc_dx_child_pugh_points_calc)
                        st.write("HCC_Dx_Child-Pugh Class calc",hcc_dx_child_pugh_class_calc)
                        st.write("HCC_Dx_Child-Pugh Points calc", hcc_dx_child_pugh_points_calc)
                        #bclc_stage_calc = st.text_input("HCC_Dx_BCLC Stage calc")
                        hcc_dx_meld_score_calc = (3.78*(int(hcc_dx_bilirubin)))+(11.2*(int(hcc_dx_inr)))+(9.57*(int(hcc_dx_creatinine)))+6.43
                        hcc_dx_meld_na_score_calc = hcc_dx_meld_score_calc + 1.32*(137-int(hcc_dx_sodium)) - (0.033*hcc_dx_meld_score_calc*(137-int(hcc_dx_sodium)))
                        def albi_calc(a,b):
                            a=int(a)*17.1
                            b=int(b)
                            t = math.log(a, 10)
                            answer = round((t * 0.66) + (b * -0.085))
                            return answer
                        
                        hcc_dx_albi_score_calc = albi_calc(hcc_dx_bilirubin, hcc_dx_albumin)
                        hcc_dx_albi_grade = albi_class(hcc_dx_albi_score_calc)
                        st.write("HCC_Dx_ALBI Score calc : ",hcc_dx_albi_score_calc)
                        st.write("HCC_Dx_ALBI Grade : ", hcc_dx_albi_grade)
                        hcc_dx_bclc_calc = st.text_area("HCC_Dx_BCLC Stage calc")
                    

                        submit_tab4 = st.form_submit_button("Submit")
                        if submit_tab4:
                                data4 = {
                                    "HCCdx_HCCdxdate": hcc_dx_hcc_diagnosis_date.strftime("%Y-%m-%d"),
                                    "HCCdx_Methoddx": hcc_dx_method_of_diagnosis,
                                    "HCCdx_Datelabs": hcc_dx_date_of_labs.strftime("%Y-%m-%d"),
                                    "HCCdx_AFP": hcc_dx_afp,
                                    "HCCdx_AFP L3": hcc_dx_afp_l3,
                                    "HCCdx_AFPL3dateFT": hcc_dx_afp_l3_date_free_text,
                                    "HCCdx_Bilirubin": hcc_dx_bilirubin,
                                    "HCCdx_Albumin": hcc_dx_albumin,
                                    "HCCdx_INR": hcc_dx_inr,
                                    "HCCdx_Creatinine": hcc_dx_creatinine,
                                    "HCCdx_Sodium": hcc_dx_sodium,
                                    "HCCdx_AscitesCTCAE": hcc_dx_ascites_CTCAE,
                                    "HCCdx_AscitesCTCAEnumb": hCC_dx_ascites_classification,
                                    "HCCdx_Ascitesdiruetics": hcc_dx_ascites_diruetics,
                                    "HCCdx_Ascitesparacentesis": hcc_dx_ascites_paracentesis,
                                    "HCCdx_Asciteshospitalization": hcc_dx_ascites_hospitalization,
                                    "HCCdx_HEgrade": hcc_dx_he_grade,
                                    "HCCdx_ECOG": hcc_dx_ecog_performance_status,
                                    "HCCdx_LIRADS": hcc_dx_lirads_score,
                                    "HCCdx_CPcalc": hcc_dx_child_pugh_points_calc,
                                    "HCCdx_CPclass": hcc_dx_child_pugh_class_calc,
                                    "HCCdx_MELD": hcc_dx_meld_score_calc,
                                    "HCCdx_MELDNa": hcc_dx_meld_na_score_calc,
                                    "HCCdx_Albiscore": hcc_dx_albi_score_calc,
                                    "HCCdx_Albigrade": hcc_dx_albi_grade,
                                    "HCCdx_BCLC": hcc_dx_bclc_calc,
                                }
                                if "patient_info" in st.session_state and st.session_state.patient_info["MRN"] == st.session_state.temp_mrn:
                                    st.session_state.patient_info.update(data4)
                                    # Update the data in Google Sheets
                                    update_google_sheet(st.session_state.patient_info, st.session_state.temp_mrn)
                                else:
                                    st.error(f"No patient information found for MRN {st.session_state.temp_mrn}")
                    #except:
                     #   st.warning("Please Fill Patient Information Page")

        elif st.session_state.selected_tab == "Previous Therapy for HCC":
            st.subheader("Previous Therapy for HCC")
            with st.form("previous_therapy_form"):
                if "MRN" not in st.session_state.data:
                    st.warning("Please complete the Patient Information tab first.")
                else:
                    try:
                        PRVTHER_Prior_LDT_Therapy = st.selectbox(
                        "PRVTHER_Prior_LDT_Therapy",
                        options=["Yes", "No","NA"],
                        #format_func=lambda x: f"{x} ({1 if x == 'Yes' else 0})",
                        help="Prior LDT Therapy",
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )
                        PRVTHER_Prior_RFA_Therapy = st.selectbox(
                            "PRVTHER_Prior RFA Therapy",
                            options=["Yes", "No", "NA"],
                            #format_func=lambda x: f"{x} ({1 if x == 'Yes' else 0})",
                            help="Prior RFA Therapy",
                            index=None,  # No default selection
                            placeholder="Choose an option",
                        )
                        PRVTHER_Prior_RFA_Date = 0 if PRVTHER_Prior_RFA_Therapy == 'No' else st.date_input("PRVTHER_Prior RFA Date")
                        PRVTHER_Prior_TARE_Therapy = st.selectbox(
                            "PRVTHER_Prior TARE Therapy",
                            options=["Yes", "No","NA"],
                            #format_func=lambda x: f"{x} ({1 if x == 'Yes' else 0})",
                            help="Prior TARE Therapy",
                            index=None,  # No default selection
                            placeholder="Choose an option",
                        )
                        PRVTHER_Prior_TARE_Date = 0 if PRVTHER_Prior_TARE_Therapy == 'No' else st.date_input("PRVTHER_Prior TARE Date")
                        PRVTHER_Prior_SBRT_Therapy = st.selectbox(
                            "PRVTHER_Prior SBRT Therapy",
                            options=["Yes", "No","NA"],
                            #format_func=lambda x: f"{x} ({1 if x == 'Yes' else 0})",
                            help="Prior SBRT Therapy",
                            index=None,  # No default selection
                            placeholder="Choose an option",
                        )
                        PRVTHER_Prior_SBRT_Date = 0 if PRVTHER_Prior_SBRT_Therapy == 'No' else st.date_input("PRVTHER_Prior SBRT Date")
                        PRVTHER_Prior_TACE_Therapy = st.selectbox(
                            "PRVTHER_Prior TACE Therapy",
                            options=["Yes", "No","NA"],
                            #format_func=lambda x: f"{x} ({1 if x == 'Yes' else 0})",
                            help="Prior TACE Therapy",
                            index=None,  # No default selection
                            placeholder="Choose an option",
                        )
                        PRVTHER_Prior_TACE_Date = 0 if PRVTHER_Prior_TACE_Therapy == 'No' else st.date_input("PRVTHER_Prior TACE Date")
                        PRVTHER_Prior_MWA_Therapy = st.selectbox(
                            "PRVTHER_Prior MWA Therapy",
                            options=["Yes", "No","NA"],
                            #format_func=lambda x: f"{x} ({1 if x == 'Yes' else 0})",
                            help="Prior MWA Therapy",
                            index=None,  # No default selection
                            placeholder="Choose an option",
                        )
                        PRVTHER_Prior_MWA_Date = 0 if PRVTHER_Prior_MWA_Therapy == 'No' else st.date_input("PRVTHER_Prior MWA Date")
                        PRVTHER_Resection = st.selectbox(
                            "PRVTHER_Resection",
                            options=["Yes", "No","NA"],
                            #format_func=lambda x: f"{x} ({1 if x == 'Yes' else 0})",
                            help="Prior MWA Therapy",
                            index=None,  # No default selection
                            placeholder="Choose an option",
                        )
                        PRVTHER_Resection_Date = 0 if PRVTHER_Resection == 'No' else st.date_input("PRVTHER_Resection Date")


                        list1=[PRVTHER_Prior_LDT_Therapy, PRVTHER_Prior_RFA_Therapy, PRVTHER_Prior_TARE_Therapy, PRVTHER_Prior_SBRT_Therapy, PRVTHER_Prior_TACE_Therapy, PRVTHER_Prior_MWA_Therapy, PRVTHER_Resection ]
                        sum=0
                        for item in list1:
                            if item == "Yes" :
                                sum+=1
                            else:
                                continue
                        
                        PRVTHER_Previous_Therapy_Sum = sum
                        st.write("PRVTHER_Prevtxsum ",PRVTHER_Previous_Therapy_Sum)
                    # PRVTHER_Previous_Therapy_Sum = PRVTHER_Prior_LDT_Therapy + PRVTHER_Prior_RFA_Therapy + PRVTHER_Prior_TARE_Therapy + PRVTHER_Prior_SBRT_Therapy + PRVTHER_Prior_TACE_Therapy + PRVTHER_Prior_MWA_Therapy

                        PRVTHER_NotesFT = st.text_area(
                        "PRVTHER_NotesFT",
                    
                        )

                        PRVTHER_Total_Recurrences_HCC = st.text_area(
                            "PRVTHER_Total Recurrences HCC",
                        )
                        PRVTHER_Location_of_Previous_Treatment_segments = st.selectbox(
                            "PRVTHER_Location of Previous Treatment Segments",
                            options=["1","2","3","4a","4b","5","6","7","8","NA"],
                            index=None,
                            placeholder="Choose an option"
                        )
                        PRVTHER_Location_of_Previous_Tx_segments_ft = st.text_area(
                            "PRVTHER_Location of Previous Tx Segments FT",
                          
                        )
                        PRVTHER_recurrence_location_note = st.selectbox(
                            "PRVTHER_Recurrence Location Note",
                            options=["1","2","3","4a","4b","5","6","7","8","NA"],
                            index=None,
                            placeholder="Choose an option"
                        )
                        PRVTHER_recurrence_date = st.text_area(
                            "PRVTHER_Recurrence Date",
                          
                        )
                        PRVTHER_recurrence_seg =  st.text_input(
                             "PRVTHER_Recurrence Seg"
                        )
                        PRVTHER_New_HCC_Outside_Previous_Treatment_Site = st.selectbox(
                            "PRVTHER_New HCC Outside Previous Treatment Site",
                            options = ["Yes","No","NA"],
                            help="new HCC occurrence that has developed in a diff location in the liver, separate from the area that was previously tx",
                            index=None,
                            placeholder="Choose an option"
                        )   
                        PRVTHER_New_HCC_Adjacent_to_Previous_Treatment_Site = st.selectbox(
                            "PRVTHER_New HCC Adjacent to Previous Treatment Site",
                            options = ["Yes","No","NA"],
                            help=" new HCC occurrence that has developed close to, but not directly in, the area that was previously treated",
                            index=None,
                            placeholder="Choose an option"
                        )   
                        PRVTHER_Residual_HCC_Note = st.text_area(
                            "PRVTHER_Residual HCC Note",
                            help="Provide information of Residual HCC"
                        ) 
                        PRVTHER_Residual_HCC = st.selectbox(
                            "PRVTHER_Residual HCC",
                            options = ["Yes","No","NA"],
                            help="new HCC occurrence that has developed in a diff location in the liver, separate from the area that was previously tx",
                            index=None,
                            placeholder="Choose an option"
                        )   

                        PRVTHER_Systemic_Therapy_Free_Text = st.selectbox(
                            "PRVTHER_Systemic Therapy Free Text",
                            options=["Yes", "No","NA"],
                            #format_func=lambda x: f"{x} ({1 if x == 'Yes' else 0})",
                            help="Prior TACE Therapy",
                            index=None,  # No default selection
                            placeholder="Choose an option",
                        )

                        PRVTHER_Date_of_Labs_in_Window = st.date_input(
                            "PRVTHER_Date of Labs for AFP",
                            help="select date of labs in window"
                        )

                        PRVTHER_AFP = st.number_input(
                            "PRVTHER_AFP",
                            help="Enter AFP value in ng/dl or NA",step=0.1
                        )

                        submit_tab5 = st.form_submit_button("Submit")

                        if submit_tab5:
                                
                            data5 = {
                            "PRVTHER_LDT": PRVTHER_Prior_LDT_Therapy,
                            "PRVTHER_RFA": PRVTHER_Prior_RFA_Therapy,
                            "PRVTHER_RFAdate": PRVTHER_Prior_RFA_Date.strftime("%Y-%m-%d") if PRVTHER_Prior_RFA_Date != 0 else PRVTHER_Prior_RFA_Date,
                            "PRVTHER_TARE": PRVTHER_Prior_TARE_Therapy,
                            "PRVTHER_TAREdate": PRVTHER_Prior_TARE_Date.strftime("%Y-%m-%d") if PRVTHER_Prior_TARE_Date != 0 else PRVTHER_Prior_TARE_Date,
                            "PRVTHER_SBRT": PRVTHER_Prior_SBRT_Therapy,
                            "PRVTHER_SBRTdate": PRVTHER_Prior_SBRT_Date.strftime("%Y-%m-%d") if PRVTHER_Prior_SBRT_Date != 0 else PRVTHER_Prior_SBRT_Date,
                            "PRVTHER_TACE": PRVTHER_Prior_TACE_Therapy,
                            "PRVTHER_TACEdate": PRVTHER_Prior_TACE_Date.strftime("%Y-%m-%d") if PRVTHER_Prior_TACE_Date != 0 else PRVTHER_Prior_TACE_Date,
                            "PRVTHER_MWA": PRVTHER_Prior_MWA_Therapy,
                            "PRVTHER_MWAdate": PRVTHER_Prior_MWA_Date.strftime("%Y-%m-%d") if PRVTHER_Prior_MWA_Date != 0 else PRVTHER_Prior_MWA_Date,
                            "PRVTHER_Resection": PRVTHER_Resection,
                            "PRVTHER_Resection date": PRVTHER_Resection_Date.strftime("%Y-%m-%d") if PRVTHER_Resection_Date != 0 else PRVTHER_Resection_Date,
                            "PRVTHER_Prevtxsum": PRVTHER_Previous_Therapy_Sum,
                            "PRVTHER_NotesFT": PRVTHER_NotesFT,
                            "PRVTHER_Totalrecur": PRVTHER_Total_Recurrences_HCC,
                            "PRVTHER_Locationprevtxseg": PRVTHER_Location_of_Previous_Treatment_segments,
                            "PRVTHER_Location of Previous Tx Segments FT": PRVTHER_Location_of_Previous_Tx_segments_ft,
                            "PRVTHER_RecurLocationFT": PRVTHER_recurrence_location_note,
                            "PRVTHER_RecurDate": PRVTHER_recurrence_date,
                            "PRVTHER_Recurrence Seg": PRVTHER_recurrence_seg,
                            "PRVTHER_NewHCCoutsideprevsite": PRVTHER_New_HCC_Outside_Previous_Treatment_Site,
                            "PRVTHER_NewHCCadjacentprevsite": PRVTHER_New_HCC_Adjacent_to_Previous_Treatment_Site,
                            "PRVTHER_ResidualHCCnoteFT": PRVTHER_Residual_HCC_Note,
                            "PRVTHER_ResidualHCC": PRVTHER_Residual_HCC,
                            "PRVTHER_SystemictherapyFT": PRVTHER_Systemic_Therapy_Free_Text,
                            "PRVTHER_DateAFP": PRVTHER_Date_of_Labs_in_Window.strftime("%Y-%m-%d"),
                            "PRVTHER_AFP": PRVTHER_AFP,
                            }
                            if "patient_info" in st.session_state and st.session_state.patient_info["MRN"] == st.session_state.temp_mrn:
                                st.session_state.patient_info.update(data5)
                                # Update the data in Google Sheets
                                update_google_sheet(st.session_state.patient_info, st.session_state.temp_mrn)
                            else:
                                st.error(f"No patient information found for MRN {st.session_state.temp_mrn}")
                    except:
                        st.warning("Please Fill Patient Information Page")

        elif st.session_state.selected_tab == "Pre Y90":
            st.subheader("Pre Y90")
            with st.form("pre_y90_form"):
                if "MRN" not in st.session_state.data:
                    st.warning("Please complete the Patient Information tab first.")
                else:
                    try:
                        prey90_symptoms = st.multiselect(
                        "PREY90_symptoms",
                        options=[
                            "portal vein HTN", 
                            "GI bleeding", 
                            "Limb edema", 
                            "Ischemic liver injury", 
                            "Variceal Bleeding", 
                            "Biliary Obstruction", 
                            "Infection"
                        ],
                            placeholder="Select all that apply"
                        )
                        prey90_symptoms = ", ".join(prey90_symptoms)
                        
                        prey90_date_of_labs = st.date_input("PREY90_date of labs in window", help="Enter the date of lab tests")
                        prey90_afp = st.text_input("PREY90_AFP", help="Enter AFP value in ng/dl or NA")
                        
                        def process_input(value):
                            
                # Handle the 'NA' case
                            if value.upper() == "NA":
                                return "NA"
                # Handle numeric cases
                            elif value.isdigit():
                                numeric_value = int(value)
                                return 1 if numeric_value < 200 else 2
                            else:
                                return "Invalid Input"

                        
                    
                        prey90_afp_prior_to_tare = process_input(prey90_afp)
                        
                        
                        prey90_bilirubin = st.number_input("PREY90_Bilirubin", help="Enter the bilirubin value in mg/dl",min_value=1.0,step=0.1)
                        prey90_albumin = st.number_input("PREY90_Albumin", help="Enter the albumin value in g/dl",step=0.1)
                        prey90_inr = st.number_input("PREY90_inr", help="Enter the INR value",step=0.1)
                        prey90_creatinine = st.number_input("PREY90_creatinine", help="Enter the creatinine value in mg/dl",step=0.1)
                        prey90_sodium = st.number_input("PREY90_sodium", help="Enter the sodium value in mmol/L",step=0.1)
                        prey90_ast = st.number_input("PREY90_AST", help="Enter AST value in U/L",step=0.1)
                        prey90_alt = st.number_input("PREY90_ALT", help="Enter ALT value in U/L",step=0.1)
                        prey90_alkaline_phosphatase = st.number_input("PREY90_Alkaline Phosphatase", help="Enter Alkaline Phosphatase value in U/L",step=0.1)
                        prey90_potassium = st.number_input("PREY90_potassium", help="Enter the potassium value in mmol/L",step=0.1)
                        
                        prey90_ascites_ctcae = st.selectbox (
                            "PREY90_Ascites CTCAE",
                            options=["none", "Asymptomatic","Minimal ascities/Mild abd distension","Symptomatic","moderate ascities/Symptomatic medical intervention", "Severe symptoms, invasive intervention indicated", "Life Threatening: Urgent operation intervention indicated"],
                            format_func=lambda x: {
                            "none": "0. none",
                            "Asymptomatic": "1. Asymptomatic",
                            "Minimal ascities/Mild abd distension": "1. Minimal ascities/Mild abd distension",
                            "Symptomatic": "2. Symptomatic",
                            "moderate ascities/Symptomatic medical intervention": " 2. moderate ascities/Symptomatic medical intervention",
                            "Severe symptoms, invasive intervention indicated": " 3. Severe symptoms, invasive intervention indicated",
                            "Life Threatening: Urgent operation intervention indicated" : "4. Life Threatening: Urgent operation intervention indicated",

                        }[x],
                            help="Select Metavir_score",
                            index=None,  # No default selection
                            placeholder="Choose an option",
                        ) 
                        def findascitesclass(score):
                            if score == "Asymptomatic" or score== "Minimal ascities/Mild abd distension":
                                 return 2
                            else:
                                 return 3
                        
                        prey90_ascites_classification = 1 if prey90_ascites_ctcae == "none" else findascitesclass(prey90_ascites_ctcae)
                        st.write("PREY90_AscitesCTCAEnumb ",prey90_ascites_classification)
                        prey90_ascites_free_text = st.text_area(
                            "PREY90_Ascites Free Text",
                        
                        )

                        prey90_ascites_diruetics = st.selectbox(
                            "PREY90_Ascites Diruetics",
                            options = ["Yes","No"],
                            index=None,  # No default selection
                            placeholder="Choose an option",
            
                        )
                        prey90_ascites_paracentesis = st.selectbox(
                            "PREY90_Ascites Paracentesis" ,
                            options = ["Yes","No"],
                            index=None,  # No default selection
                            placeholder="Choose an option",
            
                        )
                        prey90_ascites_hospitalization = st.selectbox(
                            "PREY90_Ascites Hospitalization",
                            options = ["Yes","No"],
                            index=None,  # No default selection
                            placeholder="Choose an option",
            
                        )

                        prey90_he_grade = st.selectbox(
                            "PREY90_HE Grade",
                            options=[1,2,3],
                            format_func=lambda x: {
                            1: "None",
                            2: "Grade 1-2",
                            3: "Grade 3-4",
                            
                        }[x],
                            index=None,  # No default selection
                            placeholder="Choose an option",

                        )
                       
                        prey90_ecog = st.selectbox("PREY90_ECOG", options=["0", "1", "2", "3", "4", "NA"],
                            index=None,  # No default selection
                            placeholder="Choose an option",)

                        
                        # Claculation of class and points
                        prey90_child_pugh_points_calc = calculatepoints(prey90_bilirubin,prey90_albumin,prey90_inr,prey90_ascites_ctcae,prey90_he_grade)
                        st.write("PREY90_CPcalc",prey90_child_pugh_points_calc)
                        prey90_child_pugh_class_calc = calculate_class(prey90_child_pugh_points_calc)
                        st.write("PREY90_CPclass",prey90_child_pugh_class_calc)
                        
                        prey90_meld_score_calc = (3.78*(int(prey90_bilirubin)))+(11.2*(int(prey90_inr)))+(9.57*(int(prey90_creatinine)))+6.43
                        st.write("PREY90_MELD",prey90_meld_score_calc)
                        prey90_meld_na_score_calc = prey90_meld_score_calc + 1.32*(137-int(prey90_sodium)) - (0.033*prey90_meld_score_calc*(137-int(prey90_sodium)))
                        st.write("PREY90_MELDNa",prey90_meld_na_score_calc)
                        prey90_albi_score_calc = albi_calc(prey90_bilirubin,prey90_albumin)
                        st.write("PREY90_Albiscore",prey90_albi_score_calc)
                        prey90_albi_grade = albi_class(prey90_albi_score_calc)
                        st.write("PREY90_Albigrade",prey90_albi_grade)

                        prey90_bclc_calc = st.text_area("PREY90_BCLC Stage calc")

                    
                        st.subheader("Mapping Y90")
                        my90_date = st.date_input("MY90_date", help="Enter the date")
                        my90_lung_shunt = st.number_input("MY90_Lung_shunt", min_value=0.0, step=0.1, help="Enter the lung shunt value")

                        submit_tab6 = st.form_submit_button("Submit")

                        if submit_tab6:

                            data6 = {
                            "PREY90_sx": prey90_symptoms,
                            "PREY90_Datelabs": prey90_date_of_labs.strftime("%Y-%m-%d"),
                            "PREY90_AFP": prey90_afp,
                            "PRE90_AFPbinary": prey90_afp_prior_to_tare,
                            "PREY90_Bilirubin": prey90_bilirubin,
                            "PREY90_Albumin": prey90_albumin,
                            "PREY90_INR": prey90_inr,
                            "PREY90_Creatinine": prey90_creatinine,
                            "PREY90_Sodium": prey90_sodium,
                            "PREY90_AST": prey90_ast,
                            "PREY90_ALT": prey90_alt,
                            "PREY90_Alkaline Phosphatase": prey90_alkaline_phosphatase,
                            "PREY90_Potassium": prey90_potassium,
                            "PREY90_AscitesCTCAE": prey90_ascites_ctcae,
                            "PREY90_AscitesCTCAEnumb": prey90_ascites_classification,
                            "PREY90_AscitesFT": prey90_ascites_free_text,
                            "PREY90_Ascitesdiruetics": prey90_ascites_diruetics,
                            "PREY90_Ascitesparacentesis": prey90_ascites_paracentesis,
                            "PREY90_Asciteshospitalization": prey90_ascites_hospitalization,
                            "PREY90_HEgrade": prey90_he_grade,
                            "PREY90_ECOG": prey90_ecog,
                            "PREY90_CPclass": prey90_child_pugh_class_calc,
                            "PREY90_CPcalc": prey90_child_pugh_points_calc,
                            "PREY90_MELD": prey90_meld_score_calc,
                            "PREY90_MELDNa": prey90_meld_na_score_calc,
                            "PREY90_Albiscore": prey90_albi_score_calc,
                            "PREY90_Albigrade": prey90_albi_grade,
                            "PREY90_BCLC": prey90_bclc_calc,
                            "MY90_date": my90_date.strftime("%Y-%m-%d"),
                            "MY90_Lung_shunt": my90_lung_shunt,
                            }
                            
                            if "patient_info" in st.session_state and st.session_state.patient_info["MRN"] == st.session_state.temp_mrn:
                                st.session_state.patient_info.update(data6)
                                # Update the data in Google Sheets
                                update_google_sheet(data6, st.session_state.temp_mrn)
                            else:
                                st.error(f"No patient information found for MRN {st.session_state.temp_mrn}")
                    except:
                        st.warning("Please Fill Patient Information Page")
        
        elif st.session_state.selected_tab == "Day_Y90":
            st.subheader("Day_Y90")
            with st.form("day_y90_form"):
                if "MRN" not in st.session_state.data:
                    st.warning("Please complete the Patient Information tab first.")
                else:
                    try:
                        dayy90_afp = st.text_input("DAYY90_AFP")
                        def process_input(value):
                            
                # Handle the 'NA' case
                            if value.upper() == "NA":
                                return "NA"
                # Handle numeric cases
                            elif value.isdigit():
                                numeric_value = int(value)
                                return 1 if numeric_value < 200 else 2
                            else:
                                return "Invalid Input"

                        dayy90_afp_prior_to_tare = process_input(dayy90_afp)
                        st.write("DAYY90_AFP Binary",dayy90_afp_prior_to_tare)
                        if hasattr(st.session_state, 'temp_mrn'):
                            prey90_afp_binarydup = get_variable_value(st.session_state.temp_mrn,"PRE90_AFPbinary")
                            st.write("PRE90_AFP BinaryDup",prey90_afp_binarydup)
                        dayy90_sodium = st.number_input("DAYY90_sodium",step=0.1)
                        dayy90_creatinine = st.number_input("DAYY90_creatinine",step=0.1)
                        dayy90_inr = st.number_input("DAYY90_inr",step=0.1)
                        dayy90_albumin = st.number_input("DAYY90_albumin",step=0.1)
                        dayy90_bilirubin = st.number_input("DAYY90_bilirubin",min_value=1.0,step=0.1)
                        dayy90_ast = st.number_input("DAYY90_AST",step=0.1)
                        dayy90_alt = st.number_input("DAYY90_ALT",step=0.1)
                        dayy90_alkaline_phosphatase = st.number_input(
                            "DAYY90_Alkaline Phosphatase",step=0.1
                        )
                        dayy90_leukocytes = st.number_input("DAYY90_leukocytes",step=0.1)
                        dayy90_platelets = st.number_input("DAYY90_platelets",step=0.1)
                        dayy90_potassium = st.number_input("DAY90_Potassium",step=0.1)

                        dayy90_ascites_ctcae = st.selectbox (
                            "DAYY90_Ascites CTCAE",
                            options=["none", "Asymptomatic","Minimal ascities/Mild abd distension","Symptomatic","moderate ascities/Symptomatic medical intervention", "Severe symptoms, invasive intervention indicated", "Life Threatening: Urgent operation intervention indicated"],
                            format_func=lambda x: {
                            "none": "0. none",
                            "Asymptomatic": "1. Asymptomatic",
                            "Minimal ascities/Mild abd distension": "1. Minimal ascities/Mild abd distension",
                            "Symptomatic": "2. Symptomatic",
                            "moderate ascities/Symptomatic medical intervention": " 2. moderate ascities/Symptomatic medical intervention",
                            "Severe symptoms, invasive intervention indicated": " 3. Severe symptoms, invasive intervention indicated",
                            "Life Threatening: Urgent operation intervention indicated" : "4. Life Threatening: Urgent operation intervention indicated",

                        }[x],
                            help="Select Metavir_score",
                            index=None,  # No default selection
                            placeholder="Choose an option",
                        ) 
                        def findascitesclass(score):
                            if score == "Asymptomatic" or score== "Minimal ascities/Mild abd distension":
                                 return 2
                            else:
                                 return 3
                        
                        dayy90_ascites_classification = 1 if dayy90_ascites_ctcae == "none" else findascitesclass(dayy90_ascites_ctcae)
                        st.write("Day90_AscitesCTCAEnumb",dayy90_ascites_classification)
                        dayy90_he_grade = st.selectbox(
                            "DAYY90_HE Grade",
                            options=[1,2,3],
                            format_func=lambda x: {
                            1: "None",
                            2: "Grade 1-2",
                            3: "Grade 3-4",
                            
                        }[x],
                            index=None,  # No default selection
                            placeholder="Choose an option",
                        )
                       
                        dayy90_ecog = st.selectbox("DAYY90_ECOG", options=["0", "1", "2", "3", "4", "NA"],
                            index=None,  # No default selection
                            placeholder="Choose an option",)
                        
                        dayy90_child_pugh_points_calc = calculatepoints(dayy90_bilirubin,dayy90_albumin,dayy90_inr,dayy90_ascites_ctcae,dayy90_he_grade)
                        st.write("DAYY90_CPcalc",dayy90_child_pugh_points_calc)
                        dayy90_child_pugh_class_calc = calculate_class(dayy90_child_pugh_points_calc)
                        st.write("DAYY90_CPclass",dayy90_child_pugh_class_calc)
                        dayy90_meld_score_calc = (3.78*(int(dayy90_bilirubin)))+(11.2*(int(dayy90_inr)))+(9.57*(int(dayy90_creatinine)))+6.43
                        st.write("DAYY90_MELD",dayy90_meld_score_calc)
                        dayy90_meld_na_score_calc = dayy90_meld_score_calc + 1.32*(137-int(dayy90_sodium)) - (0.033*dayy90_meld_score_calc*(137-int(dayy90_sodium)))
                        st.write("DAYY90_MELDNa",dayy90_meld_na_score_calc)
                        dayy90_albi_score_calc = albi_calc(dayy90_bilirubin,dayy90_albumin)
                        st.write("DAYY90_Albiscore",dayy90_albi_score_calc)
                        dayy90_albi_grade = albi_class(dayy90_albi_score_calc)
                        st.write("DAYY90_Albigrade",dayy90_albi_grade)
                        dayy90_bclc_calc = st.text_area("PREY90_BCLC Stage calc")


                        dayy90_type_of_sphere = st.selectbox(
                            "DAYY90_Type of Sphere", options=["Therasphere-1", "SIR-2"],
                            index=None,  # No default selection
                            placeholder="Choose an option",
                        )

                        dayy90_lt_notes_ftx = st.text_area("DAYY90_LT Notes Free Text")

                        ken_childpughscore = st.selectbox(
                            "ken_ChildPughscore",
                            options=["A","B","C"],
                            index=None,  # No default selection
                            placeholder="Choose an option",
                        )
                        ken_meldpretare = st.number_input("ken_MELDpreTARE",step=0.1)


                    # Submit button
                        submit_tab7 = st.form_submit_button("Submit")
                    
                        if submit_tab7:
                            data7 = {
                                "DAYY90_AFP": dayy90_afp,
                                "DAYY90_AFP Binary": dayy90_afp_prior_to_tare,
                                "PRE90_AFP BinaryDup": prey90_afp_binarydup,
                                "DAYY90_Sodium": dayy90_sodium,
                                "DAYY90_Creatinine": dayy90_creatinine,
                                "DAYY90_INR": dayy90_inr,
                                "DAYY90_Albumin": dayy90_albumin,
                                "DAYY90_Bilirubin": dayy90_bilirubin,
                                "DAYY90_AST": dayy90_ast,
                                "DAYY90_ALT": dayy90_alt,
                                "DAYY90_Alkphos": dayy90_alkaline_phosphatase,
                                "DAYY90_Leukocytes": dayy90_leukocytes,
                                "DAYY90_Platelets": dayy90_platelets,
                                "DAY90_Potassium": dayy90_potassium,
                                "Day90_AscitesCTCAE": dayy90_ascites_ctcae,
                                "Day90_AscitesCTCAEnumb": dayy90_ascites_classification,
                                "Day90_HEgrade": dayy90_he_grade,
                                "PREY90_ECOG": dayy90_ecog,
                                "DAYY90_CPclass": dayy90_child_pugh_class_calc,
                                "DAYY90_CPcalc": dayy90_child_pugh_points_calc,
                                "DAYY90_MELD": dayy90_meld_score_calc,
                                "DAYY90_MELDNa": dayy90_meld_na_score_calc,
                                "DAYY90_Albiscore": dayy90_albi_score_calc,
                                "DAYY90_Albigrade": dayy90_albi_grade,
                                "DAYY90_BCLC": dayy90_bclc_calc,
                                "DAYY90_Sphere": dayy90_type_of_sphere,
                                "DAYY90_LTnoteFT": dayy90_lt_notes_ftx,
                                "ken_ChildPughscore": ken_childpughscore,
                                "ken_MELDpreTARE (MELDpreTARE)": ken_meldpretare,
                                }
                            if "patient_info" in st.session_state :
                                update_google_sheet(data7, st.session_state.temp_mrn)
                            else:
                                st.error(f"No patient information found for MRN {st.session_state.temp_mrn}")
                    except:
                        st.warning("Please Fill Patient Information Page")
        
        elif st.session_state.selected_tab == "Post Y90 Within 30 Days Labs":
            st.subheader("Post Y90 Within 30 Days Labs")
            with st.form("post_y90_form"):
                if "MRN" not in st.session_state.data:
                    st.warning("Please complete the Patient Information tab first.")
                else:
                    try:
                        posty90_date_labs = st.date_input("POSTY90_30DY_date_labs", help="Enter the date of lab tests")
                        posty90_afp = st.text_input("POSTY90_30DY_afp", help="Enter AFP value in ng/dl or NA")
                        posty90_afp_date = st.date_input("POSTY90_30DY_afp DATE", help="Enter the date for AFP")
                        posty90_sodium = st.number_input("POSTY90_30DY_Sodium", help="Enter the sodium value in mmol/L",step=0.1)
                        posty90_creatinine = st.number_input("POSTY90_30DY_creatinine", help="Enter the creatinine value in mg/dl",step=0.1)
                        posty90_inr = st.number_input("POSTY90_30DY_INR", help="Enter the INR value",step=0.1)
                        posty90_albumin = st.number_input("POSTY90_30DY_albumin", help="Enter the albumin value in g/dl",step=0.1)
                        posty90_bilirubin = st.number_input("POSTY90_30DY_bilirubin", help="Enter the bilirubin value in mg/dl",min_value=1.0,step=0.1)
                        posty90_ast = st.number_input("POSTY90_30DY_AST", help="Enter AST value in U/L",step=0.1)
                        posty90_alt = st.number_input("POSTY90_30DY_ALT", help="Enter ALT value in U/L",step=0.1)
                        posty90_alkaline_phosphatase = st.number_input("POSTY90_30DY_Alkaline Phosphatase", help="Enter Alkaline Phosphatase value in U/L",step=0.1)
                        posty90_leukocytes = st.number_input("POSTY90_30DY_leukocytes", help="Enter leukocytes value in x10^3/µL",step=0.1)
                        posty90_platelets = st.number_input("POSTY90_30DY_platelets", help="Enter platelets value in x10^3/µL",step=0.1)
                        posty90_potassium = st.number_input("POSTY90_30DY_potassium", help="Enter the potassium value in mmol/L",step=0.1)
                        
                        posty90_ascites_ctcae = st.selectbox (
                        "30DY_AE_AscitesCTCAE",
                        options=["none", "Asymptomatic","Minimal ascities/Mild abd distension","Symptomatic","moderate ascities/Symptomatic medical intervention", "Severe symptoms, invasive intervention indicated", "Life Threatening: Urgent operation intervention indicated"],
                        format_func=lambda x: {
                        "none": "0. none",
                        "Asymptomatic": "1. Asymptomatic",
                        "Minimal ascities/Mild abd distension": "1. Minimal ascities/Mild abd distension",
                        "Symptomatic": "2. Symptomatic",
                        "moderate ascities/Symptomatic medical intervention": " 2. moderate ascities/Symptomatic medical intervention",
                        "Severe symptoms, invasive intervention indicated": " 3. Severe symptoms, invasive intervention indicated",
                        "Life Threatening: Urgent operation intervention indicated" : "4. Life Threatening: Urgent operation intervention indicated",

                        }[x],
                            help="Select Metavir_score",
                            index=None,  # No default selection
                            placeholder="Choose an option",
                        ) 
                        def findascitesclass(score):
                            if score == "Asymptomatic" or score== "Minimal ascities/Mild abd distension":
                                    return 2
                            else:
                                    return 3
                        
                        posty90_ascites_classification = 1 if posty90_ascites_ctcae == "none" else findascitesclass(posty90_ascites_ctcae)

                        posty90_ascites_diruetics = st.selectbox(
                            "30DY_AE_Ascitesdiruetics",
                            options = ["Yes","No"],
                            index=None,  # No default selection
                            placeholder="Choose an option",
            
                        )
                        posty90_ascites_paracentesis = st.selectbox(
                            "30DY_AE_Ascitesparacentesis" ,
                            options = ["Yes","No"],
                            index=None,  # No default selection
                            placeholder="Choose an option",
            
                        )
                        posty90_ascites_hospitalization = st.selectbox(
                            "30DY_AE_Asciteshospitalization",
                            options = ["Yes","No"],
                            index=None,  # No default selection
                            placeholder="Choose an option",
            
                        )
                        posty90_he_grade = st.selectbox(
                            "30DY_AE_HE Grade",
                            options=[1,2,3],
                            format_func=lambda x: {
                            1: "None",
                            2: "Grade 1-2",
                            3: "Grade 3-4",
                            
                        }[x],
                            index=None,  # No default selection
                            placeholder="Choose an option",

                        )

                        posty90_ascites_free_text = st.text_area(
                            "30DY_AE_ascities_freetext",
                        
                        )

                        posty90_ecog = st.selectbox("POSTY90_30DY_ECOG", options=["0", "1", "2", "3", "4", "NA"],
                            index=None,  # No default selection
                            placeholder="Choose an option",
                            )
                        
                        posty90_child_pugh_class = st.selectbox(
                            "POSTY90_30DY_Child-Pugh Class calc",
                            options=["Class A", "Class B", "Class C", "NA"],
                            help="Select the Child-Pugh class",
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )

                        inputp90 = st.text_input(
                            "POSTY90_30DY_Child-Pugh Points calc",
                            help="Write in number in range 5-15, or NA"
                        )
                        posty90_child_pugh_points = validate_input(inputp90)

                        posty90_bclc = st.selectbox(
                            "POSTY90_30DY_BCLC stage",
                            options=["0", "A", "B", "C", "D"],
                            help="Select the BCLC stage",
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )

                        input_meld = st.text_input(
                            "POSTY90_30DY_MELD EMR",
                            help="Write in number in range 6-40, or NA"
                        )
                        posty90_meld = validate_input2(input_meld)


                        input_meld_na = st.text_input(
                            "POSTY90_30DY_MELD Na EMR",
                            help="Write in number in range 6-40, or NA"
                        )
                        posty90_meld_na = validate_input2(input_meld_na)

                        posty90_albi_score = st.number_input(
                            "POSTY90_30DY_ALBI Score calc",
                            help="Enter ALBI score",step=0.1
                        )
                        posty90_albi_grade = albi_class(posty90_albi_score)

                    
                        ken_bclc_stage_post90 = st.text_input(
                            "Ken_BCLCStagepost90",
                            help="Enter BCLC Stage Post-90"
                        )

                        ken_meld_stage_post90 = st.text_input(
                            "Ken_MELD_Stagepost90",
                            help="Enter MELD Score Pre-TARE"
                        )
                        ## New Part
                        st.subheader("Post_Y90_within_30_days_adverse_events")
                        DYAE_CTCAE_portal_htn = st.selectbox(
                            "30DYAE_portal_htn CTCAE",
                            options=["0","1","2","3","4","5"],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )
                        DYAE_CTCAE_Vascular_comp = st.selectbox(
                            "30DYAE_Vascular comp CTCAE",
                            options=["0","1","2","3","4","5"],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )
                        DYAE_CTCAE_fatigue = st.selectbox(
                            "30DYAE_fatigue CTCAE",
                            options=["0","1","2"],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )
                        DYAE_CTCAE_diarrhea = st.selectbox(
                            "30DYAE_diarrhea CTCAE",
                            options=["0","1","2","3","4","5"],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )

                        DYAE_CTCAE_hypoalbuminemia_emr = st.text_input(
                            "30DYAE_hypoalbuminemia CTCAE"
                        )
                        DYAE_CTCAE_hyperbilirubinemia_emr = st.text_input(
                            "30DYAE_hyperbilirubinemia CTCAE"
                        )
                        DYAE_CTCAE_Increase_creatinine_emr = st.text_input(
                            "30DYAE_Increase_creatinine CTCAE"
                        )
                        DYAE_CTCAE_abdominal_pain = st.selectbox(
                            "30DYAE_abdominal pain CTCAE",
                            options=["0","1","2","3"],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )
                        DYAE_CTCAE_sepsis = st.selectbox(
                            "30DYAE_sepsis CTCAE",
                            options=["0","3","4","5"],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )
                        
                        DYAE_CTCAE_bacterial_peritonitis = st.selectbox(
                            "30DYAE_CTCAE_bacterial_peritonitis",
                            options=["0", "3", "4", "5"],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )

                        DYAE_CTCAE_hemorrhage = st.selectbox(
                        "30DYAE_CTCAE_hemorrhage",
                        options=["0", "3", "4", "5"],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )

                        DYAE_CTCAE_anorexia = st.selectbox(
                            "30DYAE_CTCAE_anorexia",
                            options=["0", "1", "2", "3"],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )

                        DYAE_CTCAE_intrahepatic_fistula = st.selectbox(
                            "30DYAE_CTCAE_intrahepatic_fistula",
                            options=["0","2", "3", "4", "5"],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )

                        DYAE_CTCAE_constipation = st.selectbox(
                            "30DYAE_CTCAE_constipation",
                            options=["0", "1", "2", "3"],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )

                        DYAE_CTCAE_nausea = st.selectbox(
                            "30DYAE_CTCAE_nausea",
                            options=["0", "1", "2", "3"],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )

                        DYAE_CTCAE_vomiting = st.selectbox(
                            "30DYAE_CTCAE_vomiting",
                            options=["0","1","2", "3", "4", "5"],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )

                        DYAE_CTCAE_cholecystitis = st.selectbox(
                            "30DYAE_CTCAE_cholecystitis",
                            options=["0", "2","3", "4", "5"],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )

                        DYAE_CTCAE_gastric_ulcers = st.selectbox(
                            "30DYAE_CTCAE_gastric_ulcers",
                            options=["0","1","2", "3", "4", "5"],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )

                        DYAE_CTCAE_hyperkalemia = st.selectbox(
                            "30DYAE_CTCAE_hyperkalemia",
                            options=["NA"],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )

                        DYAE_CTCAE_respiratory_failure = st.selectbox(
                            "30DYAE_CTCAE_respiratory_failure",
                            options=["0", "4", "5"],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )

                        DYAE_CTCAE_AKI = st.selectbox(
                            "30DYAE_CTCAE_AKI",
                            options=["0", "3", "4", "5"],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )

                        DYAE_CTCAE_Radiation_pneumonitis = st.selectbox(
                            "30DYAE_CTCAE_Radiation_pneumonitis",
                            options=["0","1","2", "3", "4", "5"],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )

                        DYAE_AE_other = st.text_area(
                            "30DY_AE_other",
                            help="Other Adverse Events (Free Text)"
                        )

                        DYAE_AE_date_of_AE = st.text_input(
                            "90DY_AE_date_of_AE",
                            help="(if AE is present after 30 days but before 90 write it here and the date)"
                        )
                        ken_grandedtoxicity = st.text_area(
                            "Ken_GradeandToxicity",

                        )
                        dy_ae_hospitalization_3 = st.selectbox(
                            "90DY_AE_Hospitalization 3 months",
                            options=["Yes","No"],
                            index=None,  # No default selection
                        placeholder="Choose an option",
                        )
                        dy_ae_hospitalization_6 = st.selectbox(
                            "90DY_AE_Hospitalization 6 months",
                            options=["Yes","No"],
                            index=None,  # No default selection
                        placeholder="Choose an option",
                        )
                        dy_ae_hosp6mo = st.selectbox(
                            "90DY_AE_Hosp6mo",
                            options=["Yes","No"],
                            index=None,  # No default selection
                        placeholder="Choose an option",
                        )
                        dy_ae_death_due = st.selectbox(
                            "90DY_AE_Death due to AE",
                            options=["Yes","No"],
                            index=None,  # No default selection
                        placeholder="Choose an option",
                        )


                        submit_tab8 = st.form_submit_button("Submit")

                        if submit_tab8:
                                
                                data8={
                                    "POSTY90_30DY_Datelabs": posty90_date_labs.strftime("%Y-%m-%d"),
                                    "POSTY90_30DY_AFP": posty90_afp,
                                    "POSTY90_30DY_AFPdate": posty90_afp_date.strftime("%Y-%m-%d"),
                                    "POSTY90_30DY_Sodium": posty90_sodium,
                                    "POSTY90_30DY_Creatinine": posty90_creatinine,
                                    "POSTY90_30DY_INR": posty90_inr,
                                    "POSTY90_30DY_Albumin": posty90_albumin,
                                    "POSTY90_30DY_Bilirubin": posty90_bilirubin,
                                    "POSTY90_30DY_AST": posty90_ast,
                                    "POSTY90_30DY_ALT": posty90_alt,
                                    "POSTY90_30DY_ALP": posty90_alkaline_phosphatase,
                                    "POSTY90_30DY_Leukocytes": posty90_leukocytes,
                                    "POSTY90_30DY_Platelets": posty90_platelets,
                                    "POSTY90_30DY_Potassium": posty90_potassium,
                                    "30DY_AE_AscitesCTCAE": posty90_ascites_ctcae,
                                    "30DY_AE_AscitesCTCAEnumb": posty90_ascites_classification,
                                    "30DY_AE_Ascitesdiruetics": posty90_ascites_diruetics,
                                    "30DY_AE_Ascitesparacentesis": posty90_ascites_paracentesis,
                                    "30DY_AE_Asciteshospitalization": posty90_ascites_hospitalization,
                                    "30DY_AE_HEgrade": posty90_he_grade,
                                    "30DY_AE_ascities_freetext": posty90_ascites_free_text,
                                    "POSTY90_30DY_ECOG": posty90_ecog,
                                    "POSTY90_30DY_CPclass": posty90_child_pugh_class,
                                    "POSTY90_30DY_CPcalc": posty90_child_pugh_points,
                                    "POSTY90_30DY_MELD": posty90_meld,
                                    "POSTY90_30DY_MELDNa": posty90_meld_na,
                                    "POSTY90_30DY_ALBIscore": posty90_albi_score,
                                    "POSTY90_30DY_ALBIgrade": posty90_albi_grade,
                                    "POSTY90_30DY_BCLC": posty90_bclc,
                                    "Ken_BCLCStagepost90": ken_bclc_stage_post90,
                                    "Ken_MELD_Stagepost90": ken_meld_stage_post90,
                                    "30DY_AE_Portalhtn": DYAE_CTCAE_portal_htn,
                                    "30DY_AE_Vascularcomp": DYAE_CTCAE_Vascular_comp,
                                    "30DY_AE_Fatigue": DYAE_CTCAE_fatigue,
                                    "30DY_AE_Diarrhea": DYAE_CTCAE_diarrhea,
                                    "30DY_AE_Hypoalbuminemia": DYAE_CTCAE_hypoalbuminemia_emr,
                                    "30DY_AE_Hyperbilirubinemia": DYAE_CTCAE_hyperbilirubinemia_emr,
                                    "30DY_AE_Increasecreatine": DYAE_CTCAE_Increase_creatinine_emr,
                                    "30DY_AE_Abdominalpain": DYAE_CTCAE_abdominal_pain,
                                    "30DY_AE_Sepsis": DYAE_CTCAE_sepsis,
                                    "30DY_AE_BacterialPer": DYAE_CTCAE_bacterial_peritonitis,
                                    "30DY_AE_Hemorrhage": DYAE_CTCAE_hemorrhage,
                                    "30DY_AE_Anorexia": DYAE_CTCAE_anorexia,
                                    "30DY_AE_Intrahepaticfistula": DYAE_CTCAE_intrahepatic_fistula,
                                    "30DY_AE_Constipation": DYAE_CTCAE_constipation,
                                    "30DY_AE_Nausea": DYAE_CTCAE_nausea,
                                    "30DY_AE_Vomiting": DYAE_CTCAE_vomiting,
                                    "30DY_AE_Cholecystitis": DYAE_CTCAE_cholecystitis,
                                    "30DY_AE_Gastriculcer": DYAE_CTCAE_gastric_ulcers,
                                    "30DY_AE_Hyperkalemia": DYAE_CTCAE_hyperkalemia,
                                    "30DY_AE_Respfailure": DYAE_CTCAE_respiratory_failure,
                                    "30DY_AE_AKI": DYAE_CTCAE_AKI,
                                    "30DY_AE_Radiationpneumonitis": DYAE_CTCAE_Radiation_pneumonitis,
                                    "30DY_AE_Other": DYAE_AE_other,
                                    "90DY_AE_DateofAE": DYAE_AE_date_of_AE,
                                    "Additional Notes FT": ken_grandedtoxicity,
                                    "90DY_AE_Hosp3mo": dy_ae_hospitalization_3,
                                    "90DY_AE_Datehosp3mo": dy_ae_hospitalization_6,
                                    "90DY_AE_Hosp6mo": dy_ae_hosp6mo,
                                    "90DY_AE_DeathduetoAE": dy_ae_death_due
                                }
                            
                                if "patient_info" in st.session_state:
                                    update_google_sheet(data8, st.session_state.temp_mrn)
                                else:
                                    st.error(f"No patient information found for MRN {st.session_state.temp_mrn}")
                    except:
                        st.warning("Please Fill Patient Information Page")
        
        elif st.session_state.selected_tab == "Other Post Tare":
            st.subheader("Other_post_TARE")
            with st.form("other_post_tare_form"):
                if "MRN" not in st.session_state.data:
                    st.warning("Please complete the Patient Information tab first.")
                else:
                    try:
                        oc_liver_transplant = st.radio("OC_Liver_transplant", options=["Yes", "No"])
                        oc_liver_transplant_date = st.date_input("OC_Liver_transplant_date")

                        st.subheader("K_other")
            # with st.form("k_other_form"):

                        k_ken_toxgtg3 = st.number_input("K_ken_ToxgtG3",step=0.1)
                        if k_ken_toxgtg3 > 3:
                            k_ken_toxgtg3 = 1
                        else:
                            k_ken_toxgtg3 =0
                                        
                        k_ken_toxgtg2 = st.number_input("K_ken_ToxgtG2",step=0.1)
                        if k_ken_toxgtg2 > 2:
                            k_ken_toxgtg2 = 1
                        else:
                            k_ken_toxgtg2 =0

                        def albigrade(intx):
                            if intx <= -2.60:
                                return "Grade 1"
                            elif -2.60 < intx <= -1.39:
                                return "Grade 2"
                            else:
                                return "Grade 3"
                        try : 
                            prey90_bilirubin = get_variable_value(st.session_state.temp_mrn,"PREY90_Bilirubin")
                            prey90_albumin = get_variable_value(st.session_state.temp_mrn,"PREY90_Albumin")
                                    
                            k_ken_albipretareraw = albi_calc(prey90_bilirubin,prey90_albumin)
                            st.write("K_ken_AlbiPreTARERaw : ", k_ken_albipretareraw)
                            k_ken_albipretaregrade = albigrade(k_ken_albipretareraw)
                            st.write("K_ken_AlbiPreTAREGrade: ",k_ken_albipretaregrade)
                        except:
                            st.warning("Fill Pre Y90 Tab")
                        
                        try :
                            posty90_bilirubin = get_variable_value(st.session_state.temp_mrn,"POSTY90_30DY_Bilirubin")
                            posty90_albumin = get_variable_value(st.session_state.temp_mrn,"POSTY90_30DY_Albumin")
                            
                            k_ken_albiposttareraw = albi_calc(posty90_bilirubin,posty90_albumin)
                            st.write("K_ken_AlbiPostTARERaw : ", k_ken_albiposttareraw)
                            k_ken_albiposttaregrade = albigrade(k_ken_albiposttareraw)
                            st.write("K_ken_AliPostTAREGrade : ", k_ken_albiposttaregrade)
                        except :
                            st.warning("Fill Post 90 Form")

                        submit_tab9 = st.form_submit_button("Submit")

                        if submit_tab9:
                            
                            data9={
                                "OC_Liver_transplant": oc_liver_transplant,
                                "OC_Liver_transplant_date": oc_liver_transplant_date.strftime("%Y-%m-%d"),
                                "K_ken_ToxgtG3": k_ken_toxgtg3,
                                "K_ken_ToxgtG2": k_ken_toxgtg2,
                                "K_ken_AlbiPreTARERaw": k_ken_albipretareraw,
                                "K_ken_AlbiPreTAREGrade": k_ken_albipretaregrade,
                                "K_ken_AlbiPostTARERaw": k_ken_albiposttareraw,
                                "K_ken_AliPostTAREGrade": k_ken_albiposttaregrade
                                }
                            if "patient_info" in st.session_state:
                               
                                # Update the data in Google Sheets
                                update_google_sheet(data9, st.session_state.temp_mrn)
                            else:
                                st.error(f"No patient information found for MRN {st.session_state.temp_mrn}")
                    except:
                           st.warning("Please Fill Patient Information Page")
        
        elif st.session_state.selected_tab == "Imaging Date":
            st.subheader("Imaging Date")
            with st.form("imaging_date_form"):
                try:
                    if "MRN" not in st.session_state.data:
                        st.warning("Please complete the Patient Information tab first.")
                    else:
                        st.subheader("Imaging PreY90")
                        
                        PREY90_prescan_modality = st.selectbox(
                                "PREY90_prescan_modality",
                                options=["CT","MRI"],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )
                        PREY90_Imaging_Date = st.date_input("PREY90_Imaging Date")
                        PREY90_total_number_of_lesions = st.selectbox(
                                "PREY90_total number of lesions",
                                options=["1","2",">3"],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )
                        PREY90_Number_Involved_Lobes = st.selectbox(
                                "PREY90_Number Involved Lobes",
                                options=["Unilobar","Bilobar"],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )
                        PREY90_target_lesion_1_segments = st.multiselect(
                                "PREY90_target_lesion_1_segments",
                                options=["1","2","3","4a","4b","5","6","7","8","NA"],
                                placeholder="Select all that apply"
                        
                        )
                        PREY90_target_lesion_1_segments = ", ".join(PREY90_target_lesion_1_segments)
                        PREY90_TL1_LAD = st.number_input(
                            "PREY90_TL1_LAD",
                            step=0.1
                        )

                        PREY90_Target_Lesion_1_PAD = st.number_input(
                            "PREY90_Target Lesion 1 PAD",
                            step=0.1
                        )

                        PREY90_Target_Lesion_1_CCD = st.number_input(
                            "PREY90_Target Lesion 1 CCD",
                            step=0.1
                        )
                        PREY90_Target_Lesion_1_VOL = 4/3*3.14*(PREY90_Target_Lesion_1_PAD)*(PREY90_TL1_LAD)*PREY90_Target_Lesion_1_CCD
                        st.write("PREY90_Target Lesion 1 VOL",PREY90_Target_Lesion_1_VOL)
                        PREY90_Target_Lesion_2_segments = st.selectbox(
                                "PREY90_Target_Lesion_2_segments",
                                options=["1","2","3","4a","4b","5","6","7","8","NA"],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )
                        PREY90_Target_Lesion_2_LAD = st.number_input(
                            "PREY90_Target_Lesion_2_LAD",
                            step=0.1
                        )
                        PREY90_Target_Lesion_2_PAD = st.number_input(
                            "PREY90_Target Lesion 2 PAD",
                            step=0.1
                        )

                        PREY90_Target_Lesion_2_CCD = st.number_input(
                            "PREY90_Target Lesion 2 CCD",
                            step=0.1
                        )
                        PREY90_Target_Lesion_2_VOL = 4/3*3.14*(PREY90_Target_Lesion_2_PAD)*(PREY90_Target_Lesion_2_LAD)*PREY90_Target_Lesion_2_CCD
                        st.write("PREY90_Target Lesion 2 VOL",PREY90_Target_Lesion_2_VOL)
                        PREY90_pretx_targeted_Lesion_Dia_Sum = max(PREY90_TL1_LAD,PREY90_Target_Lesion_1_PAD,PREY90_Target_Lesion_1_CCD)+max(PREY90_Target_Lesion_2_PAD,PREY90_Target_Lesion_2_LAD,PREY90_Target_Lesion_2_CCD)
                        st.write("PREY90_ pretx targeted Lesion Dia Sum",PREY90_pretx_targeted_Lesion_Dia_Sum)
                        PREY90_Non_Target_Lesion_Location = st.selectbox( "PREY90_Non-Target Lesion Location" , options=["1","2","3","4a","4b","5","6","7","8","NA"],
                        index=None,  # No default selection
                        placeholder="Choose an option",)

                        PREY90_Non_Target_Lesion_2_LAD_Art_Enhanc = st.number_input(
                            "PREY90_Non_Target_Lesion_2_LAD_Art_Enhanc",
                            step=0.1
                        )
                        PREY90_Non_Target_Lesion_2_PAD_Art_Enhanc = st.number_input(
                            "PREY90_Non_Target_Lesion_2_PAD_Art_Enhanc",
                            step=0.1
                        )

                        PREY90_Non_Target_Lesion_2_CCD_Art_Enhanc = st.number_input(
                            "PREY90_Non_Target_Lesion_2_CCD_Art_Enhanc",
                            step=0.1
                        )
                        PREY90_Non_targeted_Lesion_Dia_Sum = max(PREY90_Non_Target_Lesion_2_PAD_Art_Enhanc,PREY90_Non_Target_Lesion_2_LAD_Art_Enhanc,PREY90_Non_Target_Lesion_2_CCD_Art_Enhanc)
                        st.write("PREY90_Non-targeted Lesion Dia Sum",PREY90_Non_targeted_Lesion_Dia_Sum)
                        PREY90_Reviewers_Initials = st.text_input(
                            "PREY90_Reviewers Initials",
                            help="Free-text input for reviewer name"
                        )

                        PREY90_Pre_Y90_Extrahepatic_Disease = st.selectbox(
                            "PREY90_Pre Y90 Extrahepatic Disease",
                            options=["Yes", "No", "NA"],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )

                        PREY90_Pre_Y90_Extrahepatic_Disease_Location = st.text_input(
                            "PREY90_Pre Y90 Extrahepatic Disease Location",
                            help="Free Text"
                        )

                        PREY90_PVT = st.selectbox(
                            "PREY90_PVT",
                            options=["Yes", "No", "NA"],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )

                        PREY90_PVT_Location = st.selectbox(
                            "PREY90_PVT Location",
                            options=["RPV", "LPV"],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )

                        PREY90_Features_of_cirrhosis = st.selectbox(
                            "PREY90_Features of cirrhosis",
                            options=["Yes", "No", "NA"],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )
                        st.subheader("Imaging_1st_Followup")
                        FU_Scan_Modality = st.selectbox(
                            "1st_FU_Scan Modality",
                            options=["CT", "MRI"],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )

                        FU_Imaging_Date = st.date_input("1st_FU_Imaging Date")
                        fetch_date = None
                        try:
                            fetch_date =  datetime.strptime(get_variable_value(st.session_state.temp_mrn,"TAREdate"),"%Y-%m-%d")
                        except:
                            st.write("Fill Patient Info form")
                       
                        FU_Months_Since_Y90 = relativedelta(FU_Imaging_Date, fetch_date).months
                        st.write("1st_FU_Months Since Y90",FU_Months_Since_Y90)
                        FU_Total_number_of_lesions = st.selectbox(
                            "1st_FU_Total number of lesions",
                            options=["1", "2", ">3"],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )

                        FU_Target_Lesion_1_LAD_Art_Enhanc = st.number_input(
                            "1st_FU_Target Lesion 1 LAD Art Enhanc",
                            step=0.1
                        )

                        FU_Target_Lesion_1_PAD_Art_Enhanc = st.number_input(
                            "1st_FU_Target Lesion 1 PAD Art Enhanc",
                            step=0.1
                        )

                        FU_Target_Lesion_1_CCD_Art_Enhanc = st.number_input(
                            "1st_FU_Target Lesion 1 CCD Art Enhanc",
                            step=0.1
                        )

                        FU_Target_Lesion_2_Segments = st.selectbox(
                            "1st_FU_Target Lesion 2 Segments",
                            options=["1", "2", "3", "4a", "4b", "5", "6", "7", "8", "NA"],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )

                        FU_Target_Lesion_2_LAD_Art_Enhanc = st.number_input(
                            "1st_FU_Target Lesion 2 LAD Art Enhanc",
                            step=0.1
                        )

                        FU_Target_Lesion_2_PAD_Art_Enhanc = st.number_input(
                            "1st_FU_Target Lesion 2 PAD Art Enhanc",
                            step=0.1
                        )

                        FU_Target_Lesion_2_CCD_Art_Enhanc = st.number_input(
                            "1st_FU_Target Lesion 2 CCD Art Enhanc",
                            step=0.1
                        )

                        FU_Follow_up_1_targeted_Lesion_Dia_Sum = max(FU_Target_Lesion_1_CCD_Art_Enhanc,FU_Target_Lesion_1_PAD_Art_Enhanc,FU_Target_Lesion_1_LAD_Art_Enhanc)+max(FU_Target_Lesion_2_CCD_Art_Enhanc,FU_Target_Lesion_2_PAD_Art_Enhanc,FU_Target_Lesion_2_LAD_Art_Enhanc)
                        st.write("1st_FU_Follow up 1 targeted Lesion Dia Sum",FU_Follow_up_1_targeted_Lesion_Dia_Sum)
                        FU_Non_Target_Lesion_2_LAD_Art_Enhanc = st.number_input(
                            "1st_FU_Non-Target Lesion 2 LAD Art Enhanc",
                            step=0.1
                        )

                        FU_Non_Target_Lesion_2_PAD_Art_Enhanc = st.number_input(
                            "1st_FU_Non-Target Lesion 2 PAD Art Enhanc",
                            step=0.1
                        )

                        FU_Non_Target_Lesion_2_CCD_Art_Enhanc = st.number_input(
                            "1st_FU_Non-Target Lesion 2 CCD Art Enhanc",
                            step=0.1
                        )

                        # Assuming "Non-targeted Lesion Dia Sum" is calculated elsewhere in the code
                        FU_Non_targeted_Lesion_Dia_Sum = max(FU_Non_Target_Lesion_2_LAD_Art_Enhanc,FU_Non_Target_Lesion_2_PAD_Art_Enhanc,FU_Non_Target_Lesion_2_CCD_Art_Enhanc)
                        st.write("1st_FU_Non-targeted Lesion Dia Sum",FU_Non_targeted_Lesion_Dia_Sum)
                        FU_Lesion_Necrosis = st.selectbox(
                            "1st_FU_Lesion Necrosis",
                            options=["No", "Yes", "NA"],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )

                        FU_Reviewers_Initials = st.text_input(
                            "1st_FU_Reviewers Initials",
                            help="Free-text input for reviewer name"
                        )

                        FU_Non_target_lesion_response = st.selectbox(
                            "1st_FU_Non target lesion response",
                            options=["No", "Yes", "NA"],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )

                        FU_New_Lesions = st.selectbox(
                            "1st_FU_New Lesions",
                            options=["No", "Yes", "NA"],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )

                        FU_NEW_Extrahepatic_Disease = st.selectbox(
                            "1st_FU_NEW Extrahepatic Disease",
                            options=["No", "Yes", "NA"],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )

                        FU_NEW_Extrahepatic_Dz_Location = st.text_input(
                            "1st_FU_NEW Extrahepatic Dz Location",
                            help="Free text"
                        )

                        FU_NEW_Extrahepatic_Dz_Date = st.date_input("1st_FU_NEW Extrahepatic Dz Date")

                        FU_change_non_target_lesion = ((PREY90_Non_targeted_Lesion_Dia_Sum - FU_Non_targeted_Lesion_Dia_Sum)/max(1,PREY90_pretx_targeted_Lesion_Dia_Sum))*100
                        st.write("1st_FU_% change for non target lesion",FU_change_non_target_lesion)
                        FU_change_target_lesion = ((PREY90_pretx_targeted_Lesion_Dia_Sum - FU_Follow_up_1_targeted_Lesion_Dia_Sum)/max(1,PREY90_pretx_targeted_Lesion_Dia_Sum))*100
                        st.write("1st_FU_% Change Target Dia",FU_change_target_lesion)
                        first_fu_mrecist_localized = st.text_input("1st_FU_mRECIST LOCALIZED")
                        first_fu_mrecist_overall = st.text_input("1st_FU_mRECIST Overall")
                        FU_Free_Text = st.text_area(
                            "1st_FU_Free Text",
                            help="Free text"
                        )

                        st.subheader("Imaging_2nd_Followup")

                        FU2_Scan_Modality = st.selectbox(
                            "2nd_FU_Scan Modality",
                            options=["CT", "MRI"],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )

                        FU2_Imaging_Date = st.date_input("2nd_FU_Imaging Date")

                        FU2_Months_Since_Y90 = relativedelta(FU2_Imaging_Date, fetch_date).months
                        st.write("2nd_FU_Months Since Y90",FU2_Months_Since_Y90)
                        FU2_Total_number_of_lesions = st.selectbox(
                            "2nd_FU_Total number of lesions",
                            options=["1", "2", ">3"],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )

                        FU2_Target_Lesion_1_LAD_Art_Enhanc = st.number_input(
                            "2nd_FU_Target Lesion 1 LAD Art Enhanc",
                            step=0.1
                        )

                        FU2_Target_Lesion_1_PAD_Art_Enhanc = st.number_input(
                            "2nd_FU_Target Lesion 1 PAD Art Enhanc",
                            step=0.1
                        )

                        FU2_Target_Lesion_1_CCD_Art_Enhanc = st.number_input(
                            "2nd_FU_Target Lesion 1 CCD Art Enhanc",
                            step=0.1
                        )

                        FU2_Target_Lesion_2_Segments = st.selectbox(
                            "2nd_FU_Target Lesion 2 Segments",
                            options=["1", "2", "3", "4a", "4b", "5", "6", "7", "8", "NA"],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )

                        FU2_Target_Lesion_2_LAD_Art_Enhanc = st.number_input(
                            "2nd_FU_Target Lesion 2 LAD Art Enhanc",
                            step=0.1
                        )

                        FU2_Target_Lesion_2_PAD_Art_Enhanc = st.number_input(
                            "2nd_FU_Target Lesion 2 PAD Art Enhanc",
                            step=0.1
                        )

                        FU2_Target_Lesion_2_CCD_Art_Enhanc = st.number_input(
                            "2nd_FU_Target Lesion 2 CCD Art Enhanc",
                            step=0.1
                        )

                        FU2_Follow_up_2_targeted_Lesion_Dia_Sum = max(FU2_Target_Lesion_1_CCD_Art_Enhanc, FU2_Target_Lesion_1_PAD_Art_Enhanc, FU2_Target_Lesion_1_LAD_Art_Enhanc) + max(FU2_Target_Lesion_2_CCD_Art_Enhanc, FU2_Target_Lesion_2_PAD_Art_Enhanc, FU2_Target_Lesion_2_LAD_Art_Enhanc)
                        st.write("2nd_FU_Follow up 2 targeted Lesion Dia Sum",FU2_Follow_up_2_targeted_Lesion_Dia_Sum)
                        FU2_Non_Target_Lesion_1_LAD_Art_Enhanc = st.number_input(
                            "2nd_FU_Non-Target Lesion 1 LAD Art Enhanc",
                            step=0.1
                        )

                        FU2_Non_Target_Lesion_1_PAD_Art_Enhanc = st.number_input(
                            "2nd_FU_Non-Target Lesion 1 PAD Art Enhanc",
                            step=0.1
                        )

                        FU2_Non_Target_Lesion_1_CCD_Art_Enhanc = st.number_input(
                            "2nd_FU_Non-Target Lesion 1 CCD Art Enhanc",
                            step=0.1
                        )

                        FU2_Non_targeted_Lesion_Dia_Sum = max(FU2_Non_Target_Lesion_1_LAD_Art_Enhanc, FU2_Non_Target_Lesion_1_PAD_Art_Enhanc, FU2_Non_Target_Lesion_1_CCD_Art_Enhanc)
                        st.write("2nd_FU_Non-targeted Lesion Dia Sum",FU2_Non_targeted_Lesion_Dia_Sum)
                        FU2_Lesion_Necrosis = st.selectbox(
                            "2nd_FU_Lesion Necrosis",
                            options=["No", "Yes", "NA"],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )

                        FU2_Reviewers_Initials = st.text_input(
                            "2nd_FU_Reviewers Initials",
                            help="Free-text input for reviewer name"
                        )

                        FU2_Non_target_lesion_response = st.selectbox(
                            "2nd_FU_Non target lesion response",
                            options=["No", "Yes", "NA"],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )

                        FU2_New_Lesions = st.selectbox(
                            "2nd_FU_New Lesions",
                            options=["No", "Yes", "NA"],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )

                        FU2_NEW_Extrahepatic_Disease = st.selectbox(
                            "2nd_FU_NEW Extrahepatic Disease",
                            options=["No", "Yes", "NA"],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )

                        FU2_NEW_Extrahepatic_Dz_Location = st.text_input(
                            "2nd_FU_NEW Extrahepatic Dz Location",
                            help="Free text"
                        )

                        FU2_NEW_Extrahepatic_Dz_Date = st.date_input("2nd_FU_NEW Extrahepatic Dz Date")

                        FU2_change_non_target_lesion = ((PREY90_Non_targeted_Lesion_Dia_Sum - FU2_Non_targeted_Lesion_Dia_Sum) / max(1,PREY90_pretx_targeted_Lesion_Dia_Sum)) * 100
                        st.write("2nd_FU_% change for non target lesion",FU2_change_non_target_lesion)
                        FU2_change_target_lesion = ((PREY90_pretx_targeted_Lesion_Dia_Sum - FU2_Follow_up_2_targeted_Lesion_Dia_Sum) / max(1,PREY90_pretx_targeted_Lesion_Dia_Sum)) * 100
                        st.write("2nd_FU_% Change Target Dia",FU2_change_target_lesion)
                        second_fu_mrecist_calc = st.text_input("2nd_FU_mRECIST Calc")
                        second_fu_mrecist_localized = st.text_input("2nd_FU_mRECIST LOCALIZED")
                        second_fu_mrecist_overall = st.text_input("2nd_FU_mRECIST Overall")
                        FU2_Free_Text = st.text_area(
                            "2nd_FU_Free Text",
                            help="Free text"
                        )
                        # 3rd Imaging Follow-up
                        st.subheader("Imaging_3rd_Followup")
                        FU3_Scan_Modality = st.selectbox(
                            "3rd_FU_Scan Modality",
                            options=["CT", "MRI"],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )
                        FU3_Imaging_Date = st.date_input("3rd_FU_Imaging Date")
                        FU3_Months_Since_Y90 = relativedelta(FU3_Imaging_Date, fetch_date).months
                        st.write("3rd_FU_Months Since Y90",FU3_Months_Since_Y90)
                        FU3_Total_number_of_lesions = st.selectbox(
                            "3rd_FU_Total number of lesions",
                            options=["1", "2", ">3"],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )

                        FU3_Target_Lesion_1_LAD_Art_Enhanc = st.number_input(
                            "3rd_FU_Target Lesion 1 LAD Art Enhanc",
                            step=0.1
                        )

                        FU3_Target_Lesion_1_PAD_Art_Enhanc = st.number_input(
                            "3rd_FU_Target Lesion 1 PAD Art Enhanc",
                            step=0.1
                        )

                        FU3_Target_Lesion_1_CCD_Art_Enhanc = st.number_input(
                            "3rd_FU_Target Lesion 1 CCD Art Enhanc",
                            step=0.1
                        )

                        FU3_Target_Lesion_2_Segments = st.selectbox(
                            "3rd_FU_Target Lesion 2 Segments",
                            options=["1", "2", "3", "4a", "4b", "5", "6", "7", "8", "NA"],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )

                        FU3_Target_Lesion_2_LAD_Art_Enhanc = st.number_input(
                            "3rd_FU_Target Lesion 2 LAD Art Enhanc",
                            step=0.1
                        )

                        FU3_Target_Lesion_2_PAD_Art_Enhanc = st.number_input(
                            "3rd_FU_Target Lesion 2 PAD Art Enhanc",
                            step=0.1
                        )

                        FU3_Target_Lesion_2_CCD_Art_Enhanc = st.number_input(
                            "3rd_FU_Target Lesion 2 CCD Art Enhanc",
                            step=0.1
                        )

                        FU3_Follow_up_2_targeted_Lesion_Dia_Sum = max(FU3_Target_Lesion_1_CCD_Art_Enhanc, FU3_Target_Lesion_1_PAD_Art_Enhanc, FU3_Target_Lesion_1_LAD_Art_Enhanc) + max(FU3_Target_Lesion_2_CCD_Art_Enhanc, FU3_Target_Lesion_2_PAD_Art_Enhanc, FU3_Target_Lesion_2_LAD_Art_Enhanc)
                        st.write("3rd_FU_Follow up 3 targeted Lesion Dia Sum",FU3_Follow_up_2_targeted_Lesion_Dia_Sum)
                        FU3_Non_Target_Lesion_1_LAD_Art_Enhanc = st.number_input(
                            "3rd_FU_Non-Target Lesion 1 LAD Art Enhanc",
                            step=0.1
                        )

                        FU3_Non_Target_Lesion_1_PAD_Art_Enhanc = st.number_input(
                            "3rd_FU_Non-Target Lesion 1 PAD Art Enhanc",
                            step=0.1
                        )

                        FU3_Non_Target_Lesion_1_CCD_Art_Enhanc = st.number_input(
                            "3rd_FU_Non-Target Lesion 1 CCD Art Enhanc",
                            step=0.1
                        )

                        FU3_Non_targeted_Lesion_Dia_Sum = max(FU3_Non_Target_Lesion_1_LAD_Art_Enhanc, FU3_Non_Target_Lesion_1_PAD_Art_Enhanc, FU3_Non_Target_Lesion_1_CCD_Art_Enhanc)
                        st.write("3rd_FU_Non-targeted Lesion Dia Sum",FU3_Non_targeted_Lesion_Dia_Sum)
                        FU3_Lesion_Necrosis = st.selectbox(
                            "3rd_FU_Lesion Necrosis",
                            options=["No", "Yes", "NA"],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )

                        FU3_Reviewers_Initials = st.text_input(
                            "3rd_FU_Reviewers Initials",
                            help="Free-text input for reviewer name"
                        )

                        FU3_Non_target_lesion_response = st.selectbox(
                            "3rd_FU_Non target lesion response",
                            options=["No", "Yes", "NA"],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )

                        FU3_New_Lesions = st.selectbox(
                            "3rd_FU_New Lesions",
                            options=["No", "Yes", "NA"],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )

                        FU3_NEW_Extrahepatic_Disease = st.selectbox(
                            "3rd_FU_NEW Extrahepatic Disease",
                            options=["No", "Yes", "NA"],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )

                        FU3_NEW_Extrahepatic_Dz_Location = st.text_input(
                            "3rd_FU_NEW Extrahepatic Dz Location",
                            help="Free text"
                        )
                        FU3_NEW_Extrahepatic_Dz_Date = st.date_input("3rd_FU_NEW Extrahepatic Dz Date")
                        FU3_change_non_target_lesion = ((PREY90_Non_targeted_Lesion_Dia_Sum - FU3_Non_targeted_Lesion_Dia_Sum) / max(1,PREY90_pretx_targeted_Lesion_Dia_Sum)) * 100
                        st.write("3rd_FU_% change for non target lesion",FU3_change_non_target_lesion)
                        FU3_change_target_lesion = ((PREY90_pretx_targeted_Lesion_Dia_Sum - FU3_Follow_up_2_targeted_Lesion_Dia_Sum) / max(1,PREY90_pretx_targeted_Lesion_Dia_Sum)) * 100
                        st.write("3rd_FU_% Change Target Dia",FU3_change_target_lesion)
                        third_fu_mrecist_calc = st.text_input("3rd_FU_mRECIST Calc")
                        third_fu_mrecist_localized = st.text_input("3rd_FU_mRECIST LOCALIZED")
                        third_fu_mrecist_overall = st.text_input("3rd_FU_mRECIST Overall")
                        FU3_Free_Text = st.text_area(
                            "3rd_FU_Free Text",
                            help="Free text"
                        )

                        # 4th Imaging Follow-up
                        st.subheader("Imaging_4th_Followup")

                        FU4_Scan_Modality = st.selectbox(
                            "4th_FU_Scan Modality",
                            options=["CT", "MRI"],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )

                        FU4_Imaging_Date = st.date_input("4th_FU_Imaging Date")

                        FU4_Months_Since_Y90 = relativedelta(FU4_Imaging_Date, fetch_date).months
                        st.write("4th_FU_Months Since Y90",FU4_Months_Since_Y90)
                        FU4_Total_number_of_lesions = st.selectbox(
                            "4th_FU_Total number of lesions",
                            options=["1", "2", ">3"],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )

                        FU4_Target_Lesion_1_LAD_Art_Enhanc = st.number_input(
                            "4th_FU_Target Lesion 1 LAD Art Enhanc",
                            step=0.1
                        )

                        FU4_Target_Lesion_1_PAD_Art_Enhanc = st.number_input(
                            "4th_FU_Target Lesion 1 PAD Art Enhanc",
                            step=0.1
                        )

                        FU4_Target_Lesion_1_CCD_Art_Enhanc = st.number_input(
                            "4th_FU_Target Lesion 1 CCD Art Enhanc",
                            step=0.1
                        )

                        FU4_Target_Lesion_2_Segments = st.selectbox(
                            "4th_FU_Target Lesion 2 Segments",
                            options=["1", "2", "3", "4a", "4b", "5", "6", "7", "8", "NA"],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )

                        FU4_Target_Lesion_2_LAD_Art_Enhanc = st.number_input(
                            "4th_FU_Target Lesion 2 LAD Art Enhanc",
                            step=0.1
                        )

                        FU4_Target_Lesion_2_PAD_Art_Enhanc = st.number_input(
                            "4th_FU_Target Lesion 2 PAD Art Enhanc",
                            step=0.1
                        )

                        FU4_Target_Lesion_2_CCD_Art_Enhanc = st.number_input(
                            "4th_FU_Target Lesion 2 CCD Art Enhanc",
                            step=0.1
                        )

                        FU4_Follow_up_2_targeted_Lesion_Dia_Sum = max(FU4_Target_Lesion_1_CCD_Art_Enhanc, FU4_Target_Lesion_1_PAD_Art_Enhanc, FU4_Target_Lesion_1_LAD_Art_Enhanc) + max(FU4_Target_Lesion_2_CCD_Art_Enhanc, FU4_Target_Lesion_2_PAD_Art_Enhanc, FU4_Target_Lesion_2_LAD_Art_Enhanc)
                        st.write("4th_FU_Follow up 4 targeted Lesion Dia Sum",FU4_Follow_up_2_targeted_Lesion_Dia_Sum)
                        FU4_Non_Target_Lesion_1_LAD_Art_Enhanc = st.number_input(
                            "4th_FU_Non-Target Lesion 1 LAD Art Enhanc",
                            step=0.1
                        )

                        FU4_Non_Target_Lesion_1_PAD_Art_Enhanc = st.number_input(
                            "4th_FU_Non-Target Lesion 1 PAD Art Enhanc",
                            step=0.1
                        )

                        FU4_Non_Target_Lesion_1_CCD_Art_Enhanc = st.number_input(
                            "4th_FU_Non-Target Lesion 1 CCD Art Enhanc",
                            step=0.1
                        )

                        FU4_Non_targeted_Lesion_Dia_Sum = max(FU4_Non_Target_Lesion_1_LAD_Art_Enhanc, FU4_Non_Target_Lesion_1_PAD_Art_Enhanc, FU4_Non_Target_Lesion_1_CCD_Art_Enhanc)
                        st.write("4th_FU_Non-targeted Lesion Dia Sum",FU4_Non_targeted_Lesion_Dia_Sum)
                        FU4_Lesion_Necrosis = st.selectbox(
                            "4th_FU_Lesion Necrosis",
                            options=["No", "Yes", "NA"],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )

                        FU4_Reviewers_Initials = st.text_input(
                            "4th_FU_Reviewers Initials",
                            help="Free-text input for reviewer name"
                        )

                        FU4_Non_target_lesion_response = st.selectbox(
                            "4th_FU_Non target lesion response",
                            options=["No", "Yes", "NA"],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )

                        FU4_New_Lesions = st.selectbox(
                            "4th_FU_New Lesions",
                            options=["No", "Yes", "NA"],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )

                        FU4_NEW_Extrahepatic_Disease = st.selectbox(
                            "4th_FU_NEW Extrahepatic Disease",
                            options=["No", "Yes", "NA"],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )

                        FU4_NEW_Extrahepatic_Dz_Location = st.text_input(
                            "4th_FU_NEW Extrahepatic Dz Location",
                            help="Free text"
                        )

                        FU4_NEW_Extrahepatic_Dz_Date = st.date_input("4th_FU_NEW Extrahepatic Dz Date")
                        FU4_change_non_target_lesion = ((PREY90_Non_targeted_Lesion_Dia_Sum - FU4_Non_targeted_Lesion_Dia_Sum) / max(1,PREY90_pretx_targeted_Lesion_Dia_Sum)) * 100
                        st.write("4th_FU_% change non target lesion",FU4_change_non_target_lesion)
                        FU4_change_target_lesion = ((PREY90_pretx_targeted_Lesion_Dia_Sum - FU4_Follow_up_2_targeted_Lesion_Dia_Sum) / max(1,PREY90_pretx_targeted_Lesion_Dia_Sum)) * 100
                        st.write("4th_FU_% Change target dia",FU4_change_target_lesion)
                        fourth_fu_mrecist_calc = st.text_input("4th_FU_mRECIST Calc")
                        fourth_fu_mrecist_localized = st.text_input("4th_FU_mRECIST LOCALIZED")
                        fourth_fu_mrecist_overall = st.text_input("4th_FU_mRECIST Overall")
                        FU4_Free_Text = st.text_area(
                            "4th_FU_Free Text",
                            help="Free text"
                        )

                        # 5th Imaging Follow-up
                        st.subheader("Imaging_5th_Followup")

                        FU5_Scan_Modality = st.selectbox(
                            "5th_FU_Scan Modality",
                            options=["CT", "MRI"],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )

                        FU5_Imaging_Date = st.date_input("5th_FU_Imaging Date")

                        FU5_Months_Since_Y90 = relativedelta(FU5_Imaging_Date, fetch_date).months
                        st.write("5th_FU_Months Since Y90",FU5_Months_Since_Y90)
                        FU5_Total_number_of_lesions = st.selectbox(
                            "5th_FU_Total number of lesions",
                            options=["1", "2", ">3"],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )

                        FU5_Non_Target_Lesion_1_LAD_Art_Enhanc = st.number_input(
                            "5th_FU_Non-Target Lesion 1 LAD Art Enhanc",
                            step=0.1
                        )

                        FU5_Non_Target_Lesion_1_PAD_Art_Enhanc = st.number_input(
                            "5th_FU_Non-Target Lesion 1 PAD Art Enhanc",
                            step=0.1
                        )

                        FU5_Non_Target_Lesion_1_CCD_Art_Enhanc = st.number_input(
                            "5th_FU_Non-Target Lesion 1 CCD Art Enhanc",
                            step=0.1
                        )

                        FU5_Non_targeted_Lesion_Dia_Sum = max(FU5_Non_Target_Lesion_1_LAD_Art_Enhanc, FU5_Non_Target_Lesion_1_PAD_Art_Enhanc, FU5_Non_Target_Lesion_1_CCD_Art_Enhanc)
                        st.write("5th_FU_Non-targeted Lesion Dia Sum",FU5_Non_targeted_Lesion_Dia_Sum)
                        FU5_Lesion_Necrosis = st.selectbox(
                            "5th_FU_Lesion Necrosis",
                            options=["No", "Yes", "NA"],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )

                        FU5_Reviewers_Initials = st.text_input(
                            "5th_FU_Reviewers Initials",
                            help="Free-text input for reviewer name"
                        )

                        FU5_Non_target_lesion_response = st.selectbox(
                            "5th_FU_Non target lesion response",
                            options=["No", "Yes", "NA"],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )

                        FU5_New_Lesions = st.selectbox(
                            "5th_FU_New Lesions",
                            options=["No", "Yes", "NA"],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )

                        FU5_NEW_Extrahepatic_Disease = st.selectbox(
                            "5th_FU_NEW Extrahepatic Disease",
                            options=["No", "Yes", "NA"],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )

                        FU5_NEW_Extrahepatic_Dz_Location = st.text_input(
                            "5th_FU_NEW Extrahepatic Dz Location",
                            help="Free text"
                        )

                        FU5_NEW_Extrahepatic_Dz_Date = st.date_input("5th_FU_NEW Extrahepatic Dz Date")

                        FU5_change_non_target_lesion = ((PREY90_Non_targeted_Lesion_Dia_Sum - FU5_Non_targeted_Lesion_Dia_Sum) / max(1,PREY90_pretx_targeted_Lesion_Dia_Sum)) * 100
                        st.write("5th_FU_% change non target lesion ",FU5_change_non_target_lesion)
                        fifth_fu_mrecist_calc = st.text_input("5th_FU_mRECIST Calc")
                        fifth_fu_mrecist_localized = st.text_input("5th_FU_mRECIST LOCALIZED")
                        fifth_fu_mrecist_overall = st.text_input("5th_FU_mRECIST Overall")
                        FU5_Free_Text = st.text_area(
                            "5th_FU_Free Text",
                            help="Free text"
                        )

                        st.subheader("Imaging_Dates for OS or PFS")

                        dead = st.selectbox(
                                "Dead",
                                options=["0", "1"],
                                format_func=lambda x:{
                                        "0":"No",
                                        "1":"Yes"
                                }[x],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )

                        Date_of_Death = 'NA' if dead == 0 else st.date_input("Date of Death")
                        Time_to_Death = 'NA' if dead == 0 else relativedelta(Date_of_Death, fetch_date).months
                        st.write("Time to Death",Time_to_Death)
                        OLT = st.selectbox(
                                "OLT",
                                options=["0", "1"],
                                format_func=lambda x:{
                                        "0":"No",
                                        "1":"Yes"
                                }[x],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )

                        Date_of_OLT = 'NA' if OLT == 0 else st.date_input("Date of OLT")
                        Time_to_OLT = 'NA' if OLT == 0 else relativedelta(Date_of_Death, fetch_date).months
                        st.write("Time to OLT",Time_to_OLT)
                        Repeat_tx_post_Y90 = st.selectbox(
                                "Repeat tx post Y90",
                                options=["0", "1"],
                                format_func=lambda x:{
                                        "0":"No",
                                        "1":"Yes"
                                }[x],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )

                        Date_of_Repeat_tx_Post_Y90 = 'NA' if Repeat_tx_post_Y90 == 0 else st.date_input("Date of Repeat tx Post Y90")
                        Time_to_Repeat_Tx_Post_Y90 = 'NA' if Repeat_tx_post_Y90 == 0 else relativedelta(Date_of_Death, fetch_date).months
                        st.write("Time to Repeat Tx Post Y90",Time_to_Repeat_Tx_Post_Y90)
                        Date_of_Localized_Progression = st.text_input("Date of Localized Progression")

                        if Date_of_Localized_Progression == "No Progression":
                                Time_to_localized_progression = 'NA'
                        else:
                                Time_to_Localized_Progression = relativedelta(Date_of_Localized_Progression, fetch_date).years
                        st.write("Time to localized progression",Time_to_Localized_Progression)
                        Date_of_Overall_Progression = st.text_input("Date of Overall Progression")

                        if Date_of_Overall_Progression == "No Progression":
                                Time_to_overall_progression = 'NA'
                        else:
                                Time_to_overall_Progression = relativedelta(Date_of_Overall_Progression, fetch_date).years
                        st.write("Time to Overall (Local or systemic) Progression",Time_to_overall_Progression)
                        Date_of_Last_Follow_up_last_imaging_date = 'NA' if dead == 1 and OLT == 1 else st.date_input("Date of Last Follow-up/last imaging date")

                        Time_to_Last_Follow_up_last_imaging_date = 'NA' if dead == 1 and OLT == 1 else relativedelta(Date_of_Last_Follow_up_last_imaging_date, fetch_date).years 
                        st.write("Time to Last follow up",Time_to_Last_Follow_up_last_imaging_date)
                        notes_free_text = st.text_input("Notes Free Text")
                        bestm_recist = st.text_input("BestmRECIST")
                        date_bestm_recist = st.text_input("Date BestmRECIST")
                        time_to_bestm_recist = st.text_input("Timeto_bestmRECIST")
                        bestm_recist_cr_vs_non_cr = st.text_input("BestmRECISTCRvsNonCR")
                        bestm_recist_r_vs_nr = st.text_input("BestmRECISTRvsNR")
                        submit_tab10 = st.form_submit_button("Submit")

                        if submit_tab10:
                            #index = st.session_state.data[st.session_state.data["MRN"] == st.session_state.temp_mrn].index[0]
                            data10={
                                    "PREY90_prescan_modality": PREY90_prescan_modality,
                                    "PREY90_Imaging Date": PREY90_Imaging_Date.strftime("%Y-%m-%d"),
                                    "PREY90_total number of lesions": PREY90_total_number_of_lesions,
                                    "PREY90_Number Involved Lobes": PREY90_Number_Involved_Lobes,
                                    "PREY90_target_lesion_1_segments": PREY90_target_lesion_1_segments,
                                    "PREY90_TL1_LAD": PREY90_TL1_LAD,
                                    "PREY90_Target Lesion 1 PAD": PREY90_Target_Lesion_1_PAD,
                                    "PREY90_Target Lesion 1 CCD": PREY90_Target_Lesion_1_CCD,
                                    "PREY90_Target Lesion 1 VOL": PREY90_Target_Lesion_1_VOL,
                                    "PREY90_Target lesion 2 Segments": PREY90_Target_Lesion_2_segments,
                                    "PREY90_Target Lesion 2 LAD": PREY90_Target_Lesion_2_LAD,
                                    "PREY90_Target Lesion 2 PAD": PREY90_Target_Lesion_2_PAD,
                                    "PREY90_Target Lesion 2 CCD": PREY90_Target_Lesion_2_CCD,
                                    "PREY90_Target Lesion 2 VOL": PREY90_Target_Lesion_2_VOL,
                                    "PREY90_pretx targeted Lesion Dia Sum": PREY90_pretx_targeted_Lesion_Dia_Sum,
                                    "PREY90_Non-Target Lesion Location": PREY90_Non_Target_Lesion_Location,
                                    "PREY90_Non-Target Lesion 2 LAD Art Enhanc": PREY90_Non_Target_Lesion_2_LAD_Art_Enhanc,
                                    "PREY90_Non-Target Lesion 2 PAD Art Enhanc": PREY90_Non_Target_Lesion_2_PAD_Art_Enhanc,
                                    "PREY90_Non-Target Lesion 2 CCD Art Enhanc": PREY90_Non_Target_Lesion_2_CCD_Art_Enhanc,
                                    "PREY90_Non-targeted Lesion Dia Sum": PREY90_Non_targeted_Lesion_Dia_Sum,
                                    "PREY90_Reviewers Initials": PREY90_Reviewers_Initials,
                                    "PREY90_Pre Y90 Extrahepatic Disease": PREY90_Pre_Y90_Extrahepatic_Disease,
                                    "PREY90_Pre Y90 Extrahepatic Disease Location": PREY90_Pre_Y90_Extrahepatic_Disease_Location,
                                    "PREY90_PVT": PREY90_PVT,
                                    "PREY90_PVT Location": PREY90_PVT_Location,
                                    "PREY90_Features of cirrhosis": PREY90_Features_of_cirrhosis,
                                    "1st_FU_Scan Modality": FU_Scan_Modality,
                                    "1st_FU_Imaging Date": FU_Imaging_Date.strftime("%Y-%m-%d"),
                                    "1st_FU_Months Since Y90": FU_Months_Since_Y90,
                                    "1st_FU_Total number of lesions": FU_Total_number_of_lesions,
                                    "1st_FU_Target Lesion 1 LAD Art Enhanc": FU_Target_Lesion_1_LAD_Art_Enhanc,
                                    "1st_FU_Target Lesion 1 PAD Art Enhanc": FU_Target_Lesion_1_PAD_Art_Enhanc,
                                    "1st_FU_Target Lesion 1 CCD Art Enhanc": FU_Target_Lesion_1_CCD_Art_Enhanc,
                                    "1st_FU_Target Lesion 2 Segments": FU_Target_Lesion_2_Segments,
                                    "1st_FU_Target Lesion 2 LAD Art Enhanc": FU_Target_Lesion_2_LAD_Art_Enhanc,
                                    "1st_FU_Target Lesion 2 PAD Art Enhanc": FU_Target_Lesion_2_PAD_Art_Enhanc,
                                    "1st_FU_Target Lesion 2 CCD Art Enhanc": FU_Target_Lesion_2_CCD_Art_Enhanc,
                                    "1st_FU_Follow up 1 targeted Lesion Dia Sum": FU_Follow_up_1_targeted_Lesion_Dia_Sum,
                                    "1st_FU_Non-Target Lesion 2 LAD Art Enhanc": FU_Non_Target_Lesion_2_LAD_Art_Enhanc,
                                    "1st_FU_Non-Target Lesion 2 PAD Art Enhanc": FU_Non_Target_Lesion_2_PAD_Art_Enhanc,
                                    "1st_FU_Non-Target Lesion 2 CCD Art Enhanc": FU_Non_Target_Lesion_2_CCD_Art_Enhanc,
                                    "1st_FU_Non-targeted Lesion Dia Sum": FU_Non_targeted_Lesion_Dia_Sum,
                                    "1st_FU_Lesion Necrosis": FU_Lesion_Necrosis,
                                    "1st_FU_Reviewers Initials": FU_Reviewers_Initials,
                                    "1st_FU_Non target lesion response": FU_Non_target_lesion_response,
                                    "1st_FU_New Lesions": FU_New_Lesions,
                                    "1st_FU_NEW Extrahepatic Disease": FU_NEW_Extrahepatic_Disease,
                                    "1st_FU_NEW Extrahepatic Dz Location": FU_NEW_Extrahepatic_Dz_Location,
                                    "1st_FU_NEW Extrahepatic Dz Date": FU_NEW_Extrahepatic_Dz_Date.strftime("%Y-%m-%d"),
                                    "1st_FU_% change non target lesion": FU_change_non_target_lesion,
                                    "1st_FU_% Change Target Dia": FU_change_target_lesion,
                                    "1st_FU_mRECIST LOCALIZED":first_fu_mrecist_localized ,
                                    "1st_FU_mRECIST Overall":first_fu_mrecist_overall ,
                                    "1st_FU_Free Text": FU_Free_Text,
                                    "2nd_FU_Scan Modality": FU2_Scan_Modality,
                                    "2nd_FU_Imaging Date": FU2_Imaging_Date.strftime("%Y-%m-%d"),
                                    "2nd_FU_Months Since Y90": FU2_Months_Since_Y90,
                                    "2nd_FU_Total number of lesions": FU2_Total_number_of_lesions,
                                    "2nd_FU_Target Lesion 1 LAD Art Enhanc": FU2_Target_Lesion_1_LAD_Art_Enhanc,
                                    "2nd_FU_Target Lesion 1 PAD Art Enhanc": FU2_Target_Lesion_1_PAD_Art_Enhanc,
                                    "2nd_FU_Target Lesion 1 CCD Art Enhanc": FU2_Target_Lesion_1_CCD_Art_Enhanc,
                                    "2nd_FU_Target Lesion 2 Segments": FU2_Target_Lesion_2_Segments,
                                    "2nd_FU_Target Lesion 2 LAD Art Enhanc": FU2_Target_Lesion_2_LAD_Art_Enhanc,
                                    "2nd_FU_Target Lesion 2 PAD Art Enhanc": FU2_Target_Lesion_2_PAD_Art_Enhanc,
                                    "2nd_FU_Target Lesion 2 CCD Art Enhanc": FU2_Target_Lesion_2_CCD_Art_Enhanc,
                                    "2nd_FU_Follow up 2 targeted Lesion Dia Sum": FU2_Follow_up_2_targeted_Lesion_Dia_Sum,
                                    "2nd_FU_Non-Target Lesion 1 LAD Art Enhanc": FU2_Non_Target_Lesion_1_LAD_Art_Enhanc,
                                    "2nd_FU_Non-Target Lesion 1 PAD Art Enhanc": FU2_Non_Target_Lesion_1_PAD_Art_Enhanc,
                                    "2nd_FU_Non-Target Lesion 1 CCD Art Enhanc": FU2_Non_Target_Lesion_1_CCD_Art_Enhanc,
                                    "2nd_FU_Non-targeted Lesion Dia Sum": FU2_Non_targeted_Lesion_Dia_Sum,
                                    "2nd_FU_Lesion Necrosis": FU2_Lesion_Necrosis,
                                    "2nd_FU_Reviewers Initials": FU2_Reviewers_Initials,
                                    "2nd_FU_Non target lesion response": FU2_Non_target_lesion_response,
                                    "2nd_FU_New Lesions": FU2_New_Lesions,
                                    "2nd_FU_Extrahepatic Disease": FU2_NEW_Extrahepatic_Disease,
                                    "2nd_FU_NEW Extrahepatic Dz Location": FU2_NEW_Extrahepatic_Dz_Location,
                                    "2nd_FU_NEW Extrahepatic Dz Date": FU2_NEW_Extrahepatic_Dz_Date.strftime("%Y-%m-%d"),
                                    "2nd_FU_% change non target lesion": FU2_change_non_target_lesion,
                                    "2nd_FU_% Change Target Dia": FU2_change_target_lesion,
                                    "2nd_FU_mRECIST Calc": second_fu_mrecist_calc ,
                                    "2nd_FU_mRECIST LOCALIZED":second_fu_mrecist_localized ,
                                    "2nd_FU_mRECIST Overall":second_fu_mrecist_overall ,
                                    "2nd_FU_Free Text": FU2_Free_Text,
                                    "3rd_FU_Scan Modality": FU3_Scan_Modality,
                                    "3rd_FU_Imaging Date": FU3_Imaging_Date.strftime("%Y-%m-%d"),
                                    "3rd_FU_Months Since Y90": FU3_Months_Since_Y90,
                                    "3rd_FU_Total number of lesions": FU3_Total_number_of_lesions,
                                    "3rd_FU_Target Lesion 1 LAD Art Enhanc": FU3_Target_Lesion_1_LAD_Art_Enhanc,
                                    "3rd_FU_Target Lesion 1 PAD Art Enhanc": FU3_Target_Lesion_1_PAD_Art_Enhanc,
                                    "3rd_FU_Target Lesion 1 CCD Art Enhanc": FU3_Target_Lesion_1_CCD_Art_Enhanc,
                                    "3rd_FU_Target Lesion 2 Segments": FU3_Target_Lesion_2_Segments,
                                    "3rd_FU_Target Lesion 2 LAD Art Enhanc": FU3_Target_Lesion_2_LAD_Art_Enhanc,
                                    "3rd_FU_Target Lesion 2 PAD Art Enhanc": FU3_Target_Lesion_2_PAD_Art_Enhanc,
                                    "3rd_FU_Target Lesion 2 CCD Art Enhanc": FU3_Target_Lesion_2_CCD_Art_Enhanc,
                                    "3rd_FU_Follow up 2 targeted Lesion Dia Sum": FU3_Follow_up_2_targeted_Lesion_Dia_Sum,
                                    "3rd_FU_Non-Target Lesion 1 LAD Art Enhanc": FU3_Non_Target_Lesion_1_LAD_Art_Enhanc,
                                    "3rd_FU_Non-Target Lesion 1 PAD Art Enhanc": FU3_Non_Target_Lesion_1_PAD_Art_Enhanc,
                                    "3rd_FU_Non-Target Lesion 1 CCD Art Enhanc": FU3_Non_Target_Lesion_1_CCD_Art_Enhanc,
                                    "3rd_FU_Non-targeted Lesion Dia Sum": FU3_Non_targeted_Lesion_Dia_Sum,
                                    "3rd_FU_Lesion Necrosis": FU3_Lesion_Necrosis,
                                    "3rd_FU_Reviewers Initials": FU3_Reviewers_Initials,
                                    "3rd_FU_Non target lesion response": FU3_Non_target_lesion_response,
                                    "3rd_FU_New Lesions": FU3_New_Lesions,
                                    "3rd_FU_Extrahepatic Disease": FU3_NEW_Extrahepatic_Disease,
                                    "3rd_FU_NEW Extrahepatic Dz Location": FU3_NEW_Extrahepatic_Dz_Location,
                                    "3rd_FU_NEW Extrahepatic Dz Date": FU3_NEW_Extrahepatic_Dz_Date.strftime("%Y-%m-%d"),
                                    "3rd_FU_% change for non target lesion": FU3_change_non_target_lesion,
                                    "3rd_FU_% Change Target Dia": FU3_change_target_lesion,
                                    "3rd_FU_mRECIST Calc" :third_fu_mrecist_calc,
                                    "3rd_FU_mRECIST LOCALIZED" :third_fu_mrecist_localized ,
                                    "3rd_FU_mRECIST Overall" :third_fu_mrecist_overall ,
                                    "3rd_FU_Free Text": FU3_Free_Text,
                                    "4th_FU_Scan Modality": FU4_Scan_Modality,
                                    "4th_FU_Imaging Date": FU4_Imaging_Date.strftime("%Y-%m-%d"),
                                    "4th_FU_Months Since Y90": FU4_Months_Since_Y90,
                                    "4th_FU_Total number of lesions": FU4_Total_number_of_lesions,
                                    "4th_FU_Target Lesion 1 LAD Art Enhanc": FU4_Target_Lesion_1_LAD_Art_Enhanc,
                                    "4th_FU_Target Lesion 1 PAD Art Enhanc": FU4_Target_Lesion_1_PAD_Art_Enhanc,
                                    "4th_FU_Target Lesion 1 CCD Art Enhanc": FU4_Target_Lesion_1_CCD_Art_Enhanc,
                                    "4th_FU_Target Lesion 2 Segments": FU4_Target_Lesion_2_Segments,
                                    "4th_FU_Target Lesion 2 LAD Art Enhanc": FU4_Target_Lesion_2_LAD_Art_Enhanc,
                                    "4th_FU_Target Lesion 2 PAD Art Enhanc": FU4_Target_Lesion_2_PAD_Art_Enhanc,
                                    "4th_FU_Target Lesion 2 CCD Art Enhanc": FU4_Target_Lesion_2_CCD_Art_Enhanc,
                                    "4th_FU_Follow up 2 targeted Lesion Dia Sum": FU4_Follow_up_2_targeted_Lesion_Dia_Sum,
                                    "4th_FU_Non-Target Lesion 1 LAD Art Enhanc": FU4_Non_Target_Lesion_1_LAD_Art_Enhanc,
                                    "4th_FU_Non-Target Lesion 1 PAD Art Enhanc": FU4_Non_Target_Lesion_1_PAD_Art_Enhanc,
                                    "4th_FU_Non-Target Lesion 1 CCD Art Enhanc": FU4_Non_Target_Lesion_1_CCD_Art_Enhanc,
                                    "4th_FU_Non-targeted Lesion Dia Sum": FU4_Non_targeted_Lesion_Dia_Sum,
                                    "4th_FU_Lesion Necrosis": FU4_Lesion_Necrosis,
                                    "4th_FU_Reviewers Initials": FU4_Reviewers_Initials,
                                    "4th_FU_Non target lesion response": FU4_Non_target_lesion_response,
                                    "4th_FU_New Lesions": FU4_New_Lesions,
                                    "4th_FU_Extrahepatic Disease": FU4_NEW_Extrahepatic_Disease,
                                    "4th_FU_NEW Extrahepatic Dz Location": FU4_NEW_Extrahepatic_Dz_Location,
                                    "4th_FU_NEW Extrahepatic Dz Date": FU4_NEW_Extrahepatic_Dz_Date.strftime("%Y-%m-%d"),
                                    "4th_FU_% change non target lesion": FU4_change_non_target_lesion,
                                    "4th_FU_% Change Target Dia": FU4_change_target_lesion,
                                    "4th_FU_mRECIST Calc" :fourth_fu_mrecist_calc ,
                                    "4th_FU_mRECIST LOCALIZED":fourth_fu_mrecist_localized ,
                                    "4th_FU_mRECIST Overall" :fourth_fu_mrecist_overall ,
                                    "4th_FU_Free Text": FU4_Free_Text,
                                    "5th_FU_Imaging Date": FU5_Imaging_Date.strftime("%Y-%m-%d"),
                                    "5th_FU_Months Since Y90": FU5_Months_Since_Y90,
                                    "5th_FU_Total number of lesions": FU5_Total_number_of_lesions,
                                    "5th_FU_Non-Target Lesion 1 LAD Art Enhanc": FU5_Non_Target_Lesion_1_LAD_Art_Enhanc,
                                    "5th_FU_Non-Target Lesion 1 PAD Art Enhanc": FU5_Non_Target_Lesion_1_PAD_Art_Enhanc,
                                    "5th_FU_Non-Target Lesion 1 CCD Art Enhanc": FU5_Non_Target_Lesion_1_CCD_Art_Enhanc,
                                    "5th_FU_Non-targeted Lesion Dia Sum": FU5_Non_targeted_Lesion_Dia_Sum,
                                    "5th_FU_Non target lesion response": FU5_Non_target_lesion_response,
                                    "5th_FU_New Lesions": FU5_New_Lesions,
                                    "5th_FU_Extrahepatic Disease": FU5_NEW_Extrahepatic_Disease,
                                    "5th_FU_NEW Extrahepatic Dz Location": FU5_NEW_Extrahepatic_Dz_Location,
                                    "5th_FU_NEW Extrahepatic Dz Date": FU5_NEW_Extrahepatic_Dz_Date.strftime("%Y-%m-%d"),
                                    "5th_FU_% change non target lesion": FU5_change_non_target_lesion,
                                    "5th_FU_mRECIST Calc": fifth_fu_mrecist_calc,
                                    "5th_FU_mRECIST LOCALIZED": fifth_fu_mrecist_localized,
                                    "5th_FU_mRECIST Overall": fifth_fu_mrecist_overall,
                                    "Dead": dead,
                                    "Date of Death": Date_of_Death.strftime("%Y-%m-%d") if Date_of_Death != "NA" else Date_of_Death,
                                    "Time to Death": Time_to_Death,
                                    "OLT": OLT,
                                    "Date of OLT": Date_of_OLT.strftime("%Y-%m-%d") if Date_of_OLT != "NA" else Date_of_OLT,
                                    "Time to OLT": Time_to_OLT,
                                    "Repeat tx post Y90": Repeat_tx_post_Y90,
                                    "Date of Repeat tx Post Y90": Date_of_Repeat_tx_Post_Y90.strftime("%Y-%m-%d") if Date_of_Repeat_tx_Post_Y90 != 'NA' else Date_of_Repeat_tx_Post_Y90,
                                    "Time to Repeat Tx Post Y90": Time_to_Repeat_Tx_Post_Y90,
                                    "Date of Localized Progression": Date_of_Localized_Progression,
                                    "Notes Free text" : notes_free_text,
                                    "BestmRECIST" :bestm_recist,
                                    "Date BestmRECIST":date_bestm_recist,
                                    "Timeto_bestmRECIST":time_to_bestm_recist,
                                    "BestmRECISTCRvsNonCR":bestm_recist_cr_vs_non_cr,
                                    "BestmRECISTRvsNR":bestm_recist_r_vs_nr,

                            }
                            if "patient_info" in st.session_state:
                                update_google_sheet(data10, st.session_state.temp_mrn)
                            else:
                                st.error(f"No patient information found for MRN {st.session_state.temp_mrn}")
                            
                except:
                    st.warning("Please Fill Patient Information Page")
    
        elif st.session_state.selected_tab == "Dosimetry Data":
            st.subheader("Dosimetry Data")
            with st.form("dosimetry_data_form"):
                if "MRN" not in st.session_state.data:
                    st.warning("Please complete the Patient Information tab first.")
                else:
                    try:
                        input_GTV_mean_dose = st.text_input("GTV mean dose")
                        input_Tx_vol_mean_dose = st.text_input("Tx vol mean dose")
                        input_Liver_Vol_Mean_dose = st.text_input("Liver Vol Mean dose")
                        input_Healthy_Liver_mean_dose = st.text_input("Healthy Liver mean dose")
                        input_GTV_Vol = st.number_input("GTV Vol",step=0.1)
                        input_Tx_vol = st.text_input("Tx vol")
                        input_Liver_vol = st.number_input("Liver vol",min_value=0.1,step=0.1)
                        input_Healthy_Liver_Vol = st.text_input("Healthy Liver Vol")
                        input_GTV_Liver = (input_GTV_Vol)/(input_Liver_vol)*100
                        st.write("GTV/Liver",input_GTV_Liver)
                        input_D98 = st.text_input("D98")
                        input_D95 = st.text_input("D95")
                        input_D90 = st.text_input("D90")
                        input_D80 = st.text_input("D80")
                        input_D70 = st.text_input("D70")
                        input_V100 = st.text_input("V100")
                        input_V200 = st.text_input("V200")
                        input_V300 = st.text_input("V300")
                        input_V400 = st.text_input("V400")
                        input_ActivityBq = st.text_input("ActivityBq")
                        input_ActivityCi = st.text_input("ActivityCi")
                        input_Tx_vol_Activity_Density = st.text_input("Tx vol Activity Density")
                        input_NEW = st.text_input("NEW")
                        input_GTV_less_D95_Vol_ml = st.text_input("GTV < D95 Vol_ml")
                        input_GTV_less_D95_Mean_Dose = st.text_input("GTV < D95 Mean Dose")
                        input_GTV_less_D95_Min_Dose = st.text_input("GTV < D95 Min Dose")
                        input_GTV_less_D95_SD = st.text_input("GTV < D95 SD")
                        input_GTV_less_D95_Vol_1 = st.text_input("GTV < D95 Vol_1")
                        input_GTV_less_D95_Mean_Dose_1 = st.text_input("GTV < D95 Mean Dose_1")
                        input_GTV_less_D95_Min_Dose_1 = st.text_input("GTV < D95 Min Dose_1")
                        input_GTV_less_D95_SD_1 = st.text_input("GTV < D95 SD_1")
                        input_GTV_less_D95_Vol_2 = st.text_input("GTV < D95 Vol_2")
                        input_GTV_less_D95_Mean_Dose_2 = st.text_input("GTV < D95 Mean Dose_2")
                        input_GTV_less_D95_Min_Dose_2 = st.text_input("GTV < D95 Min Dose_2")
                        input_GTV_less_D95_SD_2 = st.text_input("GTV < D95 SD_2")
                        input_GTV_less_100_Gy_Vol = st.text_input("GTV < 100 Gy Vol")
                        input_GTV_less_100_Gy_Mean_Dose = st.text_input("GTV < 100 Gy Mean Dose")
                        input_GTV_less_100_Gy_Min_Dose = st.text_input("GTV < 100 Gy Min Dose")
                        input_GTV_less_100_Gy_SD = st.text_input("GTV < 100 Gy SD")

                        submit_dosimetry_data = st.form_submit_button("Submit")

                        if submit_dosimetry_data:
                            data11 = {
                                    "GTV mean dose": input_GTV_mean_dose,
                                    "Tx vol mean dose": input_Tx_vol_mean_dose,
                                    "Liver Vol Mean dose": input_Liver_Vol_Mean_dose,
                                    "Healthy Liver mean dose": input_Healthy_Liver_mean_dose,
                                    "GTV Vol": input_GTV_Vol,
                                    "Tx vol": input_Tx_vol,
                                    "Liver vol": input_Liver_vol,
                                    "Healthy Liver Vol": input_Healthy_Liver_Vol,
                                    "GTV/Liver": input_GTV_Liver,
                                    "D98": input_D98,
                                    "D95": input_D95,
                                    "D90": input_D90,
                                    "D80": input_D80,
                                    "D70": input_D70,
                                    "V100": input_V100,
                                    "V200": input_V200,
                                    "V300": input_V300,
                                    "V400": input_V400,
                                    "ActivityBq": input_ActivityBq,
                                    "ActivityCi": input_ActivityCi,
                                    "Tx vol Activity Density": input_Tx_vol_Activity_Density,
                                    "NEW": input_NEW,
                                    "GTV < D95 Vol_ml": input_GTV_less_D95_Vol_ml,
                                    "GTV < D95 Mean Dose": input_GTV_less_D95_Mean_Dose,
                                    "GTV < D95 Min Dose": input_GTV_less_D95_Min_Dose,
                                    "GTV < D95 SD": input_GTV_less_D95_SD,
                                    "GTV < D95 Vol_1": input_GTV_less_D95_Vol_1,
                                    "GTV < D95 Mean Dose_1": input_GTV_less_D95_Mean_Dose_1,
                                    "GTV < D95 Min Dose_1": input_GTV_less_D95_Min_Dose_1,
                                    "GTV < D95 SD_1": input_GTV_less_D95_SD_1,
                                    "GTV < D95 Vol_2": input_GTV_less_D95_Vol_2,
                                    "GTV < D95 Mean Dose_2": input_GTV_less_D95_Mean_Dose_2,
                                    "GTV < D95 Min Dose_2": input_GTV_less_D95_Min_Dose_2,
                                    "GTV < D95 SD_2": input_GTV_less_D95_SD_2,
                                    "GTV < 100 Gy Vol": input_GTV_less_100_Gy_Vol,
                                    "GTV < 100 Gy Mean Dose": input_GTV_less_100_Gy_Mean_Dose,
                                    "GTV < 100 Gy Min Dose": input_GTV_less_100_Gy_Min_Dose,
                                    "GTV < 100 Gy SD": input_GTV_less_100_Gy_SD
                                }
                            if "patient_info" in st.session_state:
                                update_google_sheet(data11, st.session_state.temp_mrn)
                            else:
                                st.error(f"No patient information found for MRN {st.session_state.temp_mrn}")
                    except:
                        st.warning("Please Fill Patient Information Page")
    
        elif st.session_state.selected_tab == "AFP":
            st.subheader("Dosimetry Data")
            with st.form("dosimetry_data_form"):
                if "MRN" not in st.session_state.data:
                    st.warning("Please complete the Patient Information tab first.")
                else:
                    try:
                        input_1AFP_Date = st.text_area("1AFP Date")
                        input_1AFP = st.text_area("1AFP")
                        input_2AFP_Date = st.text_area("2AFP Date")
                        input_2AFP = st.text_area("2AFP")
                        input_3AFP_Date = st.text_area("3AFP Date")
                        input_3AFP = st.text_area("3AFP")
                        input_4AFP_Date = st.text_area("4AFP Date")
                        input_4AFP = st.text_area("4AFP")
                        input_5AFP_Date = st.text_area("5AFP Date")
                        input_5AFP = st.text_area("5AFP")
                        input_6AFP_Date = st.text_area("6AFP Date")
                        input_6AFP = st.text_area("6AFP")
                        input_7AFP_Date = st.text_area("7AFP Date")
                        input_7AFP = st.text_area("7AFP")
                        input_8AFP_Date = st.text_area("8AFP Date")
                        input_8AFP = st.text_area("8AFP")
                        input_9AFP_Date = st.text_area("9AFP Date")
                        input_9AFP = st.text_area("9AFP")
                        input_10AFP_Date = st.text_area("10AFP Date")
                        input_10AFP = st.text_area("10AFP")
                        input_11AFP_Date = st.text_area("11AFP Date")
                        input_11AFP = st.text_area("11AFP")
                        input_12AFP_Date = st.text_area("12AFP Date")
                        input_12AFP = st.text_area("12AFP")
                        input_13AFP_Date = st.text_area("13AFP Date")
                        input_13AFP = st.text_area("13AFP")
                        input_14AFP_Date = st.text_area("14AFP Date")
                        input_14AFP = st.text_area("14AFP")
                        input_15AFP_Date = st.text_area("15AFP Date")
                        input_15AFP = st.text_area("15AFP")
                        input_16AFP_Date = st.text_area("16AFP Date")
                        input_16AFP = st.text_area("16AFP")
                        input_17AFP_Date = st.text_area("17AFP Date")
                        input_17AFP = st.text_area("17AFP")
                        input_18AFP_DATE = st.text_area("18AFP DATE")
                        input_18AFP = st.text_area("18AFP")
                        input_19AFP_DATE = st.text_area("19AFP DATE")
                        input_19AFP = st.text_area("19AFP")
                        input_20AFP_DATE = st.text_area("20AFP DATE")
                        input_20AFP = st.text_area("20AFP")
                        input_21AFP_DATE = st.text_area("21AFP DATE")
                        input_21AFP = st.text_area("21AFP")
                        input_22AFP_DATE = st.text_area("22AFP DATE")
                        input_22AFP = st.text_area("22AFP")
                        input_23AFP_DATE = st.text_area("23AFP DATE")
                        input_23AFP = st.text_area("23AFP")
                        input_24AFP_DATE = st.text_area("24AFP DATE")
                        input_24AFP = st.text_area("24AFP")
                        input_25AFP_DATE = st.text_area("25AFP DATE")
                        input_25AFP = st.text_area("25AFP")
                        input_26AFP_DATE = st.text_area("26AFP DATE")
                        input_26AFP = st.text_area("26AFP")
                        input_27AFP_DATE = st.text_area("27AFP DATE")
                        input_27AFP = st.text_area("27AFP")
                        input_28AFP_DATE = st.text_area("28AFP DATE")
                        input_28AFP = st.text_area("28AFP")
                        input_29AFP_DATE = st.text_area("29AFP DATE")
                        input_29AFP = st.text_area("29AFP")
                        input_30AFP_DATE = st.text_area("30AFP DATE")
                        input_30AFP = st.text_area("30AFP")
                        input_31AFP_Date = st.text_area("31AFP Date")
                        input_31AFP = st.text_area("31AFP")
                        input_32AFP_DATE = st.text_area("32AFP DATE")
                        input_32AFP = st.text_area("32AFP")
                        input_33AFP_DATE = st.text_area("33AFP DATE")
                        input_33AFP = st.text_area("33AFP")
                        input_34AFP_DATE = st.text_area("34AFP DATE")
                        input_34AFP = st.text_area("34AFP")

                        submit_afp = st.form_submit_button("Submit")

                        if submit_afp:
                            data12 = {
                                    "1AFP Date": input_1AFP_Date, "1AFP": input_1AFP,
                                    "2AFP Date": input_2AFP_Date, "2AFP": input_2AFP,
                                    "3AFP Date": input_3AFP_Date, "3AFP": input_3AFP,
                                    "4AFP Date": input_4AFP_Date, "4AFP": input_4AFP,
                                    "5AFP Date": input_5AFP_Date, "5AFP": input_5AFP,
                                    "6AFP Date": input_6AFP_Date, "6AFP": input_6AFP,
                                    "7AFP Date": input_7AFP_Date, "7AFP": input_7AFP,
                                    "8AFP Date": input_8AFP_Date, "8AFP": input_8AFP,
                                    "9AFP Date": input_9AFP_Date, "9AFP": input_9AFP,
                                    "10AFP Date": input_10AFP_Date, "10AFP": input_10AFP,
                                    "11AFP Date": input_11AFP_Date, "11AFP": input_11AFP,
                                    "12AFP Date": input_12AFP_Date, "12AFP": input_12AFP,
                                    "13AFP Date": input_13AFP_Date, "13AFP": input_13AFP,
                                    "14AFP Date": input_14AFP_Date, "14AFP": input_14AFP,
                                    "15AFP Date": input_15AFP_Date, "15AFP": input_15AFP,
                                    "16AFP Date": input_16AFP_Date, "16AFP": input_16AFP,
                                    "17AFP Date": input_17AFP_Date, "17AFP": input_17AFP,
                                    "18AFP DATE": input_18AFP_DATE, "18AFP": input_18AFP,
                                    "19AFP DATE": input_19AFP_DATE, "19AFP": input_19AFP,
                                    "20AFP DATE": input_20AFP_DATE, "20AFP": input_20AFP,
                                    "21AFP DATE": input_21AFP_DATE, "21AFP": input_21AFP,
                                    "22AFP DATE": input_22AFP_DATE, "22AFP": input_22AFP,
                                    "23AFP DATE": input_23AFP_DATE, "23AFP": input_23AFP,
                                    "24AFP DATE": input_24AFP_DATE, "24AFP": input_24AFP,
                                    "25AFP DATE": input_25AFP_DATE, "25AFP": input_25AFP,
                                    "26AFP DATE": input_26AFP_DATE, "26AFP": input_26AFP,
                                    "27AFP DATE": input_27AFP_DATE, "27AFP": input_27AFP,
                                    "28AFP DATE": input_28AFP_DATE, "28AFP": input_28AFP,
                                    "29AFP DATE": input_29AFP_DATE, "29AFP": input_29AFP,
                                    "30AFP DATE": input_30AFP_DATE, "30AFP": input_30AFP,
                                    "31AFP Date": input_31AFP_Date, "31AFP": input_31AFP,
                                    "32AFP DATE": input_32AFP_DATE, "32AFP": input_32AFP,
                                    "33AFP DATE": input_33AFP_DATE, "33AFP": input_33AFP,
                                    "34AFP DATE": input_34AFP_DATE, "34AFP": input_34AFP
                                }
                            if "patient_info" in st.session_state :
                                update_google_sheet(data12, st.session_state.temp_mrn)
                            else:
                                st.error(f"No patient information found for MRN {st.session_state.temp_mrn}")
                    except:
                        st.warning("Please Fill Patient Information Page")
    
def edit_existing_data():
      
        def calculatepoints(bilirubin, albumin, inr, ascites, encephalopathy):
                            if bilirubin < 2:
                                bilirubin_points = 1
                            elif 2 <= bilirubin <= 3:
                                bilirubin_points = 2
                            else:
                                bilirubin_points = 3

                            if albumin > 3.5:
                                albumin_points = 1
                            elif 2.8 <= albumin <= 3.5:
                                albumin_points = 2
                            else:
                                albumin_points = 3

                            if inr < 1.7:
                                inr_points = 1
                            elif 1.7 <= inr <= 2.3:
                                inr_points = 2
                            else:
                                inr_points = 3

                # Points for Ascites
                            if ascites == 'none':
                                ascites_points = 1
                            elif ascites == 'Asymptomatic' or ascites == 'Minimal ascities/Mild abd distension, no sx' or ascites == "Symptomatic" :
                                ascites_points = 2
                            else:  # 'moderate/severe'
                                ascites_points = 3

                # Points for Hepatic Encephalopathy
                            if encephalopathy == 'No':
                                encephalopathy_points = 1
                            elif encephalopathy == 'Yes':
                                encephalopathy_points = 2
                            else:  # 'grade iii-iv'
                                encephalopathy_points = 3

                # Total Child-Pugh score
                            total_score = (
                                bilirubin_points + albumin_points + inr_points + ascites_points + encephalopathy_points
                            )

                            return total_score
        
        def calculate_class(poin):
                            if 5 <= poin <= 6:
                                return 'A'
                            elif 7 <= poin <= 9:
                                return 'B'
                            elif 10 <= poin <= 15:
                                return 'C'
                            else:
                                return "Invalid points: must be between 5 and 15."
        
        def albi_calc(a,b):
                            a=int(a)
                            b=int(b)
                            t = math.log(a, 10)
                            answer = (t * 0.66) + (b * -0.085)
                            return answer
        
        def albi_class(albi_score):
            if albi_score <= -2.60:
                return "Grade 1"
            elif albi_score > -2.60 and albi_score <= -1.39:
                return "Grade 2"
            else:
                return "Grade 3"

        def process_input(value):
                            
                # Handle the 'NA' case
                            if value.upper() == "NA":
                                return "NA"
                # Handle numeric cases
                            elif value.isdigit():
                                numeric_value = int(value)
                                return 1 if numeric_value < 200 else 2
                            else:
                                return "Invalid Input"
        
        def validate_input(value):
                            if value.isdigit() and 5 <= int(value) <= 15:
                                return value  # Valid number
                            elif value.upper() == "NA":
                                return "NA"  # Valid 'NA'
                            else:
                                return "NA" 
        def validate_input2(value):
                            if value.isdigit() and 6 <= int(value) <= 40:
                                return value  # Valid number
                            elif value.upper() == "NA":
                                return "NA"  # Valid 'NA'
                            else:
                                return "NA" 

        st.title("Edit Existing Data")

        st.write("Current Data:")
        df1=fetch_data_from_google_sheet()
        st.dataframe(df1)
        
        mrn = st.text_input("Enter MRN to edit and Press Enter")
        #mrn=int(mrn)
        #load_button = st.button("Edit Data")
        #if load_button:
        if mrn:
            if df1.empty and mrn not in df1['MRN'].values:
                st.error(f"MRN {mrn} not exists. Please enter a unique MRN.")
            else:
                st.subheader("Change_Data")
                st.write(f"Editing data for MRN: {mrn}")
                df = fetch_data_for_mrn(mrn)
                st.write(df)
                fetch_date = pd.to_datetime(df.loc[df['MRN'] == mrn, 'TAREdate'].values[0]).date()
                # Convert fetch_date to a datetime.date object
                fetch_date = pd.to_datetime(fetch_date).date()
                index = (df["MRN"] == mrn)
                col1, col2 = st.columns([0.3, 0.7],gap="small")
                tabs = ["Patient Information","Patient Demographics", "Cirrhosis PMH","HCC Diagnosis", "Previous Therapy for HCC", "Pre Y90", "Day_Y90", "Post Y90 Within 30 Days Labs", "Other Post Tare","Imaging Date","Dosimetry Data","AFP"]
                
                with col1:
                    st.header("Patient Deatils")
                    st.session_state.selected_tab = st.radio("", tabs)

                with col2:
                    if st.session_state.selected_tab == "Patient Information":
                        st.subheader("Patient_Info")
                        with st.form("patient_info_form"):
                            try:
                            # Patient Info Section
                                col1, col2 = st.columns(2)
                                name=df.iloc[0]["Name"]
                                last_name = col1.text_input("Last Name",value=name.split(",")[0])
                                last_name = last_name.lower()
                                first_name = col2.text_input("First Name",value=name.split(",")[1])
                                first_name = first_name.lower()
                                
                                st.write(mrn)
                                
                                duplicate_procedure_check = 0
                                if mrn in st.session_state.data["MRN"].values:
                                    st.write("Are you sure this is a duplicate")
                                    duplicate_procedure_check = 1
                                
                                tare_date = st.date_input("TARE Tx Date", help="Select the treatment date",value=datetime.strptime(df.iloc[0]["TAREdate"], "%Y-%m-%d").date())
                                
                                procedure_technique = st.selectbox(
                                "Procedure Technique",
                                options=["1", "2"],
                                format_func=lambda x: {
                                                    "1": "Lobar",
                                                    "2": " Segmental",
                                                }[x],
                                index=["1", "2"].index(df.iloc[0]["PTech"]) if df.iloc[0]["PTech"]  else 0,
                                # No default selection
                                placeholder="Choose an option",
                                )

                                age = st.number_input("Age at time of TARE", value=int(df.iloc[0]["Tareage"]) ,min_value=0, max_value=150, step=1, format="%d")
                            
                                submit_tab1 = st.form_submit_button("Submit")
                                if submit_tab1:
                                    data = {
                                        "Name": f"{last_name}, {first_name}",
                                        "MRN": mrn,
                                        "Duplicate" : duplicate_procedure_check,
                                        "TAREdate": tare_date.strftime("%Y-%m-%d"),
                                        "PTech": procedure_technique,
                                        "Tareage": age
                                        } 
                                    
                                    update_google_sheet(data, mrn)
                            except:
                                pass

                    elif st.session_state.selected_tab == "Patient Demographics":
                        st.subheader("Patient Demographics")
                        with st.form("demographics_form"):

                            gender = st.selectbox(
                                "Gender",
                                options=["Male", "Female"],
                                index=["Male", "Female"].index(df.iloc[0]["Gender"]) if df.iloc[0]["Gender"] else None,
                                placeholder="Choose an option",
                            )

                            # Ethnicity dropdown
                            ethnicity = st.selectbox(
                                "Ethnicity",
                                options=["Black","White", "Asian", "Hispanic", "Other", "NA", "0"],
                                index=["Black","White", "Asian", "Hispanic", "Other", "NA", "0"].index(df.iloc[0]["Ethnicity"]) if df.iloc[0]["Ethnicity"] else None,  # No default selection
                                placeholder="Choose an option",
                            )

                            hypertension = st.selectbox(
                                "PMHx Hypertension",
                                options=["No", "Yes"],
                                index=["No", "Yes"].index(df.iloc[0]["PMHxHTN"]) if df.iloc[0]["PMHxHTN"] else None,  # No default selection
                                placeholder="Choose an option",
                            )

                            diabetes = st.selectbox(
                                "PMHx Diabetes (T1 or T2)",
                                options=["No", "Yes"],
                                index=["No", "Yes"].index(df.iloc[0]["PMHxDM"]) if df.iloc[0]["PMHxDM"] else None,  # No default selection
                                placeholder="Choose an option",
                            )

                            hypercholesterolemia = st.selectbox(
                                "Hypercholesterolemia",
                                options=["No", "Yes"],
                                index=["No", "Yes"].index(df.iloc[0]["Hypercholesterolemia"]) if df.iloc[0]["Hypercholesterolemia"] else None,  # No default selection
                                placeholder="Choose an option",
                            )

                            smoking = st.selectbox(
                                "Hx of Smoking",
                                options=["No", "Yes"],
                                index=["No", "Yes"].index(df.iloc[0]["PMHxSmoking"]) if df.iloc[0]["PMHxSmoking"] else None,  
                                placeholder="Choose an option",
                            )

                            obesity = st.selectbox(
                                "Obesity",
                                options=["No", "Yes"],
                                index=["No", "Yes"].index(df.iloc[0]["Obesity"]) if df.iloc[0]["Obesity"] else None,  
                                placeholder="Choose an option",
                            )

                            
                           
                            submit_tab2 = st.form_submit_button("Submit")
                            if submit_tab2:
                                data1={
                                "Gender": gender,
                                "Ethnicity":ethnicity,
                                "PMHxHTN": hypertension,
                                "PMHxDM":diabetes,
                                "Hypercholesterolemia" : hypercholesterolemia,
                                "PMHxSmoking" : smoking,
                                "Obesity" : obesity,
                                }
                                update_google_sheet(data1,mrn)
                        
                    elif st.session_state.selected_tab == "Cirrhosis PMH":
                        st.subheader("Cirrhosis PMH")
                        with st.form("cirrhosis_pmh_form"):

                            cir_pmh_hbv_status = st.selectbox(
                                "Cir PMH HBV Status",
                                options=["Yes", "No"],
                                help="Select HBV Status",
                                index=["Yes", "No"].index(df.iloc[0]["CirPMH_HBV"]) if df.iloc[0]["CirPMH_HBV"] else None,
                                placeholder="Choose an option",
                            )

                            cir_pmh_hbv_free_text = "0" if cir_pmh_hbv_status == "No" else st.text_input(
                                "Cir PMH HBV Free Text",
                                value = df.iloc[0]["CirPMH_HBVFT"],
                            )
                            
                            cir_pmh_hbv_art = "0" if cir_pmh_hbv_status == "No" else st.selectbox(
                                "Cir PMH HBV ART",
                                options=["Entecavir", "Tenofovir", "NA"],
                                index=["Entecavir", "Tenofovir", "NA"].index(df.iloc[0]["CirPMH_HBVART"]) if df.iloc[0]["CirPMH_HBVART"] else None,  # No default selection
                                placeholder="Choose an option",
                            )

                            cir_pmh_hcv_status = st.selectbox(
                                "Cir_PMH_HCV Status",
                                options=["Yes", "No"],
                                index=["Yes", "No"].index(df.iloc[0]["CirPMH_HCV"]) if df.iloc[0]["CirPMH_HCV"] else None,  # No default selection
                                placeholder="Choose an option",
                            )

                            cir_pmh_hcv_free_text = "No" if cir_pmh_hcv_status == "No" else st.text_input(
                                "Cir_PMH_HCV Free Text",
                                value = df.iloc[0]["CirPMH_HCVFT"],
                                help="Provide additional details for HCV Status",
                            )

                            cir_pmh_hcv_art = "No" if cir_pmh_hcv_status == "No" else st.selectbox(
                                "Cir_PMH_HCV ART",
                                options=["sofosbuvir/velpatasvir", "ledipasvir/sofosbuvir", "NA", "Glecaprevir/pibrentasvi"],
                                help="Select ART treatment for HCV",
                                index=["sofosbuvir/velpatasvir", "ledipasvir/sofosbuvir", "NA", "Glecaprevir/pibrentasvi"].index(df.iloc[0]["CirPMH_HCVART"]) if df.iloc[0]["CirPMH_HCVART"] else None, 
                                placeholder="Choose an option",
                        
                            )

                            cir_pmh_alcohol_use_disorder = st.selectbox( 
                                "Cir_PMH_Alcohol Use Disorder",
                                options=["Yes", "No"],
                                help="Select Alcohol Disorder",
                                index=["Yes", "No"].index(df.iloc[0]["CirPMH_AUD"]) if df.iloc[0]["CirPMH_AUD"] else None,  
                                placeholder="Choose an option",
                            )

                            cir_pmh_alcohol_free_text = "0" if cir_pmh_alcohol_use_disorder == "No" else st.text_input(
                                "Cir_PMH_Alcohol Free Text",
                                value = df.iloc[0]["CirPMH_AUDFT"],
                                help="Provide additional details for Alcohol Disorder",
                            )

                            cir_pmh_ivdu_status = st.selectbox(
                                "Cir_PMH_IVDU Status",
                                options=["Yes", "No"],
                                #format_func=lambda x: f"{x} ({1 if x == 'Yes' else 0})",
                                help="Select IVDU Status",
                                index=["Yes", "No"].index(df.iloc[0]["CirPMH_IVDU"]) if df.iloc[0]["CirPMH_IVDU"] else None, 
                                placeholder="Choose an option",
                            )

                            cir_pmh_ivdu_free_text = "0" if cir_pmh_ivdu_status == "No" else st.text_input(
                                "Cir_PMH_IVDU Free Text",
                                value = df.iloc[0]["CirPMH_IVDUFT"],
                                help="Provide additional details for IVDU"
                        
                            )

                            cir_pmh_liver_addtional_factor = st.selectbox(
                                "Cir_PMH_Liver Additional Factors",
                                options=["NAFLD", "MAFLD", "NASH", "Autoimmune Hepatitis", "Hereditary Hemochromatosis","none"],
                                help="Select Other Contributing Factors",
                                index=["NAFLD", "MAFLD", "NASH", "Autoimmune Hepatitis", "Hereditary Hemochromatosis","none"].index(df.iloc[0]["CirPMH_Liverfactors"]) if df.iloc[0]["CirPMH_Liverfactors"] else None,
                                placeholder="Choose an option",
                            )
                    
                            st.subheader("Cirrhosis Dx")
                            if df.iloc[0]["Cirdx_DateLabs"]:
                                Cirdx_Value = datetime.strptime(df.iloc[0]["Cirdx_DateLabs"], "%Y-%m-%d").date()
                            else:
                                Cirdx_Value = None
                            Cirrhosis_Dx_Diagnosis_Date = st.date_input("Cirrhosis Dx Diagnosis Date", value = Cirdx_Value)

                            Cirrhosis_Dx_Diagnosis_Method = st.selectbox(
                                "Cirrhosis_Dx_Diagnosis Method",
                                options=["Biopsy", "Imaging"],
                                help="Select Diagnosis Method",
                                index=["Biopsy", "Imaging"].index(df.iloc[0]["Cirdx_Dxmethod"]) if df.iloc[0]["Cirdx_Dxmethod"] else None,  # No default selection
                                placeholder="Choose an option",
                            ) 
                            Cirrhosis_Dx_HPI_EMR_Note_Free_Text = st.text_area(
                                "Cirrhosis_Dx_HPI EMR Note Free Text",
                                value = df.iloc[0]["Cirdx_HPIFT"],
                                help="Provide details of HPI EMR"
                            )
                            Cirrhosis_Dx_Imaging_Findings_EMR_Note_Free_Text = st.text_area(
                                "Cirrhosis_Dx_Imaging Findings EMR Note Free Text",
                                value = df.iloc[0]["Cirdx_ImageemrFT"],
                                help="Provide details of Imaging Findings"
                            )

                            Cirrhosis_Dx_Metavir_Score = st.selectbox (
                                "Cirrhosis_Dx_Metavir Score",
                                options=["F0/F1", "F2","F3","F4","NA"],
                                help="Select Metavir_score",
                                index=["F0/F1", "F2","F3","F4","NA"].index(df.iloc[0]["Cirdx_Metavir"]) if df.iloc[0]["Cirdx_Metavir"] else None,  # No default selection
                                placeholder="Choose an option",
                            ) 
                            complications = df.loc[df["MRN"] == mrn, "Cirdx_Compatdx"].values[0]
                            if complications:
                                # If complications is a string, split it into a list and strip spaces
                                complications_list = [comp.strip() for comp in complications.split(',')] if isinstance(complications, str) else complications
                            else:
                                complications_list = []

                            # Ensure the default list matches the options exactly
                            valid_complications = ["ascites", "ariceal hemorrhage", "Hepatic encephalopathy", "jaundice", "SBP", "Hepatorenal Syndrome", "Coagulopathy", "Portal HTN", "PVT", "PVTT", "Portal Vein Thrombosis", "none"]

                            # Filter out any items that are not part of the valid complications list
                            complications_list = [comp for comp in complications_list if comp in valid_complications]
                            Cirrhosis_Dx_Complications_at_Time_of_Diagnosis = st.multiselect(
                                "Cirrhosis_Dx_Complications at Time of Diagnosis",
                                options=["ascites", "ariceal hemorrhage", "Hepatic encephalopathy", "jaundice", "SBP", "Hepatorenal Syndrome", "Coagulopathy", "Portal HTN", "PVT", "PVTT", "Portal Vein Thrombosis", "none"],
                                help="Provide details of Compilications at time of Diagnosis",
                                default=complications_list,
                                placeholder="Select all that apply"
                            )
                            Cirrhosis_Dx_Complications_at_Time_of_Diagnosis_String = ", ".join(Cirrhosis_Dx_Complications_at_Time_of_Diagnosis)

                            Cirrhosis_Dx_Complications_at_Time_of_Diagnosis_Binary = st.selectbox(
                                "Cirrhosis_Dx_Complications at Time of Diagnosis Binary",
                                options=["0","1"],
                                format_func=lambda x: {
                                    "1": " >1 ",
                                    "0": "None",
                                }[x],
                                help="Provide details of Complications_at_Time_of_Diagnosis_Binary",
                                index=["0","1"].index(df.iloc[0]["Cirdx_Compatdxbinary"]) if df.iloc[0]["Cirdx_Compatdxbinary"] else None, 
                                placeholder="Choose an option",
                            )

                            Cirrhosis_Dx_Complications_Free_Text =  st.text_area(
                                "Cirrhosis_Dx_Complications Free Text",
                                value = df.iloc[0]["Cirdx_CompFT"],
                                help="Provide details of Complications"
                            )
                            if df.iloc[0]["Cirdx_Dxdate"]:
                                Cirdx_Dxdate_value = datetime.strptime(df.iloc[0]["Cirdx_Dxdate"], "%Y-%m-%d").date()
                            else:
                                Cirdx_Dxdate_value = None 

                            Cirrhosis_Dx_Date_of_Labs_in_Window = st.date_input(" Cirrhosis_Dx_Date of Labs in Window", value =Cirdx_Dxdate_value)

                            Cirrhosis_Dx_AFP = st.text_input(
                                "Cirrhosis_Dx_AFP",
                                value = df.iloc[0]["Cirdx_AFP"],
                                help="Enter AFP value in ng/dl"
                                
                            )

                            Cirrhosis_Dx_AFP_L3 = st.text_input(
                                "Cirrhosis_Dx_AFP L3",
                                value = df.iloc[0]["Cirdx_AFP L3"],
                                help="Enter AFP_L3 value in ng/dl"
                                
                            )
                            Cirrhosis_Dx_AFP_L3_Date_Free_Text = st.text_area("Cirrhosis_Dx_AFP L3 Date Free Text",value = df.iloc[0]["Cirdx_AFPL3DateFT"])

                            Cirrhosis_Dx_Ascites_CTCAE = st.selectbox (
                                "Cirrhosis_Dx_Ascites CTCAE",
                                options=["none", "Asymptomatic","Minimal ascities/Mild abd distension","Symptomatic","moderate ascities/Symptomatic medical intervention", "Severe symptoms, invasive intervention indicated", "Life Threatening: Urgent operation intervention indicated"],
                                format_func=lambda x: {
                                "none": "0. none",
                                "Asymptomatic": "1. Asymptomatic",
                                "Minimal ascities/Mild abd distension": "1. Minimal ascities/Mild abd distension",
                                "Symptomatic": "2. Symptomatic",
                                "moderate ascities/Symptomatic medical intervention": " 2. moderate ascities/Symptomatic medical intervention",
                                "Severe symptoms, invasive intervention indicated": " 3. Severe symptoms, invasive intervention indicated",
                                "Life Threatening: Urgent operation intervention indicated" : "4. Life Threatening: Urgent operation intervention indicated",

                                }[x],
                                help="Select Metavir_score",
                                index=["none", "Asymptomatic","Minimal ascities/Mild abd distension","Symptomatic","moderate ascities/Symptomatic medical intervention", "Severe symptoms, invasive intervention indicated", "Life Threatening: Urgent operation intervention indicated"].index(df.iloc[0]["Cirdx_AscitesCTCAE"]) if df.iloc[0]["Cirdx_AscitesCTCAE"] else None,  # No default selection
                                placeholder="Choose an option",
                            ) 
                            def findascitesclass(score):
                                if score == "Asymptomatic" or score== "Minimal ascities/Mild abd distension":
                                    return 2
                                elif score == "Symptomatic" or score == "moderate ascities/Symptomatic medical intervention":
                                    return 3
                                elif score == "Severe symptoms, invasive intervention indicated" or score == "Life Threatening: Urgent operation intervention indicated" :
                                    return 3
                            
                            Cirrhosis_Dx_Ascites_Classification = 1 if Cirrhosis_Dx_Ascites_CTCAE == "none" else findascitesclass(Cirrhosis_Dx_Ascites_CTCAE)
                            st.write("Cirdx_AscitesCTCAEnumb ",Cirrhosis_Dx_Ascites_Classification)
                            Cirrhosis_Dx_Ascites_Free_Text = "NA" if Cirrhosis_Dx_Ascites_CTCAE == "none" else st.text_area(
                                "Cirrhosis_Dx_Ascites Free Text",
                                value = df.iloc[0]["Cirdx_AscitesFT"]
                            
                            )
                            Cirrhosis_Dx_Diagnosis_Date = (
                            Cirrhosis_Dx_Diagnosis_Date.strftime("%Y-%m-%d") 
                            if Cirrhosis_Dx_Diagnosis_Date is not None 
                            else None
                            )
                            Cirrhosis_Dx_Date_of_Labs_in_Window = (
                            Cirrhosis_Dx_Date_of_Labs_in_Window.strftime("%Y-%m-%d")
                            if Cirrhosis_Dx_Date_of_Labs_in_Window is not None
                            else None
                            )

                            submit_tab3 = st.form_submit_button("Submit")
                            if submit_tab3:
                                data2={
                                    "CirPMH_HBV" : cir_pmh_hbv_status,
                                    "CirPMH_HBVFT" : cir_pmh_hbv_free_text,
                                    "CirPMH_HBVART" : cir_pmh_hbv_art,
                                    "CirPMH_HCV" : cir_pmh_hcv_status,
                                    "CirPMH_HCVFT" : cir_pmh_hcv_free_text,
                                    "CirPMH_HCVART" : cir_pmh_hcv_art,
                                    "CirPMH_AUD" : cir_pmh_alcohol_use_disorder,
                                    "CirPMH_AUDFT" : cir_pmh_alcohol_free_text,
                                    "CirPMH_IVDU" : cir_pmh_ivdu_status,
                                    "CirPMH_IVDUFT" : cir_pmh_ivdu_free_text,
                                    "CirPMH_Liverfactors" : cir_pmh_liver_addtional_factor,
                                    "Cirdx_Dxdate" : Cirrhosis_Dx_Diagnosis_Date,
                                    "Cirdx_Dxmethod" : Cirrhosis_Dx_Diagnosis_Method,
                                    "Cirdx_HPIFT" : Cirrhosis_Dx_HPI_EMR_Note_Free_Text,
                                    "Cirdx_ImageemrFT" : Cirrhosis_Dx_Imaging_Findings_EMR_Note_Free_Text,
                                    "Cirdx_Metavir" : Cirrhosis_Dx_Metavir_Score,
                                    "Cirdx_Compatdx" : Cirrhosis_Dx_Complications_at_Time_of_Diagnosis_String,
                                    "Cirdx_Compatdxbinary" : Cirrhosis_Dx_Complications_at_Time_of_Diagnosis_Binary,
                                    "Cirdx_CompFT" : Cirrhosis_Dx_Complications_Free_Text,
                                    "Cirdx_DateLabs" : Cirrhosis_Dx_Date_of_Labs_in_Window,
                                    "Cirdx_AFP" : Cirrhosis_Dx_AFP,
                                    "Cirdx_AFP L3" : Cirrhosis_Dx_AFP_L3,
                                    "Cirdx_AFPL3DateFT" : Cirrhosis_Dx_AFP_L3_Date_Free_Text,
                                    "Cirdx_AscitesCTCAE" : Cirrhosis_Dx_Ascites_CTCAE,
                                    "Cirdx_AscitesCTCAEnumb" : Cirrhosis_Dx_Ascites_Classification,
                                    "Cirdx_AscitesFT" : Cirrhosis_Dx_Ascites_Free_Text,
                                        
                                    }
                                    
                                update_google_sheet(data2, mrn)

                    elif st.session_state.selected_tab == "HCC Diagnosis":
                        st.subheader("HCC Diagnosis")
                        with st.form("hcc_dx_form"):

                            hcc_dx_hcc_diagnosis_date = st.date_input("HCC_Dx_HCC Diagnosis Date", help="Enter the HCC diagnosis date",value = datetime.strptime(df.iloc[0]["HCCdx_HCCdxdate"], "%Y-%m-%d").date() if df.iloc[0]["HCCdx_HCCdxdate"] else None)

                            hcc_dx_method_of_diagnosis = st.selectbox(
                                "HCC_Dx_Method of Diagnosis",   
                                options=["Biopsy", "Imaging", "Unknown"],
                                index=["Biopsy", "Imaging", "Unknown"].index(df.iloc[0]["HCCdx_Methoddx"]) if df.iloc[0]["HCCdx_Methoddx"] else None, 
                                placeholder="Choose an option",
                                #format_func=lambda x: f"{x} ({1 if x == 'Biopsy' else 2 if x == 'Imaging' else 'NA'})"
                            )

                            hcc_dx_date_of_labs = st.date_input("HCC_Dx_Date of Labs in Window",value=datetime.strptime(df.iloc[0]["HCCdx_Datelabs"], "%Y-%m-%d").date() if df.iloc[0]["HCCdx_Datelabs"] else None)

                            hcc_dx_afp = st.number_input("HCC_Dx_AFP",step=0.1, help="Enter AFP value in ng/dl",value = float(df.iloc[0]["HCCdx_AFP"]) if pd.notnull(df.iloc[0]["HCCdx_AFP"]) and str(df.iloc[0]["HCCdx_AFP"]).isdigit() else 0.0 )

                            hcc_dx_afp_l3 = st.number_input("HCC_Dx_AFP L3",step=0.1, help="Enter AFP L3 and date details",value = float(df.iloc[0]["HCCdx_AFP L3"]) if pd.notnull(df.iloc[0]["HCCdx_AFP L3"]) and str(df.iloc[0]["HCCdx_AFP L3"]).isdigit() else 0.0)
                            hcc_dx_afp_l3_date_free_text = st.text_area("HCC_Dx_AFP L3 Date Free Text",value = df.iloc[0]["HCCdx_AFPL3dateFT"])

                            hcc_dx_bilirubin = st.number_input("HCC_Dx_Bilirubin",step=0.1, help="Enter the bilirubin value in mg/dl", min_value=1.0,value = float(df.iloc[0]["HCCdx_Bilirubin"]) if pd.notnull(df.iloc[0]["HCCdx_Bilirubin"]) and str(df.iloc[0]["HCCdx_Bilirubin"]).isdigit() else 1.0)
                            hcc_dx_albumin = st.number_input("HCC_Dx_Albumin",step=0.1, help="Enter the albumin value in g/dl",value = float(df.iloc[0]["HCCdx_Albumin"]) if pd.notnull(df.iloc[0]["HCCdx_Albumin"]) and str(df.iloc[0]["HCCdx_Albumin"]).isdigit() else 0.0)
                            hcc_dx_inr = st.number_input("HCC_Dx_INR",step=0.1, help="Enter the INR value", value = float(df.iloc[0]["HCCdx_INR"]) if pd.notnull(df.iloc[0]["HCCdx_INR"]) and str(df.iloc[0]["HCCdx_INR"]).isdigit() else 0.0)
                            hcc_dx_creatinine = st.number_input("HCC_Dx_Creatinine",step=0.1, help="Enter the creatinine value in mg/dl", value = float(df.iloc[0]["HCCdx_Creatinine"]) if pd.notnull(df.iloc[0]["HCCdx_Creatinine"]) and str(df.iloc[0]["HCCdx_Creatinine"]).isdigit() else 0.0)
                            hcc_dx_sodium = st.number_input("HCC_Dx_Sodium",step=0.1, help="Enter the sodium value in mmol/L", value = float(df.iloc[0]["HCCdx_Sodium"]) if pd.notnull(df.iloc[0]["HCCdx_Sodium"]) and str(df.iloc[0]["HCCdx_Sodium"]).isdigit() else 0.0)

                            hcc_dx_ascites_CTCAE = st.selectbox (
                                "HCC_Dx_Ascites CTCAE",
                                options=["none", "Asymptomatic","Minimal ascities/Mild abd distension","Symptomatic","moderate ascities/Symptomatic medical intervention", "Severe symptoms, invasive intervention indicated", "Life Threatening: Urgent operation intervention indicated"],
                                format_func=lambda x: {
                                "none": "0. none",
                                "Asymptomatic": "1. Asymptomatic",
                                "Minimal ascities/Mild abd distension": "1. Minimal ascities/Mild abd distension",
                                "Symptomatic": "2. Symptomatic",
                                "moderate ascities/Symptomatic medical intervention": " 2. moderate ascities/Symptomatic medical intervention",
                                "Severe symptoms, invasive intervention indicated": " 3. Severe symptoms, invasive intervention indicated",
                                "Life Threatening: Urgent operation intervention indicated" : "4. Life Threatening: Urgent operation intervention indicated",

                            }[x],
                                help="Select Metavir_score",
                                index=["none", "Asymptomatic","Minimal ascities/Mild abd distension","Symptomatic","moderate ascities/Symptomatic medical intervention", "Severe symptoms, invasive intervention indicated", "Life Threatening: Urgent operation intervention indicated"].index(df.iloc[0]["HCCdx_AscitesCTCAE"]) if df.iloc[0]["HCCdx_AscitesCTCAE"] else None,
                                placeholder="Choose an option",
                            ) 
                            def findascitesclass(score):
                                if score == "Asymptomatic" or score== "Minimal ascities/Mild abd distension":
                                    return 2
                                elif score == "Symptomatic" or score == "moderate ascities/Symptomatic medical intervention":
                                    return 3
                                elif score == "Severe symptoms, invasive intervention indicated" or score == "Life Threatening: Urgent operation intervention indicated" :
                                    return 3
                            
                            hCC_dx_ascites_classification = 1 if hcc_dx_ascites_CTCAE == "none" else findascitesclass(hcc_dx_ascites_CTCAE)
                            st.write("HCCdx_AscitesCTCAEnumb : ",hCC_dx_ascites_classification)

                            hcc_dx_ascites_diruetics = 0 if hcc_dx_ascites_CTCAE == "none" else st.selectbox(
                                "HCC_Dx_Ascites Diruetics",
                                options = ["Yes","No"],
                                index=["Yes","No"].index(df.iloc[0]["HCCdx_Ascitesdiruetics"]) if df.iloc[0]["HCCdx_Ascitesdiruetics"] else None,  # No default selection
                                placeholder="Choose an option",
                
                            )
                            hcc_dx_ascites_paracentesis = 0 if hcc_dx_ascites_CTCAE == "none" else st.selectbox(
                                "HCC_Dx_Ascites Paracentesis ",
                                options = ["Yes","No"],
                                index= ["Yes","No"].index(df.iloc[0]["HCCdx_Ascitesparacentesis"]) if df.iloc[0]["HCCdx_Ascitesparacentesis"] else None,
                                placeholder="Choose an option",
                
                            )
                            hcc_dx_ascites_hospitalization = 0 if hcc_dx_ascites_CTCAE == "none" else st.selectbox(
                                "HCC_Dx_Ascites Hospitalization",
                                options = ["Yes","No"],
                                index=["Yes","No"].index(df.iloc[0]["HCCdx_Asciteshospitalization"]) if df.iloc[0]["HCCdx_Asciteshospitalization"] else None,
                                placeholder="Choose an option",
                
                            )

                            hcc_dx_he_grade = st.selectbox(
                                "HCC_Dx_HE Grade",
                                options=[1,2,3],
                                format_func=lambda x: {
                                1: "None",
                                2: "Grade 1-2",
                                3: "Grade 3-4",
                                
                            }[x],
                                index=[1,2,3].index(int(df.iloc[0]["HCCdx_HEgrade"])) if df.iloc[0]["HCCdx_HEgrade"] else None,  
                                placeholder="Choose an option",

                            )
                        
                            hcc_dx_ecog_performance_status = st.selectbox("HCC_Dx_ECOG Performance Status", options=["0", "1", "2", "3", "4", "NA"],
                                index=["0", "1", "2", "3", "4", "NA"].index(df.iloc[0]["HCCdx_ECOG"]) if df.iloc[0]["HCCdx_ECOG"] else None,  
                                placeholder="Choose an option",)

                            hcc_dx_lirads_score = st.selectbox(
                                "HCC_Dx_LIRADS Score",
                                options=["LR-1", "LR-2", "LR-3", "LR-4", "LR-5", "LR-5V", "LR-M"],
                                index=["LR-1", "LR-2", "LR-3", "LR-4", "LR-5", "LR-5V", "LR-M"].index(df.iloc[0]["HCCdx_LIRADS"]) if df.iloc[0]["HCCdx_LIRADS"] else None, 
                                placeholder="Choose an option",
                            )

                            hcc_dx_child_pugh_points_calc = calculatepoints(hcc_dx_bilirubin,hcc_dx_albumin,hcc_dx_inr,hcc_dx_ascites_CTCAE,hcc_dx_he_grade)
                            st.write("HCCdx_CPcalc ",hcc_dx_child_pugh_points_calc)
                            hcc_dx_child_pugh_class_calc = calculate_class(hcc_dx_child_pugh_points_calc)
                            st.write("HCCdx_CPclass ",hcc_dx_child_pugh_class_calc)
                        
                            #bclc_stage_calc = st.text_input("HCC_Dx_BCLC Stage calc")
                            hcc_dx_meld_score_calc = (3.78*(int(hcc_dx_bilirubin)))+(11.2*(int(hcc_dx_inr)))+(9.57*(int(hcc_dx_creatinine)))+6.43
                            st.write("HCCdx_MELD ",hcc_dx_meld_score_calc)
                            hcc_dx_meld_na_score_calc = hcc_dx_meld_score_calc + 1.32*(137-int(hcc_dx_sodium)) - (0.033*hcc_dx_meld_score_calc*(137-int(hcc_dx_sodium)))
                            st.write("HCCdx_MELDNa ",hcc_dx_meld_na_score_calc)
                            def albi_calc(a,b):
                                a=int(a)*17.1
                                b=int(b)
                                t = math.log(a, 10)
                                answer = round((t * 0.66) + (b * -0.085))
                                return answer
                            
                            hcc_dx_albi_score_calc = albi_calc(hcc_dx_bilirubin, hcc_dx_albumin)
                            st.write("HCCdx_Albiscore ",hcc_dx_albi_score_calc)
                            hcc_dx_albi_grade = albi_class(hcc_dx_albi_score_calc)
                            st.write("HCCdx_Albigrade ",hcc_dx_albi_grade)

                            hcc_dx_bclc_calc = st.text_area("HCC_Dx_BCLC Stage calc",value = df.iloc[0]["HCCdx_BCLC"])
                            hcc_dx_hcc_diagnosis_date_formatted = (
                            hcc_dx_hcc_diagnosis_date.strftime("%Y-%m-%d") 
                            if hcc_dx_hcc_diagnosis_date is not None 
                            else None
                            )
                            hcc_dx_date_of_labs_date_formattes = (
                            hcc_dx_date_of_labs.strftime("%Y-%m-%d")
                            if hcc_dx_date_of_labs is not None
                            else None
                            )


                            submit_tab4 = st.form_submit_button("Submit")
                            if submit_tab4:
                                    
                                data4 = {
                                    "HCCdx_HCCdxdate": hcc_dx_hcc_diagnosis_date_formatted,
                                    "HCCdx_Methoddx": hcc_dx_method_of_diagnosis,
                                    "HCCdx_Datelabs": hcc_dx_date_of_labs_date_formattes,
                                    "HCCdx_AFP": hcc_dx_afp,
                                    "HCCdx_AFP L3": hcc_dx_afp_l3,
                                    "HCCdx_AFPL3dateFT": hcc_dx_afp_l3_date_free_text,
                                    "HCCdx_Bilirubin": hcc_dx_bilirubin,
                                    "HCCdx_Albumin": hcc_dx_albumin,
                                    "HCCdx_INR": hcc_dx_inr,
                                    "HCCdx_Creatinine": hcc_dx_creatinine,
                                    "HCCdx_Sodium": hcc_dx_sodium,
                                    "HCCdx_AscitesCTCAE": hcc_dx_ascites_CTCAE,
                                    "HCCdx_AscitesCTCAEnumb": hCC_dx_ascites_classification,
                                    "HCCdx_Ascitesdiruetics": hcc_dx_ascites_diruetics,
                                    "HCCdx_Ascitesparacentesis": hcc_dx_ascites_paracentesis,
                                    "HCCdx_Asciteshospitalization": hcc_dx_ascites_hospitalization,
                                    "HCCdx_HEgrade": hcc_dx_he_grade,
                                    "HCCdx_ECOG": hcc_dx_ecog_performance_status,
                                    "HCCdx_LIRADS": hcc_dx_lirads_score,
                                    "HCCdx_CPcalc": hcc_dx_child_pugh_points_calc,
                                    "HCCdx_CPclass": hcc_dx_child_pugh_class_calc,
                                    "HCCdx_MELD": hcc_dx_meld_score_calc,
                                    "HCCdx_MELDNa": hcc_dx_meld_na_score_calc,
                                    "HCCdx_Albiscore": hcc_dx_albi_score_calc,
                                    "HCCdx_Albigrade": hcc_dx_albi_grade,
                                    "HCCdx_BCLC": hcc_dx_bclc_calc,
                                }
                                
                                update_google_sheet(data4, mrn)
            
                    elif st.session_state.selected_tab == "Previous Therapy for HCC":
                        st.subheader("Previous Therapy for HCC")
                        with st.form("previous_therapy_form"):

                            PRVTHER_Prior_LDT_Therapy = st.selectbox(
                            "PRVTHER_Prior_LDT_Therapy",
                            options=["Yes", "No","NA"],
                            #format_func=lambda x: f"{x} ({1 if x == 'Yes' else 0})",
                            help="Prior LDT Therapy",
                            index=["Yes", "No","NA"].index(df.iloc[0]["PRVTHER_LDT"]) if df.iloc[0]["PRVTHER_LDT"] else None,  
                            placeholder="Choose an option",
                            )
                            PRVTHER_Prior_RFA_Therapy = st.selectbox(
                                "PRVTHER_Prior RFA Therapy",
                                options=["Yes", "No", "NA"],
                                #format_func=lambda x: f"{x} ({1 if x == 'Yes' else 0})",
                                help="Prior RFA Therapy",
                                index=["Yes", "No", "NA"].index(df.iloc[0]["PRVTHER_RFA"]) if df.iloc[0]["PRVTHER_RFA"] else None,
                                placeholder="Choose an option",
                            )
                            PRVTHER_Prior_RFA_Date = 0 if PRVTHER_Prior_RFA_Therapy == 'No' else st.date_input("PRVTHER_Prior RFA Date",value=datetime.strptime(df.iloc[0]["PRVTHER_RFAdate"], "%Y-%m-%d").date() if df.iloc[0]["PRVTHER_RFAdate"] else None)

                        
                            PRVTHER_Prior_TARE_Therapy = st.selectbox(
                                "PRVTHER_Prior TARE Therapy",
                                options=["Yes", "No","NA"],
                                #format_func=lambda x: f"{x} ({1 if x == 'Yes' else 0})",
                                help="Prior TARE Therapy",
                                index=["Yes", "No","NA"].index(df.iloc[0]["PRVTHER_TARE"]) if df.iloc[0]["PRVTHER_TARE"] else None, 
                                placeholder="Choose an option",
                            )
                            PRVTHER_Prior_TARE_Date = 0 if PRVTHER_Prior_TARE_Therapy == 'No' else st.date_input("PRVTHER_Prior TARE Date",value=datetime.strptime(df.iloc[0]["PRVTHER_TAREdate"], "%Y-%m-%d").date() if df.iloc[0]["PRVTHER_TAREdate"] else None)
                        
                            PRVTHER_Prior_SBRT_Therapy = st.selectbox(
                                "PRVTHER_Prior SBRT Therapy",
                                options=["Yes", "No","NA"],
                                #format_func=lambda x: f"{x} ({1 if x == 'Yes' else 0})",
                                help="Prior SBRT Therapy",
                                index=["Yes", "No","NA"].index(df.iloc[0]["PRVTHER_SBRT"]) if df.iloc[0]["PRVTHER_SBRT"] else None,  
                                placeholder="Choose an option",
                            )
                            
                            PRVTHER_Prior_SBRT_Date = 0 if PRVTHER_Prior_SBRT_Therapy == 'No' else st.date_input("PRVTHER_Prior SBRT Date",value=datetime.strptime(df.iloc[0]["PRVTHER_SBRTdate"], "%Y-%m-%d").date() if df.iloc[0]["PRVTHER_SBRTdate"] else None)


                        
                            PRVTHER_Prior_TACE_Therapy = st.selectbox(
                                "PRVTHER_Prior TACE Therapy",
                                options=["Yes", "No","NA"],
                                #format_func=lambda x: f"{x} ({1 if x == 'Yes' else 0})",
                                help="Prior TACE Therapy",
                                index=["Yes", "No","NA"].index(df.iloc[0]["PRVTHER_TACE"]) if df.iloc[0]["PRVTHER_TACE"] else None,
                                placeholder="Choose an option",
                            )
                            
                            PRVTHER_Prior_TACE_Date = 0 if PRVTHER_Prior_TACE_Therapy == 'No' else st.date_input("PRVTHER_Prior TACE Date",value=datetime.strptime(df.iloc[0]["PRVTHER_TACEdate"], "%Y-%m-%d").date() if df.iloc[0]["PRVTHER_TACEdate"] else None)

                            PRVTHER_Prior_MWA_Therapy = st.selectbox(
                                "PRVTHER_Prior MWA Therapy",
                                options=["Yes", "No","NA"],
                                #format_func=lambda x: f"{x} ({1 if x == 'Yes' else 0})",
                                help="Prior MWA Therapy",
                                index=["Yes", "No","NA"].index(df.iloc[0]["PRVTHER_MWA"]) if df.iloc[0]["PRVTHER_MWA"] else None, 
                                placeholder="Choose an option",
                            )
                            PRVTHER_Prior_MWA_Date = 0 if PRVTHER_Prior_MWA_Therapy == 'No' else st.date_input("PRVTHER_Prior MWA Date",value=datetime.strptime(df.iloc[0]["PRVTHER_MWAdate"], "%Y-%m-%d").date() if df.iloc[0]["PRVTHER_MWAdate"] else None)

                            PRVTHER_Resection = st.selectbox(
                                "PRVTHER_Resection",
                                options=["Yes", "No","NA"],
                                #format_func=lambda x: f"{x} ({1 if x == 'Yes' else 0})",
                                help="Prior MWA Therapy",
                                index=["Yes", "No","NA"].index(df.iloc[0]["PRVTHER_Resection"]) if df.iloc[0]["PRVTHER_Resection"] else None, 
                                placeholder="Choose an option",
                            )
                            PRVTHER_Resection_Date = 0 if PRVTHER_Resection == 'No' else st.date_input("PRVTHER_Resection Date",value=datetime.strptime(df.iloc[0]["PRVTHER_Resection date"].values[0], "%Y-%m-%d").date() if df.iloc[0]["PRVTHER_Resection date"] else None)


                            list1=[PRVTHER_Prior_LDT_Therapy, PRVTHER_Prior_RFA_Therapy, PRVTHER_Prior_TARE_Therapy, PRVTHER_Prior_SBRT_Therapy, PRVTHER_Prior_TACE_Therapy, PRVTHER_Prior_MWA_Therapy, PRVTHER_Resection ]
                            sum=0
                            for item in list1:
                                if item == "Yes" :
                                    sum+=1
                                else:
                                    continue
                            
                            PRVTHER_Previous_Therapy_Sum = sum
                            st.write("PRVTHER_Prevtxsum ",PRVTHER_Previous_Therapy_Sum)
                        # PRVTHER_Previous_Therapy_Sum = PRVTHER_Prior_LDT_Therapy + PRVTHER_Prior_RFA_Therapy + PRVTHER_Prior_TARE_Therapy + PRVTHER_Prior_SBRT_Therapy + PRVTHER_Prior_TACE_Therapy + PRVTHER_Prior_MWA_Therapy

                            PRVTHER_NotesFT = st.text_area(
                            "PRVTHER_NotesFT",  value=df.iloc[0]["PRVTHER_NotesFT"]
                        
                            )

                            PRVTHER_Total_Recurrences_HCC = st.text_area(
                                "PRVTHER_Total Recurrences HCC", value=df.iloc[0]["PRVTHER_Totalrecur"]
                            )
                            PRVTHER_Location_of_Previous_Treatment_segments = st.selectbox(
                                "PRVTHER_Location of Previous Treatment Segments",
                                options=["1","2","3","4a","4b","5","6","7","8","NA"],
                                index=["1","2","3","4a","4b","5","6","7","8","NA"].index(df.iloc[0]["PRVTHER_Locationprevtxseg"]) if df.iloc[0]["PRVTHER_Locationprevtxseg"] else None,
                                placeholder="Choose an option"
                            )
                            PRVTHER_Location_of_Previous_Tx_segments_ft = st.text_area(
                                "PRVTHER_Location of Previous Tx Segments FT",  value=df.iloc[0]["PRVTHER_Location of Previous Tx Segments FT"]
                            
                            )
                            PRVTHER_recurrence_location_note = st.selectbox(
                                "PRVTHER_Recurrence Location Note",
                                options=["1","2","3","4a","4b","5","6","7","8","NA"],
                                index=["1","2","3","4a","4b","5","6","7","8","NA"].index(df.iloc[0]["PRVTHER_RecurLocationFT"]) if df.iloc[0]["PRVTHER_RecurLocationFT"] else None,
                                placeholder="Choose an option"
                            )
                            PRVTHER_recurrence_date = st.text_area(
                                "PRVTHER_Recurrence Date", value=df.iloc[0]["PRVTHER_RecurDate"],
                            
                            )
                            PRVTHER_recurrence_seg =  st.text_input(
                                "PRVTHER_Recurrence Seg" , value=df.iloc[0]["PRVTHER_Recurrence Seg"]
                            )
                            PRVTHER_New_HCC_Outside_Previous_Treatment_Site = st.selectbox(
                                "PRVTHER_New HCC Outside Previous Treatment Site",
                                options = ["Yes","No","NA"],
                                help="new HCC occurrence that has developed in a diff location in the liver, separate from the area that was previously tx",
                                index=["Yes","No","NA"].index(df.iloc[0]["PRVTHER_NewHCCoutsideprevsite"]) if df.iloc[0]["PRVTHER_NewHCCoutsideprevsite"] else None,
                                placeholder="Choose an option"
                            )   
                            PRVTHER_New_HCC_Adjacent_to_Previous_Treatment_Site = st.selectbox(
                                "PRVTHER_New HCC Adjacent to Previous Treatment Site",
                                options = ["Yes","No","NA"],
                                help=" new HCC occurrence that has developed close to, but not directly in, the area that was previously treated",
                                index=["Yes","No","NA"].index(df.iloc[0]["PRVTHER_NewHCCadjacentprevsite"]) if df.iloc[0]["PRVTHER_NewHCCadjacentprevsite"] else None,
                                placeholder="Choose an option"
                            )   
                            PRVTHER_Residual_HCC_Note = st.text_area(
                                "PRVTHER_Residual HCC Note",
                                help="Provide information of Residual HCC",
                                value = df.iloc[0]["PRVTHER_ResidualHCCnoteFT"]
                            ) 
                            PRVTHER_Residual_HCC = st.selectbox(
                                "PRVTHER_Residual HCC",
                                options = ["Yes","No","NA"],
                                help="new HCC occurrence that has developed in a diff location in the liver, separate from the area that was previously tx",
                                index=["Yes","No","NA"].index(df.iloc[0]["PRVTHER_ResidualHCC"]) if df.iloc[0]["PRVTHER_ResidualHCC"] else None,
                                placeholder="Choose an option"
                            )   

                            PRVTHER_Systemic_Therapy_Free_Text = st.selectbox(
                                "PRVTHER_Systemic Therapy Free Text",
                                options=["Yes", "No","NA"],
                                #format_func=lambda x: f"{x} ({1 if x == 'Yes' else 0})",
                                help="Prior TACE Therapy",
                                index=["Yes", "No","NA"].index(df.iloc[0]["PRVTHER_SystemictherapyFT"]) if df.iloc[0]["PRVTHER_SystemictherapyFT"] else None, 
                                placeholder="Choose an option",
                            )

                            PRVTHER_Date_of_Labs_in_Window = st.date_input(
                                "PRVTHER_Date of Labs for AFP",
                                help="select date of labs in window",
                                value=datetime.strptime(df.iloc[0]["PRVTHER_DateAFP"], "%Y-%m-%d").date() if df.iloc[0]["PRVTHER_DateAFP"] else None
                            )

                            PRVTHER_AFP = st.number_input(
                                "PRVTHER_AFP",
                                help="Enter AFP value in ng/dl or NA",step=0.1,
                                value=float(df.iloc[0]["PRVTHER_AFP"]) if pd.notnull(df.iloc[0]["PRVTHER_AFP"]) and str(df.iloc[0]["PRVTHER_AFP"]).isdigit() else 0.0
                            )
                            if PRVTHER_Prior_RFA_Date == 0:
                                PRVTHER_Prior_RFA_Date = 0
                            elif PRVTHER_Prior_RFA_Date == None :
                                PRVTHER_Prior_RFA_Date = None
                            else:
                                PRVTHER_Prior_RFA_Date=PRVTHER_Prior_RFA_Date.strftime("%Y-%m-%d") 
                            
                            if PRVTHER_Prior_TARE_Date == 0:
                                PRVTHER_Prior_TARE_Date = 0
                            elif PRVTHER_Prior_TARE_Date == None :
                                PRVTHER_Prior_TARE_Date = None
                            else:
                                PRVTHER_Prior_TARE_Date=PRVTHER_Prior_TARE_Date.strftime("%Y-%m-%d")

                            if PRVTHER_Prior_SBRT_Date == 0:
                                PRVTHER_Prior_SBRT_Date = 0
                            elif PRVTHER_Prior_SBRT_Date == None :
                                PRVTHER_Prior_SBRT_Date = None
                            else:
                                PRVTHER_Prior_SBRT_Date=PRVTHER_Prior_SBRT_Date.strftime("%Y-%m-%d")

                            if PRVTHER_Prior_TACE_Date == 0:
                                PRVTHER_Prior_TACE_Date = 0
                            elif PRVTHER_Prior_TACE_Date == None :
                                PRVTHER_Prior_TACE_Date = None
                            else:
                                PRVTHER_Prior_TACE_Date=PRVTHER_Prior_TACE_Date.strftime("%Y-%m-%d")

                            if PRVTHER_Prior_MWA_Date == 0:
                                PRVTHER_Prior_MWA_Date = 0
                            elif PRVTHER_Prior_MWA_Date == None :
                                PRVTHER_Prior_MWA_Date = None
                            else:
                                PRVTHER_Prior_MWA_Date=PRVTHER_Prior_MWA_Date.strftime("%Y-%m-%d")   

                            if PRVTHER_Resection_Date == 0:
                                PRVTHER_Resection_Date = 0
                            elif PRVTHER_Resection_Date == None :
                                PRVTHER_Resection_Date = None
                            else:
                                PRVTHER_Resection_Date=PRVTHER_Resection_Date.strftime("%Y-%m-%d")

                            if PRVTHER_Date_of_Labs_in_Window == 0:
                                PRVTHER_Date_of_Labs_in_Window = 0
                            elif PRVTHER_Date_of_Labs_in_Window == None :
                                PRVTHER_Date_of_Labs_in_Window = None
                            else:
                                PRVTHER_Date_of_Labs_in_Window = PRVTHER_Date_of_Labs_in_Window.strftime("%Y-%m-%d")      

                            submit_tab5 = st.form_submit_button("Submit")

                            if submit_tab5:
                                data5 = {
                                "PRVTHER_LDT": PRVTHER_Prior_LDT_Therapy,
                                "PRVTHER_RFA": PRVTHER_Prior_RFA_Therapy,
                                "PRVTHER_RFAdate": PRVTHER_Prior_RFA_Date,
                                "PRVTHER_TARE": PRVTHER_Prior_TARE_Therapy,
                                "PRVTHER_TAREdate": PRVTHER_Prior_TARE_Date ,
                                "PRVTHER_SBRT": PRVTHER_Prior_SBRT_Therapy,
                                "PRVTHER_SBRTdate": PRVTHER_Prior_SBRT_Date ,
                                "PRVTHER_TACE": PRVTHER_Prior_TACE_Therapy,
                                "PRVTHER_TACEdate": PRVTHER_Prior_TACE_Date ,
                                "PRVTHER_MWA": PRVTHER_Prior_MWA_Therapy,
                                "PRVTHER_MWAdate": PRVTHER_Prior_MWA_Date ,
                                "PRVTHER_Resection": PRVTHER_Resection,
                                "PRVTHER_Resection date": PRVTHER_Resection_Date ,
                                "PRVTHER_Prevtxsum": PRVTHER_Previous_Therapy_Sum,
                                "PRVTHER_NotesFT": PRVTHER_NotesFT,
                                "PRVTHER_Totalrecur": PRVTHER_Total_Recurrences_HCC,
                                "PRVTHER_Locationprevtxseg": PRVTHER_Location_of_Previous_Treatment_segments,
                                "PRVTHER_Location of Previous Tx Segments FT": PRVTHER_Location_of_Previous_Tx_segments_ft,
                                "PRVTHER_RecurLocationFT": PRVTHER_recurrence_location_note,
                                "PRVTHER_RecurDate": PRVTHER_recurrence_date,
                                "PRVTHER_Recurrence Seg": PRVTHER_recurrence_seg,
                                "PRVTHER_NewHCCoutsideprevsite": PRVTHER_New_HCC_Outside_Previous_Treatment_Site,
                                "PRVTHER_NewHCCadjacentprevsite": PRVTHER_New_HCC_Adjacent_to_Previous_Treatment_Site,
                                "PRVTHER_ResidualHCCnoteFT": PRVTHER_Residual_HCC_Note,
                                "PRVTHER_ResidualHCC": PRVTHER_Residual_HCC,
                                "PRVTHER_SystemictherapyFT": PRVTHER_Systemic_Therapy_Free_Text,
                                "PRVTHER_DateAFP": PRVTHER_Date_of_Labs_in_Window,
                                "PRVTHER_AFP": PRVTHER_AFP,
                                }
                            
                                update_google_sheet(data5, mrn)
                
                    elif st.session_state.selected_tab == "Pre Y90":
                        st.subheader("Pre Y90")
                        with st.form("pre_y90_form"):
                            prey90_sx = df.loc[df["MRN"] == mrn, "PREY90_sx"].values[0]
                            if prey90_sx:
                                # If complications is a string, split it into a list and strip spaces
                                prey90_sx_list = [comp.strip() for comp in prey90_sx.split(',')] if isinstance(prey90_sx, str) else prey90_sx
                            else:
                                prey90_sx_list = []

                            # Ensure the default list matches the options exactly
                            valid_prey90_sx = [
                                "portal vein HTN", 
                                "GI bleeding", 
                                "Limb edema", 
                                "Ischemic liver injury", 
                                "Variceal Bleeding", 
                                "Biliary Obstruction", 
                                "Infection"
                            ]
                            
                            prey90_sx_list = [comp for comp in prey90_sx_list if comp in valid_prey90_sx]

                            prey90_symptoms = st.multiselect(
                            "PREY90_symptoms",
                            options=[
                                "portal vein HTN", 
                                "GI bleeding", 
                                "Limb edema", 
                                "Ischemic liver injury", 
                                "Variceal Bleeding", 
                                "Biliary Obstruction", 
                                "Infection"
                            ],
                            help="Select all that apply",
                            default=prey90_sx_list,
                            placeholder="Select all that apply"
                            )
                            prey90_symptoms = ", ".join(prey90_symptoms)
                            prey90_date_of_labs = st.date_input("PREY90_date of labs in window", help="Enter the date of lab tests",value = datetime.strptime(df.iloc[0]["PREY90_Datelabs"], "%Y-%m-%d").date() if df.iloc[0]["PREY90_Datelabs"] else None)
                            prey90_afp = st.text_input("PREY90_AFP", help="Enter AFP value in ng/dl or NA",value = df.iloc[0]["PREY90_AFP"])
                            
                            def process_input(value):
                                
                    # Handle the 'NA' case
                                if value.upper() == "NA":
                                    return "NA"
                    # Handle numeric cases
                                elif value.isdigit():
                                    numeric_value = int(value)
                                    return 1 if numeric_value < 200 else 2
                                else:
                                    return "Invalid Input"
                        
                            prey90_afp_prior_to_tare = process_input(prey90_afp)
                            st.write("PRE90_AFPbinary ",prey90_afp_prior_to_tare)
                            
                            prey90_bilirubin = st.number_input("PREY90_Bilirubin",step=0.1,min_value=1.0,value = float(df.iloc[0]["PREY90_Bilirubin"]) if pd.notnull(df.iloc[0]["PREY90_Bilirubin"]) and str(df.iloc[0]["PREY90_Bilirubin"]).isdigit() else 1.0)
                            prey90_albumin = st.number_input("PREY90_Albumin",step=0.1, help="Enter the albumin value in g/dl",value = float(df.iloc[0]["PREY90_Albumin"]) if pd.notnull(df.iloc[0]["PREY90_Albumin"]) and str(df.iloc[0]["PREY90_Albumin"]).isdigit() else 0.0)
                            prey90_inr = st.number_input("PREY90_inr",step=0.1, help="Enter the INR value",value = float(df.iloc[0]["PREY90_INR"]) if pd.notnull(df.iloc[0]["PREY90_INR"]) and str(df.iloc[0]["PREY90_INR"]).isdigit() else 0.0)
                            prey90_creatinine = st.number_input("PREY90_creatinine",step=0.1, help="Enter the creatinine value in mg/dl",value = float(df.iloc[0]["PREY90_Creatinine"]) if pd.notnull(df.iloc[0]["PREY90_Creatinine"]) and str(df.iloc[0]["PREY90_Creatinine"]).isdigit() else 0.0)
                            prey90_sodium = st.number_input("PREY90_sodium",step=0.1, help="Enter the sodium value in mmol/L",value = float(df.iloc[0]["PREY90_Sodium"]) if pd.notnull(df.iloc[0]["PREY90_Sodium"]) and str(df.iloc[0]["PREY90_Sodium"]).isdigit() else 0.0)
                            prey90_ast = st.number_input("PREY90_AST",step=0.1, help="Enter AST value in U/L",value = float(df.iloc[0]["PREY90_AST"]) if pd.notnull(df.iloc[0]["PREY90_AST"]) and str(df.iloc[0]["PREY90_AST"]).isdigit() else 0.0)
                            prey90_alt = st.number_input("PREY90_ALT",step=0.1, help="Enter ALT value in U/L",value = float(df.iloc[0]["PREY90_ALT"]) if pd.notnull(df.iloc[0]["PREY90_ALT"]) and str(df.iloc[0]["PREY90_ALT"]).isdigit() else 0.0)
                            prey90_alkaline_phosphatase = st.number_input("PREY90_Alkaline Phosphatase",step=0.1, help="Enter Alkaline Phosphatase value in U/L",value = float(df.iloc[0]["PREY90_Alkaline Phosphatase"]) if pd.notnull(df.iloc[0]["PREY90_Alkaline Phosphatase"]) and str(df.iloc[0]["PREY90_Alkaline Phosphatase"]).isdigit() else 0.0)
                            prey90_potassium = st.number_input("PREY90_potassium",step=0.1, help="Enter the potassium value in mmol/L",value = float(df.iloc[0]["PREY90_Potassium"]) if pd.notnull(df.iloc[0]["PREY90_Potassium"]) and str(df.iloc[0]["PREY90_Potassium"]).isdigit() else 0.0)
                            
                            prey90_ascites_ctcae = st.selectbox (
                                "PREY90_Ascites CTCAE",
                                options=["none", "Asymptomatic","Minimal ascities/Mild abd distension","Symptomatic","moderate ascities/Symptomatic medical intervention", "Severe symptoms, invasive intervention indicated", "Life Threatening: Urgent operation intervention indicated"],
                                format_func=lambda x: {
                                "none": "0. none",
                                "Asymptomatic": "1. Asymptomatic",
                                "Minimal ascities/Mild abd distension": "1. Minimal ascities/Mild abd distension",
                                "Symptomatic": "2. Symptomatic",
                                "moderate ascities/Symptomatic medical intervention": " 2. moderate ascities/Symptomatic medical intervention",
                                "Severe symptoms, invasive intervention indicated": " 3. Severe symptoms, invasive intervention indicated",
                                "Life Threatening: Urgent operation intervention indicated" : "4. Life Threatening: Urgent operation intervention indicated",

                            }[x],
                                help="Select Metavir_score",
                                index=["none", "Asymptomatic","Minimal ascities/Mild abd distension","Symptomatic","moderate ascities/Symptomatic medical intervention", "Severe symptoms, invasive intervention indicated", "Life Threatening: Urgent operation intervention indicated"].index(df.iloc[0]["PREY90_AscitesCTCAE"]) if df.iloc[0]["PREY90_AscitesCTCAE"] else None,
                                placeholder="Choose an option",
                            ) 
                            def findascitesclass(score):
                                if score == "Asymptomatic" or score== "Minimal ascities/Mild abd distension":
                                    return 2
                                else:
                                    return 3
                            
                            prey90_ascites_classification = 1 if prey90_ascites_ctcae == "none" else findascitesclass(prey90_ascites_ctcae)
                            st.write("PREY90_AscitesCTCAEnumb ",prey90_ascites_classification)

                            prey90_ascites_free_text = st.text_area(
                                "PREY90_Ascites Free Text",
                                value = df.iloc[0]["PREY90_AscitesFT"],
                            
                            )

                            prey90_ascites_diruetics = st.selectbox(
                                "PREY90_Ascites Diruetics",
                                options = ["Yes","No"],
                                index=["Yes","No"].index(df.iloc[0]["PREY90_Ascitesdiruetics"]) if df.iloc[0]["PREY90_Ascitesdiruetics"] else None,  # No default selection
                                placeholder="Choose an option",
                
                            )
                            prey90_ascites_paracentesis = st.selectbox(
                                "PREY90_Ascites Paracentesis" ,
                                options = ["Yes","No"],
                                index=["Yes","No"].index(df.iloc[0]["PREY90_Ascitesparacentesis"]) if df.iloc[0]["PREY90_Ascitesparacentesis"] else None,  # No default selection
                                placeholder="Choose an option",
                
                            )
                            prey90_ascites_hospitalization = st.selectbox(
                                "PREY90_Ascites Hospitalization",
                                options = ["Yes","No"],
                                index=["Yes","No"].index(df.iloc[0]["PREY90_Asciteshospitalization"]) if df.iloc[0]["PREY90_Asciteshospitalization"] else None,  # No default selection
                                placeholder="Choose an option",
                
                            )

                            prey90_he_grade = st.selectbox(
                                "PREY90_HE Grade",
                                options=[1,2,3],
                                format_func=lambda x: {
                                1: "None",
                                2: "Grade 1-2",
                                3: "Grade 3-4",
                                
                            }[x],
                                index=[1,2,3].index(int(df.iloc[0]["PREY90_HEgrade"])) if df.iloc[0]["PREY90_HEgrade"] else None,  # No default selection
                                placeholder="Choose an option",

                            )
                        
                            prey90_ecog = st.selectbox("PREY90_ECOG", options=["0", "1", "2", "3", "4", "NA"],
                                index=["0", "1", "2", "3", "4", "NA"].index(df.iloc[0]["PREY90_ECOG"]) if df.iloc[0]["PREY90_ECOG"] else None,  # No default selection
                                placeholder="Choose an option",)

                            
                            # Claculation of class and points
                            prey90_child_pugh_points_calc = calculatepoints(prey90_bilirubin,prey90_albumin,prey90_inr,prey90_ascites_ctcae,prey90_he_grade)
                            st.write("PREY90_CPcalc",prey90_child_pugh_points_calc)
                    
                            prey90_child_pugh_class_calc = calculate_class(prey90_child_pugh_points_calc)
                            st.write("PREY90_CPclass",prey90_child_pugh_class_calc)
                    
                            # Additional Calculated Fields
                            
                            #prey90_bclc_stage_calc = st.text_input("PREY90_BCLC Stage calc", help="Enter calculated BCLC stage")
                            prey90_meld_score_calc = (3.78*(int(prey90_bilirubin)))+(11.2*(int(prey90_inr)))+(9.57*(int(prey90_creatinine)))+6.43
                            st.write("PREY90_MELD",prey90_meld_score_calc)
                    
                            prey90_meld_na_score_calc = prey90_meld_score_calc + 1.32*(137-int(prey90_sodium)) - (0.033*prey90_meld_score_calc*(137-int(prey90_sodium)))
                            st.write("PREY90_MELDNa",prey90_meld_na_score_calc)
                    
                            prey90_albi_score_calc = albi_calc(prey90_bilirubin,prey90_albumin)
                            st.write("PREY90_Albiscore",prey90_albi_score_calc)
                    
                            prey90_albi_grade = albi_class(prey90_albi_score_calc)
                            st.write("PREY90_Albigrade",prey90_albi_grade)
                    

                            prey90_bclc_calc = st.text_area("PREY90_BCLC Stage calc",value = df.iloc[0]["PREY90_BCLC"])

                        
                            st.subheader("Mapping Y90")
                            my90_date = st.date_input("MY90_date", help="Enter the date",value = datetime.strptime(df.iloc[0]["MY90_date"], "%Y-%m-%d").date() if df.iloc[0]["MY90_date"] else None)
                            my90_lung_shunt = st.number_input("MY90_Lung_shunt", min_value=0.0, step=0.1, help="Enter the lung shunt value",value = float(df.iloc[0]["MY90_Lung_shunt"]) if pd.notnull(df.iloc[0]["MY90_Lung_shunt"]) and str(df.iloc[0]["MY90_Lung_shunt"]).isdigit() else 0.0)
                            
                            prey90_date_of_labs = (
                                prey90_date_of_labs.strftime("%Y-%m-%d")
                                if prey90_date_of_labs is not None
                                else None
                                )
                            my90_date = (
                                my90_date.strftime("%Y-%m-%d")
                                if my90_date is not None
                                else None
                                )
                            submit_tab4 = st.form_submit_button("Submit")

                            if submit_tab4:
                               
                                data6 = {
                                "PREY90_sx": prey90_symptoms,
                                "PREY90_Datelabs": prey90_date_of_labs,
                                "PREY90_AFP": prey90_afp,
                                "PRE90_AFPbinary": prey90_afp_prior_to_tare,
                                "PREY90_Bilirubin": prey90_bilirubin,
                                "PREY90_Albumin": prey90_albumin,
                                "PREY90_INR": prey90_inr,
                                "PREY90_Creatinine": prey90_creatinine,
                                "PREY90_Sodium": prey90_sodium,
                                "PREY90_AST": prey90_ast,
                                "PREY90_ALT": prey90_alt,
                                "PREY90_Alkaline Phosphatase": prey90_alkaline_phosphatase,
                                "PREY90_Potassium": prey90_potassium,
                                "PREY90_AscitesCTCAE": prey90_ascites_ctcae,
                                "PREY90_AscitesCTCAEnumb": prey90_ascites_classification,
                                "PREY90_AscitesFT": prey90_ascites_free_text,
                                "PREY90_Ascitesdiruetics": prey90_ascites_diruetics,
                                "PREY90_Ascitesparacentesis": prey90_ascites_paracentesis,
                                "PREY90_Asciteshospitalization": prey90_ascites_hospitalization,
                                "PREY90_HEgrade": prey90_he_grade,
                                "PREY90_ECOG": prey90_ecog,
                                "PREY90_CPclass": prey90_child_pugh_class_calc,
                                "PREY90_CPcalc": prey90_child_pugh_points_calc,
                                "PREY90_MELD": prey90_meld_score_calc,
                                "PREY90_MELDNa": prey90_meld_na_score_calc,
                                "PREY90_Albiscore": prey90_albi_score_calc,
                                "PREY90_Albigrade": prey90_albi_grade,
                                "PREY90_BCLC": prey90_bclc_calc,
                                "MY90_date": my90_date,
                                "MY90_Lung_shunt": my90_lung_shunt,
                                }
                                update_google_sheet(data6,mrn)
                              
                    elif st.session_state.selected_tab == "Day_Y90":
                        st.subheader("Day_Y90")
                        with st.form("day_y90_form"):

                            dayy90_afp = st.text_input("DAYY90_AFP",value = df.iloc[0]["DAYY90_AFP"])
                            def process_input(value):
                                
                    # Handle the 'NA' case
                                if value.upper() == "NA":
                                    return "NA"
                    # Handle numeric cases
                                elif value.isdigit():
                                    numeric_value = int(value)
                                    return 1 if numeric_value < 200 else 2
                                else:
                                    return "Invalid Input"

                            dayy90_afp_prior_to_tare = process_input(dayy90_afp)
                            st.write("DAYY90_AFP Binary : ",dayy90_afp_prior_to_tare)

                            prey90_afp_binarydup = df.loc[df["MRN"] == mrn, "PRE90_AFPbinary"].values[0]
                            st.write("PRE90_AFP BinaryDup",prey90_afp_binarydup)
                        
                        # Inputs for other variables
                            dayy90_sodium = st.number_input("DAYY90_sodium",step=0.1,value = float(df.iloc[0]["DAYY90_Sodium"]) if pd.notnull(df.iloc[0]["DAYY90_Sodium"]) and str(df.iloc[0]["DAYY90_Sodium"]).isdigit() else 0.0)
                            dayy90_creatinine = st.number_input("DAYY90_creatinine",step=0.1,value = float(df.iloc[0]["DAYY90_Creatinine"]) if pd.notnull(df.iloc[0]["DAYY90_Creatinine"]) and str(df.iloc[0]["DAYY90_Creatinine"]).isdigit() else 0.0
                                                                )
                            dayy90_inr = st.number_input("DAYY90_inr",step=0.1,value = float(df.iloc[0]["DAYY90_INR"]) if pd.notnull(df.iloc[0]["DAYY90_INR"]) and str(df.iloc[0]["DAYY90_INR"]).isdigit() else 0.0)
                            dayy90_albumin = st.number_input("DAYY90_albumin",step=0.1,value = float(df.iloc[0]["DAYY90_Albumin"]) if pd.notnull(df.iloc[0]["DAYY90_Albumin"]) and str(df.iloc[0]["DAYY90_Albumin"]).isdigit() else 0.0)
                            dayy90_bilirubin = st.number_input("DAYY90_bilirubin",min_value=1.0,step=0.1,value = float(df.iloc[0]["DAYY90_Bilirubin"]) if pd.notnull(df.iloc[0]["DAYY90_Bilirubin"]) and str(df.iloc[0]["DAYY90_Bilirubin"]).isdigit() else 1.0)
                            dayy90_ast = st.number_input("DAYY90_AST",step=0.1,value = float(df.iloc[0]["DAYY90_AST"]) if pd.notnull(df.iloc[0]["DAYY90_AST"]) and str(df.iloc[0]["DAYY90_AST"]).isdigit() else 0.0)
                            dayy90_alt = st.number_input("DAYY90_ALT",step=0.1,value = float(df.iloc[0]["DAYY90_ALT"]) if pd.notnull(df.iloc[0]["DAYY90_ALT"]) and str(df.iloc[0]["DAYY90_ALT"]).isdigit() else 0.0)
                            dayy90_alkaline_phosphatase = st.number_input(
                                "DAYY90_Alkaline Phosphatase",step=0.1,
                                value = float(df.iloc[0]["DAYY90_Alkphos"]) if pd.notnull(df.iloc[0]["DAYY90_Alkphos"]) and str(df.iloc[0]["DAYY90_Alkphos"]).isdigit() else 0.0
                            )
                            dayy90_leukocytes = st.number_input("DAYY90_leukocytes",step=0.1,value = float(df.iloc[0]["DAYY90_Leukocytes"]) if pd.notnull(df.iloc[0]["DAYY90_Leukocytes"]) and str(df.iloc[0]["DAYY90_Leukocytes"]).isdigit() else 0.0)
                            dayy90_platelets = st.number_input("DAYY90_platelets",step=0.1,value = float(df.iloc[0]["DAYY90_Platelets"]) if pd.notnull(df.iloc[0]["DAYY90_Platelets"]) and str(df.iloc[0]["DAYY90_Platelets"]).isdigit() else 0.0)
                            dayy90_potassium = st.number_input("DAY90_Potassium",step=0.1,value = float(df.iloc[0]["DAY90_Potassium"]) if pd.notnull(df.iloc[0]["DAY90_Potassium"]) and str(df.iloc[0]["DAY90_Potassium"]).isdigit() else 0.0)

                            dayy90_ascites_ctcae = st.selectbox (
                                "DAYY90_Ascites CTCAE",
                                options=["none", "Asymptomatic","Minimal ascities/Mild abd distension","Symptomatic","moderate ascities/Symptomatic medical intervention", "Severe symptoms, invasive intervention indicated", "Life Threatening: Urgent operation intervention indicated"],
                                format_func=lambda x: {
                                "none": "0. none",
                                "Asymptomatic": "1. Asymptomatic",
                                "Minimal ascities/Mild abd distension": "1. Minimal ascities/Mild abd distension",
                                "Symptomatic": "2. Symptomatic",
                                "moderate ascities/Symptomatic medical intervention": " 2. moderate ascities/Symptomatic medical intervention",
                                "Severe symptoms, invasive intervention indicated": " 3. Severe symptoms, invasive intervention indicated",
                                "Life Threatening: Urgent operation intervention indicated" : "4. Life Threatening: Urgent operation intervention indicated",

                            }[x],
                                help="Select Metavir_score",
                                index=["none", "Asymptomatic","Minimal ascities/Mild abd distension","Symptomatic","moderate ascities/Symptomatic medical intervention", "Severe symptoms, invasive intervention indicated", "Life Threatening: Urgent operation intervention indicated"].index(df.iloc[0]["Day90_AscitesCTCAE"]) if df.iloc[0]["Day90_AscitesCTCAE"] else None,
                                placeholder="Choose an option",
                            ) 
                            def findascitesclass(score):
                                if score == "Asymptomatic" or score== "Minimal ascities/Mild abd distension":
                                    return 2
                                else:
                                    return 3
                            
                            dayy90_ascites_classification = 1 if dayy90_ascites_ctcae == "none" else findascitesclass(dayy90_ascites_ctcae)
                            st.write("Day90_AscitesCTCAEnumb ",dayy90_ascites_classification)

                            dayy90_he_grade = st.selectbox(
                                "DAYY90_HE Grade",
                                options=[1,2,3],
                                format_func=lambda x: {
                                1: "None",
                                2: "Grade 1-2",
                                3: "Grade 3-4",
                                
                            }[x],
                                index=[1,2,3].index(int(df.iloc[0]["Day90_HEgrade"])) if df.iloc[0]["Day90_HEgrade"] else None,  # No default selection
                                placeholder="Choose an option",

                            )
                        
                            dayy90_ecog = st.selectbox("DAYY90_ECOG", options=["0", "1", "2", "3", "4", "NA"],
                                index=["0", "1", "2", "3", "4", "NA"].index(df.iloc[0]["Day90_ECOG"]) if df.iloc[0]["Day90_ECOG"] else None,  # No default selection
                                placeholder="Choose an option",)
                            
                            dayy90_child_pugh_points_calc = calculatepoints(dayy90_bilirubin,dayy90_albumin,dayy90_inr,dayy90_ascites_ctcae,dayy90_he_grade)
                            st.write("DAYY90_CPcalc",dayy90_child_pugh_points_calc)
                            dayy90_child_pugh_class_calc = calculate_class(dayy90_child_pugh_points_calc)
                            # Additional Calculated Fields
                            st.write("DAYY90_CPclass",dayy90_child_pugh_class_calc)
                            #prey90_bclc_stage_calc = st.text_input("PREY90_BCLC Stage calc", help="Enter calculated BCLC stage")
                            dayy90_meld_score_calc = (3.78*(int(dayy90_bilirubin)))+(11.2*(int(dayy90_inr)))+(9.57*(int(dayy90_creatinine)))+6.43
                            st.write("DAYY90_MELD",dayy90_meld_score_calc)
                            dayy90_meld_na_score_calc = dayy90_meld_score_calc + 1.32*(137-int(dayy90_sodium)) - (0.033*dayy90_meld_score_calc*(137-int(dayy90_sodium)))
                            st.write("DAYY90_MELDNa",dayy90_meld_na_score_calc)
                            dayy90_albi_score_calc = albi_calc(dayy90_bilirubin,dayy90_albumin)
                            st.write("DAYY90_Albiscore",dayy90_albi_score_calc)
                            dayy90_albi_grade = albi_class(dayy90_albi_score_calc)
                            st.write("DAYY90_Albigrade",dayy90_albi_grade)

                            dayy90_bclc_calc = st.text_area("PREY90_BCLC Stage calc",value = df.iloc[0]["DAYY90_BCLC"])

                            dayy90_type_of_sphere = st.selectbox(
                                "DAYY90_Type of Sphere", options=["Therasphere-1", "SIR-2"],
                                index=["Therasphere-1", "SIR-2"].index(df.iloc[0]["DAYY90_Sphere"]) if df.iloc[0]["DAYY90_Sphere"] else None,  
                                placeholder="Choose an option",
                            )

                            dayy90_lt_notes_ftx = st.text_area("DAYY90_LT Notes Free Text",value = df.iloc[0]["DAYY90_LTnoteFT"])

                            ken_childpughscore = st.selectbox(
                                "ken_ChildPughscore",
                                options=["A","B","C"],
                                index=["A","B","C"].index(df.iloc[0]["ken_ChildPughscore"]) if df.iloc[0]["ken_ChildPughscore"] else None,  
                                placeholder="Choose an option",
                            )
                            ken_meldpretare = st.number_input("ken_MELDpreTARE",step=0.1,value = float(df.iloc[0]["ken_MELDpreTARE (MELDpreTARE)"]) if pd.notnull(df.iloc[0]["ken_MELDpreTARE (MELDpreTARE)"]) and str(df.iloc[0]["ken_MELDpreTARE (MELDpreTARE)"]).isdigit() else 0.0)


                        # Submit button
                            submit_tab7 = st.form_submit_button("Submit")
                        
                            if submit_tab7:
                                data7 = {
                                    "DAYY90_AFP": dayy90_afp,
                                    "DAYY90_AFP Binary": dayy90_afp_prior_to_tare,
                                    "PRE90_AFP BinaryDup": prey90_afp_binarydup,
                                    "DAYY90_Sodium": dayy90_sodium,
                                    "DAYY90_Creatinine": dayy90_creatinine,
                                    "DAYY90_INR": dayy90_inr,
                                    "DAYY90_Albumin": dayy90_albumin,
                                    "DAYY90_Bilirubin": dayy90_bilirubin,
                                    "DAYY90_AST": dayy90_ast,
                                    "DAYY90_ALT": dayy90_alt,
                                    "DAYY90_Alkphos": dayy90_alkaline_phosphatase,
                                    "DAYY90_Leukocytes": dayy90_leukocytes,
                                    "DAYY90_Platelets": dayy90_platelets,
                                    "DAY90_Potassium": dayy90_potassium,
                                    "Day90_AscitesCTCAE": dayy90_ascites_ctcae,
                                    "Day90_AscitesCTCAEnumb": dayy90_ascites_classification,
                                    "Day90_HEgrade": dayy90_he_grade,
                                    "Day90_ECOG": dayy90_ecog,
                                    "DAYY90_CPclass": dayy90_child_pugh_class_calc,
                                    "DAYY90_CPcalc": dayy90_child_pugh_points_calc,
                                    "DAYY90_MELD": dayy90_meld_score_calc,
                                    "DAYY90_MELDNa": dayy90_meld_na_score_calc,
                                    "DAYY90_Albiscore": dayy90_albi_score_calc,
                                    "DAYY90_Albigrade": dayy90_albi_grade,
                                    "DAYY90_BCLC": dayy90_bclc_calc,
                                    "DAYY90_Sphere": dayy90_type_of_sphere,
                                    "DAYY90_LTnoteFT": dayy90_lt_notes_ftx,
                                    "ken_ChildPughscore": ken_childpughscore,
                                    "ken_MELDpreTARE (MELDpreTARE)": ken_meldpretare,
                                    }
                                update_google_sheet(data7, mrn)
                
                    elif st.session_state.selected_tab == "Post Y90 Within 30 Days Labs":
                        st.subheader("Post Y90 Within 30 Days Labs")
                        with st.form("post_y90_form"):

                            posty90_date_labs = st.date_input("POSTY90_30DY_date_labs", value = datetime.strptime(df.iloc[0]["POSTY90_30DY_Datelabs"], "%Y-%m-%d").date() if df.iloc[0]["POSTY90_30DY_Datelabs"] else None)
                            posty90_afp = st.text_input("POSTY90_30DY_afp", value = df.iloc[0]["POSTY90_30DY_AFP"])
                            posty90_afp_date = st.date_input("POSTY90_30DY_afp DATE", value = datetime.strptime(df.iloc[0]["POSTY90_30DY_AFPdate"], "%Y-%m-%d").date() if df.iloc[0]["POSTY90_30DY_AFPdate"] else None)
                            posty90_sodium = st.number_input("POSTY90_30DY_Sodium",step=0.1, value = float(df.iloc[0]["POSTY90_30DY_Sodium"]) if pd.notnull(df.iloc[0]["POSTY90_30DY_Sodium"]) and str(df.iloc[0]["POSTY90_30DY_Sodium"]).isdigit() else 0.0)
                            posty90_creatinine = st.number_input("POSTY90_30DY_creatinine",step=0.1, value = float(df.iloc[0]["POSTY90_30DY_Creatinine"]) if pd.notnull(df.iloc[0]["POSTY90_30DY_Creatinine"]) and str(df.iloc[0]["POSTY90_30DY_Creatinine"]).isdigit() else 0.0)
                            posty90_inr = st.number_input("POSTY90_30DY_INR",step=0.1,value = float(df.iloc[0]["POSTY90_30DY_INR"]) if pd.notnull(df.iloc[0]["POSTY90_30DY_INR"]) and str(df.iloc[0]["POSTY90_30DY_INR"]).isdigit() else 0.0)
                            posty90_albumin = st.number_input("POSTY90_30DY_albumin",step=0.1, value = float(df.iloc[0]["POSTY90_30DY_Albumin"]) if pd.notnull(df.iloc[0]["POSTY90_30DY_Albumin"]) and str(df.iloc[0]["POSTY90_30DY_Albumin"]).isdigit() else 0.0)
                            posty90_bilirubin = st.number_input("POSTY90_30DY_bilirubin",min_value=1.0,step=0.1,value = float(df.iloc[0]["POSTY90_30DY_Bilirubin"]) if pd.notnull(df.iloc[0]["POSTY90_30DY_Bilirubin"]) and str(df.iloc[0]["POSTY90_30DY_Bilirubin"]).isdigit() else 1.0)
                            posty90_ast = st.number_input("POSTY90_30DY_AST", step=0.1,value = float(df.iloc[0]["POSTY90_30DY_AST"]) if pd.notnull(df.iloc[0]["POSTY90_30DY_AST"]) and str(df.iloc[0]["POSTY90_30DY_AST"]).isdigit() else 0.0)
                            posty90_alt = st.number_input("POSTY90_30DY_ALT",step=0.1,value = float(df.iloc[0]["POSTY90_30DY_ALT"]) if pd.notnull(df.iloc[0]["POSTY90_30DY_ALT"]) and str(df.iloc[0]["POSTY90_30DY_ALT"]).isdigit() else 0.0)
                            posty90_alkaline_phosphatase = st.number_input("POSTY90_30DY_Alkaline Phosphatase",step=0.1,value = float(df.iloc[0]["POSTY90_30DY_ALP"]) if pd.notnull(df.iloc[0]["POSTY90_30DY_ALP"]) and str(df.iloc[0]["POSTY90_30DY_ALP"]).isdigit() else 0.0)
                            posty90_leukocytes = st.number_input("POSTY90_30DY_leukocytes",step=0.1,value = float(df.iloc[0]["POSTY90_30DY_Leukocytes"]) if pd.notnull(df.iloc[0]["POSTY90_30DY_Leukocytes"]) and str(df.iloc[0]["POSTY90_30DY_Leukocytes"]).isdigit() else 0.0)
                            posty90_platelets = st.number_input("POSTY90_30DY_platelets",step=0.1,value = float(df.iloc[0]["POSTY90_30DY_Platelets"]) if pd.notnull(df.iloc[0]["POSTY90_30DY_Platelets"]) and str(df.iloc[0]["POSTY90_30DY_Platelets"]).isdigit() else 0.0)
                            posty90_potassium = st.number_input("POSTY90_30DY_potassium",step=0.1,value = float(df.iloc[0]["POSTY90_30DY_Potassium"]) if pd.notnull(df.iloc[0]["POSTY90_30DY_Potassium"]) and str(df.iloc[0]["POSTY90_30DY_Potassium"]).isdigit() else 0.0)
                            
                            posty90_ascites_ctcae = st.selectbox (
                            "30DY_AE_AscitesCTCAE",
                            options=["none", "Asymptomatic","Minimal ascities/Mild abd distension","Symptomatic","moderate ascities/Symptomatic medical intervention", "Severe symptoms, invasive intervention indicated", "Life Threatening: Urgent operation intervention indicated"],
                            format_func=lambda x: {
                            "none": "0. none",
                            "Asymptomatic": "1. Asymptomatic",
                            "Minimal ascities/Mild abd distension": "1. Minimal ascities/Mild abd distension",
                            "Symptomatic": "2. Symptomatic",
                            "moderate ascities/Symptomatic medical intervention": " 2. moderate ascities/Symptomatic medical intervention",
                            "Severe symptoms, invasive intervention indicated": " 3. Severe symptoms, invasive intervention indicated",
                            "Life Threatening: Urgent operation intervention indicated" : "4. Life Threatening: Urgent operation intervention indicated",

                            }[x],
                                help="Select Metavir_score",
                                index=["none", "Asymptomatic","Minimal ascities/Mild abd distension","Symptomatic","moderate ascities/Symptomatic medical intervention", "Severe symptoms, invasive intervention indicated", "Life Threatening: Urgent operation intervention indicated"].index(df.iloc[0]["30DY_AE_AscitesCTCAE"]) if df.iloc[0]["30DY_AE_AscitesCTCAE"] else None,
                                placeholder="Choose an option",
                            ) 
                            def findascitesclass(score):
                                if score == "Asymptomatic" or score== "Minimal ascities/Mild abd distension":
                                        return 2
                                else:
                                        return 3
                            
                            posty90_ascites_classification = 1 if posty90_ascites_ctcae == "none" else findascitesclass(posty90_ascites_ctcae)
                            st.write("30DY_AE_AscitesCTCAEnumb : ",posty90_ascites_classification)
                            posty90_ascites_diruetics = st.selectbox(
                                "30DY_AE_Ascitesdiruetics",
                                options = ["Yes","No"],
                                index=["Yes","No"].index(df.iloc[0]["30DY_AE_Ascitesdiruetics"]) if df.iloc[0]["30DY_AE_Ascitesdiruetics"] else None,
                                placeholder="Choose an option",
                
                            )
                            posty90_ascites_paracentesis = st.selectbox(
                                "30DY_AE_Ascitesparacentesis" ,
                                options = ["Yes","No"],
                                index=["Yes","No"].index(df.iloc[0]["30DY_AE_Ascitesparacentesis"]) if df.iloc[0]["30DY_AE_Ascitesparacentesis"] else None,
                                placeholder="Choose an option",
                
                            )
                            posty90_ascites_hospitalization = st.selectbox(
                                "30DY_AE_Asciteshospitalization",
                                options = ["Yes","No"],
                                index=["Yes","No"].index(df.iloc[0]["30DY_AE_Asciteshospitalization"]) if df.iloc[0]["30DY_AE_Asciteshospitalization"] else None,
                                placeholder="Choose an option",
                
                            )
                            posty90_he_grade = st.selectbox(
                                "30DY_AE_HE Grade",
                                options=[1,2,3],
                                format_func=lambda x: {
                                1: "None",
                                2: "Grade 1-2",
                                3: "Grade 3-4",
                                
                            }[x],
                                index=[1,2,3].index(int(df.iloc[0]["30DY_AE_HEgrade"])) if df.iloc[0]["30DY_AE_HEgrade"] else None,
                                placeholder="Choose an option",

                            )

                            posty90_ascites_free_text = st.text_area(
                                "30DY_AE_ascities_freetext",
                                value = df.iloc[0]["30DY_AE_ascities_freetext"]
                            
                            )

                            posty90_ecog = st.selectbox("POSTY90_30DY_ECOG", options=["0", "1", "2", "3", "4", "NA"],
                                index=["0", "1", "2", "3", "4", "NA"].index(df.iloc[0]["POSTY90_30DY_ECOG"]) if df.iloc[0]["POSTY90_30DY_ECOG"] else None,
                                placeholder="Choose an option",
                                )
                            
                            posty90_child_pugh_class = st.selectbox(
                                "POSTY90_30DY_Child-Pugh Class calc",
                                options=["Class A", "Class B", "Class C", "NA"],
                                help="Select the Child-Pugh class",
                            index=["Class A", "Class B", "Class C", "NA"].index(df.iloc[0]["POSTY90_30DY_CPcalc"]) if df.iloc[0]["POSTY90_30DY_CPcalc"] else None,
                            placeholder="Choose an option",
                            )

                            inputp90 = st.text_input(
                                "POSTY90_30DY_Child-Pugh Points calc",
                                help="Write in number in range 5-15, or NA",
                                value = df.iloc[0]["POSTY90_30DY_CPclass"]
                                
                            )
                            posty90_child_pugh_points = validate_input(inputp90)

                            posty90_bclc = st.selectbox(
                                "POSTY90_30DY_BCLC stage",
                                options=["0", "A", "B", "C", "D"],
                                help="Select the BCLC stage",
                            index=["0", "A", "B", "C", "D"].index(df.iloc[0]["POSTY90_30DY_BCLC"]) if df.iloc[0]["POSTY90_30DY_BCLC"] else None,
                            placeholder="Choose an option",
                            )

                            input_meld = st.text_input(
                                "POSTY90_30DY_MELD EMR",
                                help="Write in number in range 6-40, or NA",
                                value = df.iloc[0]["POSTY90_30DY_MELD"]
                            )
                            posty90_meld = validate_input2(input_meld)


                            input_meld_na = st.text_input(
                                "POSTY90_30DY_MELD Na EMR",
                                help="Write in number in range 6-40, or NA",
                                value = df.iloc[0]["POSTY90_30DY_MELDNa"]
                            )
                            posty90_meld_na = validate_input2(input_meld_na)

                            posty90_albi_score = st.number_input(
                                "POSTY90_30DY_ALBI Score calc",step=0.1,
                                help="Enter ALBI score",
                                value = float(df.iloc[0]["POSTY90_30DY_ALBIscore"]) if pd.notnull(df.iloc[0]["POSTY90_30DY_ALBIscore"]) and str(df.iloc[0]["POSTY90_30DY_ALBIscore"]).isdigit() else 0.0
                            )
                            posty90_albi_grade = albi_class(posty90_albi_score)
                            st.write("POSTY90_30DY_ALBIgrade ",posty90_albi_grade)

                        
                            ken_bclc_stage_post90 = st.text_input(
                                "Ken_BCLCStagepost90",
                                help="Enter BCLC Stage Post-90",
                                value=df.iloc[0]["Ken_BCLCStagepost90"]
                            )

                            ken_meld_stage_post90 = st.text_input(
                                "Ken_MELD_Stagepost90",
                                help="Enter MELD Score Pre-TARE",
                                value=df.iloc[0]["Ken_MELD_Stagepost90"]
                            )
                            ## New Part
                            st.subheader("Post_Y90_within_30_days_adverse_events")
                            DYAE_CTCAE_portal_htn = st.selectbox(
                                "30DYAE_portal_htn CTCAE",
                                options=["0","1","2","3","4","5"],
                            index=["0","1","2","3","4","5"].index(df.iloc[0]["30DY_AE_Portalhtn"]) if df.iloc[0]["30DY_AE_Portalhtn"] else None,
                            placeholder="Choose an option",
                            )
                            DYAE_CTCAE_Vascular_comp = st.selectbox(
                                "30DYAE_Vascular comp CTCAE",
                                options=["0","1","2","3","4","5"],
                            index=["0","1","2","3","4","5"].index(df.iloc[0]["30DY_AE_Vascularcomp"]) if df.iloc[0]["30DY_AE_Vascularcomp"] else None,
                            placeholder="Choose an option",
                            )
                            DYAE_CTCAE_fatigue = st.selectbox(
                                "30DYAE_fatigue CTCAE",
                                options=["0","1","2"],
                            index=["0","1","2"].index(df.iloc[0]["30DY_AE_Fatigue"]) if df.iloc[0]["30DY_AE_Fatigue"] else None,
                            placeholder="Choose an option",
                            )
                            DYAE_CTCAE_diarrhea = st.selectbox(
                                "30DYAE_diarrhea CTCAE",
                                options=["0","1","2","3","4","5"],
                            index=["0","1","2","3","4","5"].index(df.iloc[0]["30DY_AE_Diarrhea"]) if df.iloc[0]["30DY_AE_Diarrhea"] else None,
                            placeholder="Choose an option",
                            )
                            DYAE_CTCAE_hypoalbuminemia_emr = st.text_input(
                                "30DYAE_hypoalbuminemia CTCAE",
                                value=df.iloc[0]["30DY_AE_Hypoalbuminemia"]
                            )
                            DYAE_CTCAE_hyperbilirubinemia_emr = st.text_input(
                                "30DYAE_hyperbilirubinemia CTCAE",
                                value=df.iloc[0]["30DY_AE_Hyperbilirubinemia"]
                            )
                            DYAE_CTCAE_Increase_creatinine_emr = st.text_input(
                                "30DYAE_Increase_creatinine CTCAE",
                                value=df.iloc[0]["30DY_AE_Increasecreatine"]
                            )
                            DYAE_CTCAE_abdominal_pain = st.selectbox(
                                "30DYAE_abdominal pain CTCAE",
                                options=["0","1","2","3"],
                            index=["0","1","2","3"].index(df.iloc[0]["30DY_AE_Abdominalpain"]) if df.iloc[0]["30DY_AE_Abdominalpain"] else None,
                            placeholder="Choose an option",
                            )
                            DYAE_CTCAE_sepsis = st.selectbox(
                                "30DYAE_sepsis CTCAE",
                                options=["0","3","4","5"],
                            index=["0","3","4","5"].index(df.iloc[0]["30DY_AE_Sepsis"]) if df.iloc[0]["30DY_AE_Sepsis"] else None,
                            placeholder="Choose an option",
                            )
                            DYAE_CTCAE_bacterial_peritonitis = st.selectbox(
                                "30DYAE_CTCAE_bacterial_peritonitis",
                                options=["0", "3", "4", "5"],
                            index=["0", "3", "4", "5"].index(df.iloc[0]["30DY_AE_BacterialPer"]) if df.iloc[0]["30DY_AE_BacterialPer"] else None,
                            placeholder="Choose an option",
                            )
                            DYAE_CTCAE_hemorrhage = st.selectbox(
                            "30DYAE_CTCAE_hemorrhage",
                            options=["0", "3", "4", "5"],
                            index=["0", "3", "4", "5"].index(df.iloc[0]["30DY_AE_Hemorrhage"]) if df.iloc[0]["30DY_AE_Hemorrhage"] else None,
                            placeholder="Choose an option",
                            )
                            DYAE_CTCAE_anorexia = st.selectbox(
                                "30DYAE_CTCAE_anorexia",
                                options=["0", "1", "2", "3"],
                            index=["0", "1", "2", "3"].index(df.iloc[0]["30DY_AE_Anorexia"]) if df.iloc[0]["30DY_AE_Anorexia"] else None,
                            placeholder="Choose an option",
                            )
                            DYAE_CTCAE_intrahepatic_fistula = st.selectbox(
                                "30DYAE_CTCAE_intrahepatic_fistula",
                                options=["0","2", "3", "4", "5"],
                            index=["0","2", "3", "4", "5"].index(df.iloc[0]["30DY_AE_Intrahepaticfistula"]) if df.iloc[0]["30DY_AE_Intrahepaticfistula"] else None,
                            placeholder="Choose an option",
                            )
                            DYAE_CTCAE_constipation = st.selectbox(
                                "30DYAE_CTCAE_constipation",
                                options=["0", "1", "2", "3"],
                            index=["0", "1", "2", "3"].index(df.iloc[0]["30DY_AE_Constipation"]) if df.iloc[0]["30DY_AE_Constipation"] else None,
                            placeholder="Choose an option",
                            )
                            DYAE_CTCAE_nausea = st.selectbox(
                                "30DYAE_CTCAE_nausea",
                                options=["0", "1", "2", "3"],
                            index=["0", "1", "2", "3"].index(df.iloc[0]["30DY_AE_Nausea"]) if df.iloc[0]["30DY_AE_Nausea"] else None,
                            placeholder="Choose an option",
                            )
                            DYAE_CTCAE_vomiting = st.selectbox(
                                "30DYAE_CTCAE_vomiting",
                                options=["0","1","2", "3", "4", "5"],
                            index=["0","1","2", "3", "4", "5"].index(df.iloc[0]["30DY_AE_Vomiting"]) if df.iloc[0]["30DY_AE_Vomiting"] else None,
                            placeholder="Choose an option",
                            )
                            DYAE_CTCAE_cholecystitis = st.selectbox(
                                "30DYAE_CTCAE_cholecystitis",
                                options=["0", "2","3", "4", "5"],
                            index=["0", "2","3", "4", "5"].index(df.iloc[0]["30DY_AE_Cholecystitis"]) if df.iloc[0]["30DY_AE_Cholecystitis"] else None,
                            placeholder="Choose an option",
                            )
                            DYAE_CTCAE_gastric_ulcers = st.selectbox(
                                "30DYAE_CTCAE_gastric_ulcers",
                                options=["0","1","2", "3", "4", "5"],
                            index=["0","1","2", "3", "4", "5"].index(df.iloc[0]["30DY_AE_Gastriculcer"]) if df.iloc[0]["30DY_AE_Gastriculcer"] else None,
                            placeholder="Choose an option",
                            )
                            DYAE_CTCAE_hyperkalemia = st.selectbox(
                                "30DYAE_CTCAE_hyperkalemia",
                                options=["NA"],
                            index=["NA"].index(df.iloc[0]["30DY_AE_Hyperkalemia"]) if df.iloc[0]["30DY_AE_Hyperkalemia"] else None,
                            placeholder="Choose an option",
                            )
                            DYAE_CTCAE_respiratory_failure = st.selectbox(
                                "30DYAE_CTCAE_respiratory_failure",
                                options=["0", "4", "5"],
                            index=["0", "4", "5"].index(df.iloc[0]["30DY_AE_Respfailure"]) if df.iloc[0]["30DY_AE_Respfailure"] else None,
                            placeholder="Choose an option",
                            )
                            DYAE_CTCAE_AKI = st.selectbox(
                                "30DYAE_CTCAE_AKI",
                                options=["0", "3", "4", "5"],
                            index=["0", "3", "4", "5"].index(df.iloc[0]["30DY_AE_AKI"]) if df.iloc[0]["30DY_AE_AKI"] else None,
                            placeholder="Choose an option",
                            )

                            DYAE_CTCAE_Radiation_pneumonitis = st.selectbox(
                                "30DYAE_CTCAE_Radiation_pneumonitis",
                                options=["0","1","2", "3", "4", "5"],
                            index=["0","1","2", "3", "4", "5"].index(df.iloc[0]["30DY_AE_Radiationpneumonitis"]) if df.iloc[0]["30DY_AE_Radiationpneumonitis"] else None,
                            placeholder="Choose an option",
                            )

                            DYAE_AE_other = st.text_area(
                                "30DY_AE_other",
                                help="Other Adverse Events (Free Text)",
                                value=df.iloc[0]["30DY_AE_Other"]
                            )

                            DYAE_AE_date_of_AE = st.text_input(
                                "90DY_AE_date_of_AE",
                                help="(if AE is present after 30 days but before 90 write it here and the date)",
                                value=df.iloc[0]["90DY_AE_DateofAE"]
                            )
                            ken_grandedtoxicity = st.text_area(
                                "Ken_GradeandToxicity",
                                value=df.iloc[0]["Additional Notes FT"]

                            )
                            dy_ae_hospitalization_3 = st.selectbox(
                                "90DY_AE_Hospitalization 3 months",
                                options=["Yes","No"],
                                index=["Yes","No"].index(df.iloc[0]["90DY_AE_Hosp3mo"]) if df.iloc[0]["90DY_AE_Hosp3mo"] else None,
                            placeholder="Choose an option",
                            )
                            dy_ae_hospitalization_6 = st.selectbox(
                                "90DY_AE_Hospitalization 6 months",
                                options=["Yes","No"],
                                index=["Yes","No"].index(df.iloc[0]["90DY_AE_Datehosp3mo"]) if df.iloc[0]["90DY_AE_Datehosp3mo"] else None,
                            placeholder="Choose an option",
                            )
                            dy_ae_hosp6mo = st.selectbox(
                                "90DY_AE_Hosp6mo",
                                options=["Yes","No"],
                                index=["Yes","No"].index(df.iloc[0]["90DY_AE_Hosp6mo"]) if df.iloc[0]["90DY_AE_Hosp6mo"] else None,
                            placeholder="Choose an option",
                            )
                            dy_ae_death_due = st.selectbox(
                                "90DY_AE_Death due to AE",
                                options=["Yes","No"],
                                index=["Yes","No"].index(df.iloc[0]["90DY_AE_DeathduetoAE"]) if df.iloc[0]["90DY_AE_DeathduetoAE"] else None,
                            placeholder="Choose an option",
                            )
                            posty90_date_labs = (
                                posty90_date_labs.strftime("%Y-%m-%d")
                                if posty90_date_labs is not None
                                else None
                                )
                            posty90_afp_date = (
                                posty90_afp_date.strftime("%Y-%m-%d")
                                if posty90_afp_date is not None
                                else None
                                )
                            submit_tab8 = st.form_submit_button("Submit")

                            if submit_tab8:
                                    
                                    data8={
                                    "POSTY90_30DY_Datelabs": posty90_date_labs,
                                    "POSTY90_30DY_AFP": posty90_afp,
                                    "POSTY90_30DY_AFPdate": posty90_afp_date,
                                    "POSTY90_30DY_Sodium": posty90_sodium,
                                    "POSTY90_30DY_Creatinine": posty90_creatinine,
                                    "POSTY90_30DY_INR": posty90_inr,
                                    "POSTY90_30DY_Albumin": posty90_albumin,
                                    "POSTY90_30DY_Bilirubin": posty90_bilirubin,
                                    "POSTY90_30DY_AST": posty90_ast,
                                    "POSTY90_30DY_ALT": posty90_alt,
                                    "POSTY90_30DY_ALP": posty90_alkaline_phosphatase,
                                    "POSTY90_30DY_Leukocytes": posty90_leukocytes,
                                    "POSTY90_30DY_Platelets": posty90_platelets,
                                    "POSTY90_30DY_Potassium": posty90_potassium,
                                    "30DY_AE_AscitesCTCAE": posty90_ascites_ctcae,
                                    "30DY_AE_AscitesCTCAEnumb": posty90_ascites_classification,
                                    "30DY_AE_Ascitesdiruetics": posty90_ascites_diruetics,
                                    "30DY_AE_Ascitesparacentesis": posty90_ascites_paracentesis,
                                    "30DY_AE_Asciteshospitalization": posty90_ascites_hospitalization,
                                    "30DY_AE_HEgrade": posty90_he_grade,
                                    "30DY_AE_ascities_freetext": posty90_ascites_free_text,
                                    "POSTY90_30DY_ECOG": posty90_ecog,
                                    "POSTY90_30DY_CPclass": posty90_child_pugh_class,
                                    "POSTY90_30DY_CPcalc": posty90_child_pugh_points,
                                    "POSTY90_30DY_MELD": posty90_meld,
                                    "POSTY90_30DY_MELDNa": posty90_meld_na,
                                    "POSTY90_30DY_ALBIscore": posty90_albi_score,
                                    "POSTY90_30DY_ALBIgrade": posty90_albi_grade,
                                    "POSTY90_30DY_BCLC": posty90_bclc,
                                    "Ken_BCLCStagepost90": ken_bclc_stage_post90,
                                    "Ken_MELD_Stagepost90": ken_meld_stage_post90,
                                    "30DY_AE_Portalhtn": DYAE_CTCAE_portal_htn,
                                    "30DY_AE_Vascularcomp": DYAE_CTCAE_Vascular_comp,
                                    "30DY_AE_Fatigue": DYAE_CTCAE_fatigue,
                                    "30DY_AE_Diarrhea": DYAE_CTCAE_diarrhea,
                                    "30DY_AE_Hypoalbuminemia": DYAE_CTCAE_hypoalbuminemia_emr,
                                    "30DY_AE_Hyperbilirubinemia": DYAE_CTCAE_hyperbilirubinemia_emr,
                                    "30DY_AE_Increasecreatine": DYAE_CTCAE_Increase_creatinine_emr,
                                    "30DY_AE_Abdominalpain": DYAE_CTCAE_abdominal_pain,
                                    "30DY_AE_Sepsis": DYAE_CTCAE_sepsis,
                                    "30DY_AE_BacterialPer": DYAE_CTCAE_bacterial_peritonitis,
                                    "30DY_AE_Hemorrhage": DYAE_CTCAE_hemorrhage,
                                    "30DY_AE_Anorexia": DYAE_CTCAE_anorexia,
                                    "30DY_AE_Intrahepaticfistula": DYAE_CTCAE_intrahepatic_fistula,
                                    "30DY_AE_Constipation": DYAE_CTCAE_constipation,
                                    "30DY_AE_Nausea": DYAE_CTCAE_nausea,
                                    "30DY_AE_Vomiting": DYAE_CTCAE_vomiting,
                                    "30DY_AE_Cholecystitis": DYAE_CTCAE_cholecystitis,
                                    "30DY_AE_Gastriculcer": DYAE_CTCAE_gastric_ulcers,
                                    "30DY_AE_Hyperkalemia": DYAE_CTCAE_hyperkalemia,
                                    "30DY_AE_Respfailure": DYAE_CTCAE_respiratory_failure,
                                    "30DY_AE_AKI": DYAE_CTCAE_AKI,
                                    "30DY_AE_Radiationpneumonitis": DYAE_CTCAE_Radiation_pneumonitis,
                                    "30DY_AE_Other": DYAE_AE_other,
                                    "90DY_AE_DateofAE": DYAE_AE_date_of_AE,
                                    "Additional Notes FT": ken_grandedtoxicity,
                                    "90DY_AE_Hosp3mo": dy_ae_hospitalization_3,
                                    "90DY_AE_Datehosp3mo": dy_ae_hospitalization_6,
                                    "90DY_AE_Hosp6mo": dy_ae_hosp6mo,
                                    "90DY_AE_DeathduetoAE": dy_ae_death_due
                                    }
                                    update_google_sheet(data8, mrn)                             
                                
                    elif st.session_state.selected_tab == "Other Post Tare":
                        st.subheader("Other_post_TARE")
                        with st.form("other_post_tare_form"):
                            oc_liver_transplant = st.radio("OC_Liver_transplant", options=["yes", "no"])
                            oc_liver_transplant_date = st.date_input("OC_Liver_transplant_date")
                            st.subheader("K_other")
                
                            k_ken_toxgtg3 = st.number_input("K_ken_ToxgtG3",step=0.1, value = float(df.iloc[0]["K_ken_ToxgtG3"]) if pd.notnull(df.iloc[0]["K_ken_ToxgtG3"]) and df.iloc[0]["K_ken_ToxgtG3"] != ""  else 0.0)
                            if k_ken_toxgtg3 > 3:
                                k_ken_toxgtg3 = 1
                            else:
                                k_ken_toxgtg3 =0
                            k_ken_toxgtg2 = st.number_input("K_ken_ToxgtG2",step=0.1,value = float(df.iloc[0]["K_ken_ToxgtG2"]) if pd.notnull(df.iloc[0]["K_ken_ToxgtG2"]) and df.iloc[0]["K_ken_ToxgtG2"] != ""  else 0.0)
                            if k_ken_toxgtg2 > 2:
                                k_ken_toxgtg2 = 1
                            else:
                                k_ken_toxgtg2 =0

                            def albigrade(intx):
                                if intx <= -2.60:
                                    return "Grade 1"
                                elif -2.60 < intx <= -1.39:
                                    return "Grade 2"
                                else:
                                    return "Grade 3"
                            try : 
                                prey90_bilirubin = df.loc[df["MRN"] == mrn,'PREY90_Bilirubin']
                                prey90_albumin = df.loc[df["MRN"] == mrn,'PREY90_Albumin']
                                k_ken_albipretareraw = albi_calc(prey90_bilirubin,prey90_albumin)
                                st.write("K_ken_AlbiPreTARERaw : ", k_ken_albipretareraw)
                                k_ken_albipretaregrade = albigrade(k_ken_albipretareraw)
                                st.write("K_ken_AlbiPreTAREGrade: ",k_ken_albipretaregrade)
                            except:
                                st.warning("Fill Pre Y90 Tab")
                            try :
                                posty90_bilirubin = df.loc[df["MRN"] == mrn,'POSTY90_30DY_Bilirubin']
                                posty90_albumin = df.loc[df["MRN"] == mrn,'POSTY90_30DY_Albumin']
                                k_ken_albiposttareraw = albi_calc(posty90_bilirubin,posty90_albumin)
                                st.write("K_ken_AlbiPostTARERaw : ", k_ken_albiposttareraw)
                                k_ken_albiposttaregrade = albigrade(k_ken_albiposttareraw)
                                st.write("K_ken_AliPostTAREGrade : ", k_ken_albiposttaregrade)
                            except :
                                st.warning("Fill Post 90 Form")
                            oc_liver_transplant_date
                            oc_liver_transplant_date = (
                                oc_liver_transplant_date.strftime("%Y-%m-%d")
                                if oc_liver_transplant_date is not None
                                else None
                                )
                            submit_tab9 = st.form_submit_button("Submit")
                            if submit_tab9:
                                data9={
                                "OC_Liver_transplant": oc_liver_transplant,
                                "OC_Liver_transplant_date": oc_liver_transplant_date,
                                "K_ken_ToxgtG3": k_ken_toxgtg3,
                                "K_ken_ToxgtG2": k_ken_toxgtg2,
                                "K_ken_AlbiPreTARERaw": k_ken_albipretareraw,
                                "K_ken_AlbiPreTAREGrade": k_ken_albipretaregrade,
                                "K_ken_AlbiPostTARERaw": k_ken_albiposttareraw,
                                "K_ken_AliPostTAREGrade": k_ken_albiposttaregrade
                                }
                                update_google_sheet(data9,mrn)
                            
                    elif st.session_state.selected_tab == "Imaging Date":
                        st.subheader("Imaging Date")
                        with st.form("imaging_date_form"):
                                PREY90_prescan_modality = st.selectbox(
                                        "PREY90_prescan_modality",
                                        options=["CT","MRI"],
                                index=["CT","MRI"].index(df.iloc[0]["PREY90_prescan_modality"]) if df.iloc[0]["PREY90_prescan_modality"] else None,
                                placeholder="Choose an option",
                                )
                                PREY90_Imaging_Date = st.date_input("PREY90_Imaging Date" ,value = datetime.strptime(df.iloc[0]["PREY90_Imaging Date"], "%Y-%m-%d").date() if df.iloc[0]["PREY90_Imaging Date"] else None
                                )
                                PREY90_total_number_of_lesions = st.selectbox(
                                        "PREY90_total number of lesions",
                                        options=["1","2",">3"],
                                index=["1","2",">3"].index(df.iloc[0]["PREY90_total number of lesions"]) if df.iloc[0]["PREY90_total number of lesions"] else None,
                                placeholder="Choose an option",
                                )
                                PREY90_Number_Involved_Lobes = st.selectbox(
                                        "PREY90_Number Involved Lobes",
                                        options=["Unilobar","Bilobar"],
                                index=["Unilobar","Bilobar"].index(df.iloc[0]["PREY90_Number Involved Lobes"]) if df.iloc[0]["PREY90_Number Involved Lobes"] else None,
                                placeholder="Choose an option",
                                )
                                prey90_sx = df.loc[df["MRN"] == mrn, "PREY90_target_lesion_1_segments"].values[0]
                                if prey90_sx:
                                    # If complications is a string, split it into a list and strip spaces
                                    prey90_sx_list = [comp.strip() for comp in prey90_sx.split(',')] if isinstance(prey90_sx, str) else prey90_sx
                                else:
                                    prey90_sx_list = []
                                valid_prey90_sx = ["1","2","3","4a","4b","5","6","7","8","NA"]
                                prey90_sx_list = [comp for comp in prey90_sx_list if comp in valid_prey90_sx]
                                PREY90_target_lesion_1_segments = st.multiselect(
                                        "PREY90_target_lesion_1_segments",
                                        options=["1","2","3","4a","4b","5","6","7","8","NA"],
                                        default=prey90_sx_list,
                                        placeholder="Select all that apply"
                                )
                                PREY90_target_lesion_1_segments = ", ".join(PREY90_target_lesion_1_segments)
                                PREY90_TL1_LAD = st.number_input(
                                    "PREY90_TL1_LAD",
                                    step=0.1,
                                    value = float(df.iloc[0]["PREY90_TL1_LAD"]) if pd.notnull(df.iloc[0]["PREY90_TL1_LAD"]) and df.iloc[0]["PREY90_TL1_LAD"] != "" else 0.0
                                )
                                PREY90_Target_Lesion_1_PAD = st.number_input(
                                    "PREY90_Target Lesion 1 PAD",step=0.1,
                                    value = float(df.iloc[0]["PREY90_Target Lesion 1 PAD"]) if pd.notnull(df.iloc[0]["PREY90_Target Lesion 1 PAD"]) and df.iloc[0]["PREY90_Target Lesion 1 PAD"] != "" else 0.0
                                )
                                PREY90_Target_Lesion_1_CCD = st.number_input(
                                    "PREY90_Target Lesion 1 CCD",step=0.1,
                                     value = float(df.iloc[0]["PREY90_Target Lesion 1 CCD"]) if pd.notnull(df.iloc[0]["PREY90_Target Lesion 1 CCD"]) and df.iloc[0]["PREY90_Target Lesion 1 CCD"] != "" else 0.0
                                )
                                PREY90_Target_Lesion_1_VOL = 4/3*3.14*(PREY90_Target_Lesion_1_PAD)*(PREY90_TL1_LAD)*PREY90_Target_Lesion_1_CCD
                                st.write("PREY90_Target Lesion 1 VOL",PREY90_Target_Lesion_1_VOL)
                                PREY90_Target_Lesion_2_segments = st.selectbox(
                                        "PREY90_Target_Lesion_2_segments",
                                        options=["1","2","3","4a","4b","5","6","7","8","NA"],
                        index=["1","2","3","4a","4b","5","6","7","8","NA"].index(df.iloc[0]["PREY90_Target lesion 2 Segments"]) if df.iloc[0]["PREY90_Target lesion 2 Segments"] else None,
                        placeholder="Choose an option",
                                )
                                PREY90_Target_Lesion_2_LAD = st.number_input(
                                    "PREY90_Target_Lesion_2_LAD",step=0.1,
                                    value = float(df.iloc[0]["PREY90_Target Lesion 2 LAD"]) if pd.notnull(df.iloc[0]["PREY90_Target Lesion 2 LAD"]) and df.iloc[0]["PREY90_Target Lesion 2 LAD"] != "" else 0.0
                                )
                                PREY90_Target_Lesion_2_PAD = st.number_input(
                                    "PREY90_Target Lesion 2 PAD",
                                    step=0.1,value = float(df.iloc[0]["PREY90_Target Lesion 2 PAD"]) if pd.notnull(df.iloc[0]["PREY90_Target Lesion 2 PAD"]) and df.iloc[0]["PREY90_Target Lesion 2 PAD"] != "" else 0.0
                                )
                                PREY90_Target_Lesion_2_CCD = st.number_input(
                                    "PREY90_Target Lesion 2 CCD",
                                    step=0.1,value = float(df.iloc[0]["PREY90_Target Lesion 2 CCD"]) if pd.notnull(df.iloc[0]["PREY90_Target Lesion 2 CCD"]) and df.iloc[0]["PREY90_Target Lesion 2 CCD"] != "" else 0.0
                                )
                                PREY90_Target_Lesion_2_VOL = 4/3*3.14*(PREY90_Target_Lesion_2_PAD)*(PREY90_Target_Lesion_2_LAD)*PREY90_Target_Lesion_2_CCD
                                st.write("PREY90_Target Lesion 2 VOL",PREY90_Target_Lesion_2_VOL)
                                PREY90_pretx_targeted_Lesion_Dia_Sum = max(PREY90_TL1_LAD,PREY90_Target_Lesion_1_PAD,PREY90_Target_Lesion_1_CCD)+max(PREY90_Target_Lesion_2_PAD,PREY90_Target_Lesion_2_LAD,PREY90_Target_Lesion_2_CCD)
                                st.write("PREY90_ pretx targeted Lesion Dia Sum",PREY90_pretx_targeted_Lesion_Dia_Sum)
                                PREY90_Non_Target_Lesion_Location = st.selectbox( "PREY90_Non-Target Lesion Location" , options=["1","2","3","4a","4b","5","6","7","8","NA"],
                                index=["1","2","3","4a","4b","5","6","7","8","NA"].index(df.iloc[0]["PREY90_Non-Target Lesion Location"]) if df.iloc[0]["PREY90_Non-Target Lesion Location"] else None,
                                placeholder="Choose an option",)
                                PREY90_Non_Target_Lesion_2_LAD_Art_Enhanc = st.number_input(
                                    "PREY90_Non_Target_Lesion_2_LAD_Art_Enhanc",
                                    step=0.1,value = float(df.iloc[0]["PREY90_Non-Target Lesion 2 LAD Art Enhanc"]) if pd.notnull(df.iloc[0]["PREY90_Non-Target Lesion 2 LAD Art Enhanc"]) and df.iloc[0]["PREY90_Non-Target Lesion 2 LAD Art Enhanc"] != "" else 0.0
                                )
                                PREY90_Non_Target_Lesion_2_PAD_Art_Enhanc = st.number_input(
                                    "PREY90_Non_Target_Lesion_2_PAD_Art_Enhanc",
                                    step=0.1,value = float(df.iloc[0]["PREY90_Non-Target Lesion 2 PAD Art Enhanc"]) if pd.notnull(df.iloc[0]["PREY90_Non-Target Lesion 2 PAD Art Enhanc"]) and df.iloc[0]["PREY90_Non-Target Lesion 2 PAD Art Enhanc"] != "" else 0.0
                                )
                                PREY90_Non_Target_Lesion_2_CCD_Art_Enhanc = st.number_input(
                                    "PREY90_Non_Target_Lesion_2_CCD_Art_Enhanc",
                                    step=0.1,value = float(df.iloc[0]["PREY90_Non-Target Lesion 2 CCD Art Enhanc"]) if pd.notnull(df.iloc[0]["PREY90_Non-Target Lesion 2 CCD Art Enhanc"]) and df.iloc[0]["PREY90_Non-Target Lesion 2 CCD Art Enhanc"] != "" else 0.0
                                )
                                PREY90_Non_targeted_Lesion_Dia_Sum = max(PREY90_Non_Target_Lesion_2_PAD_Art_Enhanc,PREY90_Non_Target_Lesion_2_LAD_Art_Enhanc,PREY90_Non_Target_Lesion_2_CCD_Art_Enhanc)
                                st.write("PREY90_Non-targeted Lesion Dia Sum",PREY90_Non_targeted_Lesion_Dia_Sum)
                                PREY90_Reviewers_Initials = st.text_input(
                                    "PREY90_Reviewers Initials",
                                    help="Free-text input for reviewer name",
                                    value = df.iloc[0]["PREY90_Reviewers Initials"]
                                )
                                PREY90_Pre_Y90_Extrahepatic_Disease = st.selectbox(
                                    "PREY90_Pre Y90 Extrahepatic Disease",
                                    options=["Yes", "No", "NA"],
                        index=["No", "Yes", "NA"].index(df.iloc[0]["PREY90_Pre Y90 Extrahepatic Disease"]) if df.iloc[0]["PREY90_Pre Y90 Extrahepatic Disease"] else None,
                        placeholder="Choose an option",
                                )
                                PREY90_Pre_Y90_Extrahepatic_Disease_Location = st.text_input(
                                    "PREY90_Pre Y90 Extrahepatic Disease Location",
                                    help="Free Text",
                                    value=df.iloc[0]["PREY90_Pre Y90 Extrahepatic Disease Location"]
                                )
                                PREY90_PVT = st.selectbox(
                                    "PREY90_PVT",
                                    options=["Yes", "No", "NA"],
                        index=["Yes", "No", "NA"].index(df.iloc[0]["PREY90_PVT"]) if df.iloc[0]["PREY90_PVT"] else None,
                        placeholder="Choose an option",
                                )
                                PREY90_PVT_Location = st.selectbox(
                                    "PREY90_PVT Location",
                                    options=["RPV", "LPV"],
                        index=["RPV", "LPV"].index(df.iloc[0]["PREY90_PVT Location"]) if df.iloc[0]["PREY90_PVT Location"] else None,
                        placeholder="Choose an option",
                                )
                                PREY90_Features_of_cirrhosis = st.selectbox(
                                    "PREY90_Features of cirrhosis",
                                    options=["Yes", "No", "NA"],
                        index=["No", "Yes", "NA"].index(df.iloc[0]["PREY90_Features of cirrhosis"]) if df.iloc[0]["PREY90_Features of cirrhosis"] else None,
                        placeholder="Choose an option",
                                )
                                st.subheader("Imaging_1st_Followup")

                                FU_Scan_Modality = st.selectbox(
                                    "1st_FU_Scan Modality",
                                    options=["CT", "MRI"],
                        index=["CT", "MRI"].index(df.iloc[0]["1st_FU_Scan Modality"]) if df.iloc[0]["1st_FU_Scan Modality"] else None,
                        placeholder="Choose an option",
                                )
                                FU_Imaging_Date = st.date_input("1st_FU_Imaging Date",value = datetime.strptime(df.iloc[0]["1st_FU_Imaging Date"], "%Y-%m-%d").date() if df.iloc[0]["1st_FU_Imaging Date"] else None)
                                FU_Months_Since_Y90 = relativedelta(FU_Imaging_Date, fetch_date).months
                                st.write("1st_FU_Months Since Y90",FU_Months_Since_Y90)
                                FU_Total_number_of_lesions = st.selectbox(
                                    "1st_FU_Total number of lesions",
                                    options=["1", "2", ">3"],
                        index=["1", "2", ">3"].index(df.iloc[0]["1st_FU_Total number of lesions"]) if df.iloc[0]["1st_FU_Total number of lesions"] else None, 
                        placeholder="Choose an option",
                                )
                                FU_Target_Lesion_1_LAD_Art_Enhanc = st.number_input(
                                    "1st_FU_Target Lesion 1 LAD Art Enhanc",
                                    step=0.1,value = float(df.iloc[0]["1st_FU_Target Lesion 1 LAD Art Enhanc"]) if pd.notnull(df.iloc[0]["1st_FU_Target Lesion 1 LAD Art Enhanc"]) and df.iloc[0]["1st_FU_Target Lesion 1 LAD Art Enhanc"] != "" else 0.0
                                )
                                FU_Target_Lesion_1_PAD_Art_Enhanc = st.number_input(
                                    "1st_FU_Target Lesion 1 PAD Art Enhanc",
                                    step=0.1,value = float(df.iloc[0]["1st_FU_Target Lesion 1 PAD Art Enhanc"]) if pd.notnull(df.iloc[0]["1st_FU_Target Lesion 1 PAD Art Enhanc"]) and df.iloc[0]["1st_FU_Target Lesion 1 PAD Art Enhanc"] != "" else 0.0
                                )
                                FU_Target_Lesion_1_CCD_Art_Enhanc = st.number_input(
                                    "1st_FU_Target Lesion 1 CCD Art Enhanc",
                                    step=0.1,value = float(df.iloc[0]["1st_FU_Target Lesion 1 CCD Art Enhanc"]) if pd.notnull(df.iloc[0]["1st_FU_Target Lesion 1 CCD Art Enhanc"]) and df.iloc[0]["1st_FU_Target Lesion 1 CCD Art Enhanc"] != "" else 0.0
                                )
                                FU_Target_Lesion_2_Segments = st.selectbox(
                                    "1st_FU_Target Lesion 2 Segments",
                                    options=["1", "2", "3", "4a", "4b", "5", "6", "7", "8", "NA"],
                        index=["1", "2", "3", "4a", "4b", "5", "6", "7", "8", "NA"].index(df.iloc[0]["1st_FU_Target Lesion 2 Segments"]) if df.iloc[0]["1st_FU_Target Lesion 2 Segments"] else None,
                        placeholder="Choose an option",
                                )
                                FU_Target_Lesion_2_LAD_Art_Enhanc = st.number_input(
                                    "1st_FU_Target Lesion 2 LAD Art Enhanc",
                                    step=0.1,value = float(df.iloc[0]["1st_FU_Target Lesion 2 LAD Art Enhanc"]) if pd.notnull(df.iloc[0]["1st_FU_Target Lesion 2 LAD Art Enhanc"]) and df.iloc[0]["1st_FU_Target Lesion 2 LAD Art Enhanc"] != "" else 0.0
                                )
                                FU_Target_Lesion_2_PAD_Art_Enhanc = st.number_input(
                                    "1st_FU_Target Lesion 2 PAD Art Enhanc",
                                    step=0.1,value = float(df.iloc[0]["1st_FU_Target Lesion 2 PAD Art Enhanc"]) if pd.notnull(df.iloc[0]["1st_FU_Target Lesion 2 PAD Art Enhanc"]) and df.iloc[0]["1st_FU_Target Lesion 2 PAD Art Enhanc"] !="" else 0.0
                                )
                                FU_Target_Lesion_2_CCD_Art_Enhanc = st.number_input(
                                    "1st_FU_Target Lesion 2 CCD Art Enhanc",
                                    step=0.1,value = float(df.iloc[0]["1st_FU_Target Lesion 2 CCD Art Enhanc"]) if pd.notnull(df.iloc[0]["1st_FU_Target Lesion 2 CCD Art Enhanc"]) and df.iloc[0]["1st_FU_Target Lesion 2 CCD Art Enhanc"] !="" else 0.0
                                )
                                FU_Follow_up_1_targeted_Lesion_Dia_Sum = max(FU_Target_Lesion_1_CCD_Art_Enhanc,FU_Target_Lesion_1_PAD_Art_Enhanc,FU_Target_Lesion_1_LAD_Art_Enhanc)+max(FU_Target_Lesion_2_CCD_Art_Enhanc,FU_Target_Lesion_2_PAD_Art_Enhanc,FU_Target_Lesion_2_LAD_Art_Enhanc)
                                st.write("1st_FU_Follow up 1 targeted Lesion Dia Sum",FU_Follow_up_1_targeted_Lesion_Dia_Sum)
                                FU_Non_Target_Lesion_2_LAD_Art_Enhanc = st.number_input(
                                    "1st_FU_Non-Target Lesion 2 LAD Art Enhanc",
                                    step=0.1,value = float(df.iloc[0]["1st_FU_Non-Target Lesion 2 LAD Art Enhanc"]) if pd.notnull(df.iloc[0]["1st_FU_Non-Target Lesion 2 LAD Art Enhanc"]) and df.iloc[0]["1st_FU_Non-Target Lesion 2 LAD Art Enhanc"] !="" else 0.0
                                )
                                FU_Non_Target_Lesion_2_PAD_Art_Enhanc = st.number_input(
                                    "1st_FU_Non-Target Lesion 2 PAD Art Enhanc",
                                    step=0.1,value = float(df.iloc[0]["1st_FU_Non-Target Lesion 2 PAD Art Enhanc"]) if pd.notnull(df.iloc[0]["1st_FU_Non-Target Lesion 2 PAD Art Enhanc"]) and df.iloc[0]["1st_FU_Non-Target Lesion 2 PAD Art Enhanc"] !="" else 0.0
                                )
                                FU_Non_Target_Lesion_2_CCD_Art_Enhanc = st.number_input(
                                    "1st_FU_Non-Target Lesion 2 CCD Art Enhanc",
                                    step=0.1,value = float(df.iloc[0]["1st_FU_Non-Target Lesion 2 CCD Art Enhanc"]) if pd.notnull(df.iloc[0]["1st_FU_Non-Target Lesion 2 CCD Art Enhanc"]) and df.iloc[0]["1st_FU_Non-Target Lesion 2 CCD Art Enhanc"] !=""  else 0.0
                                )
                                FU_Non_targeted_Lesion_Dia_Sum = max(FU_Non_Target_Lesion_2_LAD_Art_Enhanc,FU_Non_Target_Lesion_2_PAD_Art_Enhanc,FU_Non_Target_Lesion_2_CCD_Art_Enhanc)
                                st.write("1st_FU_Non-targeted Lesion Dia Sum",FU_Non_targeted_Lesion_Dia_Sum)
                                FU_Lesion_Necrosis = st.selectbox(
                                    "1st_FU_Lesion Necrosis",
                                    options=["No", "Yes", "NA"],
                        index=["No", "Yes", "NA"].index(df.iloc[0]["1st_FU_Lesion Necrosis"]) if df.iloc[0]["1st_FU_Lesion Necrosis"] else None,
                        placeholder="Choose an option",
                                )
                                FU_Reviewers_Initials = st.text_input(
                                    "1st_FU_Reviewers Initials",
                                    help="Free-text input for reviewer name",
                                    value = df.iloc[0]["1st_FU_Reviewers Initials"]
                                )
                                FU_Non_target_lesion_response = st.selectbox(
                                    "1st_FU_Non target lesion response",
                                    options=["No", "Yes", "NA"],
                        index=["No", "Yes", "NA"].index(df.iloc[0]["1st_FU_Non target lesion response"]) if df.iloc[0]["1st_FU_Non target lesion response"] else None,
                        placeholder="Choose an option",
                                )
                                FU_New_Lesions = st.selectbox(
                                    "1st_FU_New Lesions",
                                    options=["No", "Yes", "NA"],
                        index=["No", "Yes", "NA"].index(df.iloc[0]["1st_FU_New Lesions"]) if df.iloc[0]["1st_FU_New Lesions"] else None,
                        placeholder="Choose an option",
                                )
                                FU_NEW_Extrahepatic_Disease = st.selectbox(
                                    "1st_FU_NEW Extrahepatic Disease",
                                    options=["No", "Yes", "NA"],
                        index=["No", "Yes", "NA"].index(df.iloc[0]["1st_FU_NEW Extrahepatic Disease"]) if df.iloc[0]["1st_FU_NEW Extrahepatic Disease"] else None,
                        placeholder="Choose an option",
                                )
                                FU_NEW_Extrahepatic_Dz_Location = st.text_input(
                                    "1st_FU_NEW Extrahepatic Dz Location",
                                    help="Free text",
                                    value=df.iloc[0]["1st_FU_NEW Extrahepatic Dz Location"]
                                )
                                FU_NEW_Extrahepatic_Dz_Date = st.date_input("1st_FU_NEW Extrahepatic Dz Date",value = datetime.strptime(df.iloc[0]["1st_FU_NEW Extrahepatic Dz Date"], "%Y-%m-%d").date() if df.iloc[0]["1st_FU_NEW Extrahepatic Dz Date"] else None)
                                FU_change_non_target_lesion = ((PREY90_Non_targeted_Lesion_Dia_Sum - FU_Non_targeted_Lesion_Dia_Sum)/max(1,PREY90_pretx_targeted_Lesion_Dia_Sum))*100
                                st.write("1st_FU_% change for non target lesion",FU_change_non_target_lesion)
                                FU_change_target_lesion = ((PREY90_pretx_targeted_Lesion_Dia_Sum - FU_Follow_up_1_targeted_Lesion_Dia_Sum)/max(1,PREY90_pretx_targeted_Lesion_Dia_Sum))*100
                                st.write("1st_FU_% Change Target Dia",FU_change_target_lesion)
                                first_fu_mrecist_localized = st.text_input("1st_FU_mRECIST LOCALIZED",value=df.iloc[0]["1st_FU_mRECIST LOCALIZED"])
                                first_fu_mrecist_overall = st.text_input("1st_FU_mRECIST Overall",value=df.iloc[0]["1st_FU_mRECIST Overall"])
                                FU_Free_Text = st.text_area(
                                    "1st_FU_Free Text",
                                    help="Free text",
                                    value = df.iloc[0]["1st_FU_Free Text"]
                                )
                                st.subheader("Imaging_2nd_Followup")

                                FU2_Scan_Modality = st.selectbox(
                                    "2nd_FU_Scan Modality",
                                    options=["CT", "MRI"],
                                    index=["CT", "MRI"].index(df.iloc[0]["2nd_FU_Scan Modality"]) if df.iloc[0]["2nd_FU_Scan Modality"] else None,
                        placeholder="Choose an option",
                                )
                                FU2_Imaging_Date = st.date_input("2nd_FU_Imaging Date",value = datetime.strptime(df.iloc[0]["2nd_FU_Imaging Date"], "%Y-%m-%d").date() if df.iloc[0]["2nd_FU_Imaging Date"] else None)

                                FU2_Months_Since_Y90 = relativedelta(FU2_Imaging_Date, fetch_date).months
                                st.write("2nd_FU_Months Since Y90",FU2_Months_Since_Y90)
                                FU2_Total_number_of_lesions = st.selectbox(
                                    "2nd_FU_Total number of lesions",
                                    options=["1", "2", ">3"],
                        index=["1", "2", ">3"].index(df.iloc[0]["2nd_FU_Total number of lesions"]) if df.iloc[0]["2nd_FU_Total number of lesions"] else None, 
                        placeholder="Choose an option",
                                )
                                FU2_Target_Lesion_1_LAD_Art_Enhanc = st.number_input(
                                    "2nd_FU_Target Lesion 1 LAD Art Enhanc",
                                    step=0.1,value = float(df.iloc[0]["2nd_FU_Target Lesion 1 LAD Art Enhanc"]) if pd.notnull(df.iloc[0]["2nd_FU_Target Lesion 1 LAD Art Enhanc"]) and df.iloc[0]["2nd_FU_Target Lesion 1 LAD Art Enhanc"] !="" else 0.0
                                )
                                FU2_Target_Lesion_1_PAD_Art_Enhanc = st.number_input(
                                    "2nd_FU_Target Lesion 1 PAD Art Enhanc",
                                    step=0.1,value = float(df.iloc[0]["2nd_FU_Target Lesion 1 PAD Art Enhanc"]) if pd.notnull(df.iloc[0]["2nd_FU_Target Lesion 1 PAD Art Enhanc"]) and df.iloc[0]["2nd_FU_Target Lesion 1 PAD Art Enhanc"] != "" else 0.0
                                )

                                FU2_Target_Lesion_1_CCD_Art_Enhanc = st.number_input(
                                    "2nd_FU_Target Lesion 1 CCD Art Enhanc",
                                    step=0.1,value = float(df.iloc[0]["2nd_FU_Target Lesion 1 CCD Art Enhanc"]) if pd.notnull(df.iloc[0]["2nd_FU_Target Lesion 1 CCD Art Enhanc"]) and df.iloc[0]["2nd_FU_Target Lesion 1 CCD Art Enhanc"]!="" else 0.0
                                )

                                FU2_Target_Lesion_2_Segments = st.selectbox(
                                    "2nd_FU_Target Lesion 2 Segments",
                                    options=["1", "2", "3", "4a", "4b", "5", "6", "7", "8", "NA"],
                        index=["1", "2", "3", "4a", "4b", "5", "6", "7", "8", "NA"].index(df.iloc[0]["2nd_FU_Target Lesion 2 Segments"]) if df.iloc[0]["2nd_FU_Target Lesion 2 Segments"] else None,
                        placeholder="Choose an option",
                                )

                                FU2_Target_Lesion_2_LAD_Art_Enhanc = st.number_input(
                                    "2nd_FU_Target Lesion 2 LAD Art Enhanc",
                                    step=0.1,value = float(df.iloc[0]["2nd_FU_Target Lesion 2 LAD Art Enhanc"]) if pd.notnull(df.iloc[0]["2nd_FU_Target Lesion 2 LAD Art Enhanc"]) and df.iloc[0]["2nd_FU_Target Lesion 2 LAD Art Enhanc"] !="" else 0.0
                                )

                                FU2_Target_Lesion_2_PAD_Art_Enhanc = st.number_input(
                                    "2nd_FU_Target Lesion 2 PAD Art Enhanc",
                                    step=0.1,value = float(df.iloc[0]["2nd_FU_Target Lesion 2 PAD Art Enhanc"]) if pd.notnull(df.iloc[0]["2nd_FU_Target Lesion 2 PAD Art Enhanc"]) and df.iloc[0]["2nd_FU_Target Lesion 2 PAD Art Enhanc"]!="" else 0.0
                                )

                                FU2_Target_Lesion_2_CCD_Art_Enhanc = st.number_input(
                                    "2nd_FU_Target Lesion 2 CCD Art Enhanc",
                                    step=0.1,value = float(df.iloc[0]["2nd_FU_Target Lesion 2 CCD Art Enhanc"]) if pd.notnull(df.iloc[0]["2nd_FU_Target Lesion 2 CCD Art Enhanc"]) and df.iloc[0]["2nd_FU_Target Lesion 2 CCD Art Enhanc"] !="" else 0.0
                                )

                                FU2_Follow_up_2_targeted_Lesion_Dia_Sum = max(FU2_Target_Lesion_1_CCD_Art_Enhanc, FU2_Target_Lesion_1_PAD_Art_Enhanc, FU2_Target_Lesion_1_LAD_Art_Enhanc) + max(FU2_Target_Lesion_2_CCD_Art_Enhanc, FU2_Target_Lesion_2_PAD_Art_Enhanc, FU2_Target_Lesion_2_LAD_Art_Enhanc)
                                st.write("2nd_FU_Follow up 2 targeted Lesion Dia Sum",FU2_Follow_up_2_targeted_Lesion_Dia_Sum)
                                FU2_Non_Target_Lesion_1_LAD_Art_Enhanc = st.number_input(
                                    "2nd_FU_Non-Target Lesion 1 LAD Art Enhanc",
                                    step=0.1,value = float(df.iloc[0]["2nd_FU_Non-Target Lesion 1 LAD Art Enhanc"]) if pd.notnull(df.iloc[0]["2nd_FU_Non-Target Lesion 1 LAD Art Enhanc"]) and df.iloc[0]["2nd_FU_Non-Target Lesion 1 LAD Art Enhanc"] !="" else 0.0
                                )

                                FU2_Non_Target_Lesion_1_PAD_Art_Enhanc = st.number_input(
                                    "2nd_FU_Non-Target Lesion 1 PAD Art Enhanc",
                                    step=0.1,value = float(df.iloc[0]["2nd_FU_Non-Target Lesion 1 PAD Art Enhanc"]) if pd.notnull(df.iloc[0]["2nd_FU_Non-Target Lesion 1 PAD Art Enhanc"]) and df.iloc[0]["2nd_FU_Non-Target Lesion 1 PAD Art Enhanc"] !="" else 0.0
                                )

                                FU2_Non_Target_Lesion_1_CCD_Art_Enhanc = st.number_input(
                                    "2nd_FU_Non-Target Lesion 1 CCD Art Enhanc",
                                    step=0.1,value = float(df.iloc[0]["2nd_FU_Non-Target Lesion 1 CCD Art Enhanc"]) if pd.notnull(df.iloc[0]["2nd_FU_Non-Target Lesion 1 CCD Art Enhanc"]) and df.iloc[0]["2nd_FU_Non-Target Lesion 1 CCD Art Enhanc"] !="" else 0.0
                                )

                                FU2_Non_targeted_Lesion_Dia_Sum = max(FU2_Non_Target_Lesion_1_LAD_Art_Enhanc, FU2_Non_Target_Lesion_1_PAD_Art_Enhanc, FU2_Non_Target_Lesion_1_CCD_Art_Enhanc)
                                st.write("2nd_FU_Non-targeted Lesion Dia Sum",FU2_Non_targeted_Lesion_Dia_Sum)
                                FU2_Lesion_Necrosis = st.selectbox(
                                    "2nd_FU_Lesion Necrosis",
                                    options=["No", "Yes", "NA"],
                                    index=["No", "Yes", "NA"].index(df.iloc[0]["2nd_FU_Lesion Necrosis"]) if df.iloc[0]["2nd_FU_Lesion Necrosis"] else None,
                                    placeholder="Choose an option",
                                )

                                FU2_Reviewers_Initials = st.text_input(
                                    "2nd_FU_Reviewers Initials",
                                    help="Free-text input for reviewer name",
                                    value = df.iloc[0]["2nd_FU_Reviewers Initials"]
                                )

                                FU2_Non_target_lesion_response = st.selectbox(
                                    "2nd_FU_Non target lesion response",
                                    options=["No", "Yes", "NA"],
                                    index=["No", "Yes", "NA"].index(df.iloc[0]["2nd_FU_Non target lesion response"]) if df.iloc[0]["2nd_FU_Non target lesion response"] else None,
                                    placeholder="Choose an option",
                                )

                                FU2_New_Lesions = st.selectbox(
                                    "2nd_FU_New Lesions",
                                    options=["No", "Yes", "NA"],
                        index=["No", "Yes", "NA"].index(df.iloc[0]["2nd_FU_New Lesions"]) if df.iloc[0]["2nd_FU_New Lesions"] else None,
                        placeholder="Choose an option",
                                )

                                FU2_NEW_Extrahepatic_Disease = st.selectbox(
                                    "2nd_FU_NEW Extrahepatic Disease",
                                    options=["No", "Yes", "NA"],
                        index=["No", "Yes", "NA"].index(df.iloc[0]["2nd_FU_Extrahepatic Disease"]) if df.iloc[0]["2nd_FU_Extrahepatic Disease"] else None,
                        placeholder="Choose an option",
                                )

                                FU2_NEW_Extrahepatic_Dz_Location = st.text_input(
                                    "2nd_FU_NEW Extrahepatic Dz Location",
                                    help="Free text",
                                    value=df.iloc[0]["2nd_FU_NEW Extrahepatic Dz Location"]
                                )

                                FU2_NEW_Extrahepatic_Dz_Date = st.date_input("2nd_FU_NEW Extrahepatic Dz Date",value = datetime.strptime(df.iloc[0]["2nd_FU_NEW Extrahepatic Dz Date"], "%Y-%m-%d").date() if df.iloc[0]["2nd_FU_NEW Extrahepatic Dz Date"] else None)

                                FU2_change_non_target_lesion = ((PREY90_Non_targeted_Lesion_Dia_Sum - FU2_Non_targeted_Lesion_Dia_Sum) / max(1,PREY90_pretx_targeted_Lesion_Dia_Sum)) * 100
                                st.write("2nd_FU_% change for non target lesion",FU2_change_non_target_lesion)
                                FU2_change_target_lesion = ((PREY90_pretx_targeted_Lesion_Dia_Sum - FU2_Follow_up_2_targeted_Lesion_Dia_Sum) / max(1,PREY90_pretx_targeted_Lesion_Dia_Sum)) * 100
                                st.write("2nd_FU_% Change Target Dia",FU2_change_target_lesion)
                                second_fu_mrecist_calc = st.text_input("2nd_FU_mRECIST Calc",value=df.iloc[0]["2nd_FU_mRECIST Calc"])
                                second_fu_mrecist_localized = st.text_input("2nd_FU_mRECIST LOCALIZED",value=df.iloc[0]["2nd_FU_mRECIST LOCALIZED"])
                                second_fu_mrecist_overall = st.text_input("2nd_FU_mRECIST Overall",value=df.iloc[0]["2nd_FU_mRECIST Overall"])
                                FU2_Free_Text = st.text_area(
                                    "2nd_FU_Free Text",
                                    help="Free text",
                                    value = df.iloc[0]["2nd_FU_Free Text"]
                                )

                               
                                st.subheader("Imaging_3rd_Followup")

                                FU3_Scan_Modality = st.selectbox(
                                    "3rd_FU_Scan Modality",
                                    options=["CT", "MRI"],
                        index=["CT", "MRI"].index(df.iloc[0]["3rd_FU_Scan Modality"]) if df.iloc[0]["3rd_FU_Scan Modality"] else None,
                        placeholder="Choose an option",
                                )

                                FU3_Imaging_Date = st.date_input("3rd_FU_Imaging Date",value = datetime.strptime(df.iloc[0]["3rd_FU_Imaging Date"], "%Y-%m-%d").date() if df.iloc[0]["3rd_FU_Imaging Date"] else None)

                                FU3_Months_Since_Y90 = relativedelta(FU3_Imaging_Date, fetch_date).months
                                st.write("3rd_FU_Months Since Y90",FU3_Months_Since_Y90)
                                FU3_Total_number_of_lesions = st.selectbox(
                                    "3rd_FU_Total number of lesions",
                                    options=["1", "2", ">3"],
                        index=["1", "2", ">3"].index(df.iloc[0]["3rd_FU_Total number of lesions"]) if df.iloc[0]["3rd_FU_Total number of lesions"] else None, 
                        placeholder="Choose an option",
                                )

                                FU3_Target_Lesion_1_LAD_Art_Enhanc = st.number_input(
                                    "3rd_FU_Target Lesion 1 LAD Art Enhanc",
                                    step=0.1,value = float(df.iloc[0]["3rd_FU_Target Lesion 1 LAD Art Enhanc"]) if pd.notnull(df.iloc[0]["3rd_FU_Target Lesion 1 LAD Art Enhanc"]) and df.iloc[0]["3rd_FU_Target Lesion 1 LAD Art Enhanc"] !="" else 0.0
                                )

                                FU3_Target_Lesion_1_PAD_Art_Enhanc = st.number_input(
                                    "3rd_FU_Target Lesion 1 PAD Art Enhanc",
                                    step=0.1,value = float(df.iloc[0]["3rd_FU_Target Lesion 1 PAD Art Enhanc"]) if pd.notnull(df.iloc[0]["3rd_FU_Target Lesion 1 PAD Art Enhanc"]) and df.iloc[0]["3rd_FU_Target Lesion 1 PAD Art Enhanc"] !="" else 0.0
                                )

                                FU3_Target_Lesion_1_CCD_Art_Enhanc = st.number_input(
                                    "3rd_FU_Target Lesion 1 CCD Art Enhanc",
                                    step=0.1,value = float(df.iloc[0]["3rd_FU_Target Lesion 1 CCD Art Enhanc"]) if pd.notnull(df.iloc[0]["3rd_FU_Target Lesion 1 CCD Art Enhanc"]) and df.iloc[0]["3rd_FU_Target Lesion 1 CCD Art Enhanc"] !="" else 0.0
                                )

                                FU3_Target_Lesion_2_Segments = st.selectbox(
                                    "3rd_FU_Target Lesion 2 Segments",
                                    options=["1", "2", "3", "4a", "4b", "5", "6", "7", "8", "NA"],
                        index=["1", "2", "3", "4a", "4b", "5", "6", "7", "8", "NA"].index(df.iloc[0]["3rd_FU_Target Lesion 2 Segments"]) if df.iloc[0]["3rd_FU_Target Lesion 2 Segments"] else None,
                        placeholder="Choose an option",
                                )

                                FU3_Target_Lesion_2_LAD_Art_Enhanc = st.number_input(
                                    "3rd_FU_Target Lesion 2 LAD Art Enhanc",
                                    step=0.1,value = float(df.iloc[0]["3rd_FU_Target Lesion 2 LAD Art Enhanc"]) if pd.notnull(df.iloc[0]["3rd_FU_Target Lesion 2 LAD Art Enhanc"]) and df.iloc[0]["3rd_FU_Target Lesion 2 LAD Art Enhanc"] !="" else 0.0
                                )

                                FU3_Target_Lesion_2_PAD_Art_Enhanc = st.number_input(
                                    "3rd_FU_Target Lesion 2 PAD Art Enhanc",
                                    step=0.1,value = float(df.iloc[0]["3rd_FU_Target Lesion 2 PAD Art Enhanc"]) if pd.notnull(df.iloc[0]["3rd_FU_Target Lesion 2 PAD Art Enhanc"]) and df.iloc[0]["3rd_FU_Target Lesion 2 PAD Art Enhanc"] !="" else 0.0
                                )

                                FU3_Target_Lesion_2_CCD_Art_Enhanc = st.number_input(
                                    "3rd_FU_Target Lesion 2 CCD Art Enhanc",
                                    step=0.1,value = float(df.iloc[0]["3rd_FU_Target Lesion 2 CCD Art Enhanc"]) if pd.notnull(df.iloc[0]["3rd_FU_Target Lesion 2 CCD Art Enhanc"]) and df.iloc[0]["3rd_FU_Target Lesion 2 CCD Art Enhanc"] !="" else 0.0
                                )

                                FU3_Follow_up_2_targeted_Lesion_Dia_Sum = max(FU3_Target_Lesion_1_CCD_Art_Enhanc, FU3_Target_Lesion_1_PAD_Art_Enhanc, FU3_Target_Lesion_1_LAD_Art_Enhanc) + max(FU3_Target_Lesion_2_CCD_Art_Enhanc, FU3_Target_Lesion_2_PAD_Art_Enhanc, FU3_Target_Lesion_2_LAD_Art_Enhanc)
                                st.write("3rd_FU_Follow up 3 targeted Lesion Dia Sum",FU3_Follow_up_2_targeted_Lesion_Dia_Sum)
                                FU3_Non_Target_Lesion_1_LAD_Art_Enhanc = st.number_input(
                                    "3rd_FU_Non-Target Lesion 1 LAD Art Enhanc",
                                    step=0.1,value = float(df.iloc[0]["3rd_FU_Non-Target Lesion 1 LAD Art Enhanc"]) if pd.notnull(df.iloc[0]["3rd_FU_Non-Target Lesion 1 LAD Art Enhanc"]) and df.iloc[0]["3rd_FU_Non-Target Lesion 1 LAD Art Enhanc"]!="" else 0.0
                                )

                                FU3_Non_Target_Lesion_1_PAD_Art_Enhanc = st.number_input(
                                    "3rd_FU_Non-Target Lesion 1 PAD Art Enhanc",
                                    step=0.1,value = float(df.iloc[0]["3rd_FU_Non-Target Lesion 1 PAD Art Enhanc"]) if pd.notnull(df.iloc[0]["3rd_FU_Non-Target Lesion 1 PAD Art Enhanc"]) and df.iloc[0]["3rd_FU_Non-Target Lesion 1 PAD Art Enhanc"] !="" else 0.0
                                )

                                FU3_Non_Target_Lesion_1_CCD_Art_Enhanc = st.number_input(
                                    "3rd_FU_Non-Target Lesion 1 CCD Art Enhanc",
                                    step=0.1,value = float(df.iloc[0]["3rd_FU_Non-Target Lesion 1 CCD Art Enhanc"]) if pd.notnull(df.iloc[0]["3rd_FU_Non-Target Lesion 1 CCD Art Enhanc"]) and df.iloc[0]["3rd_FU_Non-Target Lesion 1 CCD Art Enhanc"] !="" else 0.0
                                )
                                FU3_Non_targeted_Lesion_Dia_Sum = max(FU3_Non_Target_Lesion_1_LAD_Art_Enhanc, FU3_Non_Target_Lesion_1_PAD_Art_Enhanc, FU3_Non_Target_Lesion_1_CCD_Art_Enhanc)
                                st.write("3rd_FU_Non-targeted Lesion Dia Sum",FU3_Non_targeted_Lesion_Dia_Sum)
                                FU3_Lesion_Necrosis = st.selectbox(
                                    "3rd_FU_Lesion Necrosis",
                                    options=["No", "Yes", "NA"],
                        index=["No", "Yes", "NA"].index(df.iloc[0]["3rd_FU_Lesion Necrosis"]) if df.iloc[0]["3rd_FU_Lesion Necrosis"] else None,
                        placeholder="Choose an option",
                                )
                                FU3_Reviewers_Initials = st.text_input(
                                    "3rd_FU_Reviewers Initials",
                                    help="Free-text input for reviewer name",
                                    value = df.iloc[0]["3rd_FU_Reviewers Initials"]
                                )
                                FU3_Non_target_lesion_response = st.selectbox(
                                    "3rd_FU_Non target lesion response",
                                    options=["No", "Yes", "NA"],
                        index=["No", "Yes", "NA"].index(df.iloc[0]["3rd_FU_Non target lesion response"]) if df.iloc[0]["3rd_FU_Non target lesion response"] else None,
                        placeholder="Choose an option",
                                )
                                FU3_New_Lesions = st.selectbox(
                                    "3rd_FU_New Lesions",
                                    options=["No", "Yes", "NA"],
                        index=["No", "Yes", "NA"].index(df.iloc[0]["3rd_FU_New Lesions"]) if df.iloc[0]["3rd_FU_New Lesions"] else None,
                        placeholder="Choose an option",
                                )
                                FU3_NEW_Extrahepatic_Disease = st.selectbox(
                                    "3rd_FU_NEW Extrahepatic Disease",
                                    options=["No", "Yes", "NA"],
                        index=["No", "Yes", "NA"].index(df.iloc[0]["3rd_FU_Extrahepatic Disease"]) if df.iloc[0]["3rd_FU_Extrahepatic Disease"] else None,
                        placeholder="Choose an option",
                                )
                                FU3_NEW_Extrahepatic_Dz_Location = st.text_input(
                                    "3rd_FU_NEW Extrahepatic Dz Location",
                                    help="Free text",
                                    value=df.iloc[0]["3rd_FU_NEW Extrahepatic Dz Location"]
                                )

                                FU3_NEW_Extrahepatic_Dz_Date = st.date_input("3rd_FU_NEW Extrahepatic Dz Date",value = datetime.strptime(df.iloc[0]["3rd_FU_NEW Extrahepatic Dz Date"], "%Y-%m-%d").date() if df.iloc[0]["3rd_FU_NEW Extrahepatic Dz Date"] else None)

                                FU3_change_non_target_lesion = ((PREY90_Non_targeted_Lesion_Dia_Sum - FU3_Non_targeted_Lesion_Dia_Sum) / max(1,PREY90_pretx_targeted_Lesion_Dia_Sum)) * 100
                                st.write("3rd_FU_% change for non target lesion",FU3_change_non_target_lesion)
                                FU3_change_target_lesion = ((PREY90_pretx_targeted_Lesion_Dia_Sum - FU3_Follow_up_2_targeted_Lesion_Dia_Sum) / max(1,PREY90_pretx_targeted_Lesion_Dia_Sum)) * 100
                                st.write("3rd_FU_% Change Target Dia",FU3_change_target_lesion)
                                third_fu_mrecist_calc = st.text_input("3rd_FU_mRECIST Calc",value=df.iloc[0]["3rd_FU_mRECIST Calc"])
                                third_fu_mrecist_localized = st.text_input("3rd_FU_mRECIST LOCALIZED",value=df.iloc[0]["3rd_FU_mRECIST LOCALIZED"])
                                third_fu_mrecist_overall = st.text_input("3rd_FU_mRECIST Overall",value=df.iloc[0]["3rd_FU_mRECIST Overall"])
                                FU3_Free_Text = st.text_area(
                                    "3rd_FU_Free Text",
                                    help="Free text",
                                    value = df.iloc[0]["3rd_FU_Free Text"]
                                )
                                # 4th Imaging Follow-up
                                st.subheader("Imaging_4th_Followup")

                                FU4_Scan_Modality = st.selectbox(
                                    "4th_FU_Scan Modality",
                                    options=["CT", "MRI"],
                        index=["CT", "MRI"].index(df.iloc[0]["4th_FU_Scan Modality"]) if df.iloc[0]["4th_FU_Scan Modality"] else None, 
                        placeholder="Choose an option",
                                )

                                FU4_Imaging_Date = st.date_input("4th_FU_Imaging Date",value = datetime.strptime(df.iloc[0]["4th_FU_Imaging Date"], "%Y-%m-%d").date() if df.iloc[0]["4th_FU_Imaging Date"] else None)

                                FU4_Months_Since_Y90 = relativedelta(FU4_Imaging_Date, fetch_date).months
                                st.write("4th_FU_Months Since Y90",FU4_Months_Since_Y90)
                                FU4_Total_number_of_lesions = st.selectbox(
                                    "4th_FU_Total number of lesions",
                                    options=["1", "2", ">3"],
                        index=["1", "2", ">3"].index(df.iloc[0]["4th_FU_Total number of lesions"]) if df.iloc[0]["4th_FU_Total number of lesions"] else None,  # No default selection
                        placeholder="Choose an option",
                                )
                                FU4_Target_Lesion_1_LAD_Art_Enhanc = st.number_input(
                                    "4th_FU_Target Lesion 1 LAD Art Enhanc",
                                    step=0.1,value = float(df.iloc[0]["4th_FU_Target Lesion 1 LAD Art Enhanc"]) if pd.notnull(df.iloc[0]["4th_FU_Target Lesion 1 LAD Art Enhanc"]) and df.iloc[0]["4th_FU_Target Lesion 1 LAD Art Enhanc"]!="" else 0.0
                                )
                                FU4_Target_Lesion_1_PAD_Art_Enhanc = st.number_input(
                                    "4th_FU_Target Lesion 1 PAD Art Enhanc",
                                    step=0.1,value = float(df.iloc[0]["4th_FU_Target Lesion 1 PAD Art Enhanc"]) if pd.notnull(df.iloc[0]["4th_FU_Target Lesion 1 PAD Art Enhanc"]) and df.iloc[0]["4th_FU_Target Lesion 1 PAD Art Enhanc"] !="" else 0.0
                                )
                                FU4_Target_Lesion_1_CCD_Art_Enhanc = st.number_input(
                                    "4th_FU_Target Lesion 1 CCD Art Enhanc",
                                    step=0.1,value = float(df.iloc[0]["4th_FU_Target Lesion 1 CCD Art Enhanc"]) if pd.notnull(df.iloc[0]["4th_FU_Target Lesion 1 CCD Art Enhanc"]) and df.iloc[0]["4th_FU_Target Lesion 1 CCD Art Enhanc"] !="" else 0.0
                                )
                                FU4_Target_Lesion_2_Segments = st.selectbox(
                                    "4th_FU_Target Lesion 2 Segments",
                                    options=["1", "2", "3", "4a", "4b", "5", "6", "7", "8", "NA"],
                        index=["1", "2", "3", "4a", "4b", "5", "6", "7", "8", "NA"].index(df.iloc[0]["4th_FU_Target Lesion 2 Segments"]) if df.iloc[0]["4th_FU_Target Lesion 2 Segments"] else None,
                        placeholder="Choose an option",
                                )
                                FU4_Target_Lesion_2_LAD_Art_Enhanc = st.number_input(
                                    "4th_FU_Target Lesion 2 LAD Art Enhanc",
                                    step=0.1,value = float(df.iloc[0]["4th_FU_Target Lesion 2 LAD Art Enhanc"]) if pd.notnull(df.iloc[0]["4th_FU_Target Lesion 2 LAD Art Enhanc"]) and df.iloc[0]["4th_FU_Target Lesion 2 LAD Art Enhanc"] !="" else 0.0
                                )
                                FU4_Target_Lesion_2_PAD_Art_Enhanc = st.number_input(
                                    "4th_FU_Target Lesion 2 PAD Art Enhanc",
                                    step=0.1,value = float(df.iloc[0]["4th_FU_Target Lesion 2 PAD Art Enhanc"]) if pd.notnull(df.iloc[0]["4th_FU_Target Lesion 2 PAD Art Enhanc"]) and df.iloc[0]["4th_FU_Target Lesion 2 PAD Art Enhanc"] !="" else 0.0
                                )

                                FU4_Target_Lesion_2_CCD_Art_Enhanc = st.number_input(
                                    "4th_FU_Target Lesion 2 CCD Art Enhanc",
                                    step=0.1,value = float(df.iloc[0]["4th_FU_Target Lesion 2 CCD Art Enhanc"]) if pd.notnull(df.iloc[0]["4th_FU_Target Lesion 2 CCD Art Enhanc"]) and df.iloc[0]["4th_FU_Target Lesion 2 CCD Art Enhanc"] !="" else 0.0
                                )

                                FU4_Follow_up_2_targeted_Lesion_Dia_Sum = max(FU4_Target_Lesion_1_CCD_Art_Enhanc, FU4_Target_Lesion_1_PAD_Art_Enhanc, FU4_Target_Lesion_1_LAD_Art_Enhanc) + max(FU4_Target_Lesion_2_CCD_Art_Enhanc, FU4_Target_Lesion_2_PAD_Art_Enhanc, FU4_Target_Lesion_2_LAD_Art_Enhanc)
                                st.write("4th_FU_Follow up 4 targeted Lesion Dia Sum",FU4_Follow_up_2_targeted_Lesion_Dia_Sum)
                                FU4_Non_Target_Lesion_1_LAD_Art_Enhanc = st.number_input(
                                    "4th_FU_Non-Target Lesion 1 LAD Art Enhanc",
                                    step=0.1,value = float(df.iloc[0]["4th_FU_Non-Target Lesion 1 LAD Art Enhanc"]) if pd.notnull(df.iloc[0]["4th_FU_Non-Target Lesion 1 LAD Art Enhanc"]) and df.iloc[0]["4th_FU_Non-Target Lesion 1 LAD Art Enhanc"] !="" else 0.0
                                )

                                FU4_Non_Target_Lesion_1_PAD_Art_Enhanc = st.number_input(
                                    "4th_FU_Non-Target Lesion 1 PAD Art Enhanc",
                                    step=0.1,value = float(df.iloc[0]["4th_FU_Non-Target Lesion 1 PAD Art Enhanc"]) if pd.notnull(df.iloc[0]["4th_FU_Non-Target Lesion 1 PAD Art Enhanc"]) and df.iloc[0]["4th_FU_Non-Target Lesion 1 PAD Art Enhanc"] !="" else 0.0
                                )

                                FU4_Non_Target_Lesion_1_CCD_Art_Enhanc = st.number_input(
                                    "4th_FU_Non-Target Lesion 1 CCD Art Enhanc",
                                    step=0.1,value = float(df.iloc[0]["4th_FU_Non-Target Lesion 1 CCD Art Enhanc"]) if pd.notnull(df.iloc[0]["4th_FU_Non-Target Lesion 1 CCD Art Enhanc"]) and df.iloc[0]["4th_FU_Non-Target Lesion 1 CCD Art Enhanc"] !="" else 0.0
                                )

                                FU4_Non_targeted_Lesion_Dia_Sum = max(FU4_Non_Target_Lesion_1_LAD_Art_Enhanc, FU4_Non_Target_Lesion_1_PAD_Art_Enhanc, FU4_Non_Target_Lesion_1_CCD_Art_Enhanc)
                                st.write("4th_FU_Non-targeted Lesion Dia Sum",FU4_Non_targeted_Lesion_Dia_Sum)
                                FU4_Lesion_Necrosis = st.selectbox(
                                    "4th_FU_Lesion Necrosis",
                                    options=["No", "Yes", "NA"],
                        index=["No", "Yes", "NA"].index(df.iloc[0]["4th_FU_Lesion Necrosis"]) if df.iloc[0]["4th_FU_Lesion Necrosis"] else None,
                        placeholder="Choose an option",
                                )

                                FU4_Reviewers_Initials = st.text_input(
                                    "4th_FU_Reviewers Initials",
                                    help="Free-text input for reviewer name",
                                    value = df.iloc[0]["4th_FU_Reviewers Initials"]
                                )

                                FU4_Non_target_lesion_response = st.selectbox(
                                    "4th_FU_Non target lesion response",
                                    options=["No", "Yes", "NA"],
                        index=["No", "Yes", "NA"].index(df.iloc[0]["4th_FU_Non target lesion response"]) if df.iloc[0]["4th_FU_Non target lesion response"] else None,
                        placeholder="Choose an option",
                                )

                                FU4_New_Lesions = st.selectbox(
                                    "4th_FU_New Lesions",
                                    options=["No", "Yes", "NA"],
                        index=["No", "Yes", "NA"].index(df.iloc[0]["4th_FU_New Lesions"]) if df.iloc[0]["4th_FU_New Lesions"] else None,
                        placeholder="Choose an option",
                                )

                                FU4_NEW_Extrahepatic_Disease = st.selectbox(
                                    "4th_FU_NEW Extrahepatic Disease",
                                    options=["No", "Yes", "NA"],
                        index=["No", "Yes", "NA"].index(df.iloc[0]["4th_FU_Extrahepatic Disease"]) if df.iloc[0]["4th_FU_Extrahepatic Disease"] else None,
                        placeholder="Choose an option",
                                )

                                FU4_NEW_Extrahepatic_Dz_Location = st.text_input(
                                    "4th_FU_NEW Extrahepatic Dz Location",
                                    help="Free text", value = df.iloc[0]["4th_FU_NEW Extrahepatic Dz Location"]
                                )

                                FU4_NEW_Extrahepatic_Dz_Date = st.date_input("4th_FU_NEW Extrahepatic Dz Date",value = datetime.strptime(df.iloc[0]["4th_FU_NEW Extrahepatic Dz Date"], "%Y-%m-%d").date() if df.iloc[0]["4th_FU_NEW Extrahepatic Dz Date"] else None)
                                FU4_change_non_target_lesion = ((PREY90_Non_targeted_Lesion_Dia_Sum - FU4_Non_targeted_Lesion_Dia_Sum) / max(1,PREY90_pretx_targeted_Lesion_Dia_Sum)) * 100
                                st.write("4th_FU_% change non target lesion",FU4_change_non_target_lesion)
                                FU4_change_target_lesion = ((PREY90_pretx_targeted_Lesion_Dia_Sum - FU4_Follow_up_2_targeted_Lesion_Dia_Sum) / max(1,PREY90_pretx_targeted_Lesion_Dia_Sum)) * 100
                                st.write("4th_FU_% Change target dia",FU4_change_target_lesion)
                                fourth_fu_mrecist_calc = st.text_input("4th_FU_mRECIST Calc",value=df.iloc[0]["4th_FU_mRECIST Calc"])
                                fourth_fu_mrecist_localized = st.text_input("4th_FU_mRECIST LOCALIZED",value=df.iloc[0]["4th_FU_mRECIST LOCALIZED"])
                                fourth_fu_mrecist_overall = st.text_input("4th_FU_mRECIST Overall",value=df.iloc[0]["4th_FU_mRECIST Overall"])
                                FU4_Free_Text = st.text_area(
                                    "4th_FU_Free Text",
                                    help="Free text", value = df.iloc[0]["4th_FU_Free Text"]
                                )
                                # 5th Imaging Follow-up
                                st.subheader("Imaging_5th_Followup")

                                FU5_Imaging_Date = st.date_input("5th_FU_Imaging Date",value = datetime.strptime(df.iloc[0]["5th_FU_Imaging Date"], "%Y-%m-%d").date() if df.iloc[0]["5th_FU_Imaging Date"] else None)

                                FU5_Months_Since_Y90 = relativedelta(FU5_Imaging_Date, fetch_date).months
                                st.write("5th_FU_Months Since Y90",FU5_Months_Since_Y90)

                                FU5_Total_number_of_lesions = st.selectbox(
                                    "5th_FU_Total number of lesions",
                                    options=["1", "2", ">3"],
                                    index=["1", "2", ">3"].index(df.iloc[0]["5th_FU_Total number of lesions"]) if df.iloc[0]["5th_FU_Total number of lesions"] else None,
                                    placeholder="Choose an option",
                                )

                                FU5_Non_Target_Lesion_1_LAD_Art_Enhanc = st.number_input(
                                    "5th_FU_Non-Target Lesion 1 LAD Art Enhanc",
                                    step=0.1,value = float(df.iloc[0]["5th_FU_Non-Target Lesion 1 LAD Art Enhanc"]) if pd.notnull(df.iloc[0]["5th_FU_Non-Target Lesion 1 LAD Art Enhanc"]) and df.iloc[0]["5th_FU_Non-Target Lesion 1 LAD Art Enhanc"] !="" else 0.0
                                )

                                FU5_Non_Target_Lesion_1_PAD_Art_Enhanc = st.number_input(
                                    "5th_FU_Non-Target Lesion 1 PAD Art Enhanc",
                                    step=0.1,value = float(df.iloc[0]["5th_FU_Non-Target Lesion 1 PAD Art Enhanc"]) if pd.notnull(df.iloc[0]["5th_FU_Non-Target Lesion 1 PAD Art Enhanc"]) and df.iloc[0]["5th_FU_Non-Target Lesion 1 PAD Art Enhanc"] !="" else 0.0
                                )

                                FU5_Non_Target_Lesion_1_CCD_Art_Enhanc = st.number_input(
                                    "5th_FU_Non-Target Lesion 1 CCD Art Enhanc",
                                    step=0.1,value = float(df.iloc[0]["5th_FU_Non-Target Lesion 1 CCD Art Enhanc"]) if pd.notnull(df.iloc[0]["5th_FU_Non-Target Lesion 1 CCD Art Enhanc"]) and df.iloc[0]["5th_FU_Non-Target Lesion 1 CCD Art Enhanc"] !="" else 0.0
                                )

                                FU5_Non_targeted_Lesion_Dia_Sum = max(FU5_Non_Target_Lesion_1_LAD_Art_Enhanc, FU5_Non_Target_Lesion_1_PAD_Art_Enhanc, FU5_Non_Target_Lesion_1_CCD_Art_Enhanc)
                                st.write("5th_FU_Non-targeted Lesion Dia Sum",FU5_Non_targeted_Lesion_Dia_Sum)
                                FU5_Non_target_lesion_response = st.selectbox(
                                    "5th_FU_Non target lesion response",
                                    options=["No", "Yes", "NA"],
                        index=["No", "Yes", "NA"].index(df.iloc[0]["5th_FU_Non target lesion response"]) if df.iloc[0]["5th_FU_Non target lesion response"] else None,
                        placeholder="Choose an option",
                                )

                                FU5_New_Lesions = st.selectbox(
                                    "5th_FU_New Lesions",
                                    options=["No", "Yes", "NA"],
                        index=["No", "Yes", "NA"].index(df.iloc[0]["5th_FU_New Lesions"]) if df.iloc[0]["5th_FU_New Lesions"] else None,
                        placeholder="Choose an option",
                                )

                                FU5_NEW_Extrahepatic_Disease = st.selectbox(
                                    "5th_FU_NEW Extrahepatic Disease",
                                    options=["No", "Yes", "NA"],
                        index=["No", "Yes", "NA"].index(df.iloc[0]["5th_FU_Extrahepatic Disease"]) if df.iloc[0]["5th_FU_Extrahepatic Disease"] else None,
                        placeholder="Choose an option",
                                )

                                FU5_NEW_Extrahepatic_Dz_Location = st.text_input(
                                    "5th_FU_NEW Extrahepatic Dz Location",
                                    help="Free text",
                                    value = df.iloc[0]["5th_FU_NEW Extrahepatic Dz Location"]
                                )
                                FU5_NEW_Extrahepatic_Dz_Date = st.date_input("5th_FU_NEW Extrahepatic Dz Date",value = datetime.strptime(df.iloc[0]["5th_FU_NEW Extrahepatic Dz Date"], "%Y-%m-%d").date() if df.iloc[0]["5th_FU_NEW Extrahepatic Dz Date"] else None)

                                FU5_change_non_target_lesion = ((PREY90_Non_targeted_Lesion_Dia_Sum - FU5_Non_targeted_Lesion_Dia_Sum) / max(1,PREY90_pretx_targeted_Lesion_Dia_Sum)) * 100
                                st.write("5th_FU_% change non target lesion ",FU5_change_non_target_lesion)
                                fifth_fu_mrecist_calc = st.text_input("5th_FU_mRECIST Calc",value = df.iloc[0]["5th_FU_mRECIST Calc"])
                                fifth_fu_mrecist_localized = st.text_input("5th_FU_mRECIST LOCALIZED",value = df.iloc[0]["5th_FU_mRECIST LOCALIZED"])
                                fifth_fu_mrecist_overall = st.text_input("5th_FU_mRECIST Overall",value = df.iloc[0]["5th_FU_mRECIST Overall"])

                                FU5_Free_Text = st.text_area(
                                    "5th_FU_mRECIST Overall",
                                    help="Free text",
                                    value = df.iloc[0]["5th_FU_mRECIST Overall"],
                                )

                                st.subheader("Imaging_Dates for OS or PFS")

                                dead = st.selectbox(
                                        "Dead",
                                        options=["0", "1"],
                                        format_func=lambda x:{
                                                "0":"No",
                                                "1":"Yes"
                                        }[x],
                                        index=["0", "1"].index(df.iloc[0]["Dead"]) if df.iloc[0]["Dead"] else None,
                                        placeholder="Choose an option",
                                )

                                Date_of_Death = 'NA' if dead == 0 else st.date_input("Date of Death",value = datetime.strptime(df.iloc[0]["Date of Death"], "%Y-%m-%d").date() if df.iloc[0]["Date of Death"] else None)
                                Time_to_Death = 'NA' if dead == 0 else relativedelta(Date_of_Death, fetch_date).months
                                st.write("Time to Death",Time_to_Death)
                                OLT = st.selectbox(
                                        "OLT",
                                        options=["0", "1"],
                                        format_func=lambda x:{
                                                "0":"No",
                                                "1":"Yes"
                                        }[x],
                                        index=["0", "1"].index(df.iloc[0]["OLT"]) if df.iloc[0]["OLT"] else None, 
                                        placeholder="Choose an option",
                                )

                                Date_of_OLT = 'NA' if OLT == 0 else st.date_input("Date of OLT",value = datetime.strptime(df.iloc[0]["Date of OLT"], "%Y-%m-%d").date() if df.iloc[0]["Date of OLT"] else None)
                                Time_to_OLT = 'NA' if OLT == 0 else relativedelta(Date_of_Death, fetch_date).months
                                st.write("Time to OLT",Time_to_OLT)
                                Repeat_tx_post_Y90 = st.selectbox(
                                        "Repeat tx post Y90",
                                        options=["0", "1"],
                                        format_func=lambda x:{
                                                "0":"No",
                                                "1":"Yes"
                                        }[x],
                                        index=["0", "1"].index(df.iloc[0]["Repeat tx post Y90"]) if df.iloc[0]["Repeat tx post Y90"] else None,  # No default selection
                                        placeholder="Choose an option",
                                )

                                Date_of_Repeat_tx_Post_Y90 = 'NA' if Repeat_tx_post_Y90 == 0 else st.date_input("Date of Repeat tx Post Y90",value = datetime.strptime(df.iloc[0]["Date of Repeat tx Post Y90"], "%Y-%m-%d").date() if df.iloc[0]["Date of Repeat tx Post Y90"] else None)
                                Time_to_Repeat_Tx_Post_Y90 = 'NA' if Repeat_tx_post_Y90 == 0 else relativedelta(Date_of_Death, fetch_date).months
                                st.write("Time to Repeat Tx Post Y90",Time_to_Repeat_Tx_Post_Y90)
                                Date_of_Localized_Progression = st.text_input("Date of Localized Progression",value = df.iloc[0]["Date of Localized Progression"])

                                if Date_of_Localized_Progression == "No Progression":
                                        Time_to_localized_progression = 'NA'
                                else:
                                        Time_to_Localized_Progression = relativedelta(Date_of_Localized_Progression, fetch_date).years
                                st.write("Time to localized progression",Time_to_Localized_Progression)
                                Date_of_Overall_Progression = st.text_input("Date of Overall Progression",value = df.iloc[0]["Date of Overall (Local or systemic) Progression"])

                                if Date_of_Overall_Progression == "No Progression":
                                        Time_to_overall_progression = 'NA'
                                else:
                                        Time_to_overall_Progression = relativedelta(Date_of_Overall_Progression, fetch_date).years
                                st.write("Time to Overall (Local or systemic) Progression",Time_to_overall_Progression)
                                Date_of_Last_Follow_up_last_imaging_date = 'NA' if dead == 1 and OLT == 1 else st.date_input("Date of Last Follow-up/last imaging date",value = datetime.strptime(df.iloc[0]["Date of Last Follow up or last imaging date (if not OLT, Death, Repeat tx)"], "%Y-%m-%d").date() if df.iloc[0]["Date of Last Follow up or last imaging date (if not OLT, Death, Repeat tx)"] else None)

                                Time_to_Last_Follow_up_last_imaging_date = 'NA' if dead == 1 and OLT == 1 else relativedelta(Date_of_Last_Follow_up_last_imaging_date, fetch_date).years 
                                st.write("Time to Last follow up",Time_to_Last_Follow_up_last_imaging_date)
                                notes_free_text = st.text_input("Notes Free Text",value=df.iloc[0]["Notes Free text"])
                                bestm_recist = st.text_input("BestmRECIST",value=df.iloc[0]["BestmRECIST"])
                                date_bestm_recist = st.text_input("Date BestmRECIST",value=df.iloc[0]["Date BestmRECIST"])
                                time_to_bestm_recist = st.text_input("Timeto_bestmRECIST",value=df.iloc[0]["Timeto_bestmRECIST"])
                                bestm_recist_cr_vs_non_cr = st.text_input("BestmRECISTCRvsNonCR",value=df.iloc[0]["BestmRECISTCRvsNonCR"])
                                bestm_recist_r_vs_nr = st.text_input("BestmRECISTRvsNR",value=df.iloc[0]["BestmRECISTRvsNR"])
                                PREY90_Imaging_Date = (
                                PREY90_Imaging_Date.strftime("%Y-%m-%d")
                                if PREY90_Imaging_Date is not None
                                else None
                                )
                                FU_Imaging_Date = (
                                FU_Imaging_Date.strftime("%Y-%m-%d")
                                if FU_Imaging_Date is not None
                                else None
                                )
                                FU_NEW_Extrahepatic_Dz_Date = (
                                FU_NEW_Extrahepatic_Dz_Date.strftime("%Y-%m-%d")
                                if FU_NEW_Extrahepatic_Dz_Date is not None
                                else None
                                )
                                FU2_Imaging_Date = (
                                FU2_Imaging_Date.strftime("%Y-%m-%d")
                                if FU2_Imaging_Date is not None
                                else None
                                )
                                FU2_NEW_Extrahepatic_Dz_Date = (
                                FU2_NEW_Extrahepatic_Dz_Date.strftime("%Y-%m-%d")
                                if FU2_NEW_Extrahepatic_Dz_Date is not None
                                else None
                                )
                                FU3_Imaging_Date = (
                                FU3_Imaging_Date.strftime("%Y-%m-%d")
                                if FU3_Imaging_Date is not None
                                else None
                                )
                                FU3_NEW_Extrahepatic_Dz_Date = (
                                FU3_NEW_Extrahepatic_Dz_Date.strftime("%Y-%m-%d")
                                if FU3_NEW_Extrahepatic_Dz_Date is not None
                                else None
                                )
                                FU4_Imaging_Date = (
                                FU4_Imaging_Date.strftime("%Y-%m-%d")
                                if FU4_Imaging_Date is not None
                                else None
                                )
                                FU4_NEW_Extrahepatic_Dz_Date = (
                                FU4_NEW_Extrahepatic_Dz_Date.strftime("%Y-%m-%d")
                                if FU4_NEW_Extrahepatic_Dz_Date is not None
                                else None
                                )
                                FU5_Imaging_Date = (
                                FU5_Imaging_Date.strftime("%Y-%m-%d")
                                if FU5_Imaging_Date is not None
                                else None
                                )
                                FU5_NEW_Extrahepatic_Dz_Date = (
                                FU5_NEW_Extrahepatic_Dz_Date.strftime("%Y-%m-%d")
                                if FU5_NEW_Extrahepatic_Dz_Date is not None
                                else None
                                )
                                if Date_of_Repeat_tx_Post_Y90 != None and Date_of_Repeat_tx_Post_Y90 != "NA" :
                                    Date_of_Repeat_tx_Post_Y90 = Date_of_Repeat_tx_Post_Y90.strftime("%Y-%m-%d")
                                if Date_of_OLT != None and Date_of_OLT != "NA" :
                                    Date_of_OLT = Date_of_OLT.strftime("%Y-%m-%d")
                                if Date_of_Death != None and Date_of_Death != "NA" :
                                    Date_of_Death = Date_of_Death.strftime("%Y-%m-%d")
                                submit_tab10 = st.form_submit_button("Submit")
                                if submit_tab10:
                                    
                                    data10={
                                    "PREY90_prescan_modality": PREY90_prescan_modality,
                                    "PREY90_Imaging Date": PREY90_Imaging_Date,
                                    "PREY90_total number of lesions": PREY90_total_number_of_lesions,
                                    "PREY90_Number Involved Lobes": PREY90_Number_Involved_Lobes,
                                    "PREY90_target_lesion_1_segments": PREY90_target_lesion_1_segments,
                                    "PREY90_TL1_LAD": PREY90_TL1_LAD,
                                    "PREY90_Target Lesion 1 PAD": PREY90_Target_Lesion_1_PAD,
                                    "PREY90_Target Lesion 1 CCD": PREY90_Target_Lesion_1_CCD,
                                    "PREY90_Target Lesion 1 VOL": PREY90_Target_Lesion_1_VOL,
                                    "PREY90_Target lesion 2 Segments": PREY90_Target_Lesion_2_segments,
                                    "PREY90_Target Lesion 2 LAD": PREY90_Target_Lesion_2_LAD,
                                    "PREY90_Target Lesion 2 PAD": PREY90_Target_Lesion_2_PAD,
                                    "PREY90_Target Lesion 2 CCD": PREY90_Target_Lesion_2_CCD,
                                    "PREY90_Target Lesion 2 VOL": PREY90_Target_Lesion_2_VOL,
                                    "PREY90_pretx targeted Lesion Dia Sum": PREY90_pretx_targeted_Lesion_Dia_Sum,
                                    "PREY90_Non-Target Lesion Location": PREY90_Non_Target_Lesion_Location,
                                    "PREY90_Non-Target Lesion 2 LAD Art Enhanc": PREY90_Non_Target_Lesion_2_LAD_Art_Enhanc,
                                    "PREY90_Non-Target Lesion 2 PAD Art Enhanc": PREY90_Non_Target_Lesion_2_PAD_Art_Enhanc,
                                    "PREY90_Non-Target Lesion 2 CCD Art Enhanc": PREY90_Non_Target_Lesion_2_CCD_Art_Enhanc,
                                    "PREY90_Non-targeted Lesion Dia Sum": PREY90_Non_targeted_Lesion_Dia_Sum,
                                    "PREY90_Reviewers Initials": PREY90_Reviewers_Initials,
                                    "PREY90_Pre Y90 Extrahepatic Disease": PREY90_Pre_Y90_Extrahepatic_Disease,
                                    "PREY90_Pre Y90 Extrahepatic Disease Location": PREY90_Pre_Y90_Extrahepatic_Disease_Location,
                                    "PREY90_PVT": PREY90_PVT,
                                    "PREY90_PVT Location": PREY90_PVT_Location,
                                    "PREY90_Features of cirrhosis": PREY90_Features_of_cirrhosis,
                                    "1st_FU_Scan Modality": FU_Scan_Modality,
                                    "1st_FU_Imaging Date": FU_Imaging_Date,
                                    "1st_FU_Months Since Y90": FU_Months_Since_Y90,
                                    "1st_FU_Total number of lesions": FU_Total_number_of_lesions,
                                    "1st_FU_Target Lesion 1 LAD Art Enhanc": FU_Target_Lesion_1_LAD_Art_Enhanc,
                                    "1st_FU_Target Lesion 1 PAD Art Enhanc": FU_Target_Lesion_1_PAD_Art_Enhanc,
                                    "1st_FU_Target Lesion 1 CCD Art Enhanc": FU_Target_Lesion_1_CCD_Art_Enhanc,
                                    "1st_FU_Target Lesion 2 Segments": FU_Target_Lesion_2_Segments,
                                    "1st_FU_Target Lesion 2 LAD Art Enhanc": FU_Target_Lesion_2_LAD_Art_Enhanc,
                                    "1st_FU_Target Lesion 2 PAD Art Enhanc": FU_Target_Lesion_2_PAD_Art_Enhanc,
                                    "1st_FU_Target Lesion 2 CCD Art Enhanc": FU_Target_Lesion_2_CCD_Art_Enhanc,
                                    "1st_FU_Follow up 1 targeted Lesion Dia Sum": FU_Follow_up_1_targeted_Lesion_Dia_Sum,
                                    "1st_FU_Non-Target Lesion 2 LAD Art Enhanc": FU_Non_Target_Lesion_2_LAD_Art_Enhanc,
                                    "1st_FU_Non-Target Lesion 2 PAD Art Enhanc": FU_Non_Target_Lesion_2_PAD_Art_Enhanc,
                                    "1st_FU_Non-Target Lesion 2 CCD Art Enhanc": FU_Non_Target_Lesion_2_CCD_Art_Enhanc,
                                    "1st_FU_Non-targeted Lesion Dia Sum": FU_Non_targeted_Lesion_Dia_Sum,
                                    "1st_FU_Lesion Necrosis": FU_Lesion_Necrosis,
                                    "1st_FU_Reviewers Initials": FU_Reviewers_Initials,
                                    "1st_FU_Non target lesion response": FU_Non_target_lesion_response,
                                    "1st_FU_New Lesions": FU_New_Lesions,
                                    "1st_FU_NEW Extrahepatic Disease": FU_NEW_Extrahepatic_Disease,
                                    "1st_FU_NEW Extrahepatic Dz Location": FU_NEW_Extrahepatic_Dz_Location,
                                    "1st_FU_NEW Extrahepatic Dz Date": FU_NEW_Extrahepatic_Dz_Date,
                                    "1st_FU_% change non target lesion": FU_change_non_target_lesion,
                                    "1st_FU_% Change Target Dia": FU_change_target_lesion,
                                    "1st_FU_mRECIST LOCALIZED":first_fu_mrecist_localized ,
                                    "1st_FU_mRECIST Overall":first_fu_mrecist_overall ,
                                    "1st_FU_Free Text": FU_Free_Text,
                                    "2nd_FU_Scan Modality": FU2_Scan_Modality,
                                    "2nd_FU_Imaging Date": FU2_Imaging_Date,
                                    "2nd_FU_Months Since Y90": FU2_Months_Since_Y90,
                                    "2nd_FU_Total number of lesions": FU2_Total_number_of_lesions,
                                    "2nd_FU_Target Lesion 1 LAD Art Enhanc": FU2_Target_Lesion_1_LAD_Art_Enhanc,
                                    "2nd_FU_Target Lesion 1 PAD Art Enhanc": FU2_Target_Lesion_1_PAD_Art_Enhanc,
                                    "2nd_FU_Target Lesion 1 CCD Art Enhanc": FU2_Target_Lesion_1_CCD_Art_Enhanc,
                                    "2nd_FU_Target Lesion 2 Segments": FU2_Target_Lesion_2_Segments,
                                    "2nd_FU_Target Lesion 2 LAD Art Enhanc": FU2_Target_Lesion_2_LAD_Art_Enhanc,
                                    "2nd_FU_Target Lesion 2 PAD Art Enhanc": FU2_Target_Lesion_2_PAD_Art_Enhanc,
                                    "2nd_FU_Target Lesion 2 CCD Art Enhanc": FU2_Target_Lesion_2_CCD_Art_Enhanc,
                                    "2nd_FU_Follow up 2 targeted Lesion Dia Sum": FU2_Follow_up_2_targeted_Lesion_Dia_Sum,
                                    "2nd_FU_Non-Target Lesion 1 LAD Art Enhanc": FU2_Non_Target_Lesion_1_LAD_Art_Enhanc,
                                    "2nd_FU_Non-Target Lesion 1 PAD Art Enhanc": FU2_Non_Target_Lesion_1_PAD_Art_Enhanc,
                                    "2nd_FU_Non-Target Lesion 1 CCD Art Enhanc": FU2_Non_Target_Lesion_1_CCD_Art_Enhanc,
                                    "2nd_FU_Non-targeted Lesion Dia Sum": FU2_Non_targeted_Lesion_Dia_Sum,
                                    "2nd_FU_Lesion Necrosis": FU2_Lesion_Necrosis,
                                    "2nd_FU_Reviewers Initials": FU2_Reviewers_Initials,
                                    "2nd_FU_Non target lesion response": FU2_Non_target_lesion_response,
                                    "2nd_FU_New Lesions": FU2_New_Lesions,
                                    "2nd_FU_Extrahepatic Disease": FU2_NEW_Extrahepatic_Disease,
                                    "2nd_FU_NEW Extrahepatic Dz Location": FU2_NEW_Extrahepatic_Dz_Location,
                                    "2nd_FU_NEW Extrahepatic Dz Date": FU2_NEW_Extrahepatic_Dz_Date,
                                    "2nd_FU_% change non target lesion": FU2_change_non_target_lesion,
                                    "2nd_FU_% Change Target Dia": FU2_change_target_lesion,
                                    "2nd_FU_mRECIST Calc": second_fu_mrecist_calc ,
                                    "2nd_FU_mRECIST LOCALIZED":second_fu_mrecist_localized ,
                                    "2nd_FU_mRECIST Overall":second_fu_mrecist_overall ,
                                    "2nd_FU_Free Text": FU2_Free_Text,
                                    "3rd_FU_Scan Modality": FU3_Scan_Modality,
                                    "3rd_FU_Imaging Date": FU3_Imaging_Date,
                                    "3rd_FU_Months Since Y90": FU3_Months_Since_Y90,
                                    "3rd_FU_Total number of lesions": FU3_Total_number_of_lesions,
                                    "3rd_FU_Target Lesion 1 LAD Art Enhanc": FU3_Target_Lesion_1_LAD_Art_Enhanc,
                                    "3rd_FU_Target Lesion 1 PAD Art Enhanc": FU3_Target_Lesion_1_PAD_Art_Enhanc,
                                    "3rd_FU_Target Lesion 1 CCD Art Enhanc": FU3_Target_Lesion_1_CCD_Art_Enhanc,
                                    "3rd_FU_Target Lesion 2 Segments": FU3_Target_Lesion_2_Segments,
                                    "3rd_FU_Target Lesion 2 LAD Art Enhanc": FU3_Target_Lesion_2_LAD_Art_Enhanc,
                                    "3rd_FU_Target Lesion 2 PAD Art Enhanc": FU3_Target_Lesion_2_PAD_Art_Enhanc,
                                    "3rd_FU_Target Lesion 2 CCD Art Enhanc": FU3_Target_Lesion_2_CCD_Art_Enhanc,
                                    "3rd_FU_Follow up 2 targeted Lesion Dia Sum": FU3_Follow_up_2_targeted_Lesion_Dia_Sum,
                                    "3rd_FU_Non-Target Lesion 1 LAD Art Enhanc": FU3_Non_Target_Lesion_1_LAD_Art_Enhanc,
                                    "3rd_FU_Non-Target Lesion 1 PAD Art Enhanc": FU3_Non_Target_Lesion_1_PAD_Art_Enhanc,
                                    "3rd_FU_Non-Target Lesion 1 CCD Art Enhanc": FU3_Non_Target_Lesion_1_CCD_Art_Enhanc,
                                    "3rd_FU_Non-targeted Lesion Dia Sum": FU3_Non_targeted_Lesion_Dia_Sum,
                                    "3rd_FU_Lesion Necrosis": FU3_Lesion_Necrosis,
                                    "3rd_FU_Reviewers Initials": FU3_Reviewers_Initials,
                                    "3rd_FU_Non target lesion response": FU3_Non_target_lesion_response,
                                    "3rd_FU_New Lesions": FU3_New_Lesions,
                                    "3rd_FU_Extrahepatic Disease": FU3_NEW_Extrahepatic_Disease,
                                    "3rd_FU_NEW Extrahepatic Dz Location": FU3_NEW_Extrahepatic_Dz_Location,
                                    "3rd_FU_NEW Extrahepatic Dz Date": FU3_NEW_Extrahepatic_Dz_Date,
                                    "3rd_FU_% change for non target lesion": FU3_change_non_target_lesion,
                                    "3rd_FU_% Change Target Dia": FU3_change_target_lesion,
                                    "3rd_FU_mRECIST Calc" :third_fu_mrecist_calc,
                                    "3rd_FU_mRECIST LOCALIZED" :third_fu_mrecist_localized ,
                                    "3rd_FU_mRECIST Overall" :third_fu_mrecist_overall ,
                                    "3rd_FU_Free Text": FU3_Free_Text,
                                    "4th_FU_Scan Modality": FU4_Scan_Modality,
                                    "4th_FU_Imaging Date": FU4_Imaging_Date,
                                    "4th_FU_Months Since Y90": FU4_Months_Since_Y90,
                                    "4th_FU_Total number of lesions": FU4_Total_number_of_lesions,
                                    "4th_FU_Target Lesion 1 LAD Art Enhanc": FU4_Target_Lesion_1_LAD_Art_Enhanc,
                                    "4th_FU_Target Lesion 1 PAD Art Enhanc": FU4_Target_Lesion_1_PAD_Art_Enhanc,
                                    "4th_FU_Target Lesion 1 CCD Art Enhanc": FU4_Target_Lesion_1_CCD_Art_Enhanc,
                                    "4th_FU_Target Lesion 2 Segments": FU4_Target_Lesion_2_Segments,
                                    "4th_FU_Target Lesion 2 LAD Art Enhanc": FU4_Target_Lesion_2_LAD_Art_Enhanc,
                                    "4th_FU_Target Lesion 2 PAD Art Enhanc": FU4_Target_Lesion_2_PAD_Art_Enhanc,
                                    "4th_FU_Target Lesion 2 CCD Art Enhanc": FU4_Target_Lesion_2_CCD_Art_Enhanc,
                                    "4th_FU_Follow up 2 targeted Lesion Dia Sum": FU4_Follow_up_2_targeted_Lesion_Dia_Sum,
                                    "4th_FU_Non-Target Lesion 1 LAD Art Enhanc": FU4_Non_Target_Lesion_1_LAD_Art_Enhanc,
                                    "4th_FU_Non-Target Lesion 1 PAD Art Enhanc": FU4_Non_Target_Lesion_1_PAD_Art_Enhanc,
                                    "4th_FU_Non-Target Lesion 1 CCD Art Enhanc": FU4_Non_Target_Lesion_1_CCD_Art_Enhanc,
                                    "4th_FU_Non-targeted Lesion Dia Sum": FU4_Non_targeted_Lesion_Dia_Sum,
                                    "4th_FU_Lesion Necrosis": FU4_Lesion_Necrosis,
                                    "4th_FU_Reviewers Initials": FU4_Reviewers_Initials,
                                    "4th_FU_Non target lesion response": FU4_Non_target_lesion_response,
                                    "4th_FU_New Lesions": FU4_New_Lesions,
                                    "4th_FU_Extrahepatic Disease": FU4_NEW_Extrahepatic_Disease,
                                    "4th_FU_NEW Extrahepatic Dz Location": FU4_NEW_Extrahepatic_Dz_Location,
                                    "4th_FU_NEW Extrahepatic Dz Date": FU4_NEW_Extrahepatic_Dz_Date,
                                    "4th_FU_% change non target lesion": FU4_change_non_target_lesion,
                                    "4th_FU_% Change Target Dia": FU4_change_target_lesion,
                                    "4th_FU_mRECIST Calc" :fourth_fu_mrecist_calc ,
                                    "4th_FU_mRECIST LOCALIZED":fourth_fu_mrecist_localized ,
                                    "4th_FU_mRECIST Overall" :fourth_fu_mrecist_overall,
                                    "4th_FU_Free Text": FU4_Free_Text,
                                    "5th_FU_Imaging Date": FU5_Imaging_Date,
                                    "5th_FU_Months Since Y90": FU5_Months_Since_Y90,
                                    "5th_FU_Total number of lesions": FU5_Total_number_of_lesions,
                                    "5th_FU_Non-Target Lesion 1 LAD Art Enhanc": FU5_Non_Target_Lesion_1_LAD_Art_Enhanc,
                                    "5th_FU_Non-Target Lesion 1 PAD Art Enhanc": FU5_Non_Target_Lesion_1_PAD_Art_Enhanc,
                                    "5th_FU_Non-Target Lesion 1 CCD Art Enhanc": FU5_Non_Target_Lesion_1_CCD_Art_Enhanc,
                                    "5th_FU_Non-targeted Lesion Dia Sum": FU5_Non_targeted_Lesion_Dia_Sum,
                                    "5th_FU_Non target lesion response": FU5_Non_target_lesion_response,
                                    "5th_FU_New Lesions": FU5_New_Lesions,
                                    "5th_FU_Extrahepatic Disease": FU5_NEW_Extrahepatic_Disease,
                                    "5th_FU_NEW Extrahepatic Dz Location": FU5_NEW_Extrahepatic_Dz_Location,
                                    "5th_FU_NEW Extrahepatic Dz Date": FU5_NEW_Extrahepatic_Dz_Date,
                                    "5th_FU_% change non target lesion": FU5_change_non_target_lesion,
                                    "5th_FU_mRECIST Calc": fifth_fu_mrecist_calc,
                                    "5th_FU_mRECIST LOCALIZED": fifth_fu_mrecist_localized,
                                    "5th_FU_mRECIST Overall": fifth_fu_mrecist_overall,
                                    "5th_FU_mRECIST Overall" : FU5_Free_Text,
                                    "Dead": dead,
                                    "Date of Death": Date_of_Death if Date_of_Death != "NA" else Date_of_Death,
                                    "Time to Death": Time_to_Death,
                                    "OLT": OLT,
                                    "Date of OLT": Date_of_OLT if Date_of_OLT != "NA" else Date_of_OLT,
                                    "Time to OLT": Time_to_OLT,
                                    "Repeat tx post Y90": Repeat_tx_post_Y90,
                                    "Date of Repeat tx Post Y90": Date_of_Repeat_tx_Post_Y90 if Date_of_Repeat_tx_Post_Y90 != 'NA' else Date_of_Repeat_tx_Post_Y90,
                                    "Time to Repeat Tx Post Y90": Time_to_Repeat_Tx_Post_Y90,
                                    "Date of Localized Progression": Date_of_Localized_Progression,
                                    "Notes Free text" : notes_free_text,
                                    "BestmRECIST" :bestm_recist,
                                    "Date BestmRECIST":date_bestm_recist,
                                    "Timeto_bestmRECIST":time_to_bestm_recist,
                                    "BestmRECISTCRvsNonCR":bestm_recist_cr_vs_non_cr,
                                    "BestmRECISTRvsNR":bestm_recist_r_vs_nr
                                    }
                                    update_google_sheet(data10, mrn)
                                            
                    elif st.session_state.selected_tab == "Dosimetry Data":
                        st.subheader("Dosimetry Data")
                        with st.form("dosimetry_data_form"):
                
                            input_GTV_mean_dose = st.text_input("GTV mean dose",value = df.iloc[0]["GTV mean dose"])
                            input_Tx_vol_mean_dose = st.text_input("Tx vol mean dose",value = df.iloc[0]["Tx vol mean dose"])
                            input_Liver_Vol_Mean_dose = st.text_input("Liver Vol Mean dose",value = df.iloc[0]["Liver Vol Mean dose"])
                            input_Healthy_Liver_mean_dose = st.text_input("Healthy Liver mean dose",value = df.iloc[0]["Healthy Liver mean dose"])
                            input_GTV_Vol = st.number_input("GTV Vol",step=0.1,value = float(df.iloc[0]["GTV Vol"]) if pd.notnull(df.iloc[0]["GTV Vol"]) and str(df.iloc[0]["GTV Vol"]).isdigit() else 0.0)
                            input_Tx_vol = st.text_input("Tx vol",value = df.iloc[0]["Tx vol"])
                            input_Liver_vol = st.number_input("Liver vol",step=0.1, min_value=0.1,value = float(df.iloc[0]["Liver vol"]) if pd.notnull(df.iloc[0]["Liver vol"]) and str(df.iloc[0]["Liver vol"]).isdigit() else 0.1)
                            input_Healthy_Liver_Vol = st.text_input("Healthy Liver Vol",value = df.iloc[0]["Healthy Liver Vol"])
                            input_GTV_Liver = (input_GTV_Vol)/(input_Liver_vol)*100
                            st.write("GTV/Liver ",input_GTV_Liver)
                            input_D98 = st.text_input("D98",value = df.iloc[0]["D98"])
                            input_D95 = st.text_input("D95",value = df.iloc[0]["D95"])
                            input_D90 = st.text_input("D90",value = df.iloc[0]["D90"])
                            input_D80 = st.text_input("D80",value = df.iloc[0]["D80"])
                            input_D70 = st.text_input("D70",value = df.iloc[0]["D70"])
                            input_V100 = st.text_input("V100",value = df.iloc[0]["V100"])
                            input_V200 = st.text_input("V200",value = df.iloc[0]["V200"])
                            input_V300 = st.text_input("V300",value = df.iloc[0]["V300"])
                            input_V400 = st.text_input("V400",value = df.iloc[0]["V400"])
                            input_ActivityBq = st.text_input("ActivityBq",value = df.iloc[0]["ActivityBq"])
                            input_ActivityCi = st.text_input("ActivityCi",value = df.iloc[0]["ActivityCi"])
                            input_Tx_vol_Activity_Density = st.text_input("Tx vol Activity Density",value = df.iloc[0]["Tx vol Activity Density"])
                            input_NEW = st.text_input("NEW",value = df.iloc[0]["NEW"])
                            input_GTV_less_D95_Vol_ml = st.text_input("GTV < D95 Vol_ml",value = df.iloc[0]["GTV < D95 Vol_ml"])
                            input_GTV_less_D95_Mean_Dose = st.text_input("GTV < D95 Mean Dose",value = df.iloc[0]["GTV < D95 Mean Dose"])
                            input_GTV_less_D95_Min_Dose = st.text_input("GTV < D95 Min Dose",value = df.iloc[0]["GTV < D95 Min Dose"])
                            input_GTV_less_D95_SD = st.text_input("GTV < D95 SD",value = df.iloc[0]["GTV < D95 SD"])
                            input_GTV_less_D95_Vol_1 = st.text_input("GTV < D95 Vol_1",value = df.iloc[0]["GTV < D95 Vol_1"])
                            input_GTV_less_D95_Mean_Dose_1 = st.text_input("GTV < D95 Mean Dose_1",value = df.iloc[0]["GTV < D95 Mean Dose_1"])
                            input_GTV_less_D95_Min_Dose_1 = st.text_input("GTV < D95 Min Dose_1",value = df.iloc[0]["GTV < D95 Min Dose_1"])
                            input_GTV_less_D95_SD_1 = st.text_input("GTV < D95 SD_1",value = df.iloc[0]["GTV < D95 SD_1"])
                            input_GTV_less_D95_Vol_2 = st.text_input("GTV < D95 Vol_2",value = df.iloc[0]["GTV < D95 Vol_2"])
                            input_GTV_less_D95_Mean_Dose_2 = st.text_input("GTV < D95 Mean Dose_2",value = df.iloc[0]["GTV < D95 Mean Dose_2"])
                            input_GTV_less_D95_Min_Dose_2 = st.text_input("GTV < D95 Min Dose_2",value = df.iloc[0]["GTV < D95 Min Dose_2"])
                            input_GTV_less_D95_SD_2 = st.text_input("GTV < D95 SD_2",value = df.iloc[0]["GTV < D95 SD_2"])
                            input_GTV_less_100_Gy_Vol = st.text_input("GTV < 100 Gy Vol",value = df.iloc[0]["GTV < 100 Gy Vol"])
                            input_GTV_less_100_Gy_Mean_Dose = st.text_input("GTV < 100 Gy Mean Dose",value = df.iloc[0]["GTV < 100 Gy Mean Dose"])
                            input_GTV_less_100_Gy_Min_Dose = st.text_input("GTV < 100 Gy Min Dose",value = df.iloc[0]["GTV < 100 Gy Min Dose"])
                            input_GTV_less_100_Gy_SD = st.text_input("GTV < 100 Gy SD",value = df.iloc[0]["GTV < 100 Gy SD"])
                            submit_dosimetry_data = st.form_submit_button("Submit")

                            if submit_dosimetry_data:
                                data11 = {
                                    "GTV mean dose": input_GTV_mean_dose,
                                    "Tx vol mean dose": input_Tx_vol_mean_dose,
                                    "Liver Vol Mean dose": input_Liver_Vol_Mean_dose,
                                    "Healthy Liver mean dose": input_Healthy_Liver_mean_dose,
                                    "GTV Vol": input_GTV_Vol,
                                    "Tx vol": input_Tx_vol,
                                    "Liver vol": input_Liver_vol,
                                    "Healthy Liver Vol": input_Healthy_Liver_Vol,
                                    "GTV/Liver": input_GTV_Liver,
                                    "D98": input_D98,
                                    "D95": input_D95,
                                    "D90": input_D90,
                                    "D80": input_D80,
                                    "D70": input_D70,
                                    "V100": input_V100,
                                    "V200": input_V200,
                                    "V300": input_V300,
                                    "V400": input_V400,
                                    "ActivityBq": input_ActivityBq,
                                    "ActivityCi": input_ActivityCi,
                                    "Tx vol Activity Density": input_Tx_vol_Activity_Density,
                                    "NEW": input_NEW,
                                    "GTV < D95 Vol_ml": input_GTV_less_D95_Vol_ml,
                                    "GTV < D95 Mean Dose": input_GTV_less_D95_Mean_Dose,
                                    "GTV < D95 Min Dose": input_GTV_less_D95_Min_Dose,
                                    "GTV < D95 SD": input_GTV_less_D95_SD,
                                    "GTV < D95 Vol_1": input_GTV_less_D95_Vol_1,
                                    "GTV < D95 Mean Dose_1": input_GTV_less_D95_Mean_Dose_1,
                                    "GTV < D95 Min Dose_1": input_GTV_less_D95_Min_Dose_1,
                                    "GTV < D95 SD_1": input_GTV_less_D95_SD_1,
                                    "GTV < D95 Vol_2": input_GTV_less_D95_Vol_2,
                                    "GTV < D95 Mean Dose_2": input_GTV_less_D95_Mean_Dose_2,
                                    "GTV < D95 Min Dose_2": input_GTV_less_D95_Min_Dose_2,
                                    "GTV < D95 SD_2": input_GTV_less_D95_SD_2,
                                    "GTV < 100 Gy Vol": input_GTV_less_100_Gy_Vol,
                                    "GTV < 100 Gy Mean Dose": input_GTV_less_100_Gy_Mean_Dose,
                                    "GTV < 100 Gy Min Dose": input_GTV_less_100_Gy_Min_Dose,
                                    "GTV < 100 Gy SD": input_GTV_less_100_Gy_SD
                                }
                                update_google_sheet(data11, mrn)

                    elif st.session_state.selected_tab == "AFP":
                        st.subheader("Dosimetry Data")
                        with st.form("dosimetry_data_form"):
                            
                                input_1AFP_Date = st.text_area("1AFP Date",value = df.iloc[0]["1AFP Date"])
                                input_1AFP = st.text_area("1AFP",value = df.iloc[0]["1AFP"])
                                input_2AFP_Date = st.text_area("2AFP Date",value = df.iloc[0]["2AFP Date"])
                                input_2AFP = st.text_area("2AFP",value = df.iloc[0]["2AFP"])
                                input_3AFP_Date = st.text_area("3AFP Date",value = df.iloc[0]["3AFP Date"])
                                input_3AFP = st.text_area("3AFP",value = df.iloc[0]["3AFP"])
                                input_4AFP_Date = st.text_area("4AFP Date",value = df.iloc[0]["4AFP Date"])
                                input_4AFP = st.text_area("4AFP",value = df.iloc[0]["4AFP"])
                                input_5AFP_Date = st.text_area("5AFP Date",value = df.iloc[0]["5AFP Date"])
                                input_5AFP = st.text_area("5AFP",value = df.iloc[0]["5AFP"])
                                input_6AFP_Date = st.text_area("6AFP Date",value = df.iloc[0]["6AFP Date"])
                                input_6AFP = st.text_area("6AFP",value = df.iloc[0]["6AFP"])
                                input_7AFP_Date = st.text_area("7AFP Date",value = df.iloc[0]["7AFP Date"])
                                input_7AFP = st.text_area("7AFP",value = df.iloc[0]["7AFP"])
                                input_8AFP_Date = st.text_area("8AFP Date",value = df.iloc[0]["8AFP Date"])
                                input_8AFP = st.text_area("8AFP",value = df.iloc[0]["8AFP"])
                                input_9AFP_Date = st.text_area("9AFP Date",value = df.iloc[0]["9AFP Date"])
                                input_9AFP = st.text_area("9AFP",value = df.iloc[0]["9AFP"])
                                input_10AFP_Date = st.text_area("10AFP Date",value = df.iloc[0]["10AFP Date"])
                                input_10AFP = st.text_area("10AFP",value = df.iloc[0]["10AFP Date"])
                                input_11AFP_Date = st.text_area("11AFP Date",value = df.iloc[0]["11AFP Date"])
                                input_11AFP = st.text_area("11AFP",value = df.iloc[0]["11AFP"])
                                input_12AFP_Date = st.text_area("12AFP Date",value = df.iloc[0]["12AFP Date"])
                                input_12AFP = st.text_area("12AFP",value = df.iloc[0]["12AFP"])
                                input_13AFP_Date = st.text_area("13AFP Date",value = df.iloc[0]["13AFP Date"])
                                input_13AFP = st.text_area("13AFP",value = df.iloc[0]["13AFP"])
                                input_14AFP_Date = st.text_area("14AFP Date",value = df.iloc[0]["14AFP Date"])
                                input_14AFP = st.text_area("14AFP",value = df.iloc[0]["14AFP"])
                                input_15AFP_Date = st.text_area("15AFP Date",value = df.iloc[0]["15AFP Date"])
                                input_15AFP = st.text_area("15AFP",value = df.iloc[0]["15AFP"])
                                input_16AFP_Date = st.text_area("16AFP Date",value = df.iloc[0]["16AFP Date"])
                                input_16AFP = st.text_area("16AFP",value = df.iloc[0]["16AFP"])
                                input_17AFP_Date = st.text_area("17AFP Date",value = df.iloc[0]["17AFP Date"])
                                input_17AFP = st.text_area("17AFP",value = df.iloc[0]["17AFP"])
                                input_18AFP_DATE = st.text_area("18AFP DATE",value = df.iloc[0]["18AFP DATE"])
                                input_18AFP = st.text_area("18AFP",value = df.iloc[0]["18AFP"])
                                input_19AFP_DATE = st.text_area("19AFP DATE",value = df.iloc[0]["19AFP DATE"])
                                input_19AFP = st.text_area("19AFP",value = df.iloc[0]["19AFP"])
                                input_20AFP_DATE = st.text_area("20AFP DATE",value = df.iloc[0]["20AFP DATE"])
                                input_20AFP = st.text_area("20AFP",value = df.iloc[0]["20AFP"])
                                input_21AFP_DATE = st.text_area("21AFP DATE",value = df.iloc[0]["21AFP DATE"])
                                input_21AFP = st.text_area("21AFP",value = df.iloc[0]["21AFP"])
                                input_22AFP_DATE = st.text_area("22AFP DATE",value = df.iloc[0]["22AFP DATE"])
                                input_22AFP = st.text_area("22AFP",value = df.iloc[0]["22AFP"])
                                input_23AFP_DATE = st.text_area("23AFP DATE",value = df.iloc[0]["23AFP DATE"])
                                input_23AFP = st.text_area("23AFP",value = df.iloc[0]["23AFP"])
                                input_24AFP_DATE = st.text_area("24AFP DATE",value = df.iloc[0]["24AFP DATE"])
                                input_24AFP = st.text_area("24AFP",value = df.iloc[0]["24AFP"])
                                input_25AFP_DATE = st.text_area("25AFP DATE",value = df.iloc[0]["25AFP DATE"])
                                input_25AFP = st.text_area("25AFP",value = df.iloc[0]["25AFP"])
                                input_26AFP_DATE = st.text_area("26AFP DATE",value = df.iloc[0]["26AFP DATE"])
                                input_26AFP = st.text_area("26AFP",value = df.iloc[0]["26AFP"])
                                input_27AFP_DATE = st.text_area("27AFP DATE",value = df.iloc[0]["27AFP DATE"])
                                input_27AFP = st.text_area("27AFP",value = df.iloc[0]["27AFP"])
                                input_28AFP_DATE = st.text_area("28AFP DATE",value = df.iloc[0]["28AFP DATE"])
                                input_28AFP = st.text_area("28AFP",value = df.iloc[0]["28AFP"])
                                input_29AFP_DATE = st.text_area("29AFP DATE",value = df.iloc[0]["29AFP DATE"])
                                input_29AFP = st.text_area("29AFP",value = df.iloc[0]["29AFP"])
                                input_30AFP_DATE = st.text_area("30AFP DATE",value = df.iloc[0]["30AFP DATE"])
                                input_30AFP = st.text_area("30AFP",value = df.iloc[0]["30AFP"])
                                input_31AFP_Date = st.text_area("31AFP Date",value = df.iloc[0]["31AFP Date"])
                                input_31AFP = st.text_area("31AFP",value = df.iloc[0]["31AFP"])
                                input_32AFP_DATE = st.text_area("32AFP DATE",value = df.iloc[0]["32AFP DATE"])
                                input_32AFP = st.text_area("32AFP",value = df.iloc[0]["32AFP"])
                                input_33AFP_DATE = st.text_area("33AFP DATE",value = df.iloc[0]["33AFP DATE"])
                                input_33AFP = st.text_area("33AFP",value = df.iloc[0]["33AFP"])
                                input_34AFP_DATE = st.text_area("34AFP DATE",value = df.iloc[0]["34AFP DATE"])
                                input_34AFP = st.text_area("34AFP",value = df.iloc[0]["34AFP"])
                                submit_afp = st.form_submit_button("Submit")

                                if submit_afp:
                                    data12 = {
                                    "1AFP Date": input_1AFP_Date, "1AFP": input_1AFP,
                                    "2AFP Date": input_2AFP_Date, "2AFP": input_2AFP,
                                    "3AFP Date": input_3AFP_Date, "3AFP": input_3AFP,
                                    "4AFP Date": input_4AFP_Date, "4AFP": input_4AFP,
                                    "5AFP Date": input_5AFP_Date, "5AFP": input_5AFP,
                                    "6AFP Date": input_6AFP_Date, "6AFP": input_6AFP,
                                    "7AFP Date": input_7AFP_Date, "7AFP": input_7AFP,
                                    "8AFP Date": input_8AFP_Date, "8AFP": input_8AFP,
                                    "9AFP Date": input_9AFP_Date, "9AFP": input_9AFP,
                                    "10AFP Date": input_10AFP_Date, "10AFP": input_10AFP,
                                    "11AFP Date": input_11AFP_Date, "11AFP": input_11AFP,
                                    "12AFP Date": input_12AFP_Date, "12AFP": input_12AFP,
                                    "13AFP Date": input_13AFP_Date, "13AFP": input_13AFP,
                                    "14AFP Date": input_14AFP_Date, "14AFP": input_14AFP,
                                    "15AFP Date": input_15AFP_Date, "15AFP": input_15AFP,
                                    "16AFP Date": input_16AFP_Date, "16AFP": input_16AFP,
                                    "17AFP Date": input_17AFP_Date, "17AFP": input_17AFP,
                                    "18AFP DATE": input_18AFP_DATE, "18AFP": input_18AFP,
                                    "19AFP DATE": input_19AFP_DATE, "19AFP": input_19AFP,
                                    "20AFP DATE": input_20AFP_DATE, "20AFP": input_20AFP,
                                    "21AFP DATE": input_21AFP_DATE, "21AFP": input_21AFP,
                                    "22AFP DATE": input_22AFP_DATE, "22AFP": input_22AFP,
                                    "23AFP DATE": input_23AFP_DATE, "23AFP": input_23AFP,
                                    "24AFP DATE": input_24AFP_DATE, "24AFP": input_24AFP,
                                    "25AFP DATE": input_25AFP_DATE, "25AFP": input_25AFP,
                                    "26AFP DATE": input_26AFP_DATE, "26AFP": input_26AFP,
                                    "27AFP DATE": input_27AFP_DATE, "27AFP": input_27AFP,
                                    "28AFP DATE": input_28AFP_DATE, "28AFP": input_28AFP,
                                    "29AFP DATE": input_29AFP_DATE, "29AFP": input_29AFP,
                                    "30AFP DATE": input_30AFP_DATE, "30AFP": input_30AFP,
                                    "31AFP Date": input_31AFP_Date, "31AFP": input_31AFP,
                                    "32AFP DATE": input_32AFP_DATE, "32AFP": input_32AFP,
                                    "33AFP DATE": input_33AFP_DATE, "33AFP": input_33AFP,
                                    "34AFP DATE": input_34AFP_DATE, "34AFP": input_34AFP
                                    }
                                    update_google_sheet(data12,mrn)
if st.session_state.logged_in:
    # Navigation options
    st.sidebar.title("Navigation")
    options = st.sidebar.radio("Select an option", ["Add New Data", "Edit Existing Data", "Logout"])
    
    if options == "Add New Data":
        add_new_data()
    elif options == "Edit Existing Data":
        edit_existing_data()
    elif options == "Logout":
        st.session_state.logged_in = False
        st.rerun()
else:
    login_page()        
