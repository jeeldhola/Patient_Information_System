import streamlit as st
import pandas as pd
import math
from datetime import datetime
from dateutil.relativedelta import relativedelta
import json
from math import pi

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
        st.success("Data saved successfully.")
        return True
    except Exception as e:
        st.error(f"An error occurred while saving data : {e}")
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

def update_google_sheet(data, mrn):
    try:
        df = fetch_data_from_google_sheet()
        if df.empty:
            st.error(f"No data found for MRN {mrn}.")
            return False
        if 'MRN' not in df.columns:
            st.error(f"MRN column not found .")
            return False
        df['MRN'] = df['MRN'].astype(str)
        mrn = str(mrn)

        index = df[df['MRN'] == mrn].index[0]
        for key, value in data.items():
            if key in df.columns:
                df.at[index, key] = value
            else:
                st.error(f"Column {key} not found.")
                return False
        values = [df.columns.tolist()] + df.values.tolist()
        body = {
            'values': values
        }
        result = service.spreadsheets().values().update(
            spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME,
            valueInputOption='RAW', body=body).execute()
        st.success("Data saved successfully.")
        return True
    except Exception as e:
        st.error(f"An error occurred while updating data: {e}")
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
    .stVerticalBlock st-emotion-cache-bjh2tb eiemyj3 >div:nth-child(2){
        max-height: 500px;
        overflow-y: auto;
        padding: 10px;
        border: 1px solid #ccc;
        border-radius: 5px;
    }
    .st-emotion-cache-j7qwjs.e1dbuyne3 {display: none !important;}
    .st-emotion-cache-kgpedg.e1dbuyne10 {height : 0px;}
    .stSidebar.st-emotion-cache-vmpjyt.e1dbuyne0 { 
    min-width: 210px;
    max-width: 210px;
    }
    .stForm.st-emotion-cache-4uzi61.e2juff41 {
    height: 500px;
    margin-bottom : 20px;
    overflow-y: auto;}
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
        st.error(f"No data found.")
        return None
    if 'MRN' not in df.columns:
        st.error(f"MRN column not found.")
        return None
    if str(mrn) not in df['MRN'].values:
        st.error(f"No data found for MRN {mrn}.")
        return None
    data = df[df['MRN'] == str(mrn)]
    return data

if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(
        columns=["FIRST", "LAST", "MRN","ID","Duplicate","TAREdate","PT","Tareage", "Gender", "Ethnicity", "PMHxHTN","PMHxDM", "Hypercholesterolemia", "PMHxSmoking", "Obesity", ]
    )
# List of 11 tabs
def hypoalbuminemia(b2):
    if b2 >= 3:
        return 0
    elif b2 >= 2:
        return 1
    elif b2 >= 1:
        return 2
    elif b2 > 0:
        return 3
    else:
        return 4

def hyperbillirubine(e3, f3, d1=1.2):
    if e3 <= d1:
        if f3 <= d1:
            return 0
        elif f3 <= 1.5 * d1:
            return 1
        elif f3 <= 3 * d1:
            return 2
        elif f3 <= 10 * d1:
            return 3
        else:
            return 4
    else:
        if f3 <= e3:
            return 0
        elif f3 <= 1.5 * e3:
            return 1
        elif f3 <= 3 * e3:
            return 2
        elif f3 <= 10 * e3:
            return 3
        else:
            return 4

def Increasecreatine(i2, j2, h1=1):
    if i2 <= h1:
        if j2 <= h1:
            return 0
        elif j2 <= 1.5 * h1:
            return 1
        elif j2 <= 3 * h1:
            return 2
        elif j2 <= 6 * h1:
            return 3
        else:
            return 4
    else:
        if j2 <= i2:
            return 0
        elif j2 <= 1.5 * i2:
            return 1
        elif j2 <= 3 * i2:
            return 2
        elif j2 <= 6 * i2:
            return 3
        else:
            return 4

def hyperkalemia(n2, l1=5):
    if n2 <= l1:
        return 0
    elif n2 <= 5.5:
        return 1
    elif n2 <= 6:
        return 2
    elif n2 <= 7:
        return 3
    else:
        return 4

def alt_calculate(q2, r2, p1=40.0):
    if q2 <= p1:
        if r2 <= p1:
            return 0
        elif r2 <= 3 * p1:
            return 1
        elif r2 <= 5 * p1:
            return 2
        elif r2 <= 20 * p1:
            return 3
        else:
            return 4
    else:
        if r2 <= q2:
            return 0
        elif r2 <= 1.5 * q2:
            return 1
        elif r2 <= 3 * q2:
            return 2
        elif r2 <= 5 * q2:
            return 3
        elif r2 <= 20 * q2:
            return 4
        else:
            return 5

def ast_calculate(u2, v2, t1=40):
    if u2 <= t1:
        if v2 <= t1:
            return 0
        elif v2 <= 3 * t1:
            return 1
        elif v2 <= 5 * t1:
            return 2
        elif v2 <= 20 * t1:
            return 3
        else:
            return 4
    else:
        if v2 <= u2:
            return 0
        elif v2 <= 1.5 * u2:
            return 1
        elif v2 <= 3 * u2:
            return 2
        elif v2 <= 5 * u2:
            return 3
        elif v2 <= 20 * u2:
            return 4
        else:
            return 5

def alp_calculate(y2, z2, x1=147):
    if y2 <= x1:
        if z2 <= x1:
            return 0
        elif z2 <= 2.5 * x1:
            return 1
        elif z2 <= 5 * x1:
            return 2
        elif z2 <= 20 * x1:
            return 3
        else:
            return 4
    else:
        if z2 <= y2:
            return 0
        elif z2 <= 2.5 * y2:
            return 1
        elif z2 <= 5 * y2:
            return 2
        elif z2 <= 20 * y2:
            return 3
        else:
            return 4

def plt_calculate(ag2, ae1=150):
    if ag2 >= ae1:
        return 0
    elif ag2 >= 75:
        return 1
    elif ag2 >= 50:
        return 2
    elif ag2 >= 25:
        return 3
    else:
        return 4

def get_variable_value(mrn, column_name):
    df = fetch_data_from_google_sheet()
    mrn = str(mrn)
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
    st.markdown(
        """
        <style>
            .stSidebar  {display: none !important;}
            .st-emotion-cache-1i55tjj.e1obcldf18 {display: none !important;}
        </style>
        """,
        unsafe_allow_html=True
    )
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == "user" and password == "pass":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Invalid username or password.")

def calculatepoints(L, M, N, Q, U):
       
        if any(val is None or val == "" for val in [L, M, N, Q, U]):
            return "NA"

        # Convert values to float for comparison (handling potential string inputs)
        try:
            L, M, N, Q, U = float(L), float(M), float(N), int(Q), int(U)
        except ValueError:
            return "NA"  # Return "NA" if conversion fails (invalid data)

        # Equivalent scoring logic
        score = (
            (1 if L < 2 else 2 if L <= 3 else 3) +
            (1 if M > 3.5 else 2 if M >= 2.8 else 3) +
            (1 if N < 1.7 else 2 if N <= 2.3 else 3) +
            (1 if Q == 1 else 2 if Q == 2 else 3) +
            (1 if U == 1 else 2 if U == 2 else 3)
        )

        return score

def calculate_class(X):
        if X is None or X == "" or X == "NA":
            return "NA"

        # Convert X to float for comparison
        try:
            X = float(X)
        except ValueError:
            return "NA"  # Return "NA" if conversion fails (invalid data)

        # Apply conditions
        if X <= 6:
            return "A"
        elif X <= 9:
            return "B"
        else:
            return "C"

def meld_calc(N, K, M):
    # Check for missing values
    if N is None or K is None or M is None or N == "" or K == "" or M == "":
        return "NA"

    try:
        # Convert to float
        N, K, M = float(N), float(K), float(M)

        # Apply formula
        result = (0.957 * math.log(max(N, 1)) + 
                  0.378 * math.log(max(K, 1)) + 
                  1.12 * math.log(max(M, 1)) + 
                  0.643) * 10
        
        # Round to nearest whole number
        return round(result, 0)

    except ValueError:
        return "NA" 

def albi_calc(K,L):
        if K is None or L is None or K == "" or L == "" or K == "NA" or L == "NA":
            return "NA"
        try:
            K, L = float(K), float(L)
            result = (math.log10(K * 17.1) * 0.66) + (L * -0.085 * 10)
            return round(result, 2)
        except ValueError:
            return "NA"

def albi_class(AB):
        if AB is None or AB == "" or AB == "NA":
            return "NA"
        try:
            # Convert to float
            AB = float(AB)

            # Apply conditions
            if AB <= -2.6:
                return 1
            elif AB <= -1.39:
                return 2
            else:
                return 3
        except ValueError:
            return "NA"

def calculate_target_lestion_vol(L, M, N):
    # Check for blank values, "NA", or 0
    if any(x in (None, "", "NA", 0) for x in (L, M, N)):
        return 0
    else :
        return L * M * N * (4/3) * pi

def calculate_value_v2(N, O, P, Q):
    # Check if any value is "NA"
    if any(x in (None, "", "NA", 0) for x in (N, O, P, Q)):
        return "NA"
    else:
        return O * P * Q * (4/3) * pi

def mrecist_local(BC):
    if BC >= 100:
        return "CR"
    elif BC >= 30:
        return "PR"
    elif -20 <= BC < 30:
        return "SD"
    else:
        return "PD"

def mrecist_calc(CE, BR, AP):
    if CE == "":
        return ""
    elif BR > AP:
        return "PD"
    elif CE >= 100:
        return "CR"
    elif CE >= 30:
        return "PR"
    elif -20 <= CE < 30:
        return "SD"
    else:
        return "PD"   

def mrecist_overall(AX, AY, BB, BC):
    if AX == "1" or AY == "1" or BB < 0:
        return "PD"
    elif BC >= 100:
        return "CR"
    elif BC >= 30:
        return "PR"
    elif -20 <= BC < 30:
        return "SD"
    else:
        return "PD"

def detect_first_progression(BD, CG, DJ, EM, FD, BI, CL, DO, EP):
    

    # Mapping follow-up responses to their corresponding imaging dates
    follow_ups = [(CG, BI), (DJ, CL), (EM, DO), (FD, EP)]
    
    # Progression rules based on BD
    progression_criteria = {
        "CR": {"PR", "SD", "PD"},
        "PR": {"SD", "PD"},
        "SD": {"PD"},
    }
    
    # Check for progression based on the initial BD value
    if BD in progression_criteria:
        for response, date in follow_ups:
            if response in progression_criteria[BD]:
                return date  # Return the first imaging date of progression
    
    return "No Progression"

def detect_overall_progression(BG, BH, CJ, CK, DM, DN, EP, EQ, FG, FH, AH, BL, CO, DR, ES):
    
    # If both BG and BH start as PD, return No Progression
    if BG == "PD" and BH == "PD":
        return "No Progression"
    
    # First Follow-Up Progression Check
    if BG != "PD" or BH != "PD":
        return AH
    
    # Mapping follow-up responses to their corresponding imaging dates
    follow_ups = [(CJ, CK, BL), (DM, DN, CO), (EP, EQ, DR), (FG, FH, ES)]
    
    # Check for progression in subsequent follow-ups
    for loc, overall, date in follow_ups:
        if loc != "PD" or overall != "PD":
            return date  # Return the first imaging date where progression occurs

    return "No Progression"

def determine_bestmrecist(BE, CH, DK, EN, FE):

    responses = [BE, CH, DK, EN, FE]

    # Check for "CR"
    if "CR" in responses:
        return "CR"

    # Check for "PR"
    if "PR" in responses:
        return "PR"

    # Check for "SD" (excluding FE since it's not checked for "SD" in the formula)
    if any(resp == "SD" for resp in [BE, CH, DK, EN]):
        return "SD"

    # Check for "PD" (excluding FE since it's not checked for "PD" in the formula)
    if any(resp == "PD" for resp in [BE, CH, DK, EN]):
        return "PD"

    # Default case
    return "No Response"

def determine_bestmrecist_date(fz, bf, ci, dl, en, fe, ah, bj, cm, dp, eq):
    
    response_map = {
        "CR": [bf, ci, dl, en, fe],
        "PR": [bf, ci, dl, en, fe],
        "SD": [bf, ci, dl, en, fe],
        "PD": [bf, ci, dl, en, fe]
    }

    date_map = [ah, bj, cm, dp, eq]

    # Check if fz exists in the map
    if fz in response_map:
        for idx, val in enumerate(response_map[fz]):
            if val == fz:
                return date_map[idx]  # Return corresponding date
    
    return "No Date"

def add_new_data():
    st.title("Patient Information System")
    df=fetch_data_from_google_sheet()
    st.dataframe(df)

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

    tabs = ["Patient Info", "Patient Demographics", "Cirrhosis PMH","HCC Diagnosis", "Previous Therapy for HCC", "Pre Y90", "Day_Y90", "Post Y90 Within 30 Days Labs", "Other Post Tare","Imaging Date","Dosimetry Data","AFP"]

    col1, col2 = st.columns([0.3, 0.7],gap="small")

    # Left column for vertical tabs
    with col1:
        st.header("Patient Details")
        st.session_state.selected_tab = st.radio("", tabs)

    with col2:
        if st.session_state.selected_tab == "Patient Info":
            st.subheader("Patient_Info")
            with st.form("patient_info_form"):
                # Patient Info Section
                col1, col2 = st.columns(2)
                first_name = col1.text_input("First Name [Excel : FIRST]")
                first_name = first_name.capitalize()
                last_name = col2.text_input("Last Name [Excel : LAST]")
                last_name = last_name.capitalize()
                
                mrn = st.number_input("MRN [Excel : MRN]",step=1)
                id=""
                
                if first_name and last_name:
                    base_id = first_name[0] + last_name[0]
                    if not df.empty:
                        existing_ids = df['ID'].tolist()
                        count = sum(1 for id in existing_ids if id.startswith(base_id))
                        id = f"{base_id}{count + 1}"
                    else:
                        id = f"{base_id}1"
                else:
                    id = ""
                
                duplicate_procedure_check = ""
                if id.endswith("1"):
                     duplicate_procedure_check = ""
                else:
                     duplicate_procedure_check = "Duplicate"
                
                tare_date = st.date_input("TARE Tx Date [Excel : TAREDATE]", help="Select the treatment date")
                procedure_technique = st.selectbox(
                "Procedure Technique    [Excel : PROTYPE]\n\nLobar (1), Segmental (2)",
                options=["1", "2"],
                format_func=lambda x: {
                                    "1": "Lobar",
                                    "2": "Segmental",
                                }[x],
                index=None,  # No default selection
                placeholder="Choose an option",
                )
                age = st.number_input("Age at time of TARE [Excel : TAREAGE]", min_value=0, max_value=150, step=1)
                submit_tab1 = st.form_submit_button("Submit")
                if submit_tab1:
                        #df = fetch_data_from_google_sheet()
                        if not df.empty and str(mrn) in df['MRN'].values:
                            st.error(f"MRN {mrn} already exists. Please enter a unique MRN.")
                        else:
                            if hasattr(st.session_state, 'temp_mrn'):
                                # If temp_mrn exists, remove the old entry with the previous MRN
                                st.session_state.data = st.session_state.data[st.session_state.data["MRN"] != st.session_state.temp_mrn]
                                # Reset temp_mrn after clearing the previous entry
                                del st.session_state.temp_mrn
                            st.write("ID :",id)
                            data = {
                                "FIRST": first_name,
                                "LAST": last_name,
                                "MRN": mrn,
                                "ID" : id,
                                "DUP" : duplicate_procedure_check,
                                "TAREDATE": tare_date.strftime("%Y-%m-%d"),
                                "PROTYPE": procedure_technique,
                                "TAREAGE": age
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
                    try:
                        gender = st.selectbox(
                            "Gender     [Excel : GENDER]\n\nMale (1) , Female (2)",
                            options=["1", "2"],
                            format_func=lambda x: {
                                                    "1": "Male",
                                                    "2": "Female",
                                                }[x],
                            index=None,  # No default selection
                            placeholder="Choose an option",
                        )

                        # Ethnicity dropdown
                        ethnicity = st.selectbox(
                            "Ethnicity      [Excel : ETHNICITY]\n\n(1) Black, (2) White, (3) Asian, (4) Hispanic, (5) Other, NA (cant find it in sheet), 0 (not present)",
                            options=["1","2", "3", "4", "5", "NA", "0"],
                            format_func=lambda x: {
                                                    "1": "Black",
                                                    "2": "White",
                                                    "3": "Asian",
                                                    "4": "Hispanic",
                                                    "5": "Other",
                                                    "NA": "NA (cant find it in sheet)",
                                                    "0" : "0 (not present)",
                                                }[x],
                            index=None,  # No default selection
                            placeholder="Choose an option",
                            
                        )

                        hypertension = st.selectbox(
                            "PMHx Hypertension      [Excel : PMHHTN]\n\nYes(1), No(0)",
                            options=["1", "0"],
                            format_func=lambda x: {
                                                    "1": "Yes",
                                                    "0": "No",
                                                }[x],
                            index=None,  # No default selection
                            placeholder="Choose an option",
                        )

                        diabetes = st.selectbox(
                            "PMHx Diabetes (T1 or T2)     [Excel : PMHDM]\n\nYes(1), No(0)",
                            options=["1", "0"],
                            format_func=lambda x: {
                                                    "1": "Yes",
                                                    "0": "No",
                                                }[x],
                            index=None,  # No default selection
                            placeholder="Choose an option",
                        )

                        hypercholesterolemia = st.selectbox(
                            "Hypercholesterolemia      [Excel : HYPERCHOL]\n\nYes(1), No(0)",
                            options=["1", "0"],
                            format_func=lambda x: {
                                                    "1": "Yes",
                                                    "0": "No",
                                                }[x],
                            index=None,  # No default selection
                            placeholder="Choose an option",
                        )

                        smoking = st.selectbox(
                            "Hx of Smoking      [Excel : PMHSMOKE]\n\nYes(1), No(0)",
                            options=["1", "0"],
                            format_func=lambda x: {
                                                    "1": "Yes",
                                                    "0": "No",
                                                }[x],
                            index=None,  # No default selection
                            placeholder="Choose an option",
                        )

                        obesity = st.selectbox(
                            "Obesity        [Excel : OBESITY]\n\nYes(1), No(0)",
                            options=["1", "0"],
                            format_func=lambda x: {
                                                    "1": "Yes",
                                                    "0": "No",
                                                }[x],
                            index=None,  # No default selection
                            placeholder="Choose an option",
                        )
                       
                        submit_tab2 = st.form_submit_button("Submit")
                        if submit_tab2:
                            #index = st.session_state.data[st.session_state.data["MRN"] == st.session_state.temp_mrn].index[0]
                            data1={
                                "GENDER": gender,
                                "ETHNICITY":ethnicity,
                                "PMHHTN": hypertension,
                                "PMHDM":diabetes,
                                "HYPERCHOL" : hypercholesterolemia,
                                "PMHSMOKE" : smoking,
                                "OBESITY" : obesity,
                            }
                            if "patient_info" in st.session_state and st.session_state.patient_info["MRN"] == st.session_state.temp_mrn:
                                st.session_state.patient_info.update(data1)
                                # Update the data in Google Sheets
                                update_google_sheet(data1, int(st.session_state.temp_mrn))
                            else:
                                st.error(f"No patient information found for MRN {st.session_state.temp_mrn}")
                    except:
                        st.warning("Please Fill Patient Information Page")
                           
        elif st.session_state.selected_tab == "Cirrhosis PMH":
            st.subheader("Cirrhosis PMH")
            with st.form("cirrhosis_pmh_form"):
                
                if "MRN" not in st.session_state.data:
                    st.warning("Please complete the Patient Information tab first.")
                else:
                    try:
                    
                # Cirrhosis PMH Fields
                        cir_pmh_hbv_status = st.selectbox(
                            "Cir PMH HBV Status [ Excel : CIRPMH_HBV ]\n\nYes(1), No(0)  ",
                            options=["1", "0"],
                            format_func=lambda x: {
                                                    "1": "Yes ",
                                                    "0": "No  ",
                                                }[x],
                            help="Select HBV Status",
                            index=None,  # No default selection
                            placeholder="Choose an option",
                        )

                        cir_pmh_hbv_free_text = "0" if cir_pmh_hbv_status == "No" else st.text_input(
                            "Cir PMH HBV Free Text [ Excel : CIRPMH_HBVFT ]"
                        )
                        
                        cir_pmh_hbv_art = "0" if cir_pmh_hbv_status == "No" else st.selectbox(
                            "Cir PMH HBV ART [ Excel : CIRPMH_HBVART ]\n\n(1) Entecavir, (2) Tenofovir, (3) NA  ",
                            options=["1", "2", "3"],
                            format_func=lambda x: {
                                                    "1": "Entecavir ",
                                                    "2": "Tenofovir ",
                                                    "3": "NA "
                                                }[x],
                            index=None,  # No default selection
                            placeholder="Choose an option",
                        )

                        cir_pmh_hcv_status = st.selectbox(
                            "Cir_PMH_HCV Status [ Excel : CIRPMH_HCV ]\n\nYes(1), No(0)  ",
                            options=["1", "0"],
                            format_func=lambda x: {
                                                    "1": "Yes ",
                                                    "0": "No  ",
                                                }[x],
                            index=None,  # No default selection
                            placeholder="Choose an option",
                        )

                        cir_pmh_hcv_free_text = "No" if cir_pmh_hcv_status == "No" else st.text_input(
                            "Cir_PMH_HCV Free Text [ Excel : CIRPMH_HCVFT ]",
                            help="Provide additional details for HCV Status",
                        )

                        cir_pmh_hcv_art = "No" if cir_pmh_hcv_status == "No" else st.selectbox(
                            "Cir_PMH_HCV ART [ Excel : CIRPMH_HCVART ]\n\n(1) sofosbuvir/velpatasvir , (2) ledipasvir/sofosbuvir, (3) NA (if u can't find a med or if they arent on it), (4) Glecaprevir/pibrentasvir",
                            options=["1", "2", "3", "4"],
                            format_func=lambda x: {
                                                    "1": " sofosbuvir/velpatasvir",
                                                    "2": " ledipasvir/sofosbuvir",
                                                    "3": " NA (if you can't find a med or if they aren't on it)",
                                                    "4": " Glecaprevir/pibrentasvir"
                                                }[x],
                            help="Select ART treatment for HCV",
                            index=None,  # No default selection
                            placeholder="Choose an option",
                    
                        )

                        cir_pmh_alcohol_use_disorder = st.selectbox( 
                            "Cir_PMH_Alcohol Use Disorder [ Excel : CIRPMH_AUD ]\n\nYes(1), No(0)  ",
                            options=["1", "0"],
                            format_func=lambda x: {
                                                    "1": "Yes ",
                                                    "0": "No  ",
                                                }[x],
                            help="Select Alcohol Disorder",
                            index=None,  # No default selection
                            placeholder="Choose an option",
                        )

                        cir_pmh_alcohol_free_text = "0" if cir_pmh_alcohol_use_disorder == "No" else st.text_input(
                            "Cir_PMH_Alcohol Free Text [ Excel : CIRPMH_AUDFT ]",
                            help="Provide additional details for Alcohol Disorder",
                        )

                        cir_pmh_ivdu_status = st.selectbox(
                            "Cir_PMH_IVDU Status [ Excel : CIRPMH_IVDU ]\n\nYes(1), No(0)  ",
                            options=["1", "0"],
                            format_func=lambda x: {
                                                    "1": "Yes",
                                                    "0": "No  ",
                                                }[x],
                            #format_func=lambda x: f"{x} ({1 if x == 'Yes' else 0})",
                            help="Select IVDU Status",
                            index=None,  # No default selection
                            placeholder="Choose an option",
                        )

                        cir_pmh_ivdu_free_text = "0" if cir_pmh_ivdu_status == "No" else st.text_input(
                            "Cir_PMH_IVDU Free Text [ Excel : CIRPMH_IVDUFT ]",
                            help="Provide additional details for IVDU"
                    
                        )

                        cir_pmh_liver_addtional_factor = st.selectbox(
                            "Cir_PMH_Liver Additional Factors [ Excel : CIRPMH_LIVERFAC ]\n\n (1) NAFLD, (2) MAFLD, (3) NASH, (4) Autoimmune Hepatitis, (5) Hereditary Hemochromatosis, (6) none  ",
                            options=["1", "2", "3", "4", "5", "6"],
                            format_func=lambda x: {
                                                    "1": "NAFLD ",
                                                        "2": "MAFLD ",
                                                        "3": "NASH ",
                                                        "4": "Autoimmune Hepatitis ",
                                                        "5": "Hereditary Hemochromatosis ",
                                                        "6": "None "
                                                }[x], 
                            help="Select Other Contributing Factors",
                            index=None,  # No default selection
                            placeholder="Choose an option",
                        )
                
                        st.subheader("Cirrhosis Dx")
                        Cirrhosis_Dx_Diagnosis_Date = st.date_input("Cirrhosis Dx Diagnosis Date [ Excel : CIRDX_DATE ]",help="Select Diagnosis date")

                        Cirrhosis_Dx_Diagnosis_Method = st.selectbox(
                            "Cirrhosis_Dx_Diagnosis Method [ Excel : CIRDX_METHOD ]\n\n(1) Biopsy, (2) Imaging  ",
                            options=["1", "2"],
                            format_func=lambda x: {
                                                    "1": "Biopsy",
                                                    "2": "maging",
                                                }[x],
                            index=None,  # No default selection
                            placeholder="Choose an option",
                        ) 
                        Cirrhosis_Dx_HPI_EMR_Note_Free_Text = st.text_area(
                            "Cirrhosis_Dx_HPI EMR Note Free Text [ Excel : CIRDX_HPIFT ]",
                            help="Provide details of HPI EMR"
                        )
                        Cirrhosis_Dx_Imaging_Findings_EMR_Note_Free_Text = st.text_area(
                            "Cirrhosis_Dx_Imaging Findings EMR Note Free Text [ Excel : CIRDX_IMAGEFT ]",
                            help="Provide details of Imaging Findings"
                        )

                        Cirrhosis_Dx_Metavir_Score = st.selectbox (
                            "Cirrhosis_Dx_Metavir Score [ Excel : CIRDX_METAVIR ]  ",
                            options=["F0/F1", "F2","F3","F4","NA"],
                            help="Select Metavir_score",
                            index=None,  # No default selection
                            placeholder="Choose an option",
                        ) 

                        Cirrhosis_Dx_Complications_at_Time_of_Diagnosis = st.multiselect(
                            "Cirrhosis_Dx_Complications at Time of Diagnosis [ Excel : CIRDX_COMPLDX ] ",
                            options=["ascites", " ariceal hemorrhage","Hepatic encephalopathy","jaundice","SBP", "Hepatorenal Syndrome", "Coagulopathy", "Portal HTN", "PVT", "PVTT","Portal Vein Thrombosis" "none"],
                            help="Provide details of Compilications at time of Diagnosis",
                            placeholder="Select all that apply"
                        )
                        Cirrhosis_Dx_Complications_at_Time_of_Diagnosis_String = ", ".join(Cirrhosis_Dx_Complications_at_Time_of_Diagnosis)

                        Cirrhosis_Dx_Complications_at_Time_of_Diagnosis_Binary = 1 if Cirrhosis_Dx_Complications_at_Time_of_Diagnosis != "none" or Cirrhosis_Dx_Complications_at_Time_of_Diagnosis != None else 0

                        Cirrhosis_Dx_Complications_Free_Text =  st.text_area(
                            "Cirrhosis_Dx_Complications Free Text [ Excel : CIRDX_COMPLFT ]",
                            help="Provide details of Complications"
                        )

                        Cirrhosis_Dx_Date_of_Labs_in_Window = st.date_input(" Cirrhosis_Dx_Date of Labs in Window [ Excel : CIRDX_DATELABS ]",help="Select the date of lab test")

                        Cirrhosis_Dx_AFP = st.text_input(
                            "Cirrhosis_Dx_AFP [ Excel : CIRDX_AFP ]",
                            help="Enter AFP value in ng/dl"
                        )

                        Cirrhosis_Dx_AFP_L3 = st.text_input(
                            "Cirrhosis_Dx_AFP L3 [ Excel : CIRDX_AFPL3 ]",
                            help="Enter AFP_L3 value in ng/dl"
                            
                        )
                        Cirrhosis_Dx_AFP_L3_Date_Free_Text = st.text_area("Cirrhosis_Dx_AFP L3 Date Free Text [ Excel : CIRDX_AFPL3DATEFT ]")

                        Cirrhosis_Dx_Ascites_CTCAE = st.selectbox (
                            "Cirrhosis_Dx_Ascites CTCAE [ Excel : CIRDX_ASCITCTCAE ] ",
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
                                 return 1
                            elif score == "Symptomatic" or score == "moderate ascities/Symptomatic medical intervention":
                                 return 2
                            elif score == "Severe symptoms, invasive intervention indicated" or score == "Life Threatening: Urgent operation intervention indicated" :
                                 return 3
                        
                        Cirrhosis_Dx_Ascites_Classification = 1 if Cirrhosis_Dx_Ascites_CTCAE == "none" else findascitesclass(Cirrhosis_Dx_Ascites_CTCAE)
                        st.write("Cirrhosis_Dx_Ascites Classification ",Cirrhosis_Dx_Ascites_Classification)
                        Cirrhosis_Dx_Ascites_Free_Text = "NA" if Cirrhosis_Dx_Ascites_CTCAE == "none" else st.text_area(
                            "Cirrhosis_Dx_Ascites Free Text [ Excel : CIRDX_ASCITFT ]",
                            
                        
                        )

                        submit_tab3 = st.form_submit_button("Submit")
                        if submit_tab3:

                            data2={
                            "CIRPMH_HBV" : cir_pmh_hbv_status,
                            "CIRPMH_HBVFT" : cir_pmh_hbv_free_text,
                            "CIRPMH_HBVART" : cir_pmh_hbv_art,
                            "CIRPMH_HCV" : cir_pmh_hcv_status,
                            "CIRPMH_HCVFT" : cir_pmh_hcv_free_text,
                            "CIRPMH_HCVART" : cir_pmh_hcv_art,
                            "CIRPMH_AUD" : cir_pmh_alcohol_use_disorder,
                            "CIRPMH_AUDFT" : cir_pmh_alcohol_free_text,
                            "CIRPMH_IVDU" : cir_pmh_ivdu_status,
                            "CIRPMH_IVDUFT" : cir_pmh_ivdu_free_text,
                            "CIRPMH_LIVERFAC" : cir_pmh_liver_addtional_factor,
                            "CIRDX_DATE" : Cirrhosis_Dx_Diagnosis_Date.strftime("%Y-%m-%d"),
                            "CIRDX_METHOD" : Cirrhosis_Dx_Diagnosis_Method,
                            "CIRDX_HPIFT" : Cirrhosis_Dx_HPI_EMR_Note_Free_Text,
                            "CIRDX_IMAGEFT" : Cirrhosis_Dx_Imaging_Findings_EMR_Note_Free_Text,
                            "CIRDX_METAVIR" : Cirrhosis_Dx_Metavir_Score,
                            "CIRDX_COMPLDX" : Cirrhosis_Dx_Complications_at_Time_of_Diagnosis_String,
                            "CIRDX_COMPLDXBIN" : Cirrhosis_Dx_Complications_at_Time_of_Diagnosis_Binary,
                            "CIRDX_COMPLFT" : Cirrhosis_Dx_Complications_Free_Text,
                            "CIRDX_DATELABS" : Cirrhosis_Dx_Date_of_Labs_in_Window.strftime("%Y-%m-%d"),
                            "CIRDX_AFP" : Cirrhosis_Dx_AFP,
                            "CIRDX_AFPL3" : Cirrhosis_Dx_AFP_L3,
                            "CIRDX_AFPL3DATEFT" : Cirrhosis_Dx_AFP_L3_Date_Free_Text,
                            "CIRDX_ASCITCTCAE" : Cirrhosis_Dx_Ascites_CTCAE,
                            "CIRDX_ASCITNUMB" : Cirrhosis_Dx_Ascites_Classification,
                            "CIRDX_ASCITFT" : Cirrhosis_Dx_Ascites_Free_Text,
                                 
                            }
                            if "patient_info" in st.session_state and st.session_state.patient_info["MRN"] == st.session_state.temp_mrn:
                                st.session_state.patient_info.update(data2)
                                # Update the data in Google Sheets
                                update_google_sheet(st.session_state.patient_info, st.session_state.temp_mrn)
                            else:
                                st.error(f"No patient information found for MRN {st.session_state.temp_mrn}")
                    except:
                        st.warning("Please Fill Patient Information Page")

        elif st.session_state.selected_tab == "HCC Diagnosis":
            st.subheader("HCC Diagnosis")
            with st.form("hcc_dx_form"): 
                if "MRN" not in st.session_state.data:
                    st.warning("Please complete the Patient Information tab first.")
                else:
                    try:
                        hcc_dx_hcc_diagnosis_date = st.date_input("HCC_Dx_HCC Diagnosis Date", help="Enter the HCC diagnosis date")

                        hcc_dx_method_of_diagnosis = st.selectbox(
                            "HCC_Dx_Method of Diagnosis [ Excel : HCCDX_METHODDX ]\n\n(1) Biopsy, (2) Imaging, (NA) Unknown  ",   
                             options=["1", "2", "NA"],
                                format_func=lambda x: {
                                    "1": "Biopsy ",
                                    "2": "Imaging ",
                                    "NA": "Unknown ",
                                }[x],
                            index=None,  # No default selection
                            placeholder="Choose an option",
                            
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
                            "HCC_Dx_Ascites CTCAE [ Excel : HCCDX_ASCITCTCAE ] ",
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
                            index=None,  # No default selection
                            placeholder="Choose an option",
                        ) 
                        def findascitesclass(score):
                            if score == "Asymptomatic" or score== "Minimal ascities/Mild abd distension":
                                 return 1
                            elif score == "Symptomatic" or score == "moderate ascities/Symptomatic medical intervention":
                                 return 2
                            elif score == "Severe symptoms, invasive intervention indicated" or score == "Life Threatening: Urgent operation intervention indicated" :
                                 return 3
                        
                        hCC_dx_ascites_classification = 1 if hcc_dx_ascites_CTCAE == "none" else findascitesclass(hcc_dx_ascites_CTCAE)

                        hcc_dx_ascites_diruetics = 0 if hcc_dx_ascites_CTCAE == "none" else st.selectbox(
                            "HCC_Dx_Ascites Diruetics [ Excel : HCCDX_ASCITDIUR ]\n\nYes(1), No(0)  ",
                             options=["1", "0"],
                            format_func=lambda x: {
                                "1": "Yes ",
                                "0": "No ",
                            }[x],
                            index=None,  # No default selection
                            placeholder="Choose an option",
            
                        )
                        hcc_dx_ascites_paracentesis = 0 if hcc_dx_ascites_CTCAE == "none" else st.selectbox(
                            "HCC_Dx_Ascites Paracentesis  [ Excel : HCCDX_ASCITPARA ]\n\nYes(1), No(0)  ",
                             options=["1", "0"],
                            format_func=lambda x: {
                                "1": "Yes ",
                                "0": "No ",
                            }[x],
                            index=None,  # No default selection
                            placeholder="Choose an option",
            
                        )
                        hcc_dx_ascites_hospitalization = 0 if hcc_dx_ascites_CTCAE == "none" else st.selectbox(
                            "HCC_Dx_Ascites Hospitalization [ Excel : HCCDX_ASCITHOSP ]\n\nYes(1), No(0) ",
                             options=["1", "0"],
                            format_func=lambda x: {
                                "1": "Yes ",
                                "0": "No ",
                            }[x],
                            index=None,  # No default selection
                            placeholder="Choose an option",
            
                        )

                        hcc_dx_he_grade = st.selectbox(
                            "HCC_Dx_HE Grade [ Excel : HCCDX_HEGRADE ]\n\n(1) None, (2) Grade 1-2, (3) Grade 3-4    ",
                            options=[1,2,3],
                            format_func=lambda x: {
                            1: "None",
                            2: "Grade 1-2",
                            3: "Grade 3-4",
                            
                        }[x],
                            index=None,  # No default selection
                            placeholder="Choose an option",

                        )
                       
                        hcc_dx_ecog_performance_status = st.selectbox("HCC_Dx_ECOG Performance Status [ Excel : HCCDX_ECOG ]  ", options=["0", "1", "2", "3", "4", "NA"],
                            index=None,  # No default selection
                            placeholder="Choose an option",)

                        hcc_dx_lirads_score = st.selectbox(
                            "HCC_Dx_LIRADS Score  [ Excel : HCCDX_LIRADS ]",
                            options=["LR-1", "LR-2", "LR-3", "LR-4", "LR-5", "LR-5V", "LR-M"],
                            index=None,  # No default selection
                            placeholder="Choose an option",
                        )

                        hcc_dx_child_pugh_points_calc = calculatepoints(hcc_dx_bilirubin,hcc_dx_albumin,hcc_dx_inr,hCC_dx_ascites_classification,hcc_dx_he_grade)
                        hcc_dx_child_pugh_class_calc = calculate_class(hcc_dx_child_pugh_points_calc)
                        st.write("HCC_Dx_Child-Pugh Class calc",hcc_dx_child_pugh_class_calc)
                        st.write("HCC_Dx_Child-Pugh Points calc", hcc_dx_child_pugh_points_calc)
                        hcc_dx_meld_score_calc = meld_calc(hcc_dx_creatinine,hcc_dx_bilirubin,hcc_dx_inr)
                        hcc_dx_meld_na_score_calc = hcc_dx_meld_score_calc + 1.32*(137-int(hcc_dx_sodium)) - (0.033*hcc_dx_meld_score_calc*(137-int(hcc_dx_sodium)))
                        st.write("HCC_Dx_MELD Score calc",hcc_dx_meld_score_calc)                        
                        hcc_dx_albi_score_calc = albi_calc(hcc_dx_bilirubin, hcc_dx_albumin)
                        hcc_dx_albi_grade = albi_class(hcc_dx_albi_score_calc)
                        st.write("HCC_Dx_ALBI Score calc : ",hcc_dx_albi_score_calc)
                        st.write("HCC_Dx_ALBI Grade : ", hcc_dx_albi_grade)
                        hcc_dx_bclc_calc = st.selectbox("HCC_Dx_BCLC Stage calc [ Excel : HCCDX_BCLC ]\n\n(NA) Not in chart, (0) Stage 0, (1) Stage A, (2) Stage B, (3) Stage C, (4) Stage D   ",
                                options=["NA", "0", "1", "2", "3", "4"],
                                format_func=lambda x: {
                                    "NA": "(NA) Not in chart",
                                    "0": " Stage 0: Very early stage, with a single nodule smaller than 2 cm in diameter",
                                    "1": " Stage A: Early stage, with one nodule smaller than 5 cm or up to three nodules smaller than 3 cm",
                                    "2": " Stage B: Intermediate stage, with multiple tumors in the liver",
                                    "3": " Stage C: Advanced stage, with cancer that has spread to other organs or blood vessels",
                                    "4": " Stage D: End-stage disease, with severe liver damage or the patient is very unwell",
                                }[x],
                                index=None,  # No default selection
                                placeholder="Choose an option",
                            )
                        submit_tab4 = st.form_submit_button("Submit")
                        if submit_tab4:
                                data4 = {
                                    "HCCDX_DATEDX": hcc_dx_hcc_diagnosis_date.strftime("%Y-%m-%d"),
                                    "HCCDX_METHODDX": hcc_dx_method_of_diagnosis,
                                    "HCCDX_LABSDATE": hcc_dx_date_of_labs.strftime("%Y-%m-%d"),
                                    "HCCDX_AFP": hcc_dx_afp,
                                    "HCCDX_AFPL3": hcc_dx_afp_l3,
                                    "HCCDX_AFPL3dateFT": hcc_dx_afp_l3_date_free_text,
                                    "HCCDX_BILI": hcc_dx_bilirubin,
                                    "HCCDX_ALBUMIN": hcc_dx_albumin,
                                    "HCCDX_INR": hcc_dx_inr,
                                    "HCCDX_CREATININE": hcc_dx_creatinine,
                                    "HCCDX_SODIUM": hcc_dx_sodium,
                                    "HCCDX_ASCITCTCAE": hcc_dx_ascites_CTCAE,
                                    "HCCDX_ASCITNUMB": hCC_dx_ascites_classification,
                                    "HCCDX_ASCITDIUR": hcc_dx_ascites_diruetics,
                                    "HCCDX_ASCITPARA": hcc_dx_ascites_paracentesis,
                                    "HCCDX_ASCITHOSP": hcc_dx_ascites_hospitalization,
                                    "HCCDX_HEGRADE": hcc_dx_he_grade,
                                    "HCCDX_ECOG": hcc_dx_ecog_performance_status,
                                    "HCCDX_LIRADS": hcc_dx_lirads_score,
                                    "HCCDX_CPCALC": hcc_dx_child_pugh_points_calc,
                                    "HCCDX_CPCLASS": hcc_dx_child_pugh_class_calc,
                                    "HCCDX_MELD": hcc_dx_meld_score_calc,
                                    "HCCDX_MELDNA": hcc_dx_meld_na_score_calc,
                                    "HCCDX_ALBISCORE": hcc_dx_albi_score_calc,
                                    "HCCDX_ALBIGRADE": hcc_dx_albi_grade,
                                    "HCCDX_BCLC": hcc_dx_bclc_calc,
                                }
                                if "patient_info" in st.session_state and st.session_state.patient_info["MRN"] == st.session_state.temp_mrn:
                                    st.session_state.patient_info.update(data4)
                                    # Update the data in Google Sheets
                                    update_google_sheet(data4, st.session_state.temp_mrn)
                                    df=fetch_data_from_google_sheet()
                                else:
                                    st.error(f"No patient information found for MRN {st.session_state.temp_mrn}")
                    except:
                        st.warning("Please Fill Patient Information Page")

        elif st.session_state.selected_tab == "Previous Therapy for HCC":
            st.subheader("Previous Therapy for HCC")
            with st.form("previous_therapy_form"):
                if "MRN" not in st.session_state.data:
                    st.warning("Please complete the Patient Information tab first.")
                else:
                    try:
                        PRVTHER_Prior_LDT_Therapy = st.selectbox(
                        "PRVTHER_Prior_LDT_Therapy [ Excel : PTHER_LDT ]\n\nNo (0), Yes (1), NA",
                        options=["0", "1", "NA"], 
                        format_func=lambda x: {
                            "0": "No",
                            "1": "Yes",
                            "NA": "NA (not in chart)"
                        }[x],
                        help="Prior LDT Therapy",
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )
                        PRVTHER_Prior_RFA_Therapy = st.selectbox(
                            "PRVTHER_Prior RFA Therapy [ Excel : PTHER_RFA ]\n\nNo (0), Yes (1), NA  ",
                           options=["0", "1", "NA"], 
                        format_func=lambda x: {
                            "0": "No",
                            "1": "Yes",
                            "NA": "NA (not in chart)"
                        }[x],
                            help="Prior RFA Therapy",
                            index=None,  # No default selection
                            placeholder="Choose an option",
                        )
                        PRVTHER_Prior_RFA_Date = 0 if PRVTHER_Prior_RFA_Therapy == '0' else st.date_input("PRVTHER_Prior RFA Date")

                    
                        PRVTHER_Prior_TARE_Therapy = st.selectbox(
                            "PRVTHER_Prior TARE Therapy [ Excel : PTHER_TARE ]\n\nNo (0), Yes (1), NA ",
                            options=["0", "1", "NA"], 
                        format_func=lambda x: {
                            "0": "No ",
                            "1": "Yes ",
                            "NA": "NA (not in chart)"
                        }[x],
                            help="Prior TARE Therapy",
                            index=None,  # No default selection
                            placeholder="Choose an option",
                        )
                        PRVTHER_Prior_TARE_Date = 0 if PRVTHER_Prior_TARE_Therapy == '0' else st.date_input("PRVTHER_Prior TARE Date")
                    
                        PRVTHER_Prior_SBRT_Therapy = st.selectbox(
                            "PRVTHER_Prior SBRT Therapy [ Excel : PTHER_SBRT ]\n\nNo (0), Yes (1), NA",
                            options=["0", "1", "NA"], 
                        format_func=lambda x: {
                            "0": "No ",
                            "1": "Yes",
                            "NA": "NA (not in chart)"
                        }[x],
                            help="Prior SBRT Therapy",
                            index=None,  # No default selection
                            placeholder="Choose an option",
                        )
                        
                        PRVTHER_Prior_SBRT_Date = 0 if PRVTHER_Prior_SBRT_Therapy == '0' else st.date_input("PRVTHER_Prior SBRT Date")
                        PRVTHER_Prior_TACE_Therapy = st.selectbox(
                            "PRVTHER_Prior TACE Therapy [ Excel : PTHER_TACE ]\n\nNo (0), Yes (1), NA ",
                            options=["0", "1", "NA"], 
                        format_func=lambda x: {
                            "0": "No ",
                            "1": "Yes ",
                            "NA": "NA (not in chart)"
                        }[x],
                            help="Prior TACE Therapy",
                            index=None,  # No default selection
                            placeholder="Choose an option",
                        )
                        PRVTHER_Prior_TACE_Date = 0 if PRVTHER_Prior_TACE_Therapy == '0' else st.date_input("PRVTHER_Prior TACE Date")

                        PRVTHER_Prior_MWA_Therapy = st.selectbox(
                            "PRVTHER_Prior MWA Therapy [ Excel : PTHER_MWA ]\n\nNo (0), Yes (1), NA",
                            options=["0", "1", "NA"], 
                        format_func=lambda x: {
                            "0": "No ",
                            "1": "Yes ",
                            "NA": "NA (not in chart)"
                        }[x],
                            help="Prior MWA Therapy",
                            index=None,  # No default selection
                            placeholder="Choose an option",
                        )
                        PRVTHER_Prior_MWA_Date = 0 if PRVTHER_Prior_MWA_Therapy == '0' else st.date_input("PRVTHER_Prior MWA Date")

                        PRVTHER_Resection = st.selectbox(
                            "PRVTHER_Resection [ Excel : PTHER_RESECTION ]\n\nNo (0), Yes (1), NA ",
                            options=["0", "1", "NA"], 
                        format_func=lambda x: {
                            "0": "No ",
                            "1": "Yes ",
                            "NA": "NA (not in chart)"
                        }[x],
                            help="Prior MWA Therapy",
                            index=None,  # No default selection
                            placeholder="Choose an option",
                        )
                        PRVTHER_Resection_Date = 0 if PRVTHER_Resection == '0' else st.date_input("PRVTHER_Resection Date")


                        list1=[PRVTHER_Prior_LDT_Therapy, PRVTHER_Prior_RFA_Therapy, PRVTHER_Prior_TARE_Therapy, PRVTHER_Prior_SBRT_Therapy, PRVTHER_Prior_TACE_Therapy, PRVTHER_Prior_MWA_Therapy, PRVTHER_Resection ]
                        total_sum=0
                        for item in list1:
                            if item == "Yes" :
                                total_sum+=1
                            else:
                                continue
                        
                        PRVTHER_Previous_Therapy_Sum = total_sum
                        st.write("PRVTHER_Prevtxsum ",PRVTHER_Previous_Therapy_Sum)
                   
                        PRVTHER_NotesFT = st.text_area(
                        "PRVTHER_NotesFT",
                        )

                        PRVTHER_Total_Recurrences_HCC = st.text_area(
                            "PRVTHER_Total Recurrences HCC",
                        )
                        PRVTHER_Location_of_Previous_Treatment_segments = st.selectbox(
                            "PRVTHER_Location of Previous Treatment Segments [ Excel : PTHER_PREVSEGMENT ]",
                            options=["1","2","3","4a","4b","5","6","7","8","NA"],
                            index=None,
                            placeholder="Choose an option"
                        )
                        PRVTHER_Location_of_Previous_Tx_segments_ft = st.text_area(
                            "PRVTHER_Location of Previous Tx Segments FT",
                          
                        )
                        PRVTHER_recurrence_location_note = st.selectbox(
                            "PRVTHER_Recurrence Location Note [ Excel : PTHER_RECURSEGMENTFT ]",
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
                            "PRVTHER_New HCC Outside Previous Treatment Site [ Excel : PTHER_NEWHCCOUT ]\n\nNo (0), Yes (1), NA",
                            options=["0", "1", "NA"], 
                        format_func=lambda x: {
                            "0": "No ",
                            "1": "Yes ",
                            "NA": "NA (not in chart)"
                        }[x],
                            index=None,
                            placeholder="Choose an option"
                        )   
                        PRVTHER_New_HCC_Adjacent_to_Previous_Treatment_Site = st.selectbox(
                            "PRVTHER_New HCC Adjacent to Previous Treatment Site [ Excel : PTHER_NEWHCCADJ ]\n\nNo (0), Yes (1), NA ",
                            options=["0", "1", "NA"], 
                        format_func=lambda x: {
                            "0": "No ",
                            "1": "Yes ",
                            "NA": "NA (not in chart)"
                        }[x],
                            index=None,
                            placeholder="Choose an option"
                        )   
                        PRVTHER_Residual_HCC_Note = st.text_area(
                            "PRVTHER_Residual HCC Note",
                            help="Provide information of Residual HCC"
                        ) 
                        PRVTHER_Residual_HCC = st.selectbox(
                            "PRVTHER_Residual HCC [ Excel : PTHER_RESIDUALHCC ]\n\nNo (0), Yes (1), NA ",
                            options=["0", "1", "NA"], 
                        format_func=lambda x: {
                            "0": "No ",
                            "1": "Yes ",
                            "NA": "NA (not in chart)"
                        }[x],
                            index=None,
                            placeholder="Choose an option"
                        )   

                        PRVTHER_Systemic_Therapy_Free_Text = st.selectbox(
                            "PRVTHER_Systemic Therapy Free Text [ Excel : PTHER_SYSTHER ]\n\nNo (0), Yes (1), NA ",
                            options=["0", "1", "NA"], 
                        format_func=lambda x: {
                            "0": "No ",
                            "1": "Yes ",
                            "NA": "NA (not in chart)"
                        }[x],
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
                            "PTHER_LDT": PRVTHER_Prior_LDT_Therapy,
                            "PTHER_RFA": PRVTHER_Prior_RFA_Therapy,
                            "PTHER_RFADATE": PRVTHER_Prior_RFA_Date.strftime("%Y-%m-%d") if PRVTHER_Prior_RFA_Date != 0 else PRVTHER_Prior_RFA_Date,
                            "PTHER_TARE": PRVTHER_Prior_TARE_Therapy,
                            "PTHER_TAREDATE": PRVTHER_Prior_TARE_Date.strftime("%Y-%m-%d") if PRVTHER_Prior_TARE_Date != 0 else PRVTHER_Prior_TARE_Date,
                            "PTHER_SBRT": PRVTHER_Prior_SBRT_Therapy,
                            "PTHER_SBRTDATE": PRVTHER_Prior_SBRT_Date.strftime("%Y-%m-%d") if PRVTHER_Prior_SBRT_Date != 0 else PRVTHER_Prior_SBRT_Date,
                            "PTHER_TACE": PRVTHER_Prior_TACE_Therapy,
                            "PTHER_TACEDATE": PRVTHER_Prior_TACE_Date.strftime("%Y-%m-%d") if PRVTHER_Prior_TACE_Date != 0 else PRVTHER_Prior_TACE_Date,
                            "PTHER_MWA": PRVTHER_Prior_MWA_Therapy,
                            "PTHER_MWADATE": PRVTHER_Prior_MWA_Date.strftime("%Y-%m-%d") if PRVTHER_Prior_MWA_Date != 0 else PRVTHER_Prior_MWA_Date,
                            "PTHER_RESECTION": PRVTHER_Resection,
                            "PTHER_RESECTIONDATE": PRVTHER_Resection_Date.strftime("%Y-%m-%d") if PRVTHER_Resection_Date != 0 else PRVTHER_Resection_Date,
                            "PTHER_PREVSUM": PRVTHER_Previous_Therapy_Sum,
                            "PTHER_NOTESFT": PRVTHER_NotesFT,
                            "PTHER_TOTRECUR": PRVTHER_Total_Recurrences_HCC,
                            "PTHER_PREVSEGMENT": PRVTHER_Location_of_Previous_Treatment_segments,
                            "PTHER_PREVSEGMENTFT": PRVTHER_Location_of_Previous_Tx_segments_ft,
                            "PTHER_RECURSEGMENTFT": PRVTHER_recurrence_location_note,
                            "PTHER_RECURDATE": PRVTHER_recurrence_date,
                            "PTHER_RECURSEGMENT": PRVTHER_recurrence_seg,
                            "PTHER_NEWHCCOUT": PRVTHER_New_HCC_Outside_Previous_Treatment_Site,
                            "PTHER_NEWHCCADJ": PRVTHER_New_HCC_Adjacent_to_Previous_Treatment_Site,
                            "PTHER_RESIDUALHCCFT": PRVTHER_Residual_HCC_Note,
                            "PTHER_RESIDUALHCC": PRVTHER_Residual_HCC,
                            "PTHER_SYSTHER": PRVTHER_Systemic_Therapy_Free_Text,
                            "PTHER_AFPDATE": PRVTHER_Date_of_Labs_in_Window.strftime("%Y-%m-%d"),
                            "PTHER_AFP": PRVTHER_AFP,
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
                        "PREY90_symptoms [Excel : PREY_SX]",
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
                            "PREY90_Ascites CTCAE [Excel : PREY_ASCITCTCAE]",
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
                                 return 1
                            elif score == "Symptomatic" or score == "moderate ascities/Symptomatic medical intervention":
                                 return 2
                            elif score == "Severe symptoms, invasive intervention indicated" or score == "Life Threatening: Urgent operation intervention indicated" :
                                 return 3
                        
                        prey90_ascites_classification = 1 if prey90_ascites_ctcae == "none" else findascitesclass(prey90_ascites_ctcae)
                        st.write("PREY90_AscitesCTCAEnumb ",prey90_ascites_classification)
                        prey90_ascites_free_text = st.text_area(
                            "PREY90_Ascites Free Text",
                        
                        )

                        prey90_ascites_diruetics = st.selectbox(
                            "PREY90_Ascites Diruetics [ Excel : PREY_ASCITDIUR ]\n\nYes(1), No(0), NA  ",
                            options=["1", "0","NA"],
                            format_func=lambda x: {
                                "1": "Yes ",
                                "0": "No ",
                                "NA" : "NA (not in chart)"
                            }[x],
                            index=None,  # No default selection
                            placeholder="Choose an option",
            
                        )
                        prey90_ascites_paracentesis = st.selectbox(
                            "PREY90_Ascites Paracentesis [Excel :PREY_ASCITPARA]\n\nYes(1), No(0), NA" ,
                            options=["1", "0","NA"],
                            format_func=lambda x: {
                                "1": "Yes ",
                                "0": "No ",
                                "NA" : "NA (not in chart)"
                            }[x],
                            index=None,  # No default selection
                            placeholder="Choose an option",
            
                        )
                        prey90_ascites_hospitalization = st.selectbox(
                            "PREY90_Ascites Hospitalization [Excel : PREY_ASCITHOSP]\n\nYes(1), No(0), NA",
                            options=["1", "0","NA"],
                            format_func=lambda x: {
                                "1": "Yes ",
                                "0": "No ",
                                "NA" : "NA (not in chart)"
                            }[x],
                            index=None,  # No default selection
                            placeholder="Choose an option",
            
                        )

                        prey90_he_grade = st.selectbox(
                            "PREY90_HE Grade [ Excel : PREY_HEGRADE ]\n\n(1) None, (2) Grade 1-2, (3) Grade 3-4 ",
                            options=[1,2,3],
                            format_func=lambda x: {
                            1: "None",
                            2: "Grade 1-2",
                            3: "Grade 3-4",
                            
                        }[x],
                            index=None,  # No default selection
                            placeholder="Choose an option",

                        )
                       
                        prey90_ecog = st.selectbox("PREY90_ECOG [Excel : PREY_ECOG]", options=["0", "1", "2", "3", "4", "NA"],
                            index=None,  # No default selection
                            placeholder="Choose an option",)

                        
                        # Claculation of class and points
                        prey90_child_pugh_points_calc = calculatepoints(prey90_bilirubin,prey90_albumin,prey90_inr,prey90_ascites_classification,prey90_he_grade)
                        st.write("PREY90_CPcalc",prey90_child_pugh_points_calc)
                        prey90_child_pugh_class_calc = calculate_class(prey90_child_pugh_points_calc)
                        st.write("PREY90_CPclass",prey90_child_pugh_class_calc)
                        prey90_meld_score_calc = meld_calc(prey90_creatinine,prey90_bilirubin,prey90_inr)
                        st.write("PREY90_MELD",prey90_meld_score_calc)
                        prey90_meld_na_score_calc = prey90_meld_score_calc + 1.32*(137-int(prey90_sodium)) - (0.033*prey90_meld_score_calc*(137-int(prey90_sodium)))
                        st.write("PREY90_MELDNa",prey90_meld_na_score_calc)
                        prey90_albi_score_calc = albi_calc(prey90_bilirubin,prey90_albumin)
                        st.write("PREY90_Albiscore",prey90_albi_score_calc)
                        prey90_albi_grade = albi_class(prey90_albi_score_calc)
                        st.write("PREY90_Albigrade",prey90_albi_grade)
                        prey90_bclc_calc = st.selectbox("PREY90_BCLC Stage calc [ Excel : PREY_BCLC ]\n\n(NA) Not in chart, (0) Stage 0, (1) Stage A, (2) Stage B, (3) Stage C, (4) Stage D   ",
                                options=["NA", "0", "1", "2", "3", "4"],
                                format_func=lambda x: {
                                    "NA": "(NA) Not in chart",
                                    "0": " Stage 0: Very early stage, with a single nodule smaller than 2 cm in diameter",
                                    "1": " Stage A: Early stage, with one nodule smaller than 5 cm or up to three nodules smaller than 3 cm",
                                    "2": " Stage B: Intermediate stage, with multiple tumors in the liver",
                                    "3": " Stage C: Advanced stage, with cancer that has spread to other organs or blood vessels",
                                    "4": " Stage D: End-stage disease, with severe liver damage or the patient is very unwell",
                                }[x],
                                index=None,  # No default selection
                                placeholder="Choose an option",
                            )
                    
                        st.subheader("Mapping Y90")
                        my90_date = st.date_input("MY90_date", help="Enter the date")
                        my90_lung_shunt = st.number_input("MY90_Lung_shunt", min_value=0.0, step=0.1, help="Enter the lung shunt value")

                        submit_tab6 = st.form_submit_button("Submit")

                        if submit_tab6:

                            data6 = {
                            "PREY_SX": prey90_symptoms,
                            "PREY_DATELABS": prey90_date_of_labs.strftime("%Y-%m-%d"),
                            "PREY_AFP": prey90_afp,
                            "PREY_AFPBINARY": prey90_afp_prior_to_tare,
                            "PREY_BILI": prey90_bilirubin,
                            "PREY_ALBUMIN": prey90_albumin,
                            "PREY_INR": prey90_inr,
                            "PREY_CREATININE": prey90_creatinine,
                            "PREY_SODIUM": prey90_sodium,
                            "PREY_AST": prey90_ast,
                            "PREY_ALT": prey90_alt,
                            "PREY_ALP": prey90_alkaline_phosphatase,
                            "PREY_POTAS": prey90_potassium,
                            "PREY_ASCITCTCAE": prey90_ascites_ctcae,
                            "PREY_ASCITNUMB": prey90_ascites_classification,
                            "PREY_ASCITFT": prey90_ascites_free_text,
                            "PREY_ASCITDIUR": prey90_ascites_diruetics,
                            "PREY_ASCITPARA": prey90_ascites_paracentesis,
                            "PREY_ASCITHOSP": prey90_ascites_hospitalization,
                            "PREY_HEGRADE": prey90_he_grade,
                            "PREY_ECOG": prey90_ecog,
                            "PREY_CPCALC": prey90_child_pugh_points_calc,
                            "PREY_CLASS": prey90_child_pugh_class_calc,
                            "PREY_MELD": prey90_meld_score_calc,
                            "PREY_MELDNA": prey90_meld_na_score_calc,
                            "PREY_ALBISCORE": prey90_albi_score_calc,
                            "PREY_ALBIGRADE": prey90_albi_grade,
                            "PREY_BCLC": prey90_bclc_calc,
                            "MY_DATE": my90_date.strftime("%Y-%m-%d"),
                            "MY_LUNGSHU": my90_lung_shunt,
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
                                return "Fill AFP"
                        #df.loc[df["MRN"] == mrn, "PREY_AFPBINARY"].values[0]
                        dayy90_afp_prior_to_tare = process_input(dayy90_afp)
                        st.write("DAYY90_AFP Binary : ",dayy90_afp_prior_to_tare)
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
                            "DAYY90_Ascites CTCAE [Excel : DAYY_ASCITCTCAE]  ",
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
                                 return 1
                            elif score == "Symptomatic" or score == "moderate ascities/Symptomatic medical intervention":
                                 return 2
                            elif score == "Severe symptoms, invasive intervention indicated" or score == "Life Threatening: Urgent operation intervention indicated" :
                                 return 3
                        
                        dayy90_ascites_classification = 1 if dayy90_ascites_ctcae == "none" else findascitesclass(dayy90_ascites_ctcae)
                        st.write("Day90_AscitesCTCAEnumb",dayy90_ascites_classification)
                        dayy90_he_grade = st.selectbox(
                            "DAYY90_HE Grade [Excel : DAYY_HEGRADE]\n\n(1) None, (2) Grade 1-2, (3) Grade 3-4",
                            options=[1,2,3],
                            format_func=lambda x: {
                            1: "None",
                            2: "Grade 1-2",
                            3: "Grade 3-4",
                            
                        }[x],
                            index=None,  # No default selection
                            placeholder="Choose an option",
                        )
                       
                        dayy90_ecog = st.selectbox("DAYY90_ECOG [Excel : DAYY_ECOG]  ", options=["0", "1", "2", "3", "4", "NA"],
                            index=None,  # No default selection
                            placeholder="Choose an option",)
                        
                        dayy90_child_pugh_points_calc = calculatepoints(dayy90_bilirubin,dayy90_albumin,dayy90_inr,dayy90_ascites_classification,dayy90_he_grade)
                        st.write("DAYY90_CPcalc",dayy90_child_pugh_points_calc)
                        dayy90_child_pugh_class_calc = calculate_class(dayy90_child_pugh_points_calc)
                        st.write("DAYY90_CPclass",dayy90_child_pugh_class_calc)
                        dayy90_meld_score_calc = meld_calc(dayy90_creatinine,dayy90_bilirubin,dayy90_inr)
                        st.write("DAYY90_MELD",dayy90_meld_score_calc)
                        dayy90_meld_na_score_calc = dayy90_meld_score_calc + 1.32*(137-int(dayy90_sodium)) - (0.033*dayy90_meld_score_calc*(137-int(dayy90_sodium)))
                        st.write("DAYY90_MELDNa",dayy90_meld_na_score_calc)
                        dayy90_albi_score_calc = albi_calc(dayy90_bilirubin,dayy90_albumin)
                        st.write("DAYY90_Albiscore",dayy90_albi_score_calc)
                        dayy90_albi_grade = albi_class(dayy90_albi_score_calc)
                        st.write("DAYY90_Albigrade",dayy90_albi_grade)
                       
                        dayy90_bclc_calc = st.selectbox("PREY90_BCLC Stage calc [ Excel : DAYY_BCLC ]\n\n(NA) Not in chart, (0) Stage 0, (1) Stage A, (2) Stage B, (3) Stage C, (4) Stage D   ",
                                options=["NA", "0", "1", "2", "3", "4"],
                                format_func=lambda x: {
                                    "NA": "(NA) Not in chart",
                                    "0": " Stage 0: Very early stage, with a single nodule smaller than 2 cm in diameter",
                                    "1": " Stage A: Early stage, with one nodule smaller than 5 cm or up to three nodules smaller than 3 cm",
                                    "2": " Stage B: Intermediate stage, with multiple tumors in the liver",
                                    "3": " Stage C: Advanced stage, with cancer that has spread to other organs or blood vessels",
                                    "4": " Stage D: End-stage disease, with severe liver damage or the patient is very unwell",
                                }[x],
                                index=None,  # No default selection
                                placeholder="Choose an option",
                            )

                        dayy90_type_of_sphere = st.selectbox(
                            "DAYY90_Type of Sphere [Excel : DAYY_SPHERE]\n\n(1) Therasphere, (2) SIR", options=["1", "2"],
                            format_func=lambda x: {
                                    "1": "Therasphere",
                                    "2": "SIR",
                                }[x],
                            index=None,  # No default selection
                            placeholder="Choose an option",
                        )

                        dayy90_lt_notes_ftx = st.text_area("DAYY90_LT Notes Free Text")

                        ken_childpughscore = st.selectbox(
                            "ken_ChildPughscore [Excel : KEN_CPPRE]\n\n(1) A, (2) B, (3) C ",
                            options=["1","2","3"],
                            format_func=lambda x: {
                                    "1": "A",
                                    "2": "B",
                                    "3": "C"
                                }[x],
                            index=None,  # No default selection
                            placeholder="Choose an option",
                        )
                        ken_meldpretare = st.number_input("ken_MELDpreTARE",step=0.1)


                    # Submit button
                        submit_tab7 = st.form_submit_button("Submit")
                    
                        if submit_tab7:
                            data7 = {
                                "DAYY_AFP": dayy90_afp,
                                "DAYY_AFPBINARY": dayy90_afp_prior_to_tare,
                                "DAYY_SODIUM": dayy90_sodium,
                                "DAYY_CREATININE": dayy90_creatinine,
                                "DAYY_INR": dayy90_inr,
                                "DAYY_ALBUMIN": dayy90_albumin,
                                "DAYY_BILI": dayy90_bilirubin,
                                "DAYY_AST": dayy90_ast,
                                "DAYY_ALT": dayy90_alt,
                                "DAYY_ALP": dayy90_alkaline_phosphatase,
                                "DAYY_LEUK": dayy90_leukocytes,
                                "DAYY_PLT": dayy90_platelets,
                                "DAYY_POTAS": dayy90_potassium,
                                "DAYY_ASCITCTCAE": dayy90_ascites_ctcae,
                                "DAYY_ASCITNUMB": dayy90_ascites_classification,
                                "DAYY_HEGRADE": dayy90_he_grade,
                                "DAYY_ECOG": dayy90_ecog,
                                "DAYY_CPCALC": dayy90_child_pugh_points_calc,
                                "DAYY_CPCLASS": dayy90_child_pugh_class_calc,
                                "DAYY_MELD": dayy90_meld_score_calc,
                                "DAYY_MELDNA": dayy90_meld_na_score_calc,
                                "DAYY_ALBISCORE": dayy90_albi_score_calc,
                                "DAYY_ALBIGRADE": dayy90_albi_grade,
                                "DAYY_BCLC": dayy90_bclc_calc,
                                "DAYY_SPHERE": dayy90_type_of_sphere,
                                "DAYY_LTFT": dayy90_lt_notes_ftx,
                                "KEN_CPPRE": ken_childpughscore,
                                "KEN_MELDPRE": ken_meldpretare
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
                        "30DY_AE_AscitesCTCAE [Excel : POST30_ASCITCTCAE]",
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
                        st.write("POST 30 days Y90 Ascites CTCAE Number" ,posty90_ascites_classification)
                        posty90_ascites_diruetics = st.selectbox(
                            "30DY_AE_Ascitesdiruetics[Excel : POST30_ASCITDIUR]\n\n Yes (1), No (0)",
                                options=["1", "0"],
                                format_func=lambda x: {
                                        "1": "Yes",
                                        "0": "No",
                                    }[x],
                            index= None,
                            placeholder="Choose an option",
            
                        )
                        posty90_ascites_paracentesis = st.selectbox(
                            "30DY_AE_Ascitesparacentesis[Excel : POST30_ASCITPARA]\n\n Yes (1), No (0)",
                                options=["1", "0"],
                                format_func=lambda x: {
                                        "1": "Yes",
                                        "0": "No",
                                    }[x],
                            index=  None,
                            placeholder="Choose an option",
            
                        )
                        posty90_ascites_hospitalization = st.selectbox(
                            "30DY_AE_Asciteshospitalization[Excel : POST30_ASCITHOSP]\n\n Yes (1), No (0)",
                                options=["1", "0"],
                                format_func=lambda x: {
                                        "1": "Yes",
                                        "0": "No",
                                    }[x],
                            index=None,
                            placeholder="Choose an option",
            
                        )
                        posty90_he_grade = st.selectbox(
                            "30DY_AE_HE Grade [Excel : POST30_HEGRADE]\n\n(1) None, (2) Grade 1-2, (3) Grade 3-4",
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

                        posty90_ecog = st.selectbox("POSTY90_30DY_ECOG [Excel : POST30_ECOG]", options=["0", "1", "2", "3", "4", "NA"],
                            index=None,  # No default selection
                            placeholder="Choose an option",
                            )
                        
                        posty90_child_pugh_points = calculatepoints(posty90_bilirubin,posty90_albumin,posty90_inr,posty90_ascites_classification,posty90_he_grade)
                        st.write("DAYY90_CPcalc",posty90_child_pugh_points)
                        posty90_child_pugh_class = calculate_class(posty90_child_pugh_points)
                        # Additional Calculated Fields
                        st.write("DAYY90_CPclass",posty90_child_pugh_class)
                        posty90_meld = meld_calc(posty90_creatinine,posty90_bilirubin,posty90_inr)
                        st.write("DAYY90_MELD",posty90_meld)
                        posty90_meld_na = posty90_meld + 1.32*(137-int(posty90_sodium)) - (0.033*posty90_meld*(137-int(posty90_sodium)))
                        st.write("DAYY90_MELDNa",posty90_meld_na)
                        posty90_albi_score = albi_calc(posty90_bilirubin,posty90_albumin)
                        st.write("DAYY90_Albiscore",posty90_albi_score)
                        posty90_albi_grade = albi_class(posty90_albi_score)
                        st.write("DAYY90_Albigrade",posty90_albi_grade)

                        posty90_bclc = st.selectbox("PREY90_BCLC Stage calc [ Excel : POST30_BCLC ]\n\n(NA) Not in chart, (0) Stage 0, (1) Stage A, (2) Stage B, (3) Stage C, (4) Stage D   ",
                            options=["NA", "0", "1", "2", "3", "4"],
                            format_func=lambda x: {
                                "NA": "(NA) Not in chart",
                                "0": " Stage 0: Very early stage, with a single nodule smaller than 2 cm in diameter",
                                "1": " Stage A: Early stage, with one nodule smaller than 5 cm or up to three nodules smaller than 3 cm",
                                "2": " Stage B: Intermediate stage, with multiple tumors in the liver",
                                "3": " Stage C: Advanced stage, with cancer that has spread to other organs or blood vessels",
                                "4": " Stage D: End-stage disease, with severe liver damage or the patient is very unwell",
                            }[x],
                            index = None,
                            placeholder="Choose an option"
                            )
                    
                        ken_bclc_stage_post90 = st.text_input(
                            "Ken_BCLCStagepost90",
                            help="Enter BCLC Stage Post-90",
                          
                        )
                        ken_meld_stage_post90 = st.text_input(
                            "Ken_MELD_Stagepost90",
                            help="Enter MELD Score Pre-TARE",
                           
                        )
                        ## New Part
                        st.subheader("Post_Y90_within_30_days_adverse_events")
                        DYAE_CTCAE_portal_htn = st.selectbox(
                            "30DYAE_portal_htn CTCAE [Excel : AE30_PORTHTN]",
                            options=["0","1","2","3","4","5"],
                        index=None,
                        placeholder="Choose an option",
                        )
                        DYAE_CTCAE_Vascular_comp = st.selectbox(
                            "30DYAE_Vascular comp CTCAE [Excel : AE30_VASCULAR]",
                            options=["0","1","2","3","4","5"],
                        index= None,
                        placeholder="Choose an option",
                        )
                        DYAE_CTCAE_fatigue = st.selectbox(
                            "30DYAE_fatigue CTCAE [Excel : AE30_FATIGUE]",
                            options=["0","1","2"],
                        index= None,
                        placeholder="Choose an option",
                        )
                        DYAE_CTCAE_diarrhea = st.selectbox(
                            "30DYAE_diarrhea CTCAE [Excel : AE30_DIAR]",
                            options=["0","1","2","3","4","5"],
                        index= None,
                        placeholder="Choose an option",
                        )
                        #Formula
                        DYAE_CTCAE_hypoalbuminemia_emr = hypoalbuminemia(posty90_albumin)
                        st.write("30 Days AE_hypoalbuminemia CTCAE : ",DYAE_CTCAE_hypoalbuminemia_emr)
                        DYAE_CTCAE_hyperbilirubinemia_emr = 0
                        DYAE_CTCAE_Increase_creatinine_emr = 0
                        try:
                            prey90_bili = get_variable_value(st.session_state.temp_mrn,"PREY_BILI")
                           
                            if prey90_bili in [None, "", " "]:  # Ensure it's valid before using
                                st.error("Cannot calculate 30 Days AE_hyperbilirubinemia CTCAE due to No data in PREY_BILI.")
                            else:
                                prey90_bili= float(prey90_bili)
                                DYAE_CTCAE_hyperbilirubinemia_emr = hyperbillirubine(prey90_bili,posty90_bilirubin)
                                st.write("30 Days AE_hyperbilirubinemia CTCAE : ",DYAE_CTCAE_hyperbilirubinemia_emr)

                            prey90_creatinine = get_variable_value(st.session_state.temp_mrn,"PREY_CREATININE")
                            
                            if prey90_creatinine in [None, "", " "]:  # Ensure it's valid before using
                                st.error("Cannot calculate 30 Days AE_CTCAE_Increase creatinine CTCAE due to No data in PREY_CREATININE.")
                            else:
                                prey90_creatinine= float(prey90_creatinine)
                                DYAE_CTCAE_Increase_creatinine_emr = Increasecreatine(prey90_creatinine,posty90_creatinine)
                                st.write("30 Days AE_CTCAE_Increase creatinine CTCAE : ",DYAE_CTCAE_Increase_creatinine_emr)
                        except:
                            st.warning("Fill Patient Info")

                        DYAE_CTCAE_abdominal_pain = st.selectbox(
                            "30DYAE_abdominal pain CTCAE [Excel : AE30_ABDPAIN]",
                            options=["0","1","2","3"],
                        index= None,
                        placeholder="Choose an option",
                        )
                        DYAE_CTCAE_sepsis = st.selectbox(
                            "30DYAE_sepsis CTCAE [Excel : AE30_SEPSIS]",
                            options=["0","3","4","5"],
                        index= None,
                        placeholder="Choose an option",
                        )
                        DYAE_CTCAE_bacterial_peritonitis = st.selectbox(
                            "30DYAE_CTCAE_bacterial_peritonitis [Excel : AE30_BACTPER]",
                            options=["0", "3", "4", "5"],
                        index= None,
                        placeholder="Choose an option",
                        )
                        DYAE_CTCAE_hemorrhage = st.selectbox(
                        "30DYAE_CTCAE_hemorrhage [Excel : AE30_HEMOR]",
                        options=["0", "3", "4", "5"],
                        index= None,
                        placeholder="Choose an option",
                        )
                        DYAE_CTCAE_anorexia = st.selectbox(
                            "30DYAE_CTCAE_anorexia [Excel : AE30_ANOREX]",
                            options=["0", "1", "2", "3"],
                        index=None,
                        placeholder="Choose an option",
                        )
                        DYAE_CTCAE_intrahepatic_fistula = st.selectbox(
                            "30DYAE_CTCAE_intrahepatic_fistula [Excel : AE30_IHFIST]",
                            options=["0","2", "3", "4", "5"],
                        index= None,
                        placeholder="Choose an option",
                        )
                        DYAE_CTCAE_constipation = st.selectbox(
                            "30DYAE_CTCAE_constipation [Excel : AE30_CONSTI]",
                            options=["0", "1", "2", "3"],
                        index=None,
                        placeholder="Choose an option",
                        )
                        DYAE_CTCAE_nausea = st.selectbox(
                            "30DYAE_CTCAE_nausea [Excel : AE30_NAUS]",
                            options=["0", "1", "2", "3"],
                        index= None,
                        placeholder="Choose an option",
                        )
                        DYAE_CTCAE_vomiting = st.selectbox(
                            "30DYAE_CTCAE_vomiting [Excel : AE30_VOM]",
                            options=["0","1","2", "3", "4", "5"],
                        index= None,
                        placeholder="Choose an option",
                        )
                        DYAE_CTCAE_cholecystitis = st.selectbox(
                            "30DYAE_CTCAE_cholecystitis [Excel : AE30_CHOLE]",
                            options=["0", "2","3", "4", "5"],
                        index=None,
                        placeholder="Choose an option",
                        )
                        DYAE_CTCAE_gastric_ulcers = st.selectbox(
                            "30DYAE_CTCAE_gastric_ulcers [Excel : AE30_GULCER]",
                            options=["0","1","2", "3", "4", "5"],
                        index= None,
                        placeholder="Choose an option",
                        )
                        
                        DYAE_CTCAE_respiratory_failure = st.selectbox(
                            "30DYAE_CTCAE_respiratory_failure [Excel : AE30_RESPFAIL]",
                            options=["0", "4", "5"],
                        index=None,
                        placeholder="Choose an option",
                        )
                        DYAE_CTCAE_AKI = st.selectbox(
                            "30DYAE_CTCAE_AKI [Excel : AE30_AKI]",
                            options=["0", "3", "4", "5"],
                        index= None,
                        placeholder="Choose an option",
                        )

                        DYAE_CTCAE_Radiation_pneumonitis = st.selectbox(
                            "30DYAE_CTCAE_Radiation_pneumonitis [Excel : AE30_RADPNEUM]",
                            options=["0","1","2", "3", "4", "5"],
                        index= None,
                        placeholder="Choose an option",
                        )

                        DYAE_CTCAE_hyperkalemia = hyperkalemia(posty90_potassium)
                        st.write("30 Days AE CTCAE Hyperkalemia",DYAE_CTCAE_hyperkalemia)
                        ae30_alt = 0
                        ae30_ast = 0
                        ae30_alp = 0
                        try:
                            day90_alt = get_variable_value(st.session_state.temp_mrn, "DAYY_ALT")
                            
                            if day90_alt in [None, "", " "]:  # Ensure it's valid before using
                                st.error("Cannot calculate AE30_ALT due to No data in DAYY_ALT.")
                            else:
                                day90_alt= float(day90_alt)
                                ae30_alt = alt_calculate(day90_alt, posty90_alt)
                                st.write("30 Days AE CTCAE ALT",ae30_alt)

                            day90_ast = get_variable_value(st.session_state.temp_mrn,"DAYY_AST")
                            
                            if day90_ast in [None, "", " "]:  # Ensure it's valid before using
                                st.error("Cannot calculate AE30_AST due to No data in DAYY_AST.")
                            else:
                                day90_ast= float(day90_ast)
                                ae30_ast = ast_calculate(day90_ast, posty90_ast)
                                st.write("30 Days AE CTCAE AST",ae30_ast)

                            day90_alp = get_variable_value(st.session_state.temp_mrn,"DAYY_ALP")
                            
                            if day90_alp in [None, "", " "]:  # Ensure it's valid before using
                                st.error("Cannot calculate AE30_AST due to No data in DAYY_ALP.")
                            else:
                                day90_alp= float(day90_alp)
                                ae30_alp = ast_calculate(day90_alp, posty90_alkaline_phosphatase)
                                st.write("30 Days AE CTCAE  Alkaline Phosphatase",ae30_alp)
                        except:
                            st.warning("Fill Patient Info.")
                        ae30_plt = plt_calculate(posty90_platelets)
                        st.write("30 Days AE CTCAE Platelets",ae30_plt)

                        ae30_otherft = st.text_input("AE30_OTHERFT",)
                        ae30_other = st.text_input("AE30_OTHER",)

                        variables = [
                                    DYAE_CTCAE_portal_htn, DYAE_CTCAE_Vascular_comp, DYAE_CTCAE_fatigue, DYAE_CTCAE_diarrhea,
                                    DYAE_CTCAE_hypoalbuminemia_emr, DYAE_CTCAE_hyperbilirubinemia_emr, DYAE_CTCAE_Increase_creatinine_emr,
                                    DYAE_CTCAE_abdominal_pain, DYAE_CTCAE_sepsis, DYAE_CTCAE_bacterial_peritonitis, DYAE_CTCAE_hemorrhage,
                                    DYAE_CTCAE_anorexia, DYAE_CTCAE_intrahepatic_fistula, DYAE_CTCAE_constipation, DYAE_CTCAE_nausea,
                                    DYAE_CTCAE_vomiting, DYAE_CTCAE_cholecystitis, DYAE_CTCAE_gastric_ulcers, DYAE_CTCAE_respiratory_failure,
                                    DYAE_CTCAE_AKI, DYAE_CTCAE_Radiation_pneumonitis, DYAE_CTCAE_hyperkalemia, ae30_alt, ae30_ast, ae30_alp, ae30_plt
                                ]

                        # Count the occurrences of 1 or 2
                        count = sum(1 for value in variables if value in ["1", "2",1,2])
                        count1 = sum(1 for value in variables if value not in ["1", "2",1,2,"",None])

                        ae30_gradesum12 = count
                        ae30_gradesum345 = count1

                        DYAE_AE_other = st.text_area(
                            "30DY_AE_other",
                            help="Other Adverse Events (Free Text)",
                            
                        )

                        DYAE_AE_date_of_AE = st.text_input(
                            "90DY_AE_date_of_AE",
                            help="(if AE is present after 30 days but before 90 write it here and the date)",
                            
                        )
                        ken_grandedtoxicity = st.text_area(
                            "AE90_OTHERFT",
                            

                        )
                        
                        ae90_gradesum12 = st.text_input("AE90_GRADESUM12" )
                        ae90_gradesum345 = st.text_input("AE90_GRADESUM345")
                        dy_ae_hospitalization_3 = st.selectbox(
                            "90DY_AE_Hospitalization 3 months [Excel : AE90_HOSP3]\n\n Yes (1), No (0)",
                                options=["1", "0"],
                                format_func=lambda x: {
                                        "1": "Yes",
                                        "0": "No",
                                    }[x],
                            
                            index=None,
                        placeholder="Choose an option",
                        )
                        dy_ae_hospitalization_6 = st.selectbox(
                            "90DY_AE_Hospitalization 6 months [Excel : AE30_HOSP3DATE]\n\n Yes (1), No (0)",
                                options=["1", "0"],
                                format_func=lambda x: {
                                        "1": "Yes",
                                        "0": "No",
                                    }[x],
                            
                            index= None,
                        placeholder="Choose an option",
                        )
                        dy_ae_hosp6mo = st.selectbox(
                            "90DY_AE_Hosp6mo [Excel : AE90_HOSP6]\n\n Yes (1), No (0)",
                                options=["1", "0"],
                                format_func=lambda x: {
                                        "1": "Yes",
                                        "0": "No",
                                    }[x],
                            
                            index=None,
                        placeholder="Choose an option",
                        )
                        dy_ae_death_due = st.selectbox(
                            "90DY_AE_Death due to AE [Excel : AE30_DEATHAE]\n\n Yes (1), No (0)",
                                options=["1", "0"],
                                format_func=lambda x: {
                                        "1": "Yes",
                                        "0": "No",
                                    }[x],
                            
                            index=None,
                        placeholder="Choose an option",
                        )


                        submit_tab8 = st.form_submit_button("Submit")

                        if submit_tab8:
                                
                                data8={
                                    "POST30_LABSDATE": posty90_date_labs.strftime("%Y-%m-%d"),
                                    "POST30_AFP": posty90_afp,
                                    "POST30_AFPDATE": posty90_afp_date.strftime("%Y-%m-%d"),
                                    "POST30_SODIUM": posty90_sodium,
                                    "POST30_CREATININE": posty90_creatinine,
                                    "POST30_INR": posty90_inr,
                                    "POST30_ALBUMIN": posty90_albumin,
                                    "POST30_BILI": posty90_bilirubin,
                                    "POST30_AST": posty90_ast,
                                    "POST30_ALT": posty90_alt,
                                    "POST30_ALP": posty90_alkaline_phosphatase,
                                    "POST30_LEUK": posty90_leukocytes,
                                    "POST30_PLT": posty90_platelets,
                                    "POST30_POTAS": posty90_potassium,
                                    "POST30_ASCITCTCAE": posty90_ascites_ctcae,
                                    "POST30_ASCITNUMB": posty90_ascites_classification,
                                    "POST30_ASCITDIUR": posty90_ascites_diruetics,
                                    "POST30_ASCITPARA": posty90_ascites_paracentesis,
                                    "POST30_ASCITHOSP": posty90_ascites_hospitalization,
                                    "POST30_HEGRADE": posty90_he_grade,
                                    "POST30_ASCITFT": posty90_ascites_free_text,
                                    "POST30_ECOG": posty90_ecog,
                                    "POST30_CPCALC": posty90_child_pugh_points,
                                    "POST30_CPCLASS": posty90_child_pugh_class,
                                    "POST30_MELD": posty90_meld,
                                    "POST30_MELDNA": posty90_meld_na,
                                    "POST30_ALBISCORE": posty90_albi_score,
                                    "POST30_ALBIGRADE": posty90_albi_grade,
                                    "POST30_BCLC": posty90_bclc,
                                    "Ken_BCLCStagepost90": ken_bclc_stage_post90,
                                    "Ken_MELD_Stagepost90": ken_meld_stage_post90,
                                    "AE30_PORTHTN": DYAE_CTCAE_portal_htn,
                                    "AE30_VASCULAR": DYAE_CTCAE_Vascular_comp,
                                    "AE30_FATIGUE": DYAE_CTCAE_fatigue,
                                    "AE30_DIAR": DYAE_CTCAE_diarrhea,
                                    "AE30_HYPOALBUM": DYAE_CTCAE_hypoalbuminemia_emr,
                                    "AE30_HYPERBILI": DYAE_CTCAE_hyperbilirubinemia_emr,
                                    "AE30_INCREASECR": DYAE_CTCAE_Increase_creatinine_emr,
                                    "AE30_ABDPAIN": DYAE_CTCAE_abdominal_pain,
                                    "AE30_SEPSIS": DYAE_CTCAE_sepsis,
                                    "AE30_BACTPER": DYAE_CTCAE_bacterial_peritonitis,
                                    "AE30_HEMOR": DYAE_CTCAE_hemorrhage,
                                    "AE30_ANOREX": DYAE_CTCAE_anorexia,
                                    "AE30_IHFIST": DYAE_CTCAE_intrahepatic_fistula,
                                    "AE30_CONSTI": DYAE_CTCAE_constipation,
                                    "AE30_NAUS": DYAE_CTCAE_nausea,
                                    "AE30_VOM": DYAE_CTCAE_vomiting,
                                    "AE30_CHOLE": DYAE_CTCAE_cholecystitis,
                                    "AE30_GULCER": DYAE_CTCAE_gastric_ulcers,
                                    "AE30_RESPFAIL": DYAE_CTCAE_respiratory_failure,
                                    "AE30_AKI": DYAE_CTCAE_AKI,
                                    "AE30_RADPNEUM": DYAE_CTCAE_Radiation_pneumonitis,
                                    "AE30_HYPERKAL": DYAE_CTCAE_hyperkalemia,
                                    "AE30_ALT" : ae30_alt,
                                    "AE30_AST" : ae30_ast,
                                    "AE30_ALP" : ae30_alp,
                                    "AE30_PLT" : ae30_plt,
                                    "AE30_OTHERFT" : ae30_otherft,
                                    "AE30_OTHER" : ae30_other,
                                    "AE30_GRADESUM12" : ae30_gradesum12,
                                    "AE30_GRADESUM345" : ae30_gradesum345,
                                    "30DY_AE_Other": DYAE_AE_other,
                                    "AE90_DATE": DYAE_AE_date_of_AE,
                                    "AE90_OTHERFT": ken_grandedtoxicity,
                                    "AE90_GRADESUM12" : ae90_gradesum12,
                                    "AE90_GRADESUM345" : ae90_gradesum345,
                                    "AE90_HOSP3": dy_ae_hospitalization_3,
                                    "AE30_HOSP3DATE": dy_ae_hospitalization_6,
                                    "AE90_HOSP6": dy_ae_hosp6mo,
                                    "AE30_DEATHAE": dy_ae_death_due
                                    
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

                        k_ken_albipretareraw = 0
                        k_ken_albipretaregrade = ""
                        try : 
                            prey90_bilirubin = get_variable_value(st.session_state.temp_mrn,"PREY_BILI")
                            prey90_albumin = get_variable_value(st.session_state.temp_mrn,"PREY_ALBUMIN")
                                    
                            k_ken_albipretareraw = albi_calc(prey90_bilirubin,prey90_albumin)
                            st.write("K_ken_AlbiPreTARERaw : ", k_ken_albipretareraw)
                            k_ken_albipretaregrade = albi_class(k_ken_albipretareraw)
                            st.write("K_ken_AlbiPreTAREGrade: ",k_ken_albipretaregrade)
                        except:
                            st.warning("Fill Pre Y90 Tab")
                        k_ken_albiposttareraw = 0
                        k_ken_albiposttaregrade =""
                        try :
                            posty90_bilirubin = get_variable_value(st.session_state.temp_mrn,"POST30_BILI")
                            posty90_albumin = get_variable_value(st.session_state.temp_mrn,"POST30_ALBUMIN")
                            
                            k_ken_albiposttareraw = albi_calc(posty90_bilirubin,posty90_albumin)
                            st.write("K_ken_AlbiPostTARERaw : ", k_ken_albiposttareraw)
                            k_ken_albiposttaregrade = albi_class(k_ken_albiposttareraw)
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
                                "PREY90_prescan_modality [Excel : PREY_MOD]\n\n(1) CT, (2) MRI",
                                        options=["1","2"],
                                        format_func=lambda x: {
                                            "1": "CT",
                                            "2": "MRI",
                                        }[x],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )
                        PREY90_Imaging_Date = st.date_input("PREY90_Imaging Date")
                        PREY90_total_number_of_lesions = st.selectbox(
                                "PREY90_total number of lesions [Excel : PREY_TOTLES]\n\n(1) 1,(2) 2,(3) >=3",
                                 options=["1", "2", "3"],
                            format_func=lambda x: {
                                            "1": "1",
                                            "2": "2",
                                            "3" : ">=3"
                                        }[x],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )
                        PREY90_Number_Involved_Lobes = st.selectbox(
                                "PREY90_Number Involved Lobes [Excel : PREY_LOBES]\n\n(1) Unilobar, (2) Bilobar",
                                        options=["1","2"],
                                        format_func=lambda x: {
                                            "1": "Unilobar",
                                            "2": "Bilobar",
                                        }[x],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )
                        PREY90_target_lesion_1_segments = st.multiselect(
                                "PREY90_target_lesion_1_segments [Excel : PREY_TL1SEG]",
                                options=["1","2","3","4a","4b","5","6","7","8","NA"],
                                placeholder="Select all that apply"
                        
                        )
                        PREY90_target_lesion_1_segments = ", ".join(PREY90_target_lesion_1_segments)
                        PREY90_TL1_LAD = st.number_input(
                            "PREY90_Target Lesion_LAD",
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
                        
                        PREY90_Target_Lesion_1_VOL = calculate_target_lestion_vol(PREY90_Target_Lesion_1_PAD, PREY90_TL1_LAD, PREY90_Target_Lesion_1_CCD)
                        st.write("PREY90_Target Lesion 1 VOL",PREY90_Target_Lesion_1_VOL)

                        PREY90_Target_Lesion_2_segments = st.selectbox(
                                "PREY90_Target_Lesion_2_segments [Excel : PREY_TL2SEG]",
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
                       
                        PREY90_Target_Lesion_2_VOL = calculate_value_v2(PREY90_Target_Lesion_2_segments, PREY90_Target_Lesion_2_LAD, PREY90_Target_Lesion_2_PAD, PREY90_Target_Lesion_2_CCD)
                        st.write("PREY90_Target Lesion 2 VOL",PREY90_Target_Lesion_2_VOL)

                        PREY90_pretx_targeted_Lesion_Dia_Sum = max(PREY90_TL1_LAD,PREY90_Target_Lesion_1_PAD,PREY90_Target_Lesion_1_CCD) + max(PREY90_Target_Lesion_2_PAD,PREY90_Target_Lesion_2_LAD,PREY90_Target_Lesion_2_CCD)
                        st.write("PREY90_ pretx targeted Lesion Dia Sum",PREY90_pretx_targeted_Lesion_Dia_Sum)
                        PREY90_Non_Target_Lesion_Location = st.selectbox( "PREY90_Non-Target Lesion Location [Excel : PREY_NTLOC]" , options=["1","2","3","4a","4b","5","6","7","8","NA"],
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
                        PREY90_Non_targeted_Lesion_Dia_Sum = "NA" if PREY90_Non_Target_Lesion_Location == 'NA' else max(PREY90_Non_Target_Lesion_2_PAD_Art_Enhanc,PREY90_Non_Target_Lesion_2_LAD_Art_Enhanc,PREY90_Non_Target_Lesion_2_CCD_Art_Enhanc)
                        st.write("PREY90_Non-targeted Lesion Dia Sum",PREY90_Non_targeted_Lesion_Dia_Sum)
                        PREY90_Reviewers_Initials = st.text_input(
                            "PREY90_Reviewers Initials",
                            help="Free-text input for reviewer name"
                        )

                        PREY90_Pre_Y90_Extrahepatic_Disease = st.selectbox(
                            "PREY90_Pre Y90 Extrahepatic Disease [Excel : PREY_EHD]\n\n Yes (1), No (0)",
                                    options=["1", "0"],
                                    format_func=lambda x: {
                                            "1": "Yes",
                                            "0": "No",
                                        }[x],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )

                        PREY90_Pre_Y90_Extrahepatic_Disease_Location = st.text_input(
                            "PREY90_Pre Y90 Extrahepatic Disease Location",
                            help="Free Text"
                        )

                        PREY90_PVT = st.selectbox(
                            "PREY90_PVT [Excel : PREY_PVT]\n\n Yes (1), No (0), NA",
                                    options=["1", "0", "NA"],
                                    format_func=lambda x: {
                                            "1": "Yes",
                                            "0": "No",
                                            "NA": "NA"
                                        }[x],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )

                        PREY90_PVT_Location = st.selectbox(
                            "PREY90_PVT Location [Excel : PREY_PVTLOC]",
                            options=["RPV", "LPV"],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )

                        PREY90_Features_of_cirrhosis = st.selectbox(
                            "PREY90_Features of cirrhosis [Excel : PREY_CIRRH]\n\n\n\n Yes (1), No (0)",
                                    options=["1", "0"],
                                    format_func=lambda x: {
                                            "1": "Yes",
                                            "0": "No",
                                        }[x],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )
                        st.subheader("Imaging_1st_Followup")
                        FU_Scan_Modality = st.selectbox(
                            "1st_FU_Scan Modality[Excel : FU1_MOD]\n\n(1) CT, (2) MRI",
                                        options=["1","2"],
                                        format_func=lambda x: {
                                            "1": "CT",
                                            "2": "MRI",
                                        }[x],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )

                        FU_Imaging_Date = st.date_input("1st_FU_Imaging Date")
                        fetch_date = None
                        try:
                            fetch_date =  datetime.strptime(get_variable_value(st.session_state.temp_mrn,"TAREDATE"),"%Y-%m-%d")
                        except:
                            st.write("Fill Patient Info form")
                       
                        FU_Months_Since_Y90 = relativedelta(FU_Imaging_Date, fetch_date).months
                        st.write("1st_FU_Months Since Y90",FU_Months_Since_Y90)
                        FU_Total_number_of_lesions = st.selectbox(
                            "1st_FU_Total number of lesions [Excel : FU1_TOTLES]\n\n(1) 1,(2) 2,(3) >=3",
                            options=["1", "2", "3"],
                            format_func=lambda x: {
                                            "1": "1",
                                            "2": "2",
                                            "3" : ">=3"
                                        }[x],
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
                            "1st_FU_Target Lesion 2 Segments [Excel : 1st_FU_Target Lesion 2 Segments]",
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
                            "1st_FU_Lesion Necrosis [Excel : FU1_NECROSIS]\n\n Yes (1), No (0), NA",
                                    options=["1", "0", "NA"],
                                    format_func=lambda x: {
                                            "1": "Yes",
                                            "0": "No",
                                            "NA": "NA"
                                        }[x],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )

                        FU_Reviewers_Initials = st.text_input(
                            "1st_FU_Reviewers Initials",
                            help="Free-text input for reviewer name"
                        )

                        FU_Non_target_lesion_response = st.selectbox(
                            "1st_FU_Non target lesion response[Excel : FU1_NTLRSP]\n\n Yes (1), No (0), NA",
                                    options=["1", "0", "NA"],
                                    format_func=lambda x: {
                                            "1": "Yes",
                                            "0": "No",
                                            "NA": "NA"
                                        }[x],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )

                        FU_New_Lesions = st.selectbox(
                            "1st_FU_New Lesions[Excel : FU1_NEWLESION]\n\n Yes (1), No (0), NA",
                                    options=["1", "0", "NA"],
                                    format_func=lambda x: {
                                            "1": "Yes",
                                            "0": "No",
                                            "NA": "NA"
                                        }[x],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )

                        FU_NEW_Extrahepatic_Disease = st.selectbox(
                            "1st_FU_NEW Extrahepatic Disease[Excel : FU1_NEWEHD]\n\n Yes (1), No (0), NA",
                                    options=["1", "0", "NA"],
                                    format_func=lambda x: {
                                            "1": "Yes",
                                            "0": "No",
                                            "NA": "NA"
                                        }[x],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )

                        FU_NEW_Extrahepatic_Dz_Location = st.text_input(
                            "1st_FU_NEW Extrahepatic Dz Location",
                            help="Free text"
                        )

                        FU_NEW_Extrahepatic_Dz_Date = st.date_input("1st_FU_NEW Extrahepatic Dz Date")

                        FU_change_non_target_lesion = 0 if PREY90_Non_targeted_Lesion_Dia_Sum == "NA" else ((PREY90_Non_targeted_Lesion_Dia_Sum - FU_Non_targeted_Lesion_Dia_Sum)/max(1,PREY90_pretx_targeted_Lesion_Dia_Sum))*100
                        st.write("1st_FU_% change for non target lesion",FU_change_non_target_lesion)
                        FU_change_target_lesion = ((PREY90_pretx_targeted_Lesion_Dia_Sum - FU_Follow_up_1_targeted_Lesion_Dia_Sum)/max(1,PREY90_pretx_targeted_Lesion_Dia_Sum))*100
                        st.write("1st_FU_% Change Target Dia",FU_change_target_lesion)
                        first_fu_mrecist_localized = mrecist_local(FU_change_target_lesion)
                        st.write("1st_FU_mRECIST LOCALIZED",first_fu_mrecist_localized)
                        
                        first_fu_mrecist_overall = mrecist_overall(FU_New_Lesions, FU_NEW_Extrahepatic_Disease, FU_change_non_target_lesion, FU_change_target_lesion)
                        st.write("1st_FU_mRECIST Overall",first_fu_mrecist_overall)
                        
                        FU_Free_Text = st.text_area(
                            "1st_FU_Free Text",
                            help="Free text"
                        )

                        st.subheader("Imaging_2nd_Followup")

                        FU2_Scan_Modality = st.selectbox(
                            "2nd_FU_Scan Modality Excel : FU2_MOD]\n\n(1) CT, (2) MRI",
                                        options=["1","2"],
                                        format_func=lambda x: {
                                            "1": "CT",
                                            "2": "MRI",
                                        }[x],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )

                        FU2_Imaging_Date = st.date_input("2nd_FU_Imaging Date")

                        FU2_Months_Since_Y90 = relativedelta(FU2_Imaging_Date, fetch_date).months
                        st.write("2nd_FU_Months Since Y90",FU2_Months_Since_Y90)
                        FU2_Total_number_of_lesions = st.selectbox(
                            "2nd_FU_Total number of lesions[Excel : FU2_TOTLES]\n\n(1) 1,(2) 2,(3) >=3",
                                 options=["1", "2", "3"],
                            format_func=lambda x: {
                                            "1": "1",
                                            "2": "2",
                                            "3" : ">=3"
                                        }[x],
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
                            "2nd_FU_Target Lesion 2 Segments [Excel : FU2_TL2SEG]",
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
                            "2nd_FU_Lesion Necrosis  [Excel : FU2_NEC]\n\n Yes (1), No (0), NA",
                                    options=["1", "0", "NA"],
                                    format_func=lambda x: {
                                            "1": "Yes",
                                            "0": "No",
                                            "NA": "NA"
                                        }[x],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )

                        FU2_Reviewers_Initials = st.text_input(
                            "2nd_FU_Reviewers Initials",
                            help="Free-text input for reviewer name"
                        )

                        FU2_Non_target_lesion_response = st.selectbox(
                            "2nd_FU_Non target lesion response[Excel : FU2_NTLRSP]\n\n Yes (1), No (0), NA",
                                    options=["1", "0", "NA"],
                                    format_func=lambda x: {
                                            "1": "Yes",
                                            "0": "No",
                                            "NA": "NA"
                                        }[x],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )

                        FU2_New_Lesions = st.selectbox(
                            "2nd_FU_New Lesions[Excel : FU2_NEWLES]\n\n Yes (1), No (0), NA",
                                    options=["1", "0", "NA"],
                                    format_func=lambda x: {
                                            "1": "Yes",
                                            "0": "No",
                                            "NA": "NA"
                                        }[x],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )

                        FU2_NEW_Extrahepatic_Disease = st.selectbox(
                            "2nd_FU_NEW Extrahepatic Disease[Excel : FU2_EHD]\n\n Yes (1), No (0), NA",
                                    options=["1", "0", "NA"],
                                    format_func=lambda x: {
                                            "1": "Yes",
                                            "0": "No",
                                            "NA": "NA"
                                        }[x],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )

                        FU2_NEW_Extrahepatic_Dz_Location = st.text_input(
                            "2nd_FU_NEW Extrahepatic Dz Location",
                            help="Free text"
                        )

                        FU2_NEW_Extrahepatic_Dz_Date = st.date_input("2nd_FU_NEW Extrahepatic Dz Date")

                        FU2_change_non_target_lesion = 0 if PREY90_Non_targeted_Lesion_Dia_Sum == "NA" else ((PREY90_Non_targeted_Lesion_Dia_Sum - FU2_Non_targeted_Lesion_Dia_Sum) / max(1,PREY90_pretx_targeted_Lesion_Dia_Sum))*100
                        st.write("2nd_FU_% change for non target lesion",FU2_change_non_target_lesion)
                        FU2_change_target_lesion = ((PREY90_pretx_targeted_Lesion_Dia_Sum - FU2_Follow_up_2_targeted_Lesion_Dia_Sum) / max(1,PREY90_pretx_targeted_Lesion_Dia_Sum)) * 100
                        st.write("2nd_FU_% Change Target Dia",FU2_change_target_lesion)
                        
                        second_fu_mrecist_calc = mrecist_local(FU2_change_target_lesion)
                        st.write("2nd_FU_mRECIST Calc", second_fu_mrecist_calc)
                        second_fu_mrecist_localized = mrecist_calc(FU2_change_target_lesion, FU2_Follow_up_2_targeted_Lesion_Dia_Sum, FU_Follow_up_1_targeted_Lesion_Dia_Sum)
                        st.write("2nd_FU_mRECIST LOCALIZED", second_fu_mrecist_localized)
                        second_fu_mrecist_overall = mrecist_overall(FU2_New_Lesions, FU2_NEW_Extrahepatic_Disease, FU2_change_non_target_lesion, FU2_change_target_lesion)
                        st.write("2nd_FU_mRECIST Overall", second_fu_mrecist_overall)
                        FU2_Free_Text = st.text_area(
                            "2nd_FU_Free Text",
                            help="Free text"
                        )
                        # 3rd Imaging Follow-up
                        st.subheader("Imaging_3rd_Followup")
                        FU3_Scan_Modality = st.selectbox(
                            "3rd_FU_Scan Modality[Excel : FU3_MOD]\n\n(1) CT, (2) MRI",
                                        options=["1","2"],
                                        format_func=lambda x: {
                                            "1": "CT",
                                            "2": "MRI",
                                        }[x],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )
                        FU3_Imaging_Date = st.date_input("3rd_FU_Imaging Date")
                        FU3_Months_Since_Y90 = relativedelta(FU3_Imaging_Date, fetch_date).months
                        st.write("3rd_FU_Months Since Y90",FU3_Months_Since_Y90)
                        FU3_Total_number_of_lesions = st.selectbox(
                            "3rd_FU_Total number of lesions[Excel : FU3_TOTLES]\n\n(1) 1,(2) 2,(3) >=3",
                                 options=["1", "2", "3"],
                            format_func=lambda x: {
                                            "1": "1",
                                            "2": "2",
                                            "3" : ">=3"
                                        }[x],

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
                            "3rd_FU_Target Lesion 2 Segments [Excel : FU3_TL2SEG]",
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
                            "3rd_FU_Lesion Necrosis[Excel : FU3_NEC]\n\n Yes (1), No (0), NA",
                                    options=["1", "0", "NA"],
                                    format_func=lambda x: {
                                            "1": "Yes",
                                            "0": "No",
                                            "NA": "NA"
                                        }[x],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )

                        FU3_Reviewers_Initials = st.text_input(
                            "3rd_FU_Reviewers Initials",
                            help="Free-text input for reviewer name"
                        )

                        FU3_Non_target_lesion_response = st.selectbox(
                            "3rd_FU_Non target lesion response[Excel : FU3_NTLRSP]\n\n Yes (1), No (0), NA",
                                    options=["1", "0", "NA"],
                                    format_func=lambda x: {
                                            "1": "Yes",
                                            "0": "No",
                                            "NA": "NA"
                                        }[x],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )

                        FU3_New_Lesions = st.selectbox(
                            "3rd_FU_New Lesions[Excel : FU3_NEWLES]\n\n Yes (1), No (0), NA",
                                    options=["1", "0", "NA"],
                                    format_func=lambda x: {
                                            "1": "Yes",
                                            "0": "No",
                                            "NA": "NA"
                                        }[x],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )

                        FU3_NEW_Extrahepatic_Disease = st.selectbox(
                            "3rd_FU_NEW Extrahepatic Disease[Excel : FU3_EHD]\n\n Yes (1), No (0), NA",
                                    options=["1", "0", "NA"],
                                    format_func=lambda x: {
                                            "1": "Yes",
                                            "0": "No",
                                            "NA": "NA"
                                        }[x],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )

                        FU3_NEW_Extrahepatic_Dz_Location = st.text_input(
                            "3rd_FU_NEW Extrahepatic Dz Location",
                            help="Free text"
                        )
                        FU3_NEW_Extrahepatic_Dz_Date = st.date_input("3rd_FU_NEW Extrahepatic Dz Date")
                        FU3_change_non_target_lesion = 0 if PREY90_Non_targeted_Lesion_Dia_Sum == 'NA' else ((PREY90_Non_targeted_Lesion_Dia_Sum - FU3_Non_targeted_Lesion_Dia_Sum) / max(1,PREY90_pretx_targeted_Lesion_Dia_Sum))*100
                        st.write("3rd_FU_% change for non target lesion",FU3_change_non_target_lesion)
                        FU3_change_target_lesion = ((PREY90_pretx_targeted_Lesion_Dia_Sum - FU3_Follow_up_2_targeted_Lesion_Dia_Sum) / max(1,PREY90_pretx_targeted_Lesion_Dia_Sum)) * 100
                        st.write("3rd_FU_% Change Target Dia",FU3_change_target_lesion)
                        third_fu_mrecist_calc = mrecist_local(FU3_change_target_lesion)
                        st.write("3rd_FU_mRECIST Calc",third_fu_mrecist_calc)

                        third_fu_mrecist_localized = mrecist_calc(FU3_change_target_lesion, FU3_Follow_up_2_targeted_Lesion_Dia_Sum, FU_Follow_up_1_targeted_Lesion_Dia_Sum)
                        st.write("3rd_FU_mRECIST LOCALIZED",third_fu_mrecist_localized)
                        third_fu_mrecist_overall = mrecist_overall (FU3_New_Lesions, FU3_NEW_Extrahepatic_Disease, FU3_change_non_target_lesion, FU3_change_target_lesion)
                        st.write("3rd_FU_mRECIST Overall", third_fu_mrecist_overall)
                        FU3_Free_Text = st.text_area(
                            "3rd_FU_Free Text",
                            help="Free text"
                        )

                        # 4th Imaging Follow-up
                        st.subheader("Imaging_4th_Followup")

                        FU4_Scan_Modality = st.selectbox(
                            "4th_FU_Scan Modality [Excel : FU4_MOD]\n\n(1) CT, (2) MRI",
                                        options=["1","2"],
                                        format_func=lambda x: {
                                            "1": "CT",
                                            "2": "MRI",
                                        }[x],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )

                        FU4_Imaging_Date = st.date_input("4th_FU_Imaging Date")

                        FU4_Months_Since_Y90 = relativedelta(FU4_Imaging_Date, fetch_date).months
                        st.write("4th_FU_Months Since Y90",FU4_Months_Since_Y90)
                        FU4_Total_number_of_lesions = st.selectbox(
                            "4th_FU_Total number of lesions [Excel : FU4_TOTLES]\n\n(1) 1,(2) 2,(3) >=3",
                                 options=["1", "2", "3"],
                            format_func=lambda x: {
                                            "1": "1",
                                            "2": "2",
                                            "3" : ">=3"
                                        }[x],
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
                            "4th_FU_Target Lesion 2 Segments [Excel : FU4_TL2SEG]",
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
                            "4th_FU_Lesion Necrosis  [Excel : FU4_NECROSIS]\n\n Yes (1), No (0), NA",
                                    options=["1", "0", "NA"],
                                    format_func=lambda x: {
                                            "1": "Yes",
                                            "0": "No",
                                            "NA": "NA"
                                        }[x],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )

                        FU4_Reviewers_Initials = st.text_input(
                            "4th_FU_Reviewers Initials",
                            help="Free-text input for reviewer name"
                        )

                        FU4_Non_target_lesion_response = st.selectbox(
                            "4th_FU_Non target lesion response  [Excel : FU4_NTLRSP]\n\n Yes (1), No (0), NA",
                                    options=["1", "0", "NA"],
                                    format_func=lambda x: {
                                            "1": "Yes",
                                            "0": "No",
                                            "NA": "NA"
                                        }[x],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )

                        FU4_New_Lesions = st.selectbox(
                            "4th_FU_New Lesions  [Excel : FU4_NEWLESION]\n\n Yes (1), No (0), NA",
                                    options=["1", "0", "NA"],
                                    format_func=lambda x: {
                                            "1": "Yes",
                                            "0": "No",
                                            "NA": "NA"
                                        }[x],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )

                        FU4_NEW_Extrahepatic_Disease = st.selectbox(
                            "4th_FU_NEW Extrahepatic Disease  [Excel : FU4_NEWEHD]\n\n Yes (1), No (0), NA",
                                    options=["1", "0", "NA"],
                                    format_func=lambda x: {
                                            "1": "Yes",
                                            "0": "No",
                                            "NA": "NA"
                                        }[x],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )

                        FU4_NEW_Extrahepatic_Dz_Location = st.text_input(
                            "4th_FU_NEW Extrahepatic Dz Location",
                            help="Free text"
                        )

                        FU4_NEW_Extrahepatic_Dz_Date = st.date_input("4th_FU_NEW Extrahepatic Dz Date")
                        FU4_change_non_target_lesion = 0 if PREY90_Non_targeted_Lesion_Dia_Sum == "NA" else ((PREY90_Non_targeted_Lesion_Dia_Sum - FU4_Non_targeted_Lesion_Dia_Sum) / max(1,PREY90_pretx_targeted_Lesion_Dia_Sum)) * 100
                        st.write("4th_FU_% change non target lesion",FU4_change_non_target_lesion)
                        FU4_change_target_lesion = ((PREY90_pretx_targeted_Lesion_Dia_Sum - FU4_Follow_up_2_targeted_Lesion_Dia_Sum) / max(1,PREY90_pretx_targeted_Lesion_Dia_Sum)) * 100
                        st.write("4th_FU_% Change target dia",FU4_change_target_lesion)
                        fourth_fu_mrecist_calc = mrecist_local(FU4_change_target_lesion)
                        st.write("4th_FU_mRECIST Calc",fourth_fu_mrecist_calc)
                        fourth_fu_mrecist_localized = mrecist_calc(FU4_change_target_lesion, FU4_Follow_up_2_targeted_Lesion_Dia_Sum, FU_Follow_up_1_targeted_Lesion_Dia_Sum)
                        st.write("4th_FU_mRECIST LOCALIZED",fourth_fu_mrecist_localized)
                        fourth_fu_mrecist_overall = mrecist_overall (FU4_New_Lesions, FU4_NEW_Extrahepatic_Disease, FU4_change_non_target_lesion, FU4_change_target_lesion)
                        st.write("4th_FU_mRECIST Overall", fourth_fu_mrecist_overall)
                        
                        FU4_Free_Text = st.text_area(
                            "4th_FU_Free Text",
                            help="Free text"
                        )

                        # 5th Imaging Follow-up
                        st.subheader("Imaging_5th_Followup")

                        FU5_Scan_Modality = st.selectbox(
                            "4th_FU_Scan Modality [Excel : FU5_MOD]\n\n(1) CT, (2) MRI",
                                        options=["1","2"],
                                        format_func=lambda x: {
                                            "1": "CT",
                                            "2": "MRI",
                                        }[x],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )
                        FU5_Imaging_Date = st.date_input("5th_FU_Imaging Date")

                        FU5_Months_Since_Y90 = relativedelta(FU5_Imaging_Date, fetch_date).months
                        st.write("5th_FU_Months Since Y90",FU5_Months_Since_Y90)
                        FU5_Total_number_of_lesions = st.selectbox(
                            "5th_FU_Total number of lesions [Excel : FU5_TOTLES]\n\n(1) 1,(2) 2,(3) >=3",
                                 options=["1", "2", "3"],
                            format_func=lambda x: {
                                            "1": "1",
                                            "2": "2",
                                            "3" : ">=3"
                                        }[x],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )
                        FU5_Target_Lesion_1_LAD_Art_Enhanc = st.number_input(
                            "5th_FU_Target Lesion 1 LAD Art Enhanc",
                            step=0.1
                        )

                        FU5_Target_Lesion_1_PAD_Art_Enhanc = st.number_input(
                            "5th_FU_Target Lesion 1 PAD Art Enhanc",
                            step=0.1
                        )

                        FU5_Target_Lesion_1_CCD_Art_Enhanc = st.number_input(
                            "5th_FU_Target Lesion 1 CCD Art Enhanc",
                            step=0.1
                        )

                        FU5_Target_Lesion_2_Segments = st.selectbox(
                            "5th_FU_Target Lesion 2 Segments [Excel : FU5_TL2SEG]",
                            options=["1", "2", "3", "4a", "4b", "5", "6", "7", "8", "NA"],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )

                        FU5_Target_Lesion_2_LAD_Art_Enhanc = st.number_input(
                            "5th_FU_Target Lesion 2 LAD Art Enhanc",
                            step=0.1
                        )

                        FU5_Target_Lesion_2_PAD_Art_Enhanc = st.number_input(
                            "5th_FU_Target Lesion 2 PAD Art Enhanc",
                            step=0.1
                        )

                        FU5_Target_Lesion_2_CCD_Art_Enhanc = st.number_input(
                            "5th_FU_Target Lesion 2 CCD Art Enhanc",
                            step=0.1
                        )

                        FU5_Follow_up_2_targeted_Lesion_Dia_Sum = max(FU5_Target_Lesion_1_CCD_Art_Enhanc, FU5_Target_Lesion_1_PAD_Art_Enhanc, FU5_Target_Lesion_1_LAD_Art_Enhanc) + max(FU5_Target_Lesion_2_CCD_Art_Enhanc, FU5_Target_Lesion_2_PAD_Art_Enhanc, FU5_Target_Lesion_2_LAD_Art_Enhanc)
                        st.write("5th_FU_Follow up 4 targeted Lesion Dia Sum",FU5_Follow_up_2_targeted_Lesion_Dia_Sum)


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
                      
                        FU5_Non_target_lesion_response = st.selectbox(
                            "5th_FU_Non target lesion response [Excel : FU5_NTLRSP]\n\n Yes (1), No (0), NA",
                                    options=["1", "0", "NA"],
                                    format_func=lambda x: {
                                            "1": "Yes",
                                            "0": "No",
                                            "NA": "NA"
                                        }[x],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )

                        FU5_New_Lesions = st.selectbox(
                            "5th_FU_New Lesions [Excel : FU5_NEWLESION]\n\n Yes (1), No (0), NA",
                                    options=["1", "0", "NA"],
                                    format_func=lambda x: {
                                            "1": "Yes",
                                            "0": "No",
                                            "NA": "NA"
                                        }[x],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )

                        FU5_NEW_Extrahepatic_Disease = st.selectbox(
                            "5th_FU_NEW Extrahepatic Disease  [Excel : FU5_NEWEHD]\n\n Yes (1), No (0), NA",
                                    options=["1", "0", "NA"],
                                    format_func=lambda x: {
                                            "1": "Yes",
                                            "0": "No",
                                            "NA": "NA"
                                        }[x],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )

                        FU5_NEW_Extrahepatic_Dz_Location = st.text_input(
                            "5th_FU_NEW Extrahepatic Dz Location",
                            help="Free text"
                        )

                        FU5_NEW_Extrahepatic_Dz_Date = st.date_input("5th_FU_NEW Extrahepatic Dz Date")

                        FU5_change_non_target_lesion = 0 if PREY90_Non_targeted_Lesion_Dia_Sum == 'NA' else ((PREY90_Non_targeted_Lesion_Dia_Sum - FU5_Non_targeted_Lesion_Dia_Sum) / max(0.1,PREY90_pretx_targeted_Lesion_Dia_Sum)) * 100
                        st.write("5th_FU_% change non target lesion ",FU5_change_non_target_lesion)
                        FU5_change_target_lesion = ((PREY90_pretx_targeted_Lesion_Dia_Sum - FU5_Follow_up_2_targeted_Lesion_Dia_Sum) / max(0.1,PREY90_pretx_targeted_Lesion_Dia_Sum)) * 100
                        st.write("5th_FU_% Change target dia",FU5_change_target_lesion)

                        fifth_fu_mrecist_calc = mrecist_local(FU5_change_target_lesion)
                        st.write("5th_FU_mRECIST Calc",fifth_fu_mrecist_calc)

                        fifth_fu_mrecist_localized = mrecist_calc(FU5_change_target_lesion, FU5_Follow_up_2_targeted_Lesion_Dia_Sum, FU_Follow_up_1_targeted_Lesion_Dia_Sum)
                        st.write("5th_FU_mRECIST LOCALIZED",fifth_fu_mrecist_localized)
                        fifth_fu_mrecist_overall = mrecist_overall (FU5_New_Lesions, FU5_NEW_Extrahepatic_Disease, FU5_change_non_target_lesion, FU5_change_target_lesion)
                        st.write("5th_FU_mRECIST Overall", fifth_fu_mrecist_overall)
                        
                        FU5_Free_Text = st.text_area(
                            "5th_FU_Free Text",
                            help="Free text"
                        )

                        st.subheader("Imaging_Dates for OS or PFS")

                        dead = st.selectbox(
                                "Dead [Excel : DEAD]\n\n Yes (1), No (0)",
                                options=[0, 1],
                                format_func=lambda x:{
                                        0:"No",
                                        1:"Yes"
                                }[x],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )

                        Date_of_Death = st.date_input("Date of Death")
                        Time_to_Death = None
                        if dead == 0:
                            Date_of_Death = 'NA'
                            Time_to_Death = 'NA'
                        else :
                            Time_to_Death = relativedelta(Date_of_Death, fetch_date).months
                        st.write("Time to Death",Time_to_Death)

                        OLT = st.selectbox(
                                "OLT [Excel : OLT]\n\n Yes (1), No (0)",
                                options=[0, 1],
                                format_func=lambda x:{
                                        0:"No",
                                        1:"Yes"
                                }[x],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )

                        Date_of_OLT = st.date_input("Date of OLT")
                        Time_to_OLT = None
                        if OLT == 0:
                            Date_of_OLT = 'NA'
                            Time_to_OLT = 'NA'
                        else:
                            Time_to_OLT = relativedelta(Date_of_OLT, fetch_date).months
                        st.write("Time to OLT",Time_to_OLT)

                        Repeat_tx_post_Y90 = st.selectbox(
                                "Repeat tx post Y90 [Excel : RTX]\n\n Yes (1), No (0)",
                                options=[0, 1],
                                format_func=lambda x:{
                                        0:"No",
                                        1:"Yes"
                                }[x],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )

                        Date_of_Repeat_tx_Post_Y90 = st.date_input("Date of Repeat tx Post Y90")
                        Time_to_Repeat_Tx_Post_Y90 = None

                        if Repeat_tx_post_Y90 == 0:
                                Date_of_Repeat_tx_Post_Y90 = 'NA'
                                Time_to_Repeat_Tx_Post_Y90 = 'NA'
                        else:
                            Time_to_Repeat_Tx_Post_Y90 = relativedelta(Date_of_Repeat_tx_Post_Y90, fetch_date).months
                        st.write("Time to Repeat Tx Post Y90",Time_to_Repeat_Tx_Post_Y90)

                        Date_of_Localized_Progression = detect_first_progression(first_fu_mrecist_localized, second_fu_mrecist_localized, third_fu_mrecist_localized, fourth_fu_mrecist_localized, fifth_fu_mrecist_localized, FU2_Imaging_Date, FU3_Imaging_Date, FU4_Imaging_Date, FU5_Imaging_Date)
                        st.write("Date of Localized Progression",Date_of_Localized_Progression)
                        Time_to_localized_progression = None
                        if Date_of_Localized_Progression == "No Progression":
                                Time_to_localized_progression = 'NA'
                        else:
                                Time_to_localized_progression = relativedelta(Date_of_Localized_Progression, fetch_date).years
                        st.write("Time to localized progression",Time_to_localized_progression)

                        Date_of_Overall_Progression = detect_overall_progression(first_fu_mrecist_localized, first_fu_mrecist_overall, second_fu_mrecist_localized, second_fu_mrecist_overall, third_fu_mrecist_localized, third_fu_mrecist_overall, fourth_fu_mrecist_localized, fourth_fu_mrecist_overall, fifth_fu_mrecist_localized, fifth_fu_mrecist_overall, FU_Imaging_Date, FU2_Imaging_Date, FU3_Imaging_Date, FU4_Imaging_Date, FU5_Imaging_Date)
                        st.write("Date of Overall Progression", Date_of_Overall_Progression)
                        Time_to_overall_progression = None
                        if Date_of_Overall_Progression == "No Progression":
                                Time_to_overall_progression = 'NA'
                        else:
                                Time_to_overall_progression = relativedelta(Date_of_Overall_Progression, fetch_date).years
                        st.write("Time to Overall (Local or systemic) Progression",Time_to_overall_progression)

                        lfu = st.selectbox("Last Follow up [Excel : LFU]\n\n(1) Yes, (0) No", options=["0", "1"],
                                format_func=lambda x:{
                                        "0":"No",
                                        "1":"Yes"
                                }[x],
                        index=None,  # No default selection
                        placeholder="Choose an option",)

                        Date_of_Last_Follow_up_last_imaging_date = st.date_input("Date of Last Follow-up/last imaging date")
                        Time_to_Last_Follow_up_last_imaging_date = None
                        if dead == 1 and OLT == 1 and Repeat_tx_post_Y90 == 1  and lfu == "0":
                            Date_of_Last_Follow_up_last_imaging_date = 'NA'
                            Time_to_Last_Follow_up_last_imaging_date = "NA"
                        else:
                            Time_to_Last_Follow_up_last_imaging_date = relativedelta(Date_of_Last_Follow_up_last_imaging_date, fetch_date).years
                        st.write("Time to Last follow up",Time_to_Last_Follow_up_last_imaging_date)

                        notes_free_text = st.text_input("Notes Free Text")

                        bestm_recist = determine_bestmrecist(first_fu_mrecist_localized, second_fu_mrecist_localized, third_fu_mrecist_localized, fourth_fu_mrecist_localized, fifth_fu_mrecist_localized)
                        st.write("BestmRECIST", bestm_recist)
                        date_bestm_recist = determine_bestmrecist_date(fifth_fu_mrecist_overall, first_fu_mrecist_overall, second_fu_mrecist_overall, third_fu_mrecist_overall, fourth_fu_mrecist_overall, fifth_fu_mrecist_localized, FU_Imaging_Date, FU2_Imaging_Date, FU3_Imaging_Date, FU4_Imaging_Date, FU5_Imaging_Date)
                        st.write("Date BestmRECIST",date_bestm_recist)
                        time_to_bestm_recist = "No Time" if date_bestm_recist == "No Date" else relativedelta(date_bestm_recist, fetch_date).months
                        st.write("Timeto_bestmRECIST", time_to_bestm_recist)
                        PERCHANGE_BEST_TTR = st.number_input("Percent change till best mRECIST 1st",step=0.1)
                        def best_cr_noncr(value):
                            if value == "CR":
                                    return 1
                            elif value in ["PR", "PD", "SD"]:
                                return 2
                            else:
                                return ""
                        bestm_recist_cr_vs_non_cr = best_cr_noncr(bestm_recist)
                        st.write("BestmRECISTCRvsNonCR", bestm_recist_cr_vs_non_cr)
                        def best_responce(value):
                            if value in ["CR", "PR"]:
                                return 1
                            elif value in ["SD", "PD"]:
                                return 2
                            else:
                                return ""
                        bestm_recist_r_vs_nr = best_responce(bestm_recist)
                        st.write("BestmRECISTRvsNR" ,bestm_recist_r_vs_nr)

                        DATE_BEST_MTR = st.date_input("Date of Best percent change (2)")
                        TIME_BEST_MRT = relativedelta(DATE_BEST_MTR, fetch_date).months
                        PERCHANGE_BEST_MTR = st.number_input("Best Overall percent change (2) ",step=0.1)

                        OS_Date = st.date_input("Overall Survival Date")
                        OS_Events = st.selectbox("Overall Survival Events [Excel : OS_Events]\n\n(1) Event: Death, (0) Censored: OLT, RTx, LFU",
                            options=["1","0"],
                            format_func=lambda x:{
                                        "0":"Event: Death",
                                        "1":"Censored: OLT, RTx, LFU"
                                }[x],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )
                        OS_Time = relativedelta(OS_Date, fetch_date).months
                        OS_Reason = st.selectbox("Overall Survival Reaons [Excel : OS_Reason]\n\nDead = dead, OLT = liver transplant, RTx = repeat treatment, LFU = Loss to Follow up",
                            options=["Dead","OLT", "RTx", "LFU"],
                            format_func=lambda x:{
                                        "Dead":"dead",
                                        "OLT":"liver transplant",
                                        "RTx":"repeat treatment",
                                        "LFU":"Loss to Follow up"
                                }[x],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )
                        #LPFS
                        LPFS_Date = st.date_input("Local Progression Free Survival Date")
                        LPFS_Events = st.selectbox("Local Progression Free Survival Event [Excel : LPFS_Events]\n\n(1) Event: Death, (0) Censored: OLT, RTx, LFU",
                            options=["1","0"],
                            format_func=lambda x:{
                                        "1":"Event: Death, LP(Local progression)",
                                        "0":"Censored: OLT, RTx, LFU"
                                }[x],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )
                        LPFS_Time = relativedelta(LPFS_Date, fetch_date).months
                        LPFS_Reason = st.selectbox("Local Progression Free Survival Reason [Excel : LPFS_Reason]",
                            options=["Dead"," LP(Local progression)", "OLT", "RTx", "LFU"],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )
                        #PFS
                        PFS_Date = st.date_input("Progression Free Survival Date")
                        PFS_Events = st.selectbox("Progression Free Survival Event [Excel : PFS_Events]\n\n(1) Event: Death, (0) Censored: OLT, RTx, LFU",
                            options=["1","0"],
                            format_func=lambda x:{
                                        "1":"Event: Death , OP (first time they progression)",
                                        "0":"Censored: OLT, RTx, LFU"
                                }[x],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )
                        PFS_Time = relativedelta(PFS_Date, fetch_date).months
                        PFS_Reason = st.selectbox("Progression Free Survival Reason [Excel : PFS_Reason]\n\nDead = dead, OLT = liver transplant, RTx = repeat treatment, LFU = Loss to Follow up",
                            options=["Dead","OP(Overall progression)" ,"OLT", "RTx", "LFU"],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )
                        DOR = LPFS_Time if time_to_bestm_recist == "No Time" else LPFS_Time - time_to_bestm_recist

                        submit_tab10 = st.form_submit_button("Submit")

                        if submit_tab10:
                            #index = st.session_state.data[st.session_state.data["MRN"] == st.session_state.temp_mrn].index[0]
                            data10={
                                    "PREY_MOD": PREY90_prescan_modality,
                                    "PREY_IMG_DATE": PREY90_Imaging_Date.strftime("%Y-%m-%d"),
                                    "PREY_TOTLES": PREY90_total_number_of_lesions,
                                    "PREY_LOBES": PREY90_Number_Involved_Lobes,
                                    "PREY_TL1SEG": PREY90_target_lesion_1_segments,
                                    "PREY_TL1LAD": PREY90_TL1_LAD,
                                    "PREY_TL1PAD": PREY90_Target_Lesion_1_PAD,
                                    "PREY_TL1CCD": PREY90_Target_Lesion_1_CCD,
                                    "PREY_TL1VOL": PREY90_Target_Lesion_1_VOL,
                                    "PREY_TL2SEG": PREY90_Target_Lesion_2_segments,
                                    "PREY_TL2LAD": PREY90_Target_Lesion_2_LAD,
                                    "PREY_TL2PAD": PREY90_Target_Lesion_2_PAD,
                                    "PREY_TL2CCD": PREY90_Target_Lesion_2_CCD,
                                    "PREY_TL2VOL": PREY90_Target_Lesion_2_VOL,
                                    "PREY_TLDIA": PREY90_pretx_targeted_Lesion_Dia_Sum,
                                    "PREY_NTLOC": PREY90_Non_Target_Lesion_Location,
                                    "PREY_NTL1LAD": PREY90_Non_Target_Lesion_2_LAD_Art_Enhanc,
                                    "PREY_NTL1PAD": PREY90_Non_Target_Lesion_2_PAD_Art_Enhanc,
                                    "PREY_NTL1CCD": PREY90_Non_Target_Lesion_2_CCD_Art_Enhanc,
                                    "PREY_NTLDIA": PREY90_Non_targeted_Lesion_Dia_Sum,
                                    "PREY_REVFT": PREY90_Reviewers_Initials,
                                    "PREY_EHD": PREY90_Pre_Y90_Extrahepatic_Disease,
                                    "PREY_EHDLOCFT": PREY90_Pre_Y90_Extrahepatic_Disease_Location,
                                    "PREY_PVT": PREY90_PVT,
                                    "PREY_PVTLOC": PREY90_PVT_Location,
                                    "PREY_CIRRH": PREY90_Features_of_cirrhosis,
                                    "FU1_MOD": FU_Scan_Modality,
                                    "FU1_IMG_DATE": FU_Imaging_Date.strftime("%Y-%m-%d"),
                                    "FU1_MS_Y90": FU_Months_Since_Y90,
                                    "FU1_TOTLES": FU_Total_number_of_lesions,
                                    "FU1_TL1LAD": FU_Target_Lesion_1_LAD_Art_Enhanc,
                                    "FU1_TL1PAD": FU_Target_Lesion_1_PAD_Art_Enhanc,
                                    "FU1_TL1CCD": FU_Target_Lesion_1_CCD_Art_Enhanc,
                                    "FU1_TL2SEG": FU_Target_Lesion_2_Segments,
                                    "FU1_TL2LAD": FU_Target_Lesion_2_LAD_Art_Enhanc,
                                    "FU1_TL2PAD": FU_Target_Lesion_2_PAD_Art_Enhanc,
                                    "FU1_TL2CCD": FU_Target_Lesion_2_CCD_Art_Enhanc,
                                    "FU1_TLDIA": FU_Follow_up_1_targeted_Lesion_Dia_Sum,
                                    "FU1_NTL1LAD": FU_Non_Target_Lesion_2_LAD_Art_Enhanc,
                                    "FU1_NTL1PAD": FU_Non_Target_Lesion_2_PAD_Art_Enhanc,
                                    "FU1_NTL1CCD": FU_Non_Target_Lesion_2_CCD_Art_Enhanc,
                                    "FU1_NTLDIA": FU_Non_targeted_Lesion_Dia_Sum,
                                    "FU1_NECROSIS": FU_Lesion_Necrosis,
                                    "FU1_REVFT": FU_Reviewers_Initials,
                                    "FU1_NTLRSP": FU_Non_target_lesion_response,
                                    "FU1_NEWLESION": FU_New_Lesions,
                                    "FU1_NEWEHD": FU_NEW_Extrahepatic_Disease,
                                    "FU1_EHDLOC": FU_NEW_Extrahepatic_Dz_Location,
                                    "FU1_EHDDATE": FU_NEW_Extrahepatic_Dz_Date.strftime("%Y-%m-%d"),
                                    "FU1_NTCHG": FU_change_non_target_lesion,
                                    "FU1_TDCHG": FU_change_target_lesion,
                                    "FU1_MREC_LOCAL": first_fu_mrecist_localized,
                                    "FU1_MREC_OVERALL": first_fu_mrecist_overall,
                                    "FU1_FT": FU_Free_Text,
                                    "FU2_MOD": FU2_Scan_Modality,
                                    "FU2_IMG_DATE": FU2_Imaging_Date.strftime("%Y-%m-%d"),
                                    "FU2_MS_Y90": FU2_Months_Since_Y90,
                                    "FU2_TOTLES": FU2_Total_number_of_lesions,
                                    "FU2_TL1LAD": FU2_Target_Lesion_1_LAD_Art_Enhanc,
                                    "FU2_TL1PAD": FU2_Target_Lesion_1_PAD_Art_Enhanc,
                                    "FU2_TL1CCD": FU2_Target_Lesion_1_CCD_Art_Enhanc,
                                    "FU2_TL2SEG": FU2_Target_Lesion_2_Segments,
                                    "FU2_TL2LAD": FU2_Target_Lesion_2_LAD_Art_Enhanc,
                                    "FU2_TL2PAD": FU2_Target_Lesion_2_PAD_Art_Enhanc,
                                    "FU2_TL2CCD": FU2_Target_Lesion_2_CCD_Art_Enhanc,
                                    "FU2_TLDIA": FU2_Follow_up_2_targeted_Lesion_Dia_Sum,
                                    "FU2_NTL1LAD": FU2_Non_Target_Lesion_1_LAD_Art_Enhanc,
                                    "FU2_NTL1PAD": FU2_Non_Target_Lesion_1_PAD_Art_Enhanc,
                                    "FU2_NTL1CCD": FU2_Non_Target_Lesion_1_CCD_Art_Enhanc,
                                    "FU2_NTLDIA": FU2_Non_targeted_Lesion_Dia_Sum,
                                    "FU2_NECROSIS": FU2_Lesion_Necrosis,
                                    "FU2_REV": FU2_Reviewers_Initials,
                                    "FU2_NTLRSP": FU2_Non_target_lesion_response,
                                    "FU2_NEWLES": FU2_New_Lesions,
                                    "FU2_EHD": FU2_NEW_Extrahepatic_Disease,
                                    "FU2_EHDLOC": FU2_NEW_Extrahepatic_Dz_Location,
                                    "FU2_EHDDATE": FU2_NEW_Extrahepatic_Dz_Date.strftime("%Y-%m-%d"),
                                    "FU2_NTCHG": FU2_change_non_target_lesion,
                                    "FU2_TDCHG": FU2_change_target_lesion,
                                    "FU2_MREC_CALC": second_fu_mrecist_calc,
                                    "FU2_MREC_LOCAL": second_fu_mrecist_localized,
                                    "FU2_MREC_OVERALL": second_fu_mrecist_overall,
                                    "FU2_FT": FU2_Free_Text,
                                    "FU3_MOD": FU3_Scan_Modality,
                                    "FU3_IMG_DATE": FU3_Imaging_Date.strftime("%Y-%m-%d"),
                                    "FU3_MS_Y90": FU3_Months_Since_Y90,
                                    "FU3_TOTLES": FU3_Total_number_of_lesions,
                                    "FU3_TL1LAD": FU3_Target_Lesion_1_LAD_Art_Enhanc,
                                    "FU3_TL1PAD": FU3_Target_Lesion_1_PAD_Art_Enhanc,
                                    "FU3_TL1CCD": FU3_Target_Lesion_1_CCD_Art_Enhanc,
                                    "FU3_TL2SEG": FU3_Target_Lesion_2_Segments,
                                    "FU3_TL2LAD": FU3_Target_Lesion_2_LAD_Art_Enhanc,
                                    "FU3_TL2PAD": FU3_Target_Lesion_2_PAD_Art_Enhanc,
                                    "FU3_TL2CCD": FU3_Target_Lesion_2_CCD_Art_Enhanc,
                                    "FU3_TLDIA": FU3_Follow_up_2_targeted_Lesion_Dia_Sum,
                                    "FU3_NTL1LAD": FU3_Non_Target_Lesion_1_LAD_Art_Enhanc,
                                    "FU3_NTL1PAD": FU3_Non_Target_Lesion_1_PAD_Art_Enhanc,
                                    "FU3_NTL1CCD": FU3_Non_Target_Lesion_1_CCD_Art_Enhanc,
                                    "FU3_NTLDIA": FU3_Non_targeted_Lesion_Dia_Sum,
                                    "FU3_NEC": FU3_Lesion_Necrosis,
                                    "FU3_REV": FU3_Reviewers_Initials,
                                    "FU3_NTLRSP": FU3_Non_target_lesion_response,
                                    "FU3_NEWLES": FU3_New_Lesions,
                                    "FU3_EHD": FU3_NEW_Extrahepatic_Disease,
                                    "FU3_EHDLOC": FU3_NEW_Extrahepatic_Dz_Location,
                                    "FU3_EHDDATE": FU3_NEW_Extrahepatic_Dz_Date.strftime("%Y-%m-%d"),
                                    "FU3_NTCHG": FU3_change_non_target_lesion,
                                    "FU3_TDCHG": FU3_change_target_lesion,
                                    "FU3_MREC_CALC": third_fu_mrecist_calc,
                                    "FU3_MREC_LOCAL": third_fu_mrecist_localized,
                                    "FU3_MREC_OVERALL": third_fu_mrecist_overall,
                                    "FU3_FT": FU3_Free_Text,
                                    "FU4_MOD": FU4_Scan_Modality,
                                    "FU4_IMG_DATE": FU4_Imaging_Date.strftime("%Y-%m-%d"),
                                    "FU4_MONTHS_Y90": FU4_Months_Since_Y90,
                                    "FU4_TOTLES": FU4_Total_number_of_lesions,
                                    "FU4_TL1LAD": FU4_Target_Lesion_1_LAD_Art_Enhanc,
                                    "FU4_TL1PAD": FU4_Target_Lesion_1_PAD_Art_Enhanc,
                                    "FU4_TL1CCD": FU4_Target_Lesion_1_CCD_Art_Enhanc,
                                    "FU4_TL2SEG": FU4_Target_Lesion_2_Segments,
                                    "FU4_TL2LAD": FU4_Target_Lesion_2_LAD_Art_Enhanc,
                                    "FU4_TL2PAD": FU4_Target_Lesion_2_PAD_Art_Enhanc,
                                    "FU4_TL2CCD": FU4_Target_Lesion_2_CCD_Art_Enhanc,
                                    "FU4_TL_DIASUM": FU4_Follow_up_2_targeted_Lesion_Dia_Sum,
                                    "FU4_NTL1LAD": FU4_Non_Target_Lesion_1_LAD_Art_Enhanc,
                                    "FU4_NTL1PAD": FU4_Non_Target_Lesion_1_PAD_Art_Enhanc,
                                    "FU4_NTL1CCD": FU4_Non_Target_Lesion_1_CCD_Art_Enhanc,
                                    "FU4_NTL_DIASUM": FU4_Non_targeted_Lesion_Dia_Sum,
                                    "FU4_NECROSIS": FU4_Lesion_Necrosis,
                                    "FU4_REVFT": FU4_Reviewers_Initials,
                                    "FU4_NTLRSP": FU4_Non_target_lesion_response,
                                    "FU4_NEWLESION": FU4_New_Lesions,
                                    "FU4_NEWEHD": FU4_NEW_Extrahepatic_Disease,
                                    "FU4_EHDLOC": FU4_NEW_Extrahepatic_Dz_Location,
                                    "FU4_EHDDATE": FU4_NEW_Extrahepatic_Dz_Date.strftime("%Y-%m-%d"),
                                    "FU4_NTL_CHANGE": FU4_change_non_target_lesion,
                                    "FU4_TL_CHANGE": FU4_change_target_lesion,
                                    "FU4_MREC_CALC": fourth_fu_mrecist_calc,
                                    "FU4_MREC_LOCAL": fourth_fu_mrecist_localized,
                                    "FU4_MREC_OVERALL": fourth_fu_mrecist_overall,
                                    "FU4_FT": FU4_Free_Text,
                                    "FU5_MOD": FU5_Scan_Modality,
                                    "FU5_IMG_DATE": FU5_Imaging_Date.strftime("%Y-%m-%d"),
                                    "FU5_MONTHS_Y90": FU5_Months_Since_Y90,
                                    "FU5_TOTLES": FU5_Total_number_of_lesions,
                                    "FU5_TL1LAD": FU5_Target_Lesion_1_LAD_Art_Enhanc,
                                    "FU5_TL1PAD": FU5_Target_Lesion_1_PAD_Art_Enhanc,
                                    "FU5_TL1CCD": FU5_Target_Lesion_1_CCD_Art_Enhanc,
                                    "FU5_TL2SEG": FU5_Target_Lesion_2_Segments,
                                    "FU5_TL2LAD": FU5_Target_Lesion_2_LAD_Art_Enhanc,
                                    "FU5_TL2PAD": FU5_Target_Lesion_2_PAD_Art_Enhanc,
                                    "FU5_TL2CCD": FU5_Target_Lesion_2_CCD_Art_Enhanc,
                                    "FU5_TL_DIASUM": FU5_Follow_up_2_targeted_Lesion_Dia_Sum,
                                    "FU5_NTL1LAD": FU5_Non_Target_Lesion_1_LAD_Art_Enhanc,
                                    "FU5_NTL1PAD": FU5_Non_Target_Lesion_1_PAD_Art_Enhanc,
                                    "FU5_NTL1CCD": FU5_Non_Target_Lesion_1_CCD_Art_Enhanc,
                                    "FU5_NTL_DIASUM": FU5_Non_targeted_Lesion_Dia_Sum,
                                    "FU5_NTLRSP": FU5_Non_target_lesion_response,
                                    "FU5_NEWLESION": FU5_New_Lesions,
                                    "FU5_NEWEHD": FU5_NEW_Extrahepatic_Disease,
                                    "FU5_EHDLOC": FU5_NEW_Extrahepatic_Dz_Location,
                                    "FU5_EHDDATE": FU5_NEW_Extrahepatic_Dz_Date.strftime("%Y-%m-%d"),
                                    "FU5_NTL_CHANGE": FU5_change_non_target_lesion,
                                    "FU5_TL_CHANGE": FU5_change_target_lesion,
                                    "FU5_MREC_CALC": fifth_fu_mrecist_calc,
                                    "FU5_MREC_LOCAL": fifth_fu_mrecist_localized,
                                    "FU5_MREC_OVERALL": fifth_fu_mrecist_overall,
                                    "FU5_FT": FU5_Free_Text,
                                    "DEAD": dead,
                                    "DATE_DEAD": Date_of_Death.strftime("%Y-%m-%d") if Date_of_Death != "NA" else Date_of_Death,
                                    "TIME_DEAD": Time_to_Death,
                                    "OLT": OLT,
                                    "DATE_OLT": Date_of_OLT.strftime("%Y-%m-%d") if Date_of_OLT != "NA" else Date_of_OLT,
                                    "TIME_OLT": Time_to_OLT,
                                    "RTX": Repeat_tx_post_Y90,
                                    "DATE_RTX": Date_of_Repeat_tx_Post_Y90.strftime("%Y-%m-%d") if Date_of_Repeat_tx_Post_Y90 != 'NA' else Date_of_Repeat_tx_Post_Y90,
                                    "TIME_RTX": Time_to_Repeat_Tx_Post_Y90,
                                    "DATE_LOCALP": Date_of_Localized_Progression.strftime("%Y-%m-%d") if Date_of_Localized_Progression != "No Progression" else Date_of_Localized_Progression,
                                    "TIME_LOCALP" : Time_to_localized_progression,
                                    "DATE_OVERALLP" :Date_of_Overall_Progression.strftime("%Y-%m-%d") if Date_of_Overall_Progression != "No Progression" else Date_of_Overall_Progression,
                                    "TIME__OVERALLP" :Time_to_overall_progression,
                                    "LFU":lfu,
                                    "DATE_LFU": Date_of_Last_Follow_up_last_imaging_date.strftime("%Y-%m-%d") if Date_of_Last_Follow_up_last_imaging_date != 'NA' else Date_of_Last_Follow_up_last_imaging_date,
                                    "TIME_LFU": Time_to_Last_Follow_up_last_imaging_date,
                                    "NOTES_FT" : notes_free_text,
                                    "BMRECIST" :bestm_recist,
                                    "DATE_BMREC_TTR":date_bestm_recist.strftime("%Y-%m-%d") if date_bestm_recist != "No Date" else date_bestm_recist,
                                    "TIME_BMREC_TTR":time_to_bestm_recist,
                                    "PERCHANGE_BEST_TTR": PERCHANGE_BEST_TTR,
                                    "BM_CRVSNON":bestm_recist_cr_vs_non_cr,
                                    "MR_RVSNR":bestm_recist_r_vs_nr,
                                    "DATE_BEST_MTR":DATE_BEST_MTR.strftime("%Y-%m-%d"),
                                    "TIME_BEST_MRT":TIME_BEST_MRT,
                                    "PERCHANGE_BEST_MTR":PERCHANGE_BEST_MTR,
                                    "OS_Date":OS_Date.strftime("%Y-%m-%d"),
                                    "OS_Events":OS_Events,
                                    "OS_Time": OS_Time,
                                    "OS_Reason":OS_Reason,
                                    "LPFS_Date":LPFS_Date.strftime("%Y-%m-%d"),
                                    "LPFS_Events":LPFS_Events,
                                    "LPFS_Time":LPFS_Time,
                                    "LPFS_Reason":LPFS_Reason,
                                    "PFS_Date" : PFS_Date.strftime("%Y-%m-%d"),
                                    "PFS_Events":PFS_Events,
                                    "PFS_Time": PFS_Time,
                                    "PFS_Reason" : PFS_Reason,
                                    "DOR" : DOR,

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
                        trlnkid = st.selectbox(
                                "TRLNKID [Excel : TRLNKID]\n\n Tumor 1 (1), Tumor 2 (2)",
                                    options=["1", "2"],
                                    format_func=lambda x: {
                                            "1": "Tumor 1",
                                            "2": "Tumor 2",
                                        }[x],
                               
                                index= None,
                            placeholder="Choose an option",
                            )
                        input_GTV_mean_dose = st.text_input("GTV mean dose")
                        input_Tx_vol_mean_dose = st.text_input("Tx vol mean dose")
                        input_Liver_Vol_Mean_dose = st.text_input("Liver Vol Mean dose")
                        input_Healthy_Liver_mean_dose = st.text_input("Healthy Liver mean dose")
                        input_GTV_Vol = st.number_input("GTV Vol",step=0.1)
                        input_Tx_vol = st.number_input("Tx vol",step=0.1)
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
                        input_ActivityBq = st.number_input("ActivityBq",step=0.1)
                        input_ActivityCi = (input_ActivityBq/37000000000.0)
                        input_Tx_vol_Activity_Density = (input_ActivityCi/max(0.1,input_Tx_vol))
                        input_ActivityCi = format(input_ActivityCi, ".5E")
                        st.write("ActivityCi", input_ActivityCi)
                        input_Tx_vol_Activity_Density = format(input_Tx_vol_Activity_Density, ".5E")
                        st.write("Tx vol Activity Density",input_Tx_vol_Activity_Density)
                        input_GTV_less_D95_Vol_ml = st.text_input("GTV < D95 Vol_ml")
                        input_GTV_less_D95_Mean_Dose = st.text_input("GTV < D95 Mean Dose")
                        input_GTV_less_D95_Mx_Dose = st.text_input("GTV < D95 Max Dose",value = df.iloc[0]["GTVLT_D95MAX"])
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
                        input_GTV_less_100_Gy_Max_Dose = st.text_input("GTV < 100 Gy Max Dose",value = df.iloc[0]["GTVLT_100MAX"])
                        input_GTV_less_100_Gy_Min_Dose = st.text_input("GTV < 100 Gy Min Dose")
                        input_GTV_less_100_Gy_SD = st.text_input("GTV < 100 Gy SD")

                        submit_dosimetry_data = st.form_submit_button("Submit")

                        if submit_dosimetry_data:
                            data11 = {
                                    "TRLNKID": trlnkid,
                                    "GTV_MEANDOSE": input_GTV_mean_dose,
                                    "TXVOL_MEANDOSE": input_Tx_vol_mean_dose,
                                    "LIVVOL__MEANDOSE": input_Liver_Vol_Mean_dose,
                                    "HEALTHYLIV_MEANDOSE": input_Healthy_Liver_mean_dose,
                                    "GTV_VOL": input_GTV_Vol,
                                    "TX_VOL": input_Tx_vol,
                                    "LIVER_VOL": input_Liver_vol,
                                    "HEALTHYLIV_VOL": input_Healthy_Liver_Vol,
                                    "GTVLIV_FRAC": input_GTV_Liver,
                                    "D98": input_D98,
                                    "D95": input_D95,
                                    "D90": input_D90,
                                    "D80": input_D80,
                                    "D70": input_D70,
                                    "V100": input_V100,
                                    "V200": input_V200,
                                    "V300": input_V300,
                                    "V400": input_V400,
                                    "ACTIVITYBQ": input_ActivityBq,
                                    "ACTIVITYCI": input_ActivityCi,
                                    "ACTIVITY_TXVOL": input_Tx_vol_Activity_Density,
                                    "GTVLT_D95VOL": input_GTV_less_D95_Vol_ml,
                                    "GTVLT_D95MEAN": input_GTV_less_D95_Mean_Dose,
                                    "GTVLT_D95MAX": input_GTV_less_D95_Mx_Dose,
                                    "GTVLT_D95MIN": input_GTV_less_D95_Min_Dose,
                                    "GTVLT_D95SD": input_GTV_less_D95_SD,
                                    "V1_GTVLT_D95VOL": input_GTV_less_D95_Vol_1,
                                    "V1_GTVLT_D95MEAN": input_GTV_less_D95_Mean_Dose_1,
                                    "V1_GTVLT_D95MIN": input_GTV_less_D95_Min_Dose_1,
                                    "V1_GTVLT_D95SD": input_GTV_less_D95_SD_1,
                                    "V2_GTVLT_D95VOL": input_GTV_less_D95_Vol_2,
                                    "V2_GTVLT_D95MEAN": input_GTV_less_D95_Mean_Dose_2,
                                    "V2_GTVLT_D95MIN": input_GTV_less_D95_Min_Dose_2,
                                    "V2_GTVLT_D95SD": input_GTV_less_D95_SD_2,
                                    "GTVLT_100VOL": input_GTV_less_100_Gy_Vol,
                                    "GTVLT_100MEAN": input_GTV_less_100_Gy_Mean_Dose,
                                    "GTVLT_100MAX": input_GTV_less_100_Gy_Max_Dose,
                                    "GTVLT_100MIN": input_GTV_less_100_Gy_Min_Dose,
                                    "GTVLT_100SD": input_GTV_less_100_Gy_SD
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
                        input_1AFP_DATE = st.text_area("1AFP Date")
                        input_1AFP = st.text_area("1AFP")
                        input_2AFP_DATE = st.text_area("2AFP Date")
                        input_2AFP = st.text_area("2AFP")
                        input_3AFP_DATE = st.text_area("3AFP Date")
                        input_3AFP = st.text_area("3AFP")
                        input_4AFP_DATE = st.text_area("4AFP Date")
                        input_4AFP = st.text_area("4AFP")
                        input_5AFP_DATE = st.text_area("5AFP Date")
                        input_5AFP = st.text_area("5AFP")
                        input_6AFP_DATE = st.text_area("6AFP Date")
                        input_6AFP = st.text_area("6AFP")
                        input_7AFP_DATE = st.text_area("7AFP Date")
                        input_7AFP = st.text_area("7AFP")
                        input_8AFP_DATE = st.text_area("8AFP Date")
                        input_8AFP = st.text_area("8AFP")
                        input_9AFP_DATE = st.text_area("9AFP Date")
                        input_9AFP = st.text_area("9AFP")
                        input_10AFP_DATE = st.text_area("10AFP Date")
                        input_10AFP = st.text_area("10AFP")
                        input_11AFP_DATE = st.text_area("11AFP Date")
                        input_11AFP = st.text_area("11AFP")
                        input_12AFP_DATE = st.text_area("12AFP Date")
                        input_12AFP = st.text_area("12AFP")
                        input_13AFP_DATE = st.text_area("13AFP Date")
                        input_13AFP = st.text_area("13AFP")
                        input_14AFP_DATE = st.text_area("14AFP Date")
                        input_14AFP = st.text_area("14AFP")
                        input_15AFP_DATE = st.text_area("15AFP Date")
                        input_15AFP = st.text_area("15AFP")
                        input_16AFP_DATE = st.text_area("16AFP Date")
                        input_16AFP = st.text_area("16AFP")
                        input_17AFP_DATE = st.text_area("17AFP Date")
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
                        input_31AFP_DATE = st.text_area("31AFP Date")
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
                                    "1AFPDATE": input_1AFP_DATE, "1AFP": input_1AFP,
                                    "2AFPDATE": input_2AFP_DATE, "2AFP": input_2AFP,
                                    "3AFPDATE": input_3AFP_DATE, "3AFP": input_3AFP,
                                    "4AFPDATE": input_4AFP_DATE, "4AFP": input_4AFP,
                                    "5AFPDATE": input_5AFP_DATE, "5AFP": input_5AFP,
                                    "6AFPDATE": input_6AFP_DATE, "6AFP": input_6AFP,
                                    "7AFPDATE": input_7AFP_DATE, "7AFP": input_7AFP,
                                    "8AFPDATE": input_8AFP_DATE, "8AFP": input_8AFP,
                                    "9AFPDATE": input_9AFP_DATE, "9AFP": input_9AFP,
                                    "10AFPDATE": input_10AFP_DATE, "10AFP": input_10AFP,
                                    "11AFPDATE": input_11AFP_DATE, "11AFP": input_11AFP,
                                    "12AFPDATE": input_12AFP_DATE, "12AFP": input_12AFP,
                                    "13AFPDATE": input_13AFP_DATE, "13AFP": input_13AFP,
                                    "14AFPDATE": input_14AFP_DATE, "14AFP": input_14AFP,
                                    "15AFPDATE": input_15AFP_DATE, "15AFP": input_15AFP,
                                    "16AFPDATE": input_16AFP_DATE, "16AFP": input_16AFP,
                                    "17AFPDATE": input_17AFP_DATE, "17AFP": input_17AFP,
                                    "18AFPDATE": input_18AFP_DATE, "18AFP": input_18AFP,
                                    "19AFPDATE": input_19AFP_DATE, "19AFP": input_19AFP,
                                    "20AFPDATE": input_20AFP_DATE, "20AFP": input_20AFP,
                                    "21AFPDATE": input_21AFP_DATE, "21AFP": input_21AFP,
                                    "22AFPDATE": input_22AFP_DATE, "22AFP": input_22AFP,
                                    "23AFPDATE": input_23AFP_DATE, "23AFP": input_23AFP,
                                    "24AFPDATE": input_24AFP_DATE, "24AFP": input_24AFP,
                                    "25AFPDATE": input_25AFP_DATE, "25AFP": input_25AFP,
                                    "26AFPDATE": input_26AFP_DATE, "26AFP": input_26AFP,
                                    "27AFPDATE": input_27AFP_DATE, "27AFP": input_27AFP,
                                    "28AFPDATE": input_28AFP_DATE, "28AFP": input_28AFP,
                                    "29AFPDATE": input_29AFP_DATE, "29AFP": input_29AFP,
                                    "30AFPDATE": input_30AFP_DATE, "30AFP": input_30AFP,
                                    "31AFPDATE": input_31AFP_DATE, "31AFP": input_31AFP,
                                    "32AFPDATE": input_32AFP_DATE, "32AFP": input_32AFP,
                                    "33AFPDATE": input_33AFP_DATE, "33AFP": input_33AFP,
                                    "34AFPDATE": input_34AFP_DATE, "34AFP": input_34AFP
                                }
                            if "patient_info" in st.session_state :
                                update_google_sheet(data12, st.session_state.temp_mrn)
                            else:
                                st.error(f"No patient information found for MRN {st.session_state.temp_mrn}")
                    except:
                        st.warning("Please Fill Patient Information Page")
    
def edit_existing_data():

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
        
        mrn = st.number_input("Enter MRN to edit and Press Enter",step=1)
        
        if mrn:
            mrn_str = str(int(mrn))
            if df1.empty or mrn not in df1['MRN'].astype(int).values:
                st.error(f"MRN {mrn} not exists. Please enter a unique MRN.")
                if 'mrn' in st.session_state:
                    del st.session_state.mrn
            else:
                st.session_state.mrn = mrn_str
                st.subheader("Change_Data")
                st.write(f"Editing data for MRN: {mrn}")
                df = fetch_data_for_mrn(mrn)
                try:
                    st.write(df)
                    mrn=str(mrn)
                    fetch_date = pd.to_datetime(df.loc[df['MRN'] == mrn, 'TAREDATE'].values[0]).date()
                    # Convert fetch_date to a datetime.date object
                    fetch_date = pd.to_datetime(fetch_date).date()
                    index = (df["MRN"] == mrn)
                except:
                     st.write("please write valid mrn")
                col1, col2 = st.columns([0.3, 0.7],gap="small")
                tabs = ["Patient Information","Patient Demographics", "Cirrhosis PMH","HCC Diagnosis", "Previous Therapy for HCC", "Pre Y90", "Day_Y90", "Post Y90 Within 30 Days Labs", "Other Post Tare","Imaging Date","Dosimetry Data","AFP"]
                
                with col1:
                    st.header("Patient Deatils")
                    st.session_state.selected_tab = st.radio("", tabs)

                with col2:
                    if st.session_state.selected_tab == "Patient Information":
                        st.subheader("Patient_Info")
                        with st.form("patient_info_form"):
                            #try:
                            # Patient Info Section
                                col1, col2 = st.columns(2)
                                first_name = col1.text_input("First Name [Excel : FIRST]",value=df.iloc[0]["FIRST"])
                                first_name = first_name.capitalize()
                                last_name = col2.text_input("Last Name [Excel : LAST]",value=df.iloc[0]["LAST"])
                                last_name = last_name.capitalize()
                                st.write(mrn)
                                id=df.iloc[0]["ID"]
                
                                if first_name and last_name:
                                    base_id = first_name[0] + last_name[0]
                                    if not df.empty:
                                        existing_ids = df['ID'].tolist()
                                        count = sum(1 for id in existing_ids if id.startswith(base_id))
                                        id = f"{base_id}{count + 1}"
                                    else:
                                        id = f"{base_id}1"
                                else:
                                    id = ""
                                
                                duplicate_procedure_check = df.iloc[0]["DUP"]
                                if id.endswith("1"):
                                    duplicate_procedure_check = ""
                                else:
                                    duplicate_procedure_check = "Duplicate"
                                
                                tare_date = st.date_input("TARE Tx Date [Excel : TAREDATE]", help="Select the treatment date",value=datetime.strptime(df.iloc[0]["TAREDATE"], "%Y-%m-%d").date())
                                
                                procedure_technique = st.selectbox(
                                "Procedure Technique    [Excel : PROTYPE]\n\nLobar (1), Segmental (2)",
                                options=["1", "2"],
                                format_func=lambda x: {
                                    "1": "Lobar",
                                    "2": "Segmental",
                                }[x],
                                index=["1", "2"].index(df.iloc[0]["PROTYPE"]) if df.iloc[0]["PROTYPE"]  else 0,
                                # No default selection
                                placeholder="Choose an option",
                                )

                                age = st.number_input("Age at time of TARE [Excel : TAREAGE]", value=int(df.iloc[0]["TAREAGE"]) ,min_value=0, max_value=150, step=1, format="%d")
                            
                                submit_tab1 = st.form_submit_button("Submit")
                                if submit_tab1:
                                    st.write("ID :",id)
                                    data = {
                                        "FIRST": first_name,
                                        "LAST": last_name,
                                        "MRN": mrn,
                                        "ID" : id,
                                        "DUP" : duplicate_procedure_check,
                                        "TAREDATE": tare_date.strftime("%Y-%m-%d"),
                                        "PROTYPE": procedure_technique,
                                        "TAREAGE": age
                                        } 
                                    update_google_sheet(data, mrn)
                            #except:
                             #   pass

                    elif st.session_state.selected_tab == "Patient Demographics":
                        st.subheader("Patient Demographics")
                        with st.form("demographics_form"):

                            gender = st.selectbox(
                                "Gender     [Excel : GENDER]\n\nMale (1) , Female (2)",
                                options=["1", "2"],
                                format_func=lambda x: {
                                                    "1": "Male",
                                                    "2": "Female",
                                                }[x],
                                index=["1", "2"].index(df.iloc[0]["GENDER"]) if df.iloc[0]["GENDER"] else None,
                                placeholder="Choose an option",
                            )
                            # Ethnicity dropdown
                            ethnicity = st.selectbox(
                                "Ethnicity      [Excel : ETHNICITY]\n\n(1) Black, (2) White, (3) Asian, (4) Hispanic, (5) Other, NA (cant find it in sheet), 0 (not present)",
                                options=["1","2", "3", "4", "5", "NA", "0"],
                                format_func=lambda x: {
                                                    "1": "Black",
                                                    "2": "White",
                                                    "3": "Asian",
                                                    "4": "Hispanic",
                                                    "5": "Other",
                                                    "NA": "NA (cant find it in sheet)",
                                                    "0" : "0 (not present)",
                                                }[x],
                                index=["1","2", "3", "4", "5", "NA", "0"].index(df.iloc[0]["ETHNICITY"]) if df.iloc[0]["ETHNICITY"] else None,  # No default selection
                                placeholder="Choose an option",
                            )

                            hypertension = st.selectbox(
                                "PMHx Hypertension      [Excel : PMHHTN]\n\nYes(1), No(0)",
                            options=["1", "0"],
                            format_func=lambda x: {
                                                    "1": "Yes",
                                                    "0": "No",
                                                }[x],
                                index=["1", "0"].index(df.iloc[0]["PMHHTN"]) if df.iloc[0]["PMHHTN"] else None,  # No default selection
                                placeholder="Choose an option",
                            )

                            diabetes = st.selectbox(
                                "PMHx Diabetes (T1 or T2)  [Excel : PMHDM]\n\nYes(1), No(0)",
                            options=["1", "0"],
                            format_func=lambda x: {
                                                    "1": "Yes",
                                                    "0": "No",
                                                }[x],
                                index=["1", "0"].index(df.iloc[0]["PMHDM"]) if df.iloc[0]["PMHDM"] else None,  # No default selection
                                placeholder="Choose an option",
                            )

                            hypercholesterolemia = st.selectbox(
                                "Hypercholesterolemia      [Excel : HYPERCHOL]\n\nYes(1), No(0)",
                            options=["1", "0"],
                            format_func=lambda x: {
                                                    "1": "Yes ",
                                                    "0": "No  ",
                                                }[x],
                                index=["1", "0"].index(df.iloc[0]["HYPERCHOL"]) if df.iloc[0]["HYPERCHOL"] else None,  # No default selection
                                placeholder="Choose an option",
                            )

                            smoking = st.selectbox(
                                "Hx of Smoking      [Excel : PMHSMOKE]\n\nYes(1), No(0)",
                            options=["1", "0"],
                            format_func=lambda x: {
                                                    "1": "Yes ",
                                                    "0": "No  ",
                                                }[x],
                                index=["1", "0"].index(df.iloc[0]["PMHSMOKE"]) if df.iloc[0]["PMHSMOKE"] else None,  
                                placeholder="Choose an option",
                            )
                            obesity = st.selectbox(
                                "Obesity        [Excel : OBESITY]\n\nYes(1), No(0)",
                            options=["1", "0"],
                            format_func=lambda x: {
                                                    "1": "Yes ",
                                                    "0": "No  ",
                                                }[x],
                                index=["1", "0"].index(df.iloc[0]["OBESITY"]) if df.iloc[0]["OBESITY"] else None,  
                                placeholder="Choose an option",
                            )
                            submit_tab2 = st.form_submit_button("Submit")
                            if submit_tab2:
                                data1={
                                "GENDER": gender,
                                "ETHNICITY":ethnicity,
                                "PMHHTN": hypertension,
                                "PMHDM":diabetes,
                                "HYPERCHOL" : hypercholesterolemia,
                                "PMHSMOKE" : smoking,
                                "OBESITY" : obesity,
                                }
                                update_google_sheet(data1,mrn)
                        
                    elif st.session_state.selected_tab == "Cirrhosis PMH":
                        st.subheader("Cirrhosis PMH")
                        with st.form("cirrhosis_pmh_form"):

                            cir_pmh_hbv_status = st.selectbox(
                                "Cir PMH HBV Status [ Excel : CIRPMH_HBV ]\n\nYes(1), No(0)  ",
                                options=["1", "0"],
                                format_func=lambda x: {
                                                    "1": "Yes ",
                                                    "0": "No  ",
                                                }[x],
                                help="Select HBV Status",
                                index=["1", "0"].index(df.iloc[0]["CIRPMH_HBV"]) if df.iloc[0]["CIRPMH_HBV"] else None,
                                placeholder="Choose an option",
                            )

                            cir_pmh_hbv_free_text = "0" if cir_pmh_hbv_status == "No" else st.text_input(
                                "Cir PMH HBV Free Text [ Excel : CIRPMH_HBVFT ]",
                                value = df.iloc[0]["CIRPMH_HBVFT"],
                            )
                            
                            cir_pmh_hbv_art = "0" if cir_pmh_hbv_status == "No" else st.selectbox(
                                "Cir PMH HBV ART [ Excel : CIRPMH_HBVART ]\n\n(1) Entecavir, (2) Tenofovir, (3) NA ",
                            options=["1", "2", "3"],
                            format_func=lambda x: {
                                                    "1": "Entecavir ",
                                                    "2": "Tenofovir ",
                                                    "3": "NA "
                                                }[x],
                                index=["1", "2", "3"].index(df.iloc[0]["CIRPMH_HBVART"]) if df.iloc[0]["CIRPMH_HBVART"] else None,  # No default selection
                                placeholder="Choose an option",
                            )

                            cir_pmh_hcv_status = st.selectbox("Cir_PMH_HCV Status [ Excel : CIRPMH_HCV ]\n\nYes(1), No(0)  ",
                            options=["1", "0"],
                            format_func=lambda x: {
                                                    "1": "Yes ",
                                                    "0": "No  ",
                                                }[x],
                               
                                index=["1", "0"].index(df.iloc[0]["CIRPMH_HCV"]) if df.iloc[0]["CIRPMH_HCV"] else None,  # No default selection
                                placeholder="Choose an option",
                            )

                            cir_pmh_hcv_free_text = "No" if cir_pmh_hcv_status == "No" else st.text_input(
                                "Cir_PMH_HCV Free Text [ Excel : CIRPMH_HCVFT ]",
                                value = df.iloc[0]["CIRPMH_HCVFT"],
                                help="Provide additional details for HCV Status",
                            )

                            cir_pmh_hcv_art = "No" if cir_pmh_hcv_status == "No" else st.selectbox(
                                "Cir_PMH_HCV ART [ Excel : CIRPMH_HCVART ]\n\n(1) sofosbuvir/velpatasvir , (2) ledipasvir/sofosbuvir, (3) NA (if u can't find a med or if they arent on it), (4) Glecaprevir/pibrentasvir",
                            options=["1", "2", "3", "4"],
                            format_func=lambda x: {
                                                    "1": " sofosbuvir/velpatasvir",
                                                    "2": " ledipasvir/sofosbuvir",
                                                    "3": " NA (if you can't find a med or if they aren't on it)",
                                                    "4": " Glecaprevir/pibrentasvir"
                                                }[x],
                                help="Select ART treatment for HCV",
                                index=["1", "2", "3", "4"].index(df.iloc[0]["CIRPMH_HCVART"]) if df.iloc[0]["CIRPMH_HCVART"] else None, 
                                placeholder="Choose an option",
                        
                            )

                            cir_pmh_alcohol_use_disorder = st.selectbox( 
                                "Cir_PMH_Alcohol Use Disorder [ Excel : CIRPMH_AUD ]\n\nYes(1), No(0)  ",
                            options=["1", "0"],
                            format_func=lambda x: {
                                                    "1": "Yes",
                                                    "0": "No ",
                                                }[x],
                                help="Select Alcohol Disorder",
                                index=["1", "0"].index(df.iloc[0]["CIRPMH_AUD"]) if df.iloc[0]["CIRPMH_AUD"] else None,  
                                placeholder="Choose an option",
                            )

                            cir_pmh_alcohol_free_text = "0" if cir_pmh_alcohol_use_disorder == "No" else st.text_input(
                                "Cir_PMH_Alcohol Free Text [ Excel : CIRPMH_AUDFT ]",
                                value = df.iloc[0]["CIRPMH_AUDFT"],
                                help="Provide additional details for Alcohol Disorder",
                            )

                            cir_pmh_ivdu_status = st.selectbox(
                              "Cir_PMH_IVDU Status [ Excel : CIRPMH_IVDU ]\n\nYes(1), No(0)  ",
                            options=["1", "0"],
                            format_func=lambda x: {
                                                    "1": "Yes ",
                                                    "0": "No  ",
                                                }[x],
                                help="Select IVDU Status",
                                index=["1", "0"].index(df.iloc[0]["CIRPMH_IVDU"]) if df.iloc[0]["CIRPMH_IVDU"] else None, 
                                placeholder="Choose an option",
                            )

                            cir_pmh_ivdu_free_text = "0" if cir_pmh_ivdu_status == "No" else st.text_input(
                                "Cir_PMH_IVDU Free Text [ Excel : CIRPMH_IVDUFT ]",
                                value = df.iloc[0]["CIRPMH_IVDUFT"],
                                help="Provide additional details for IVDU"
                        
                            )

                            cir_pmh_liver_addtional_factor = st.selectbox(
                                "Cir_PMH_Liver Additional Factors [ Excel : CIRPMH_LIVERFAC ]\n\n (1) NAFLD, (2) MAFLD, (3) NASH, (4) Autoimmune Hepatitis, (5) Hereditary Hemochromatosis, (6) none",
                            options=["1", "2", "3", "4", "5", "6"],
                            format_func=lambda x: {
                                                    "1": "NAFLD ",
                                                        "2": "MAFLD ",
                                                        "3": "NASH ",
                                                        "4": "Autoimmune Hepatitis ",
                                                        "5": "Hereditary Hemochromatosis",
                                                        "6": "None "
                                                }[x], 
                                help="Select Other Contributing Factors",
                                index=["1", "2", "3", "4", "4 ","6"].index(df.iloc[0]["CIRPMH_LIVERFAC"]) if df.iloc[0]["CIRPMH_LIVERFAC"] else None,
                                placeholder="Choose an option",
                            )
                    
                            st.subheader("Cirrhosis Dx")
                            if df.iloc[0]["CIRDX_DATE"]:
                                Cirdx_Value = datetime.strptime(df.iloc[0]["CIRDX_DATE"], "%Y-%m-%d").date()
                            else:
                                Cirdx_Value = None
                            Cirrhosis_Dx_Diagnosis_Date = st.date_input("Cirrhosis Dx Diagnosis Date [ Excel : CIRDX_DATE ]", value = Cirdx_Value)

                            Cirrhosis_Dx_Diagnosis_Method = st.selectbox(
                                "Cirrhosis_Dx_Diagnosis Method [ Excel : CIRDX_METHOD ]\n\n(1) Biopsy, (2) Imaging  ",
                                options=["1", "2"],
                                format_func=lambda x: {
                                                        "1": " Biopsy",
                                                        "2": " Imaging",
                                                    }[x],
                                help="Select Diagnosis Method",
                                index=["1", "2"].index(df.iloc[0]["CIRDX_METHOD"]) if df.iloc[0]["CIRDX_METHOD"] else None,  # No default selection
                                placeholder="Choose an option",
                            ) 
                            Cirrhosis_Dx_HPI_EMR_Note_Free_Text = st.text_area(
                                "Cirrhosis_Dx_HPI EMR Note Free Text [ Excel : CIRDX_HPIFT ]",
                                value = df.iloc[0]["CIRDX_HPIFT"],
                                help="Provide details of HPI EMR"
                            )
                            Cirrhosis_Dx_Imaging_Findings_EMR_Note_Free_Text = st.text_area(
                                "Cirrhosis_Dx_Imaging Findings EMR Note Free Text [ Excel : CIRDX_IMAGEFT ]",
                                value = df.iloc[0]["CIRDX_IMAGEFT"],
                                help="Provide details of Imaging Findings"
                            )

                            Cirrhosis_Dx_Metavir_Score = st.selectbox (
                                "Cirrhosis_Dx_Metavir Score [ Excel : CIRDX_METAVIR ]  ",
                                options=["F0/F1", "F2","F3","F4","NA"],
                                help="Select Metavir_score",
                                index=["F0/F1", "F2","F3","F4","NA"].index(df.iloc[0]["CIRDX_METAVIR"]) if df.iloc[0]["CIRDX_METAVIR"] else None,  # No default selection
                                placeholder="Choose an option",
                            ) 
                            complications = df.loc[df["MRN"] == mrn, "CIRDX_COMPLDX"].values[0]
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
                            "Cirrhosis_Dx_Complications at Time of Diagnosis [ Excel : CIRDX_COMPLDX ] ",
                                options=["ascites", "ariceal hemorrhage", "Hepatic encephalopathy", "jaundice", "SBP", "Hepatorenal Syndrome", "Coagulopathy", "Portal HTN", "PVT", "PVTT", "Portal Vein Thrombosis", "none"],
                                help="Provide details of Compilications at time of Diagnosis",
                                default=complications_list,
                                placeholder="Select all that apply"
                            )
                            Cirrhosis_Dx_Complications_at_Time_of_Diagnosis_String = ", ".join(Cirrhosis_Dx_Complications_at_Time_of_Diagnosis)

                            Cirrhosis_Dx_Complications_at_Time_of_Diagnosis_Binary = 1 if Cirrhosis_Dx_Complications_at_Time_of_Diagnosis != "none" or Cirrhosis_Dx_Complications_at_Time_of_Diagnosis != None else 0

                            Cirrhosis_Dx_Complications_Free_Text =  st.text_area(
                                "Cirrhosis_Dx_Complications Free Text [ Excel : CIRDX_COMPLFT ]",
                                value = df.iloc[0]["CIRDX_COMPLFT"],
                                help="Provide details of Complications"
                            )
                            if df.iloc[0]["CIRDX_DATELABS"]:
                                Cirdx_Dxdate_value = datetime.strptime(df.iloc[0]["CIRDX_DATELABS"], "%Y-%m-%d").date()
                            else:
                                Cirdx_Dxdate_value = None 

                            Cirrhosis_Dx_Date_of_Labs_in_Window = st.date_input(" Cirrhosis_Dx_Date of Labs in Window [ Excel : CIRDX_DATELABS ]", value =Cirdx_Dxdate_value)

                            Cirrhosis_Dx_AFP = st.text_input(
                                "Cirrhosis_Dx_AFP [ Excel : CIRDX_AFP ]",
                                value = df.iloc[0]["CIRDX_AFP"],
                                help="Enter AFP value in ng/dl"
                                
                            )

                            Cirrhosis_Dx_AFP_L3 = st.text_input(
                                "Cirrhosis_Dx_AFP L3 [ Excel : CIRDX_AFPL3 ]",
                                value = df.iloc[0]["CIRDX_AFPL3"],
                                help="Enter AFP_L3 value in ng/dl"
                                
                            )
                            Cirrhosis_Dx_AFP_L3_Date_Free_Text = st.text_area("Cirrhosis_Dx_AFP L3 Date Free Text [ Excel : CIRDX_AFPL3DATEFT ]",value = df.iloc[0]["CIRDX_AFPL3DATEFT"])

                            Cirrhosis_Dx_Ascites_CTCAE = st.selectbox (
                                "Cirrhosis_Dx_Ascites CTCAE [ Excel : CIRDX_ASCITCTCAE ]",
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
                                index=["none", "Asymptomatic","Minimal ascities/Mild abd distension","Symptomatic","moderate ascities/Symptomatic medical intervention", "Severe symptoms, invasive intervention indicated", "Life Threatening: Urgent operation intervention indicated"].index(df.iloc[0]["CIRDX_ASCITCTCAE"]) if df.iloc[0]["CIRDX_ASCITCTCAE"] else None,  # No default selection
                                placeholder="Choose an option",
                            ) 
                            def findascitesclass(score):
                                if score == "Asymptomatic" or score== "Minimal ascities/Mild abd distension":
                                    return 1
                                elif score == "Symptomatic" or score == "moderate ascities/Symptomatic medical intervention":
                                    return 2
                                elif score == "Severe symptoms, invasive intervention indicated" or score == "Life Threatening: Urgent operation intervention indicated" :
                                    return 3
                            
                            Cirrhosis_Dx_Ascites_Classification = 0 if Cirrhosis_Dx_Ascites_CTCAE == "none" else findascitesclass(Cirrhosis_Dx_Ascites_CTCAE)
                            st.write("Cirdx_AscitesCTCAEnumb ",Cirrhosis_Dx_Ascites_Classification)
                            Cirrhosis_Dx_Ascites_Free_Text = "NA" if Cirrhosis_Dx_Ascites_CTCAE == "none" else st.text_area(
                                "Cirrhosis_Dx_Ascites Free Text [ Excel : CIRDX_ASCITFT ]",
                                value = df.iloc[0]["CIRDX_ASCITFT"]
                            
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
                                    "CIRPMH_HBV" : cir_pmh_hbv_status,
                                    "CIRPMH_HBVFT" : cir_pmh_hbv_free_text,
                                    "CIRPMH_HBVART" : cir_pmh_hbv_art,
                                    "CIRPMH_HCV" : cir_pmh_hcv_status,
                                    "CIRPMH_HCVFT" : cir_pmh_hcv_free_text,
                                    "CIRPMH_HCVART" : cir_pmh_hcv_art,
                                    "CIRPMH_AUD" : cir_pmh_alcohol_use_disorder,
                                    "CIRPMH_AUDFT" : cir_pmh_alcohol_free_text,
                                    "CIRPMH_IVDU" : cir_pmh_ivdu_status,
                                    "CIRPMH_IVDUFT" : cir_pmh_ivdu_free_text,
                                    "CIRPMH_LIVERFAC" : cir_pmh_liver_addtional_factor,
                                    "CIRDX_DATE" : Cirrhosis_Dx_Diagnosis_Date,
                                    "CIRDX_METHOD" : Cirrhosis_Dx_Diagnosis_Method,
                                    "CIRDX_HPIFT" : Cirrhosis_Dx_HPI_EMR_Note_Free_Text,
                                    "CIRDX_IMAGEFT" : Cirrhosis_Dx_Imaging_Findings_EMR_Note_Free_Text,
                                    "CIRDX_METAVIR" : Cirrhosis_Dx_Metavir_Score,
                                    "CIRDX_COMPLDX" : Cirrhosis_Dx_Complications_at_Time_of_Diagnosis_String,
                                    "CIRDX_COMPLDXBIN" : Cirrhosis_Dx_Complications_at_Time_of_Diagnosis_Binary,
                                    "CIRDX_COMPLFT" : Cirrhosis_Dx_Complications_Free_Text,
                                    "CIRDX_DATELABS" : Cirrhosis_Dx_Date_of_Labs_in_Window,
                                    "CIRDX_AFP" : Cirrhosis_Dx_AFP,
                                    "CIRDX_AFPL3" : Cirrhosis_Dx_AFP_L3,
                                    "CIRDX_AFPL3DATEFT" : Cirrhosis_Dx_AFP_L3_Date_Free_Text,
                                    "CIRDX_ASCITCTCAE" : Cirrhosis_Dx_Ascites_CTCAE,
                                    "CIRDX_ASCITNUMB" : Cirrhosis_Dx_Ascites_Classification,
                                    "CIRDX_ASCITFT" : Cirrhosis_Dx_Ascites_Free_Text,
                                    }
                                    
                                update_google_sheet(data2, mrn)

                    elif st.session_state.selected_tab == "HCC Diagnosis":
                        st.subheader("HCC Diagnosis")
                        with st.form("hcc_dx_form"):

                            hcc_dx_hcc_diagnosis_date = st.date_input("HCC_Dx_HCC Diagnosis Date", help="Enter the HCC diagnosis date",value = datetime.strptime(df.iloc[0]["HCCDX_DATEDX"], "%Y-%m-%d").date() if df.iloc[0]["HCCDX_DATEDX"] else None)

                            hcc_dx_method_of_diagnosis = st.selectbox(
                                 "HCC_Dx_Method of Diagnosis [ Excel : HCCDX_METHODDX ]\n\n(1) Biopsy, (2) Imaging, (NA) Unknown",   
                             options=["1", "2", "NA"],
                                format_func=lambda x: {
                                    "1": "Biopsy ",
                                    "2": "Imaging ",
                                    "NA": "Unknown ",
                                }[x],
                                index=["1", "2", "NA"].index(df.iloc[0]["HCCDX_METHODDX"]) if df.iloc[0]["HCCDX_METHODDX"] else None, 
                                placeholder="Choose an option",
                                
                            )

                            hcc_dx_date_of_labs = st.date_input("HCC_Dx_Date of Labs in Window",value=datetime.strptime(df.iloc[0]["HCCDX_LABSDATE"], "%Y-%m-%d").date() if df.iloc[0]["HCCDX_LABSDATE"] else None)

                            hcc_dx_afp = st.number_input("HCC_Dx_AFP",step=0.1, help="Enter AFP value in ng/dl",value = float(df.iloc[0]["HCCDX_AFP"]) if pd.notnull(df.iloc[0]["HCCDX_AFP"]) and str(df.iloc[0]["HCCDX_AFP"]).isdigit() else 0.0 )

                            hcc_dx_afp_l3 = st.number_input("HCC_Dx_AFP L3",step=0.1, help="Enter AFP L3 and date details",value = float(df.iloc[0]["HCCDX_AFPL3"]) if pd.notnull(df.iloc[0]["HCCDX_AFPL3"]) and str(df.iloc[0]["HCCDX_AFPL3"]).isdigit() else 0.0)
                            hcc_dx_afp_l3_date_free_text = st.text_area("HCC_Dx_AFP L3 Date Free Text",value = df.iloc[0]["HCCDX_AFPL3dateFT"])

                            hcc_dx_bilirubin = st.number_input("HCC_Dx_Bilirubin",step=0.1, help="Enter the bilirubin value in mg/dl", min_value=1.0,value = float(df.iloc[0]["HCCDX_BILI"]) if pd.notnull(df.iloc[0]["HCCDX_BILI"]) and str(df.iloc[0]["HCCDX_BILI"]).isdigit() else 1.0)
                            hcc_dx_albumin = st.number_input("HCC_Dx_Albumin",step=0.1, help="Enter the albumin value in g/dl",value = float(df.iloc[0]["HCCDX_ALBUMIN"]) if pd.notnull(df.iloc[0]["HCCDX_ALBUMIN"]) and str(df.iloc[0]["HCCDX_ALBUMIN"]).isdigit() else 0.0)
                            hcc_dx_inr = st.number_input("HCC_Dx_INR",step=0.1, help="Enter the INR value", value = float(df.iloc[0]["HCCDX_INR"]) if pd.notnull(df.iloc[0]["HCCDX_INR"]) and str(df.iloc[0]["HCCDX_INR"]).isdigit() else 0.0)
                            hcc_dx_creatinine = st.number_input("HCC_Dx_Creatinine",step=0.1, help="Enter the creatinine value in mg/dl", value = float(df.iloc[0]["HCCDX_CREATININE"]) if pd.notnull(df.iloc[0]["HCCDX_CREATININE"]) and str(df.iloc[0]["HCCDX_CREATININE"]).isdigit() else 0.0)
                            hcc_dx_sodium = st.number_input("HCC_Dx_Sodium",step=0.1, help="Enter the sodium value in mmol/L", value = float(df.iloc[0]["HCCDX_SODIUM"]) if pd.notnull(df.iloc[0]["HCCDX_SODIUM"]) and str(df.iloc[0]["HCCDX_SODIUM"]).isdigit() else 0.0)

                            hcc_dx_ascites_CTCAE = st.selectbox (
                                "HCC_Dx_Ascites CTCAE [ Excel : HCCDX_ASCITCTCAE ] ",
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
                                index=["none", "Asymptomatic","Minimal ascities/Mild abd distension","Symptomatic","moderate ascities/Symptomatic medical intervention", "Severe symptoms, invasive intervention indicated", "Life Threatening: Urgent operation intervention indicated"].index(df.iloc[0]["HCCDX_ASCITCTCAE"]) if df.iloc[0]["HCCDX_ASCITCTCAE"] else None,
                                placeholder="Choose an option",
                            ) 
                            def findascitesclass(score):
                                if score == "Asymptomatic" or score== "Minimal ascities/Mild abd distension":
                                    return 1
                                elif score == "Symptomatic" or score == "moderate ascities/Symptomatic medical intervention":
                                    return 2
                                elif score == "Severe symptoms, invasive intervention indicated" or score == "Life Threatening: Urgent operation intervention indicated" :
                                    return 3
                            
                            hCC_dx_ascites_classification = 1 if hcc_dx_ascites_CTCAE == "none" else findascitesclass(hcc_dx_ascites_CTCAE)
                            st.write("HCCdx_AscitesCTCAEnumb : ",hCC_dx_ascites_classification)

                            hcc_dx_ascites_diruetics = 0 if hcc_dx_ascites_CTCAE == "none" else st.selectbox(
                                "HCC_Dx_Ascites Diruetics [ Excel : HCCDX_ASCITDIUR ]\n\nYes(1), No(0)",
                             options=["1", "0"],
                            format_func=lambda x: {
                                "1": "Yes ",
                                "0": "No ",
                            }[x],
                                index=["1","0"].index(df.iloc[0]["HCCDX_ASCITDIUR"]) if df.iloc[0]["HCCDX_ASCITDIUR"] else None,  # No default selection
                                placeholder="Choose an option",
                
                            )
                            hcc_dx_ascites_paracentesis = 0 if hcc_dx_ascites_CTCAE == "none" else st.selectbox(
                                "HCC_Dx_Ascites Paracentesis  [ Excel : HCCDX_ASCITPARA ]\n\nYes(1), No(0)  ",
                             options=["1", "0"],
                            format_func=lambda x: {
                                "1": "Yes ",
                                "0": "No ",
                            }[x],
                                index= ["1","0"].index(df.iloc[0]["HCCDX_ASCITPARA"]) if df.iloc[0]["HCCDX_ASCITPARA"] else None,
                                placeholder="Choose an option",
                
                            )
                            hcc_dx_ascites_hospitalization = 0 if hcc_dx_ascites_CTCAE == "none" else st.selectbox(
                                "HCC_Dx_Ascites Hospitalization [ Excel : HCCDX_ASCITHOSP ]\n\nYes(1), No(0)",
                             options=["1", "0"],
                            format_func=lambda x: {
                                "1": "Yes ",
                                "0": "No ",
                            }[x],
                                index=["1","0"].index(df.iloc[0]["HCCDX_ASCITHOSP"]) if df.iloc[0]["HCCDX_ASCITHOSP"] else None,
                                placeholder="Choose an option",
                
                            )
                            hcc_dx_he_grade = st.selectbox(
                                "HCC_Dx_HE Grade [ Excel : HCCDX_HEGRADE ]\n\n(1) None, (2) Grade 1-2, (3) Grade 3-4   ",
                                options=[1,2,3],
                                format_func=lambda x: {
                                1: "None",
                                2: "Grade 1-2",
                                3: "Grade 3-4",
                                
                            }[x],
                                index=[1,2,3].index(int(df.iloc[0]["HCCDX_HEGRADE"])) if df.iloc[0]["HCCDX_HEGRADE"] else None,  
                                placeholder="Choose an option",

                            )
                            hcc_dx_ecog_performance_status = st.selectbox("HCC_Dx_ECOG Performance Status [ Excel : HCCDX_ECOG ]  ", options=["0", "1", "2", "3", "4", "NA"],
                                index=["0", "1", "2", "3", "4", "NA"].index(df.iloc[0]["HCCDX_ECOG"]) if df.iloc[0]["HCCDX_ECOG"] else None,  
                                placeholder="Choose an option",)

                            hcc_dx_lirads_score = st.selectbox(
                                "HCC_Dx_LIRADS Score  [ Excel : HCCDX_LIRADS ]",
                                options=["LR-1", "LR-2", "LR-3", "LR-4", "LR-5", "LR-5V", "LR-M"],
                                index=["LR-1", "LR-2", "LR-3", "LR-4", "LR-5", "LR-5V", "LR-M"].index(df.iloc[0]["HCCDX_LIRADS"]) if df.iloc[0]["HCCDX_LIRADS"] else None, 
                                placeholder="Choose an option",
                            )
                            hcc_dx_child_pugh_points_calc = calculatepoints(hcc_dx_bilirubin,hcc_dx_albumin,hcc_dx_inr,hCC_dx_ascites_classification,hcc_dx_he_grade)
                            st.write("HCCdx_CPcalc ",hcc_dx_child_pugh_points_calc)
                            hcc_dx_child_pugh_class_calc = calculate_class(hcc_dx_child_pugh_points_calc)
                            st.write("HCCdx_CPclass ",hcc_dx_child_pugh_class_calc)
                            hcc_dx_meld_score_calc = meld_calc(hcc_dx_creatinine,hcc_dx_bilirubin,hcc_dx_inr)
                            st.write("HCCdx_MELD ",hcc_dx_meld_score_calc)
                            hcc_dx_meld_na_score_calc = hcc_dx_meld_score_calc + 1.32*(137-int(hcc_dx_sodium)) - (0.033*hcc_dx_meld_score_calc*(137-int(hcc_dx_sodium)))
                            st.write("HCCdx_MELDNa ",hcc_dx_meld_na_score_calc)
                            
                            hcc_dx_albi_score_calc = albi_calc(hcc_dx_bilirubin, hcc_dx_albumin)
                            st.write("HCCdx_Albiscore ",hcc_dx_albi_score_calc)
                            hcc_dx_albi_grade = albi_class(hcc_dx_albi_score_calc)
                            st.write("HCCdx_Albigrade ",hcc_dx_albi_grade)

                            hcc_dx_bclc_calc = st.selectbox("HCC_Dx_BCLC Stage calc [ Excel : HCCDX_BCLC ]\n\n(NA) Not in chart, (0) Stage 0, (1) Stage A, (2) Stage B, (3) Stage C, (4) Stage D  ",
                                    options=["NA", "0", "1", "2", "3", "4"],
                                format_func=lambda x: {
                                    "NA": " Not in chart",
                                    "0": " Stage 0: Very early stage, with a single nodule smaller than 2 cm in diameter",
                                    "1": " Stage A: Early stage, with one nodule smaller than 5 cm or up to three nodules smaller than 3 cm",
                                    "2": " Stage B: Intermediate stage, with multiple tumors in the liver",
                                    "3": " Stage C: Advanced stage, with cancer that has spread to other organs or blood vessels",
                                    "4": " Stage D: End-stage disease, with severe liver damage or the patient is very unwell",
                                }[x],index=["NA", "0", "1", "2", "3", "4"].index(df.iloc[0]["HCCDX_BCLC"]) if df.iloc[0]["HCCDX_BCLC"] else None, 
                                placeholder="Choose an option",)
                            
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
                                    "HCCDX_DATEDX": hcc_dx_hcc_diagnosis_date_formatted,
                                    "HCCDX_METHODDX": hcc_dx_method_of_diagnosis,
                                    "HCCDX_LABSDATE": hcc_dx_date_of_labs_date_formattes,
                                    "HCCDX_AFP": hcc_dx_afp,
                                    "HCCDX_AFPL3": hcc_dx_afp_l3,
                                    "HCCDX_AFPL3dateFT": hcc_dx_afp_l3_date_free_text,
                                    "HCCDX_BILI": hcc_dx_bilirubin,
                                    "HCCDX_ALBUMIN": hcc_dx_albumin,
                                    "HCCDX_INR": hcc_dx_inr,
                                    "HCCDX_CREATININE": hcc_dx_creatinine,
                                    "HCCDX_SODIUM": hcc_dx_sodium,
                                    "HCCDX_ASCITCTCAE": hcc_dx_ascites_CTCAE,
                                    "HCCDX_ASCITNUMB": hCC_dx_ascites_classification,
                                    "HCCDX_ASCITDIUR": hcc_dx_ascites_diruetics,
                                    "HCCDX_ASCITPARA": hcc_dx_ascites_paracentesis,
                                    "HCCDX_ASCITHOSP": hcc_dx_ascites_hospitalization,
                                    "HCCDX_HEGRADE": hcc_dx_he_grade,
                                    "HCCDX_ECOG": hcc_dx_ecog_performance_status,
                                    "HCCDX_LIRADS": hcc_dx_lirads_score,
                                    "HCCDX_CPCALC": hcc_dx_child_pugh_points_calc,
                                    "HCCDX_CPCLASS": hcc_dx_child_pugh_class_calc,
                                    "HCCDX_MELD": hcc_dx_meld_score_calc,
                                    "HCCDX_MELDNA": hcc_dx_meld_na_score_calc,
                                    "HCCDX_ALBISCORE": hcc_dx_albi_score_calc,
                                    "HCCDX_ALBIGRADE": hcc_dx_albi_grade,
                                    "HCCDX_BCLC": hcc_dx_bclc_calc,
                                }
                                
                                update_google_sheet(data4, mrn)
            
                    elif st.session_state.selected_tab == "Previous Therapy for HCC":
                        st.subheader("Previous Therapy for HCC")
                        with st.form("previous_therapy_form"):
                            
                            PRVTHER_Prior_LDT_Therapy = st.selectbox(
                                "PRVTHER_Prior_LDT_Therapy [ Excel : PTHER_LDT ]\n\nNo (0), Yes (1), NA ",
                                options=["0", "1", "NA"], 
                                format_func=lambda x: {
                                    "0": "No",
                                    "1": "Yes",
                                    "NA": "NA (not in chart)"
                                }[x],
                            index=["0", "1", "NA"].index(df.iloc[0]["PTHER_LDT"]) if df.iloc[0]["PTHER_LDT"] else None,  
                            placeholder="Choose an option",
                            )
                            
                            PRVTHER_Prior_RFA_Therapy = st.selectbox(
                                "PRVTHER_Prior RFA Therapy [ Excel : PTHER_RFA ]\n\nNo (0), Yes (1), NA ",
                                options=["0", "1", "NA"], 
                                format_func=lambda x: {
                                    "0": "No",
                                    "1": "Yes",
                                    "NA": "NA"
                                }[x],
                                index=["0", "1", "NA"].index(df.iloc[0]["PTHER_RFA"]) if df.iloc[0]["PTHER_RFA"] else None,
                                placeholder="Choose an option",
                            )
                            PRVTHER_Prior_RFA_Date = 0 if PRVTHER_Prior_RFA_Therapy == '0' else st.date_input("PRVTHER_Prior RFA Date",value=datetime.strptime(df.iloc[0]["PTHER_RFADATE"], "%Y-%m-%d").date() if df.iloc[0]["PTHER_RFADATE"] else None)
                        
                            PRVTHER_Prior_TARE_Therapy = st.selectbox(
                                "PRVTHER_Prior TARE Therapy [ Excel : PTHER_TARE ]\n\nNo (0), Yes (1), NA ",
                                    options=["0", "1", "NA"], 
                                format_func=lambda x: {
                                    "0": "No",
                                    "1": "Yes",
                                    "NA": "NA (not in chart)"
                                }[x],
                                index=["0", "1", "NA"].index(df.iloc[0]["PTHER_TARE"]) if df.iloc[0]["PTHER_TARE"] else None, 
                                placeholder="Choose an option",
                            )
                            PRVTHER_Prior_TARE_Date = 0 if PRVTHER_Prior_TARE_Therapy == '0' else st.date_input("PRVTHER_Prior TARE Date",value=datetime.strptime(df.iloc[0]["PTHER_TAREDATE"], "%Y-%m-%d").date() if df.iloc[0]["PTHER_TAREDATE"] else None)
                        
                            PRVTHER_Prior_SBRT_Therapy = st.selectbox(
                                "PRVTHER_Prior SBRT Therapy [ Excel : PTHER_SBRT ]\n\nNo (0), Yes (1), NA ",
                                    options=["0", "1", "NA"], 
                                format_func=lambda x: {
                                    "0": "No",
                                    "1": "Yes",
                                    "NA": "NA (not in chart)"
                                }[x],
                                index=["0", "1", "NA"].index(df.iloc[0]["PTHER_SBRT"]) if df.iloc[0]["PTHER_SBRT"] else None,  
                                placeholder="Choose an option",
                            )
                            
                            PRVTHER_Prior_SBRT_Date = 0 if PRVTHER_Prior_SBRT_Therapy == '0' else st.date_input("PRVTHER_Prior SBRT Date",value=datetime.strptime(df.iloc[0]["PTHER_SBRTDATE"], "%Y-%m-%d").date() if df.iloc[0]["PTHER_SBRTDATE"] else None)
                        
                            PRVTHER_Prior_TACE_Therapy = st.selectbox(
                               "PRVTHER_Prior TACE Therapy [ Excel : PTHER_TACE ]\n\nNo (0), Yes (1), NA ",
                                    options=["0", "1", "NA"], 
                                format_func=lambda x: {
                                    "0": "No",
                                    "1": "Yes",
                                    "NA": "NA (not in chart)"
                                }[x],
                                index=["0", "1", "NA"].index(df.iloc[0]["PTHER_TACE"]) if df.iloc[0]["PTHER_TACE"] else None,
                                placeholder="Choose an option",
                            )
                            
                            PRVTHER_Prior_TACE_Date = 0 if PRVTHER_Prior_TACE_Therapy == '0' else st.date_input("PRVTHER_Prior TACE Date",value=datetime.strptime(df.iloc[0]["PTHER_TACEDATE"], "%Y-%m-%d").date() if df.iloc[0]["PTHER_TACEDATE"] else None)

                            PRVTHER_Prior_MWA_Therapy = st.selectbox(
                               "PRVTHER_Prior MWA Therapy [ Excel : PTHER_MWA ]\n\nNo (0), Yes (1), NA ",
                                    options=["0", "1", "NA"], 
                                format_func=lambda x: {
                                    "0": "No",
                                    "1": "Yes",
                                    "NA": "NA (not in chart)"
                                }[x],
                                index=["0", "1", "NA"].index(df.iloc[0]["PTHER_MWA"]) if df.iloc[0]["PTHER_MWA"] else None, 
                                placeholder="Choose an option",
                            )
                            PRVTHER_Prior_MWA_Date = 0 if PRVTHER_Prior_MWA_Therapy == '0' else st.date_input("PRVTHER_Prior MWA Date",value=datetime.strptime(df.iloc[0]["PTHER_MWADATE"], "%Y-%m-%d").date() if df.iloc[0]["PTHER_MWADATE"] else None)

                            PRVTHER_Resection = st.selectbox(
                               "PRVTHER_Resection [ Excel : PTHER_RESECTION ]\n\nNo (0), Yes (1), NA ",
                                    options=["0", "1", "NA"], 
                                format_func=lambda x: {
                                    "0": "No",
                                    "1": "Yes",
                                    "NA": "NA (not in chart)"
                                }[x],
                                index=["0", "1", "NA"].index(df.iloc[0]["PTHER_RESECTION"]) if df.iloc[0]["PTHER_RESECTION"] else None, 
                                placeholder="Choose an option",
                            )
                            PRVTHER_Resection_Date = 0 if PRVTHER_Resection == "0" else st.date_input("PRVTHER_Resection Date",value=datetime.strptime(df.iloc[0]["PTHER_RESECTIONDATE"], "%Y-%m-%d").date() if df.iloc[0]["PTHER_RESECTIONDATE"] else None)


                            list1=[PRVTHER_Prior_LDT_Therapy, PRVTHER_Prior_RFA_Therapy, PRVTHER_Prior_TARE_Therapy, PRVTHER_Prior_SBRT_Therapy, PRVTHER_Prior_TACE_Therapy, PRVTHER_Prior_MWA_Therapy, PRVTHER_Resection ]
                            total_sum=0
                            for item in list1:
                                if item == "Yes" :
                                    total_sum+=1
                                else:
                                    continue
                            
                            PRVTHER_Previous_Therapy_Sum = total_sum
                            st.write("PRVTHER_Prevtxsum ",PRVTHER_Previous_Therapy_Sum)
                        # PRVTHER_Previous_Therapy_Sum = PRVTHER_Prior_LDT_Therapy + PRVTHER_Prior_RFA_Therapy + PRVTHER_Prior_TARE_Therapy + PRVTHER_Prior_SBRT_Therapy + PRVTHER_Prior_TACE_Therapy + PRVTHER_Prior_MWA_Therapy

                            PRVTHER_NotesFT = st.text_area(
                            "PRVTHER_NotesFT",  value=df.iloc[0]["PTHER_NOTESFT"]
                        
                            )

                            PRVTHER_Total_Recurrences_HCC = st.text_area(
                                "PRVTHER_Total Recurrences HCC", value=df.iloc[0]["PTHER_TOTRECUR"]
                            )
                            PRVTHER_Location_of_Previous_Treatment_segments = st.selectbox(
                                "PRVTHER_Location of Previous Treatment Segments [Excel : PTHER_PREVSEGMENT]",
                                options=["1","2","3","4a","4b","5","6","7","8","NA"],
                                index=["1","2","3","4a","4b","5","6","7","8","NA"].index(df.iloc[0]["PTHER_PREVSEGMENT"]) if df.iloc[0]["PTHER_PREVSEGMENT"] else None,
                                placeholder="Choose an option"
                            )
                            PRVTHER_Location_of_Previous_Tx_segments_ft = st.text_area(
                                "PRVTHER_Location of Previous Tx Segments FT",  value=df.iloc[0]["PTHER_PREVSEGMENTFT"]
                            
                            )
                            PRVTHER_recurrence_location_note = st.selectbox(
                                "PRVTHER_Recurrence Location Note [Excel : PTHER_RECURSEGMENTFT]",
                                options=["1","2","3","4a","4b","5","6","7","8","NA"],
                                index=["1","2","3","4a","4b","5","6","7","8","NA"].index(df.iloc[0]["PTHER_RECURSEGMENTFT"]) if df.iloc[0]["PTHER_RECURSEGMENTFT"] else None,
                                placeholder="Choose an option"
                            )
                            PRVTHER_recurrence_date = st.text_area(
                                "PRVTHER_Recurrence Date", value=df.iloc[0]["PTHER_RECURDATE"],
                            
                            )
                            PRVTHER_recurrence_seg =  st.text_input(
                                "PRVTHER_Recurrence Seg" , value=df.iloc[0]["PTHER_RECURSEGMENT"]
                            )
                            PRVTHER_New_HCC_Outside_Previous_Treatment_Site = st.selectbox(
                                "PRVTHER_New HCC Outside Previous Treatment Site [ Excel : PTHER_NEWHCCOUT ]\n\nNo (0), Yes (1), NA",
                                    options=["0", "1", "NA"], 
                                format_func=lambda x: {
                                    "0": "No ",
                                    "1": "Yes ",
                                    "NA": "NA (not in chart)"
                                }[x],
                                help = "new HCC occurrence that has developed in a diff location in the liver, separate from the area that was previously tx",
                                index=["0", "1", "NA"].index(df.iloc[0]["PTHER_NEWHCCOUT"]) if df.iloc[0]["PTHER_NEWHCCOUT"] else None,
                                placeholder="Choose an option"
                            )   
                            PRVTHER_New_HCC_Adjacent_to_Previous_Treatment_Site = st.selectbox(
                                "PRVTHER_New HCC Adjacent to Previous Treatment Site [ Excel : PTHER_NEWHCCADJ ]\n\nNo (0), Yes (1), NA ",
                                    options=["0", "1", "NA"], 
                                format_func=lambda x: {
                                    "0": "No ",
                                    "1": "Yes ",
                                    "NA": "NA (not in chart)"
                                }[x],
                                help = "New HCC adjacent to previous treatment site: new HCC occurrence that has developed close to, but not directly in, the area that was previously treated",
                                index=["0", "1", "NA"].index(df.iloc[0]["PTHER_NEWHCCADJ"]) if df.iloc[0]["PTHER_NEWHCCADJ"] else None,
                                placeholder="Choose an option"
                            )   
                            PRVTHER_Residual_HCC_Note = st.text_area(
                                "PRVTHER_Residual HCC Note",
                                help="Provide information of Residual HCC",
                                value = df.iloc[0]["PTHER_RESIDUALHCCFT"]
                            ) 
                            PRVTHER_Residual_HCC = st.selectbox(
                                "PRVTHER_Residual HCC [ Excel : PTHER_RESIDUALHCC ]\n\nNo (0), Yes (1), NA ",
                                    options=["0", "1", "NA"], 
                                format_func=lambda x: {
                                    "0": "No ",
                                    "1": "Yes ",
                                    "NA": "NA (not in chart)"
                                }[x],
                                index=["0", "1", "NA"].index(df.iloc[0]["PTHER_RESIDUALHCC"]) if df.iloc[0]["PTHER_RESIDUALHCC"] else None,
                                placeholder="Choose an option"
                            )   

                            PRVTHER_Systemic_Therapy_Free_Text = st.selectbox(
                                "PRVTHER_Systemic Therapy Free Text [ Excel : PTHER_SYSTHER ]\n\nNo (0), Yes (1), NA",
                                options=["0", "1", "NA"], 
                                format_func=lambda x: {
                                    "0": "No ",
                                    "1": "Yes ",
                                    "NA": "NA (not in chart)"
                                }[x],
                                index=["0", "1", "NA"].index(df.iloc[0]["PTHER_SYSTHER"]) if df.iloc[0]["PTHER_SYSTHER"] else None, 
                                placeholder="Choose an option",
                            )

                            PRVTHER_Date_of_Labs_in_Window = st.date_input(
                                "PRVTHER_Date of Labs for AFP",
                                help="select date of labs in window",
                                value=datetime.strptime(df.iloc[0]["PTHER_AFPDATE"], "%Y-%m-%d").date() if df.iloc[0]["PTHER_AFPDATE"] else None
                            )

                            PRVTHER_AFP = st.number_input(
                                "PRVTHER_AFP",
                                help="Enter AFP value in ng/dl or NA",step=0.1,
                                value=float(df.iloc[0]["PTHER_AFP"]) if pd.notnull(df.iloc[0]["PTHER_AFP"]) and str(df.iloc[0]["PTHER_AFP"]).isdigit() else 0.0
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
                                "PTHER_LDT": PRVTHER_Prior_LDT_Therapy,
                                "PTHER_RFA": PRVTHER_Prior_RFA_Therapy,
                                "PTHER_RFADATE": PRVTHER_Prior_RFA_Date,
                                "PTHER_TARE": PRVTHER_Prior_TARE_Therapy,
                                "PTHER_TAREDATE": PRVTHER_Prior_TARE_Date,
                                "PTHER_SBRT": PRVTHER_Prior_SBRT_Therapy,
                                "PTHER_SBRTDATE": PRVTHER_Prior_SBRT_Date,
                                "PTHER_TACE": PRVTHER_Prior_TACE_Therapy,
                                "PTHER_TACEDATE": PRVTHER_Prior_TACE_Date,
                                "PTHER_MWA": PRVTHER_Prior_MWA_Therapy,
                                "PTHER_MWADATE": PRVTHER_Prior_MWA_Date,
                                "PTHER_RESECTION": PRVTHER_Resection,
                                "PTHER_RESECTIONDATE": PRVTHER_Resection_Date,
                                "PTHER_PREVSUM": PRVTHER_Previous_Therapy_Sum,
                                "PTHER_NOTESFT": PRVTHER_NotesFT,
                                "PTHER_TOTRECUR": PRVTHER_Total_Recurrences_HCC,
                                "PTHER_PREVSEGMENT": PRVTHER_Location_of_Previous_Treatment_segments,
                                "PTHER_PREVSEGMENTFT": PRVTHER_Location_of_Previous_Tx_segments_ft,
                                "PTHER_RECURSEGMENTFT": PRVTHER_recurrence_location_note,
                                "PTHER_RECURDATE": PRVTHER_recurrence_date,
                                "PTHER_RECURSEGMENT": PRVTHER_recurrence_seg,
                                "PTHER_NEWHCCOUT": PRVTHER_New_HCC_Outside_Previous_Treatment_Site,
                                "PTHER_NEWHCCADJ": PRVTHER_New_HCC_Adjacent_to_Previous_Treatment_Site,
                                "PTHER_RESIDUALHCCFT": PRVTHER_Residual_HCC_Note,
                                "PTHER_RESIDUALHCC": PRVTHER_Residual_HCC,
                                "PTHER_SYSTHER": PRVTHER_Systemic_Therapy_Free_Text,
                                "PTHER_AFPDATE": PRVTHER_Date_of_Labs_in_Window,
                                "PTHER_AFP": PRVTHER_AFP,
                                }
                                update_google_sheet(data5, mrn)
                
                    elif st.session_state.selected_tab == "Pre Y90":
                        st.subheader("Pre Y90")
                        with st.form("pre_y90_form"):
                            #mrn = int(mrn)
                            prey90_sx = df.loc[df["MRN"] == mrn, "PREY_SX"].values[0]
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
                            "PREY90_symptoms [Excel : PREY_SX]",
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
                            prey90_date_of_labs = st.date_input("PREY90_date of labs in window", help="Enter the date of lab tests",value = datetime.strptime(df.iloc[0]["PREY_DATELABS"], "%Y-%m-%d").date() if df.iloc[0]["PREY_DATELABS"] else None)
                            prey90_afp = st.text_input("PREY90_AFP", help="Enter AFP value in ng/dl or NA",value = df.iloc[0]["PREY_AFP"])
                            
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
                            
                            prey90_bilirubin = st.number_input("PREY90_Bilirubin",step=0.1,min_value=1.0,value = float(df.iloc[0]["PREY_BILI"]) if pd.notnull(df.iloc[0]["PREY_BILI"]) and str(df.iloc[0]["PREY_BILI"]).isdigit() else 1.0)
                            prey90_albumin = st.number_input("PREY90_Albumin",step=0.1, help="Enter the albumin value in g/dl",value = float(df.iloc[0]["PREY_ALBUMIN"]) if pd.notnull(df.iloc[0]["PREY_ALBUMIN"]) and str(df.iloc[0]["PREY_ALBUMIN"]).isdigit() else 0.0)
                            prey90_inr = st.number_input("PREY90_inr",step=0.1, help="Enter the INR value",value = float(df.iloc[0]["PREY_INR"]) if pd.notnull(df.iloc[0]["PREY_INR"]) and str(df.iloc[0]["PREY_INR"]).isdigit() else 0.0)
                            prey90_creatinine = st.number_input("PREY90_creatinine",step=0.1, help="Enter the creatinine value in mg/dl",value = float(df.iloc[0]["PREY_CREATININE"]) if pd.notnull(df.iloc[0]["PREY_CREATININE"]) and str(df.iloc[0]["PREY_CREATININE"]).isdigit() else 0.0)
                            prey90_sodium = st.number_input("PREY90_sodium",step=0.1, help="Enter the sodium value in mmol/L",value = float(df.iloc[0]["PREY_SODIUM"]) if pd.notnull(df.iloc[0]["PREY_SODIUM"]) and str(df.iloc[0]["PREY_SODIUM"]).isdigit() else 0.0)
                            prey90_ast = st.number_input("PREY90_AST",step=0.1, help="Enter AST value in U/L",value = float(df.iloc[0]["PREY_AST"]) if pd.notnull(df.iloc[0]["PREY_AST"]) and str(df.iloc[0]["PREY_AST"]).isdigit() else 0.0)
                            prey90_alt = st.number_input("PREY90_ALT",step=0.1, help="Enter ALT value in U/L",value = float(df.iloc[0]["PREY_ALT"]) if pd.notnull(df.iloc[0]["PREY_ALT"]) and str(df.iloc[0]["PREY_ALT"]).isdigit() else 0.0)
                            prey90_alkaline_phosphatase = st.number_input("PREY90_Alkaline Phosphatase",step=0.1, help="Enter Alkaline Phosphatase value in U/L",value = float(df.iloc[0]["PREY_ALP"]) if pd.notnull(df.iloc[0]["PREY_ALP"]) and str(df.iloc[0]["PREY_ALP"]).isdigit() else 0.0)
                            prey90_potassium = st.number_input("PREY90_potassium",step=0.1, help="Enter the potassium value in mmol/L",value = float(df.iloc[0]["PREY_POTAS"]) if pd.notnull(df.iloc[0]["PREY_POTAS"]) and str(df.iloc[0]["PREY_POTAS"]).isdigit() else 0.0)
                            
                            prey90_ascites_ctcae = st.selectbox (
                                "PREY90_Ascites CTCAE [ Excel : PREY_ASCITCTCAE ]",
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
                                index=["none", "Asymptomatic","Minimal ascities/Mild abd distension","Symptomatic","moderate ascities/Symptomatic medical intervention", "Severe symptoms, invasive intervention indicated", "Life Threatening: Urgent operation intervention indicated"].index(df.iloc[0]["PREY_ASCITCTCAE"]) if df.iloc[0]["PREY_ASCITCTCAE"] else None,
                                placeholder="Choose an option",
                            ) 
                            def findascitesclass(score):
                                if score == "Asymptomatic" or score== "Minimal ascities/Mild abd distension":
                                    return 1
                                elif score == "Symptomatic" or score == "moderate ascities/Symptomatic medical intervention":
                                    return 2
                                elif score == "Severe symptoms, invasive intervention indicated" or score == "Life Threatening: Urgent operation intervention indicated" :
                                    return 3
                            
                            prey90_ascites_classification = 1 if prey90_ascites_ctcae == "none" else findascitesclass(prey90_ascites_ctcae)
                            st.write("PREY90_AscitesCTCAEnumb ",prey90_ascites_classification)

                            prey90_ascites_free_text = st.text_area(
                                "PREY90_Ascites Free Text",
                                value = df.iloc[0]["PREY_ASCITFT"],
                            
                            )

                            prey90_ascites_diruetics = st.selectbox(
                                "PREY90_Ascites Diruetics [ Excel : PREY_ASCITDIUR ]\n\nYes(1), No(0), NA  ",
                            options=["1", "0","NA"],
                            format_func=lambda x: {
                                "1": "Yes ",
                                "0": "No ",
                                "NA" : "NA (not in chart)"
                            }[x],
                                index=["1", "0","NA"].index(df.iloc[0]["PREY_ASCITDIUR"]) if df.iloc[0]["PREY_ASCITDIUR"] else None,  # No default selection
                                placeholder="Choose an option",
                
                            )
                            prey90_ascites_paracentesis = st.selectbox(
                                "PREY90_Ascites Paracentesis [Excel :PREY_ASCITPARA]\n\nYes(1), No(0), NA" ,
                            options=["1", "0","NA"],
                            format_func=lambda x: {
                                "1": "Yes ",
                                "0": "No ",
                                "NA" : "NA (not in chart)"
                            }[x],
                                index=["1", "0","NA"].index(df.iloc[0]["PREY_ASCITPARA"]) if df.iloc[0]["PREY_ASCITPARA"] else None,  # No default selection
                                placeholder="Choose an option",
                
                            )
                            prey90_ascites_hospitalization = st.selectbox(
                                "PREY90_Ascites Hospitalization [Excel : PREY_ASCITHOSP]\n\nYes(1), No(0), NA",
                            options=["1", "0","NA"],
                            format_func=lambda x: {
                                "1": "Yes ",
                                "0": "No ",
                                "NA" : "NA (not in chart)"
                            }[x],
                                index=["1", "0","NA"].index(df.iloc[0]["PREY_ASCITHOSP"]) if df.iloc[0]["PREY_ASCITHOSP"] else None,  # No default selection
                                placeholder="Choose an option",
                
                            )

                            prey90_he_grade = st.selectbox(
                                "PREY90_HE Grade [ Excel : PREY_HEGRADE ]\n\n(1) None, (2) Grade 1-2, (3) Grade 3-4 ",
                                options=[1,2,3],
                                format_func=lambda x: {
                                1: "None",
                                2: "Grade 1-2",
                                3: "Grade 3-4",
                                
                            }[x],
                                index=[1,2,3].index(int(df.iloc[0]["PREY_HEGRADE"])) if df.iloc[0]["PREY_HEGRADE"] else None,  # No default selection
                                placeholder="Choose an option",

                            )
                        
                            prey90_ecog = st.selectbox("PREY90_ECOG [Excel : PREY_ECOG]", options=["0", "1", "2", "3", "4", "NA"],
                                index=["0", "1", "2", "3", "4", "NA"].index(df.iloc[0]["PREY_ECOG"]) if df.iloc[0]["PREY_ECOG"] else None,  # No default selection
                                placeholder="Choose an option",)

                            prey90_child_pugh_points_calc = calculatepoints(prey90_bilirubin,prey90_albumin,prey90_inr,prey90_ascites_classification,prey90_he_grade)
                            st.write("PREY90_CPcalc",prey90_child_pugh_points_calc)
                    
                            prey90_child_pugh_class_calc = calculate_class(prey90_child_pugh_points_calc)
                            st.write("PREY90_CPclass",prey90_child_pugh_class_calc)
                            prey90_meld_score_calc = meld_calc(prey90_creatinine,prey90_bilirubin,prey90_inr)
                            st.write("PREY90_MELD",prey90_meld_score_calc)
                    
                            prey90_meld_na_score_calc = prey90_meld_score_calc + 1.32*(137-int(prey90_sodium)) - (0.033*prey90_meld_score_calc*(137-int(prey90_sodium)))
                            st.write("PREY90_MELDNa",prey90_meld_na_score_calc)
                            prey90_albi_score_calc = albi_calc(prey90_bilirubin,prey90_albumin)
                            st.write("PREY90_Albiscore",prey90_albi_score_calc)
                            prey90_albi_grade = albi_class(prey90_albi_score_calc)
                            st.write("PREY90_Albigrade",prey90_albi_grade)
                            prey90_bclc_calc = st.selectbox("PREY90_BCLC Stage calc [ Excel : PREY_BCLC ]\n\n(NA) Not in chart, (0) Stage 0, (1) Stage A, (2) Stage B, (3) Stage C, (4) Stage D   ",
                                options=["NA", "0", "1", "2", "3", "4"],
                                format_func=lambda x: {
                                    "NA": "(NA) Not in chart",
                                    "0": " Stage 0: Very early stage, with a single nodule smaller than 2 cm in diameter",
                                    "1": " Stage A: Early stage, with one nodule smaller than 5 cm or up to three nodules smaller than 3 cm",
                                    "2": " Stage B: Intermediate stage, with multiple tumors in the liver",
                                    "3": " Stage C: Advanced stage, with cancer that has spread to other organs or blood vessels",
                                    "4": " Stage D: End-stage disease, with severe liver damage or the patient is very unwell",
                                }[x],
                                index=["NA", "0", "1", "2", "3", "4"].index(df.iloc[0]["PREY_BCLC"]) if df.iloc[0]["PREY_BCLC"] else None,
                                placeholder="Choose an option",
                            )
                        
                            st.subheader("Mapping Y90")
                            my90_date = st.date_input("MY90_date", help="Enter the date",value = datetime.strptime(df.iloc[0]["MY_DATE"], "%Y-%m-%d").date() if df.iloc[0]["MY_DATE"] else None)
                            my90_lung_shunt = st.number_input("MY90_Lung_shunt", min_value=0.0, step=0.1, help="Enter the lung shunt value",value = float(df.iloc[0]["MY_LUNGSHU"]) if pd.notnull(df.iloc[0]["MY_LUNGSHU"]) and str(df.iloc[0]["MY_LUNGSHU"]).isdigit() else 0.0)
                            
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
                                "PREY_SX": prey90_symptoms,
                                "PREY_DATELABS": prey90_date_of_labs,
                                "PREY_AFP": prey90_afp,
                                "PREY_AFPBINARY": prey90_afp_prior_to_tare,
                                "PREY_BILI": prey90_bilirubin,
                                "PREY_ALBUMIN": prey90_albumin,
                                "PREY_INR": prey90_inr,
                                "PREY_CREATININE": prey90_creatinine,
                                "PREY_SODIUM": prey90_sodium,
                                "PREY_AST": prey90_ast,
                                "PREY_ALT": prey90_alt,
                                "PREY_ALP": prey90_alkaline_phosphatase,
                                "PREY_POTAS": prey90_potassium,
                                "PREY_ASCITCTCAE": prey90_ascites_ctcae,
                                "PREY_ASCITNUMB": prey90_ascites_classification,
                                "PREY_ASCITFT": prey90_ascites_free_text,
                                "PREY_ASCITDIUR": prey90_ascites_diruetics,
                                "PREY_ASCITPARA": prey90_ascites_paracentesis,
                                "PREY_ASCITHOSP": prey90_ascites_hospitalization,
                                "PREY_HEGRADE": prey90_he_grade,
                                "PREY_ECOG": prey90_ecog,
                                "PREY_CPCALC": prey90_child_pugh_points_calc,
                                "PREY_CLASS": prey90_child_pugh_class_calc,
                                "PREY_MELD": prey90_meld_score_calc,
                                "PREY_MELDNA": prey90_meld_na_score_calc,
                                "PREY_ALBISCORE": prey90_albi_score_calc,
                                "PREY_ALBIGRADE": prey90_albi_grade,
                                "PREY_BCLC": prey90_bclc_calc,
                                "MY_DATE": my90_date,
                                "MY_LUNGSHU": my90_lung_shunt,
                                }
                                update_google_sheet(data6,mrn)
                              
                    elif st.session_state.selected_tab == "Day_Y90":
                        st.subheader("Day_Y90")
                        with st.form("day_y90_form"):

                            dayy90_afp = st.text_input("DAYY90_AFP",value = df.iloc[0]["DAYY_AFP"])
                            def process_input(value):
                                
                    # Handle the 'NA' case
                                if value.upper() == "NA":
                                    return "NA"
                    # Handle numeric cases
                                elif value.isdigit():
                                    numeric_value = int(value)
                                    return 1 if numeric_value < 200 else 2
                                else:
                                    return "Fill AFP"

                            dayy90_afp_prior_to_tare = process_input(dayy90_afp)
                            st.write("DAYY90_AFP Binary : ",dayy90_afp_prior_to_tare)
                        
                        # Inputs for other variables
                            dayy90_sodium = st.number_input("DAYY90_sodium",step=0.1,value = float(df.iloc[0]["DAYY_SODIUM"]) if pd.notnull(df.iloc[0]["DAYY_SODIUM"]) and str(df.iloc[0]["DAYY_SODIUM"]).isdigit() else 0.0)
                            dayy90_creatinine = st.number_input("DAYY90_creatinine",step=0.1,value = float(df.iloc[0]["DAYY_CREATININE"]) if pd.notnull(df.iloc[0]["DAYY_CREATININE"]) and str(df.iloc[0]["DAYY_CREATININE"]).isdigit() else 0.0
                                                                )
                            dayy90_inr = st.number_input("DAYY90_inr",step=0.1,value = float(df.iloc[0]["DAYY_INR"]) if pd.notnull(df.iloc[0]["DAYY_INR"]) and str(df.iloc[0]["DAYY_INR"]).isdigit() else 0.0)
                            dayy90_albumin = st.number_input("DAYY90_albumin",step=0.1,value = float(df.iloc[0]["DAYY_ALBUMIN"]) if pd.notnull(df.iloc[0]["DAYY_ALBUMIN"]) and str(df.iloc[0]["DAYY_ALBUMIN"]).isdigit() else 0.0)
                            dayy90_bilirubin = st.number_input("DAYY90_bilirubin",min_value=1.0,step=0.1,value = float(df.iloc[0]["DAYY_BILI"]) if pd.notnull(df.iloc[0]["DAYY_BILI"]) and str(df.iloc[0]["DAYY_BILI"]).isdigit() else 1.0)
                            dayy90_ast = st.number_input("DAYY90_AST",step=0.1,value = float(df.iloc[0]["DAYY_AST"]) if pd.notnull(df.iloc[0]["DAYY_AST"]) and str(df.iloc[0]["DAYY_AST"]).isdigit() else 0.0)
                            dayy90_alt = st.number_input("DAYY90_ALT",step=0.1,value = float(df.iloc[0]["DAYY_ALT"]) if pd.notnull(df.iloc[0]["DAYY_ALT"]) and str(df.iloc[0]["DAYY_ALT"]).isdigit() else 0.0)
                            dayy90_alkaline_phosphatase = st.number_input(
                                "DAYY90_Alkaline Phosphatase",step=0.1,
                                value = float(df.iloc[0]["DAYY_ALP"]) if pd.notnull(df.iloc[0]["DAYY_ALP"]) and str(df.iloc[0]["DAYY_ALP"]).isdigit() else 0.0
                            )
                            dayy90_leukocytes = st.number_input("DAYY90_leukocytes",step=0.1,value = float(df.iloc[0]["DAYY_LEUK"]) if pd.notnull(df.iloc[0]["DAYY_LEUK"]) and str(df.iloc[0]["DAYY_LEUK"]).isdigit() else 0.0)
                            dayy90_platelets = st.number_input("DAYY90_platelets",step=0.1,value = float(df.iloc[0]["DAYY_PLT"]) if pd.notnull(df.iloc[0]["DAYY_PLT"]) and str(df.iloc[0]["DAYY_PLT"]).isdigit() else 0.0)
                            dayy90_potassium = st.number_input("DAY90_Potassium",step=0.1,value = float(df.iloc[0]["DAYY_POTAS"]) if pd.notnull(df.iloc[0]["DAYY_POTAS"]) and str(df.iloc[0]["DAYY_POTAS"]).isdigit() else 0.0)

                            dayy90_ascites_ctcae = st.selectbox (
                                "DAYY90_Ascites CTCAE [Excel : DAYY_ASCITCTCAE]  ",
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
                                index=["none", "Asymptomatic","Minimal ascities/Mild abd distension","Symptomatic","moderate ascities/Symptomatic medical intervention", "Severe symptoms, invasive intervention indicated", "Life Threatening: Urgent operation intervention indicated"].index(df.iloc[0]["DAYY_ASCITCTCAE"]) if df.iloc[0]["DAYY_ASCITCTCAE"] else None,
                                placeholder="Choose an option",
                            ) 
                            def findascitesclass(score):
                                if score == "Asymptomatic" or score== "Minimal ascities/Mild abd distension":
                                 return 1
                                elif score == "Symptomatic" or score == "moderate ascities/Symptomatic medical intervention":
                                    return 2
                                elif score == "Severe symptoms, invasive intervention indicated" or score == "Life Threatening: Urgent operation intervention indicated" :
                                    return 3
                            
                            dayy90_ascites_classification = 1 if dayy90_ascites_ctcae == "none" else findascitesclass(dayy90_ascites_ctcae)
                            st.write("Day90_AscitesCTCAEnumb ",dayy90_ascites_classification)

                            dayy90_he_grade = st.selectbox(
                                "DAYY90_HE Grade [Excel : DAYY_HEGRADE]\n\n(1) None, (2) Grade 1-2, (3) Grade 3-4",
                                options=[1,2,3],
                                format_func=lambda x: {
                                1: "None",
                                2: "Grade 1-2",
                                3: "Grade 3-4",
                                
                            }[x],
                                index=[1,2,3].index(int(df.iloc[0]["DAYY_HEGRADE"])) if df.iloc[0]["DAYY_HEGRADE"] else None,  # No default selection
                                placeholder="Choose an option",

                            )
                        
                            dayy90_ecog = st.selectbox("DAYY90_ECOG [Excel : DAYY_ECOG]", options=["0", "1", "2", "3", "4", "NA"],
                                index=["0", "1", "2", "3", "4", "NA"].index(df.iloc[0]["DAYY_ECOG"]) if df.iloc[0]["DAYY_ECOG"] else None,  # No default selection
                                placeholder="Choose an option",)
                            
                            dayy90_child_pugh_points_calc = calculatepoints(dayy90_bilirubin,dayy90_albumin,dayy90_inr,dayy90_ascites_classification,dayy90_he_grade)
                            st.write("DAYY90_CPcalc",dayy90_child_pugh_points_calc)
                            dayy90_child_pugh_class_calc = calculate_class(dayy90_child_pugh_points_calc)
                            st.write("DAYY90_CPclass",dayy90_child_pugh_class_calc)
                            dayy90_meld_score_calc = meld_calc(dayy90_creatinine,dayy90_bilirubin,dayy90_inr)
                            st.write("DAYY90_MELD",dayy90_meld_score_calc)
                            dayy90_meld_na_score_calc = dayy90_meld_score_calc + 1.32*(137-int(dayy90_sodium)) - (0.033*dayy90_meld_score_calc*(137-int(dayy90_sodium)))
                            st.write("DAYY90_MELDNa",dayy90_meld_na_score_calc)
                            dayy90_albi_score_calc = albi_calc(dayy90_bilirubin,dayy90_albumin)
                            st.write("DAYY90_Albiscore",dayy90_albi_score_calc)
                            dayy90_albi_grade = albi_class(dayy90_albi_score_calc)
                            st.write("DAYY90_Albigrade",dayy90_albi_grade)

                            dayy90_bclc_calc = st.selectbox("PREY90_BCLC Stage calc [ Excel : DAYY_BCLC ]\n\n(NA) Not in chart, (0) Stage 0, (1) Stage A, (2) Stage B, (3) Stage C, (4) Stage D   ",
                                options=["NA", "0", "1", "2", "3", "4"],
                                format_func=lambda x: {
                                    "NA": "(NA) Not in chart",
                                    "0": " Stage 0: Very early stage, with a single nodule smaller than 2 cm in diameter",
                                    "1": " Stage A: Early stage, with one nodule smaller than 5 cm or up to three nodules smaller than 3 cm",
                                    "2": " Stage B: Intermediate stage, with multiple tumors in the liver",
                                    "3": " Stage C: Advanced stage, with cancer that has spread to other organs or blood vessels",
                                    "4": " Stage D: End-stage disease, with severe liver damage or the patient is very unwell",
                                }[x],
                                index = ["NA", "0", "1", "2", "3", "4"].index(df.iloc[0]["DAYY_BCLC"]) if df.iloc[0]["DAYY_BCLC"] else None,
                                placeholder="Choose an option"
                                )

                            dayy90_type_of_sphere = st.selectbox(
                                "DAYY90_Type of Sphere [Excel : DAYY_SPHERE]\n\n(1) Therasphere, (2) SIR", options=["1", "2"],
                            format_func=lambda x: {
                                    "1": "Therasphere",
                                    "2": "SIR",
                                }[x],
                                index=["1", "2"].index(df.iloc[0]["DAYY_SPHERE"]) if df.iloc[0]["DAYY_SPHERE"] else None,  
                                placeholder="Choose an option",
                            )

                            dayy90_lt_notes_ftx = st.text_area("DAYY90_LT Notes Free Text",value = df.iloc[0]["DAYY_LTFT"])

                            ken_childpughscore = st.selectbox(
                                "ken_ChildPughscore [Excel : KEN_CPPRE]\n\n(1) A, (2) B, (3) C ",
                            options=["1","2","3"],
                            format_func=lambda x: {
                                    "1": "A",
                                    "2": "B",
                                    "3": "C"
                                }[x],
                               
                                index=["1","2","3"].index(df.iloc[0]["KEN_CPPRE"]) if df.iloc[0]["KEN_CPPRE"] else None,  
                                placeholder="Choose an option",
                            )
                            ken_meldpretare = st.number_input("ken_MELDpreTARE",step=0.1,value = float(df.iloc[0]["KEN_MELDPRE"]) if pd.notnull(df.iloc[0]["KEN_MELDPRE"]) and str(df.iloc[0]["KEN_MELDPRE"]).isdigit() else 0.0)


                        # Submit button
                            submit_tab7 = st.form_submit_button("Submit")
                        
                            if submit_tab7:
                                data7 = {
                                    "DAYY_AFP": dayy90_afp,
                                    "DAYY_AFPBINARY": dayy90_afp_prior_to_tare,
                                    "DAYY_SODIUM": dayy90_sodium,
                                    "DAYY_CREATININE": dayy90_creatinine,
                                    "DAYY_INR": dayy90_inr,
                                    "DAYY_ALBUMIN": dayy90_albumin,
                                    "DAYY_BILI": dayy90_bilirubin,
                                    "DAYY_AST": dayy90_ast,
                                    "DAYY_ALT": dayy90_alt,
                                    "DAYY_ALP": dayy90_alkaline_phosphatase,
                                    "DAYY_LEUK": dayy90_leukocytes,
                                    "DAYY_PLT": dayy90_platelets,
                                    "DAYY_POTAS": dayy90_potassium,
                                    "DAYY_ASCITCTCAE": dayy90_ascites_ctcae,
                                    "DAYY_ASCITNUMB": dayy90_ascites_classification,
                                    "DAYY_HEGRADE": dayy90_he_grade,
                                    "DAYY_ECOG": dayy90_ecog,
                                    "DAYY_CPCALC": dayy90_child_pugh_points_calc,
                                    "DAYY_CPCLASS": dayy90_child_pugh_class_calc,
                                    "DAYY_MELD": dayy90_meld_score_calc,
                                    "DAYY_MELDNA": dayy90_meld_na_score_calc,
                                    "DAYY_ALBISCORE": dayy90_albi_score_calc,
                                    "DAYY_ALBIGRADE": dayy90_albi_grade,
                                    "DAYY_BCLC": dayy90_bclc_calc,
                                    "DAYY_SPHERE": dayy90_type_of_sphere,
                                    "DAYY_LTFT": dayy90_lt_notes_ftx,
                                    "KEN_CPPRE": ken_childpughscore,
                                    "KEN_MELDPRE": ken_meldpretare
                                    }
                                update_google_sheet(data7, mrn)

                    elif st.session_state.selected_tab == "Post Y90 Within 30 Days Labs":
                        st.subheader("Post Y90 Within 30 Days Labs")
                        with st.form("post_y90_form"):

                            posty90_date_labs = st.date_input("POSTY90_30DY_date_labs", value = datetime.strptime(df.iloc[0]["POST30_LABSDATE"], "%Y-%m-%d").date() if df.iloc[0]["POST30_LABSDATE"] else None)
                            posty90_afp = st.text_input("POSTY90_30DY_afp", value = df.iloc[0]["POST30_AFP"])
                            posty90_afp_date = st.date_input("POSTY90_30DY_afp DATE", value = datetime.strptime(df.iloc[0]["POST30_AFPDATE"], "%Y-%m-%d").date() if df.iloc[0]["POST30_AFPDATE"] else None)
                            posty90_sodium = st.number_input("POSTY90_30DY_Sodium", step=0.1, value = float(df.iloc[0]["POST30_SODIUM"]) if pd.notnull(df.iloc[0]["POST30_SODIUM"]) and str(df.iloc[0]["POST30_SODIUM"]).isdigit() else 0.0)
                            posty90_creatinine = st.number_input("POSTY90_30DY_creatinine", step=0.1, value = float(df.iloc[0]["POST30_CREATININE"]) if pd.notnull(df.iloc[0]["POST30_CREATININE"]) and str(df.iloc[0]["POST30_CREATININE"]).isdigit() else 0.0)
                            posty90_inr = st.number_input("POSTY90_30DY_INR", step=0.1, value = float(df.iloc[0]["POST30_INR"]) if pd.notnull(df.iloc[0]["POST30_INR"]) and str(df.iloc[0]["POST30_INR"]).isdigit() else 0.0)
                            posty90_albumin = st.number_input("POSTY90_30DY_albumin", step=0.1, value = float(df.iloc[0]["POST30_ALBUMIN"]) if pd.notnull(df.iloc[0]["POST30_ALBUMIN"]) and str(df.iloc[0]["POST30_ALBUMIN"]).isdigit() else 0.0)
                            posty90_bilirubin = st.number_input("POSTY90_30DY_bilirubin", min_value=1.0, step=0.1, value = float(df.iloc[0]["POST30_BILI"]) if pd.notnull(df.iloc[0]["POST30_BILI"]) and str(df.iloc[0]["POST30_BILI"]).isdigit() else 1.0)
                            posty90_ast = st.number_input("POSTY90_30DY_AST", step=0.1, value = float(df.iloc[0]["POST30_AST"]) if pd.notnull(df.iloc[0]["POST30_AST"]) and str(df.iloc[0]["POST30_AST"]).isdigit() else 0.0)
                            posty90_alt = st.number_input("POSTY90_30DY_ALT", step=0.1, value = float(df.iloc[0]["POST30_ALT"]) if pd.notnull(df.iloc[0]["POST30_ALT"]) and str(df.iloc[0]["POST30_ALT"]).isdigit() else 0.0)
                            posty90_alkaline_phosphatase = st.number_input("POSTY90_30DY_Alkaline Phosphatase", step=0.1, value = float(df.iloc[0]["POST30_ALP"]) if pd.notnull(df.iloc[0]["POST30_ALP"]) and str(df.iloc[0]["POST30_ALP"]).isdigit() else 0.0)
                            posty90_leukocytes = st.number_input("POSTY90_30DY_leukocytes", step=0.1, value = float(df.iloc[0]["POST30_LEUK"]) if pd.notnull(df.iloc[0]["POST30_LEUK"]) and str(df.iloc[0]["POST30_LEUK"]).isdigit() else 0.0)
                            posty90_platelets = st.number_input("POSTY90_30DY_platelets", step=0.1, value = float(df.iloc[0]["POST30_PLT"]) if pd.notnull(df.iloc[0]["POST30_PLT"]) and str(df.iloc[0]["POST30_PLT"]).isdigit() else 0.0)
                            posty90_potassium = st.number_input("POSTY90_30DY_potassium", step=0.1, value = float(df.iloc[0]["POST30_POTAS"]) if pd.notnull(df.iloc[0]["POST30_POTAS"]) and str(df.iloc[0]["POST30_POTAS"]).isdigit() else 0.0)
                            
                            posty90_ascites_ctcae = st.selectbox (
                            "30DY_AE_AscitesCTCAE [Excel : POST30_ASCITCTCAE]",
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
                                index=["none", "Asymptomatic","Minimal ascities/Mild abd distension","Symptomatic","moderate ascities/Symptomatic medical intervention", "Severe symptoms, invasive intervention indicated", "Life Threatening: Urgent operation intervention indicated"].index(df.iloc[0]["POST30_ASCITCTCAE"]) if df.iloc[0]["POST30_ASCITCTCAE"] else None,
                                placeholder="Choose an option",
                            ) 
                            def findascitesclass(score):
                                if score == "Asymptomatic" or score== "Minimal ascities/Mild abd distension":
                                 return 1
                                elif score == "Symptomatic" or score == "moderate ascities/Symptomatic medical intervention":
                                 return 2
                                elif score == "Severe symptoms, invasive intervention indicated" or score == "Life Threatening: Urgent operation intervention indicated" :
                                 return 3
                            
                            posty90_ascites_classification = 1 if posty90_ascites_ctcae == "none" else findascitesclass(posty90_ascites_ctcae)
                            st.write("30DY_AE_AscitesCTCAEnumb : ",posty90_ascites_classification)
                            posty90_ascites_diruetics = st.selectbox(
                                "30DY_AE_Ascitesdiruetics[Excel : POST30_ASCITDIUR]\n\n Yes (1), No (0)",
                                    options=["1", "0"],
                                    format_func=lambda x: {
                                            "1": "Yes",
                                            "0": "No",
                                        }[x],
                                index=["1","0"].index(df.iloc[0]["POST30_ASCITDIUR"]) if df.iloc[0]["POST30_ASCITDIUR"] else None,
                                placeholder="Choose an option",
                
                            )
                            posty90_ascites_paracentesis = st.selectbox(
                                "30DY_AE_Ascitesparacentesis[Excel : POST30_ASCITPARA]\n\n Yes (1), No (0)",
                                    options=["1", "0"],
                                    format_func=lambda x: {
                                            "1": "Yes",
                                            "0": "No",
                                        }[x],
                                index=["1","0"].index(df.iloc[0]["POST30_ASCITPARA"]) if df.iloc[0]["POST30_ASCITPARA"] else None,
                                placeholder="Choose an option",
                
                            )
                            posty90_ascites_hospitalization = st.selectbox(
                                "30DY_AE_Asciteshospitalization[Excel : POST30_ASCITHOSP]\n\n Yes (1), No (0)",
                                    options=["1", "0"],
                                    format_func=lambda x: {
                                            "1": "Yes",
                                            "0": "No",
                                        }[x],
                                index=["1","0"].index(df.iloc[0]["POST30_ASCITHOSP"]) if df.iloc[0]["POST30_ASCITHOSP"] else None,
                                placeholder="Choose an option",
                
                            )
                            posty90_he_grade = st.selectbox(
                                "30DY_AE_HE Grade [Excel : POST30_HEGRADE]\n\n(1) None, (2) Grade 1-2, (3) Grade 3-4",
                                options=[1,2,3],
                                format_func=lambda x: {
                                1: "None",
                                2: "Grade 1-2",
                                3: "Grade 3-4",
                                
                            }[x],
                                index=[1,2,3].index(int(df.iloc[0]["POST30_HEGRADE"])) if df.iloc[0]["POST30_HEGRADE"] else None,
                                placeholder="Choose an option",

                            )

                            posty90_ascites_free_text = st.text_area(
                                "30DY_AE_ascities_freetext",
                                value = df.iloc[0]["POST30_ASCITFT"]
                            
                            )

                            posty90_ecog = st.selectbox("POSTY90_30DY_ECOG [Excel : POST30_ECOG]", options=["0", "1", "2", "3", "4", "NA"],
                                index=["0", "1", "2", "3", "4", "NA"].index(df.iloc[0]["POST30_ECOG"]) if df.iloc[0]["POST30_ECOG"] else None,
                                placeholder="Choose an option",
                                )
                            posty90_child_pugh_points = calculatepoints(posty90_bilirubin,posty90_albumin,posty90_inr,posty90_ascites_classification,posty90_he_grade)
                            st.write("DAYY90_CPcalc",posty90_child_pugh_points)
                            posty90_child_pugh_class = calculate_class(posty90_child_pugh_points)
                            st.write("DAYY90_CPclass",posty90_child_pugh_class)
                            posty90_meld = meld_calc(posty90_creatinine,posty90_bilirubin,posty90_inr)
                            st.write("DAYY90_MELD",posty90_meld)
                            posty90_meld_na = posty90_meld + 1.32*(137-int(posty90_sodium)) - (0.033*posty90_meld*(137-int(posty90_sodium)))
                            st.write("DAYY90_MELDNa",posty90_meld_na)
                            posty90_albi_score = albi_calc(posty90_bilirubin,posty90_albumin)
                            st.write("DAYY90_Albiscore",posty90_albi_score)
                            posty90_albi_grade = albi_class(posty90_albi_score)
                            st.write("DAYY90_Albigrade",posty90_albi_grade)

                            posty90_bclc = st.selectbox("PREY90_BCLC Stage calc [ Excel : POST30_BCLC ]\n\n(NA) Not in chart, (0) Stage 0, (1) Stage A, (2) Stage B, (3) Stage C, (4) Stage D   ",
                                options=["NA", "0", "1", "2", "3", "4"],
                                format_func=lambda x: {
                                    "NA": "(NA) Not in chart",
                                    "0": " Stage 0: Very early stage, with a single nodule smaller than 2 cm in diameter",
                                    "1": " Stage A: Early stage, with one nodule smaller than 5 cm or up to three nodules smaller than 3 cm",
                                    "2": " Stage B: Intermediate stage, with multiple tumors in the liver",
                                    "3": " Stage C: Advanced stage, with cancer that has spread to other organs or blood vessels",
                                    "4": " Stage D: End-stage disease, with severe liver damage or the patient is very unwell",
                                }[x],
                                index = ["NA", "0", "1", "2", "3", "4"].index(df.iloc[0]["POST30_BCLC"]) if df.iloc[0]["POST30_BCLC"] else None,
                                placeholder="Choose an option"
                                )
                        
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
                                "30DYAE_portal_htn CTCAE [Excel : AE30_PORTHTN]",
                                options=["0","1","2","3","4","5"],
                            index=["0","1","2","3","4","5"].index(df.iloc[0]["AE30_PORTHTN"]) if df.iloc[0]["AE30_PORTHTN"] else None,
                            placeholder="Choose an option",
                            )
                            DYAE_CTCAE_Vascular_comp = st.selectbox(
                                "30DYAE_Vascular comp CTCAE [Excel : AE30_VASCULAR]",
                                options=["0","1","2","3","4","5"],
                            index=["0","1","2","3","4","5"].index(df.iloc[0]["AE30_VASCULAR"]) if df.iloc[0]["AE30_VASCULAR"] else None,
                            placeholder="Choose an option",
                            )
                            DYAE_CTCAE_fatigue = st.selectbox(
                                "30DYAE_fatigue CTCAE [Excel : AE30_FATIGUE]",
                                options=["0","1","2"],
                            index=["0","1","2"].index(df.iloc[0]["AE30_FATIGUE"]) if df.iloc[0]["AE30_FATIGUE"] else None,
                            placeholder="Choose an option",
                            )
                            DYAE_CTCAE_diarrhea = st.selectbox(
                                "30DYAE_diarrhea CTCAE [Excel : AE30_DIAR]",
                                options=["0","1","2","3","4","5"],
                            index=["0","1","2","3","4","5"].index(df.iloc[0]["AE30_DIAR"]) if df.iloc[0]["AE30_DIAR"] else None,
                            placeholder="Choose an option",
                            )
                            # Formula
                            DYAE_CTCAE_hypoalbuminemia_emr = hypoalbuminemia(posty90_albumin)
                            st.write("30 Days AE_hypoalbuminemia CTCAE : ",DYAE_CTCAE_hypoalbuminemia_emr)

                            prey90_bili = df.iloc[0]["PREY_BILI"]
                            DYAE_CTCAE_hyperbilirubinemia_emr = 0
                            if prey90_bili in [None, "", " "]:  # Ensure it's valid before using
                                st.error("Cannot calculate 30 Days AE_hyperbilirubinemia CTCAE due to No data in PREY_BILI.")
                            else:
                                prey90_bili= float(prey90_bili)
                                DYAE_CTCAE_hyperbilirubinemia_emr = hyperbillirubine(prey90_bili,posty90_bilirubin)
                                st.write("30 Days AE_hyperbilirubinemia CTCAE : ",DYAE_CTCAE_hyperbilirubinemia_emr)

                            prey90_creatinine = df.iloc[0]["PREY_CREATININE"]
                            DYAE_CTCAE_Increase_creatinine_emr = 0
                            if prey90_creatinine in [None, "", " "]:  # Ensure it's valid before using
                                st.error("Cannot calculate 30 Days AE_CTCAE_Increase creatinine CTCAE due to No data in PREY_CREATININE.")
                            else:
                                prey90_creatinine= float(prey90_creatinine)
                                DYAE_CTCAE_Increase_creatinine_emr = Increasecreatine(prey90_creatinine,posty90_creatinine)
                                st.write("30 Days AE_CTCAE_Increase creatinine CTCAE : ",DYAE_CTCAE_Increase_creatinine_emr)

                            DYAE_CTCAE_abdominal_pain = st.selectbox(
                                "30DYAE_abdominal pain CTCAE [Excel : AE30_ABDPAIN]",
                                options=["0","1","2","3"],
                            index=["0","1","2","3"].index(df.iloc[0]["AE30_ABDPAIN"]) if df.iloc[0]["AE30_ABDPAIN"] else None,
                            placeholder="Choose an option",
                            )
                            DYAE_CTCAE_sepsis = st.selectbox(
                                "30DYAE_sepsis CTCAE [Excel : AE30_SEPSIS]",
                                options=["0","3","4","5"],
                            index=["0","3","4","5"].index(df.iloc[0]["AE30_SEPSIS"]) if df.iloc[0]["AE30_SEPSIS"] else None,
                            placeholder="Choose an option",
                            )
                            DYAE_CTCAE_bacterial_peritonitis = st.selectbox(
                                "30DYAE_CTCAE_bacterial_peritonitis [Excel : AE30_BACTPER]",
                                options=["0", "3", "4", "5"],
                            index=["0", "3", "4", "5"].index(df.iloc[0]["AE30_BACTPER"]) if df.iloc[0]["AE30_BACTPER"] else None,
                            placeholder="Choose an option",
                            )
                            DYAE_CTCAE_hemorrhage = st.selectbox(
                            "30DYAE_CTCAE_hemorrhage [Excel : AE30_HEMOR]",
                            options=["0", "3", "4", "5"],
                            index=["0", "3", "4", "5"].index(df.iloc[0]["AE30_HEMOR"]) if df.iloc[0]["AE30_HEMOR"] else None,
                            placeholder="Choose an option",
                            )
                            DYAE_CTCAE_anorexia = st.selectbox(
                                "30DYAE_CTCAE_anorexia [Excel : AE30_ANOREX]",
                                options=["0", "1", "2", "3"],
                            index=["0", "1", "2", "3"].index(df.iloc[0]["AE30_ANOREX"]) if df.iloc[0]["AE30_ANOREX"] else None,
                            placeholder="Choose an option",
                            )
                            DYAE_CTCAE_intrahepatic_fistula = st.selectbox(
                                "30DYAE_CTCAE_intrahepatic_fistula [Excel : AE30_IHFIST]",
                                options=["0","2", "3", "4", "5"],
                            index=["0","2", "3", "4", "5"].index(df.iloc[0]["AE30_IHFIST"]) if df.iloc[0]["AE30_IHFIST"] else None,
                            placeholder="Choose an option",
                            )
                            DYAE_CTCAE_constipation = st.selectbox(
                                "30DYAE_CTCAE_constipation [Excel : AE30_CONSTI]",
                                options=["0", "1", "2", "3"],
                            index=["0", "1", "2", "3"].index(df.iloc[0]["AE30_CONSTI"]) if df.iloc[0]["AE30_CONSTI"] else None,
                            placeholder="Choose an option",
                            )
                            DYAE_CTCAE_nausea = st.selectbox(
                                "30DYAE_CTCAE_nausea [Excel : AE30_NAUS]",
                                options=["0", "1", "2", "3"],
                            index=["0", "1", "2", "3"].index(df.iloc[0]["AE30_NAUS"]) if df.iloc[0]["AE30_NAUS"] else None,
                            placeholder="Choose an option",
                            )
                            DYAE_CTCAE_vomiting = st.selectbox(
                                "30DYAE_CTCAE_vomiting [Excel : AE30_VOM]",
                                options=["0","1","2", "3", "4", "5"],
                            index=["0","1","2", "3", "4", "5"].index(df.iloc[0]["AE30_VOM"]) if df.iloc[0]["AE30_VOM"] else None,
                            placeholder="Choose an option",
                            )
                            DYAE_CTCAE_cholecystitis = st.selectbox(
                                "30DYAE_CTCAE_cholecystitis [Excel : AE30_CHOLE]",
                                options=["0", "2","3", "4", "5"],
                            index=["0", "2","3", "4", "5"].index(df.iloc[0]["AE30_CHOLE"]) if df.iloc[0]["AE30_CHOLE"] else None,
                            placeholder="Choose an option",
                            )
                            DYAE_CTCAE_gastric_ulcers = st.selectbox(
                                "30DYAE_CTCAE_gastric_ulcers [Excel : AE30_GULCER]",
                                options=["0","1","2", "3", "4", "5"],
                            index=["0","1","2", "3", "4", "5"].index(df.iloc[0]["AE30_GULCER"]) if df.iloc[0]["AE30_GULCER"] else None,
                            placeholder="Choose an option",
                            )
                           
                            DYAE_CTCAE_respiratory_failure = st.selectbox(
                                "30DYAE_CTCAE_respiratory_failure [Excel : AE30_RESPFAIL]",
                                options=["0", "4", "5"],
                            index=["0", "4", "5"].index(df.iloc[0]["AE30_RESPFAIL"]) if df.iloc[0]["AE30_RESPFAIL"] else None,
                            placeholder="Choose an option",
                            )
                            DYAE_CTCAE_AKI = st.selectbox(
                                "30DYAE_CTCAE_AKI [Excel : AE30_AKI]",
                                options=["0", "3", "4", "5"],
                            index=["0", "3", "4", "5"].index(df.iloc[0]["AE30_AKI"]) if df.iloc[0]["AE30_AKI"] else None,
                            placeholder="Choose an option",
                            )

                            DYAE_CTCAE_Radiation_pneumonitis = st.selectbox(
                                "30DYAE_CTCAE_Radiation_pneumonitis [Excel : AE30_RADPNEUM]",
                                options=["0","1","2", "3", "4", "5"],
                            index=["0","1","2", "3", "4", "5"].index(df.iloc[0]["AE30_RADPNEUM"]) if df.iloc[0]["AE30_RADPNEUM"] else None,
                            placeholder="Choose an option",
                            )
                            DYAE_CTCAE_hyperkalemia = hyperkalemia(posty90_potassium)
                            st.write("30 Days AE CTCAE Hyperkalemia",DYAE_CTCAE_hyperkalemia)
                            day90_alt = df.iloc[0]["DAYY_ALT"]
                            ae30_alt = 0
                            if day90_alt in [None, "", " "]:  # Ensure it's valid before using
                                st.error("Cannot calculate AE30_ALT due to No data in DAYY_ALT.")
                            else:
                                day90_alt= float(day90_alt)
                                ae30_alt = alt_calculate(day90_alt, posty90_alt)
                                st.write("30 Days AE CTCAE ALT",ae30_alt)

                            day90_ast = df.iloc[0]["DAYY_AST"]
                            ae30_ast = 0
                            if day90_ast in [None, "", " "]:  # Ensure it's valid before using
                                st.error("Cannot calculate AE30_AST due to No data in DAYY_AST.")
                            else:
                                day90_ast= float(day90_ast)
                                ae30_ast = ast_calculate(day90_ast, posty90_ast)
                                st.write("30 Days AE CTCAE AST",ae30_ast)

                            day90_alp = df.iloc[0]["DAYY_ALP"]
                            ae30_alp = 0
                            if day90_alp in [None, "", " "]:  # Ensure it's valid before using
                                st.error("Cannot calculate AE30_AST due to No data in DAYY_ALP.")
                            else:
                                day90_alp= float(day90_alp)
                                ae30_alp = ast_calculate(day90_alp, posty90_alkaline_phosphatase)
                                st.write("30 Days AE CTCAE  Alkaline Phosphatase",ae30_alp)
                            
                            ae30_plt = plt_calculate(posty90_platelets)
                            st.write("30 Days AE CTCAE Platelets",ae30_plt)

                            ae30_otherft = st.text_input("AE30_OTHERFT", value=df.iloc[0]["AE30_OTHERFT"] if "AE30_OTHERFT" in df.columns else "")
                            ae30_other = st.text_input("AE30_OTHER", value=df.iloc[0]["AE30_OTHER"] if "AE30_OTHER" in df.columns else "")

                            variables = [
                                    DYAE_CTCAE_portal_htn, DYAE_CTCAE_Vascular_comp, DYAE_CTCAE_fatigue, DYAE_CTCAE_diarrhea,
                                    DYAE_CTCAE_hypoalbuminemia_emr, DYAE_CTCAE_hyperbilirubinemia_emr, DYAE_CTCAE_Increase_creatinine_emr,
                                    DYAE_CTCAE_abdominal_pain, DYAE_CTCAE_sepsis, DYAE_CTCAE_bacterial_peritonitis, DYAE_CTCAE_hemorrhage,
                                    DYAE_CTCAE_anorexia, DYAE_CTCAE_intrahepatic_fistula, DYAE_CTCAE_constipation, DYAE_CTCAE_nausea,
                                    DYAE_CTCAE_vomiting, DYAE_CTCAE_cholecystitis, DYAE_CTCAE_gastric_ulcers, DYAE_CTCAE_respiratory_failure,
                                    DYAE_CTCAE_AKI, DYAE_CTCAE_Radiation_pneumonitis, DYAE_CTCAE_hyperkalemia, ae30_alt, ae30_ast, ae30_alp, ae30_plt
                                ]

                            # Count the occurrences of 1 or 2
                            count = sum(1 for value in variables if value in ["1", "2",1,2])
                            count1 = sum(1 for value in variables if value not in ["1", "2",1,2,"",None])

                            ae30_gradesum12 = count
                            ae30_gradesum345 = count1

                            DYAE_AE_other = st.text_area(
                                "30DY_AE_other",
                                help="Other Adverse Events (Free Text)",
                                value=df.iloc[0]["30DY_AE_Other"]
                            )

                            DYAE_AE_date_of_AE = st.text_input(
                                "90DY_AE_date_of_AE",
                                help="(if AE is present after 30 days but before 90 write it here and the date)",
                                value=df.iloc[0]["AE90_DATE"]
                            )
                            ken_grandedtoxicity = st.text_area(
                                "AE90_OTHERFT",
                                value=df.iloc[0]["AE90_OTHERFT"]

                            )
                            
                            ae90_gradesum12 = st.text_input("AE90_GRADESUM12", value=df.iloc[0]["AE90_GRADESUM12"] )
                            ae90_gradesum345 = st.text_input("AE90_GRADESUM345", value=df.iloc[0]["AE90_GRADESUM345"] )
                            dy_ae_hospitalization_3 = st.selectbox(
                                "90DY_AE_Hospitalization 3 months [Excel : AE90_HOSP3]\n\n Yes (1), No (0)",
                                    options=["1", "0"],
                                    format_func=lambda x: {
                                            "1": "Yes",
                                            "0": "No",
                                        }[x],
                                
                                index=["1","0"].index(df.iloc[0]["AE90_HOSP3"]) if df.iloc[0]["AE90_HOSP3"] else None,
                            placeholder="Choose an option",
                            )
                            dy_ae_hospitalization_6 = st.selectbox(
                                "90DY_AE_Hospitalization 6 months [Excel : AE30_HOSP3DATE]\n\n Yes (1), No (0)",
                                    options=["1", "0"],
                                    format_func=lambda x: {
                                            "1": "Yes",
                                            "0": "No",
                                        }[x],
                             
                                index=["1","0"].index(df.iloc[0]["AE30_HOSP3DATE"]) if df.iloc[0]["AE30_HOSP3DATE"] else None,
                            placeholder="Choose an option",
                            )
                            dy_ae_hosp6mo = st.selectbox(
                                "90DY_AE_Hosp6mo [Excel : AE90_HOSP6]\n\n Yes (1), No (0)",
                                    options=["1", "0"],
                                    format_func=lambda x: {
                                            "1": "Yes",
                                            "0": "No",
                                        }[x],
                                
                                index=["1","0"].index(df.iloc[0]["AE90_HOSP6"]) if df.iloc[0]["AE90_HOSP6"] else None,
                            placeholder="Choose an option",
                            )
                            dy_ae_death_due = st.selectbox(
                                "90DY_AE_Death due to AE [Excel : AE30_DEATHAE]\n\n Yes (1), No (0)",
                                    options=["1", "0"],
                                    format_func=lambda x: {
                                            "1": "Yes",
                                            "0": "No",
                                        }[x],
                               
                                index=["1","0"].index(df.iloc[0]["AE30_DEATHAE"]) if df.iloc[0]["AE30_DEATHAE"] else None,
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
                                    "POST30_LABSDATE": posty90_date_labs,
                                    "POST30_AFP": posty90_afp,
                                    "POST30_AFPDATE": posty90_afp_date,
                                    "POST30_SODIUM": posty90_sodium,
                                    "POST30_CREATININE": posty90_creatinine,
                                    "POST30_INR": posty90_inr,
                                    "POST30_ALBUMIN": posty90_albumin,
                                    "POST30_BILI": posty90_bilirubin,
                                    "POST30_AST": posty90_ast,
                                    "POST30_ALT": posty90_alt,
                                    "POST30_ALP": posty90_alkaline_phosphatase,
                                    "POST30_LEUK": posty90_leukocytes,
                                    "POST30_PLT": posty90_platelets,
                                    "POST30_POTAS": posty90_potassium,
                                    "POST30_ASCITCTCAE": posty90_ascites_ctcae,
                                    "POST30_ASCITNUMB": posty90_ascites_classification,
                                    "POST30_ASCITDIUR": posty90_ascites_diruetics,
                                    "POST30_ASCITPARA": posty90_ascites_paracentesis,
                                    "POST30_ASCITHOSP": posty90_ascites_hospitalization,
                                    "POST30_HEGRADE": posty90_he_grade,
                                    "POST30_ASCITFT": posty90_ascites_free_text,
                                    "POST30_ECOG": posty90_ecog,
                                    "POST30_CPCALC": posty90_child_pugh_points,
                                    "POST30_CPCLASS": posty90_child_pugh_class,
                                    "POST30_MELD": posty90_meld,
                                    "POST30_MELDNA": posty90_meld_na,
                                    "POST30_ALBISCORE": posty90_albi_score,
                                    "POST30_ALBIGRADE": posty90_albi_grade,
                                    "POST30_BCLC": posty90_bclc,
                                    "Ken_BCLCStagepost90": ken_bclc_stage_post90,
                                    "Ken_MELD_Stagepost90": ken_meld_stage_post90,
                                    "AE30_PORTHTN": DYAE_CTCAE_portal_htn,
                                    "AE30_VASCULAR": DYAE_CTCAE_Vascular_comp,
                                    "AE30_FATIGUE": DYAE_CTCAE_fatigue,
                                    "AE30_DIAR": DYAE_CTCAE_diarrhea,
                                    "AE30_HYPOALBUM": DYAE_CTCAE_hypoalbuminemia_emr,
                                    "AE30_HYPERBILI": DYAE_CTCAE_hyperbilirubinemia_emr,
                                    "AE30_INCREASECR": DYAE_CTCAE_Increase_creatinine_emr,
                                    "AE30_ABDPAIN": DYAE_CTCAE_abdominal_pain,
                                    "AE30_SEPSIS": DYAE_CTCAE_sepsis,
                                    "AE30_BACTPER": DYAE_CTCAE_bacterial_peritonitis,
                                    "AE30_HEMOR": DYAE_CTCAE_hemorrhage,
                                    "AE30_ANOREX": DYAE_CTCAE_anorexia,
                                    "AE30_IHFIST": DYAE_CTCAE_intrahepatic_fistula,
                                    "AE30_CONSTI": DYAE_CTCAE_constipation,
                                    "AE30_NAUS": DYAE_CTCAE_nausea,
                                    "AE30_VOM": DYAE_CTCAE_vomiting,
                                    "AE30_CHOLE": DYAE_CTCAE_cholecystitis,
                                    "AE30_GULCER": DYAE_CTCAE_gastric_ulcers,
                                    "AE30_RESPFAIL": DYAE_CTCAE_respiratory_failure,
                                    "AE30_AKI": DYAE_CTCAE_AKI,
                                    "AE30_RADPNEUM": DYAE_CTCAE_Radiation_pneumonitis,
                                    "AE30_HYPERKAL": DYAE_CTCAE_hyperkalemia,
                                    "AE30_ALT" : ae30_alt,
                                    "AE30_AST" : ae30_ast,
                                    "AE30_ALP" : ae30_alp,
                                    "AE30_PLT" : ae30_plt,
                                    "AE30_OTHERFT" : ae30_otherft,
                                    "AE30_OTHER" : ae30_other,
                                    "AE30_GRADESUM12" : ae30_gradesum12,
                                    "AE30_GRADESUM345" : ae30_gradesum345,
                                    "30DY_AE_Other": DYAE_AE_other,
                                    "AE90_DATE": DYAE_AE_date_of_AE,
                                    "AE90_OTHERFT": ken_grandedtoxicity,
                                    "AE90_GRADESUM12" : ae90_gradesum12,
                                    "AE90_GRADESUM345" : ae90_gradesum345,
                                    "AE90_HOSP3": dy_ae_hospitalization_3,
                                    "AE30_HOSP3DATE": dy_ae_hospitalization_6,
                                    "AE90_HOSP6": dy_ae_hosp6mo,
                                    "AE30_DEATHAE": dy_ae_death_due
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

                            
                            try : 
                                prey90_bilirubin = df.iloc[0]['PREY_BILI']
                                prey90_albumin = df.iloc[0]['PREY_ALBUMIN']
                                k_ken_albipretareraw = albi_calc(prey90_bilirubin,prey90_albumin)
                                st.write("K_ken_AlbiPreTARERaw : ", k_ken_albipretareraw)
                                k_ken_albipretaregrade = albi_class(k_ken_albipretareraw)
                                st.write("K_ken_AlbiPreTAREGrade: ",k_ken_albipretaregrade)
                            except:
                                st.warning("Fill Pre Y90 Tab")
                            try :
                                posty90_bilirubin = df.iloc[0]['POST30_BILI']
                                posty90_albumin = df.iloc[0]['POST30_ALBUMIN']
                                k_ken_albiposttareraw = albi_calc(posty90_bilirubin,posty90_albumin)
                                st.write("K_ken_AlbiPostTARERaw : ", k_ken_albiposttareraw)
                                k_ken_albiposttaregrade = albi_class(k_ken_albiposttareraw)
                                st.write("K_ken_AliPostTAREGrade : ", k_ken_albiposttaregrade)
                            except :
                                st.warning("Fill Post 90 Form")
                            
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
                                        "PREY90_prescan_modality [Excel : PREY_MOD]\n\n(1) CT, (2) MRI",
                                        options=["1","2"],
                                        format_func=lambda x: {
                                            "1": "CT",
                                            "2": "MRI",
                                        }[x],
                                index=["1","2"].index(df.iloc[0]["PREY_MOD"]) if df.iloc[0]["PREY_MOD"] else None,
                                placeholder="Choose an option",
                                )
                                PREY90_Imaging_Date = st.date_input("PREY90_Imaging Date" ,value = datetime.strptime(df.iloc[0]["PREY_IMG_DATE"], "%Y-%m-%d").date() if df.iloc[0]["PREY_IMG_DATE"] else None
                                )
                                PREY90_total_number_of_lesions = st.selectbox(
                                        "PREY90_total number of lesions [Excel : PREY_TOTLES]",
                                        options=["1","2",">3"],
                                index=["1","2",">3"].index(df.iloc[0]["PREY_TOTLES"]) if df.iloc[0]["PREY_TOTLES"] else None,
                                placeholder="Choose an option",
                                )
                                PREY90_Number_Involved_Lobes = st.selectbox(
                                        "PREY90_Number Involved Lobes [Excel : PREY_LOBES]\n\n(1) Unilobar, (2) Bilobar",
                                        options=["1","2"],
                                        format_func=lambda x: {
                                            "1": "Unilobar",
                                            "2": "Bilobar",
                                        }[x],
                                index=["1","2"].index(df.iloc[0]["PREY_LOBES"]) if df.iloc[0]["PREY_LOBES"] else None,
                                placeholder="Choose an option",
                                )
                                prey90_sx = df.loc[df["MRN"] == mrn, "PREY_TL1SEG"].values[0]
                                if prey90_sx:
                                    # If complications is a string, split it into a list and strip spaces
                                    prey90_sx_list = [comp.strip() for comp in prey90_sx.split(',')] if isinstance(prey90_sx, str) else prey90_sx
                                else:
                                    prey90_sx_list = []
                                valid_prey90_sx = ["1","2","3","4a","4b","5","6","7","8","NA"]
                                prey90_sx_list = [comp for comp in prey90_sx_list if comp in valid_prey90_sx]
                                PREY90_target_lesion_1_segments = st.multiselect(
                                        "PREY90_target_lesion_1_segments [Excel : PREY_TL1SEG]",
                                        options=["1","2","3","4a","4b","5","6","7","8","NA"],
                                        default=prey90_sx_list,
                                        placeholder="Select all that apply"
                                )
                                PREY90_target_lesion_1_segments = ", ".join(PREY90_target_lesion_1_segments)
                                PREY90_TL1_LAD = st.number_input(
                                    "PREY90_TL1_LAD",
                                    step=0.1,
                                    value = float(df.iloc[0]["PREY_TL1LAD"]) if pd.notnull(df.iloc[0]["PREY_TL1LAD"]) and df.iloc[0]["PREY_TL1LAD"] != "" else 0.0
                                )
                                PREY90_Target_Lesion_1_PAD = st.number_input(
                                    "PREY90_Target Lesion 1 PAD",step=0.1,
                                    value = float(df.iloc[0]["PREY_TL1PAD"]) if pd.notnull(df.iloc[0]["PREY_TL1PAD"]) and df.iloc[0]["PREY_TL1PAD"] != "" else 0.0
                                )
                                PREY90_Target_Lesion_1_CCD = st.number_input(
                                    "PREY90_Target Lesion 1 CCD",step=0.1,
                                    value = float(df.iloc[0]["PREY_TL1CCD"]) if pd.notnull(df.iloc[0]["PREY_TL1CCD"]) and df.iloc[0]["PREY_TL1CCD"] != "" else 0.0
                                )
                                
                               
                                PREY90_Target_Lesion_1_VOL = calculate_target_lestion_vol(PREY90_Target_Lesion_1_PAD, PREY90_TL1_LAD, PREY90_Target_Lesion_1_CCD)
                                st.write("PREY90_Target Lesion 1 VOL",PREY90_Target_Lesion_1_VOL)
                                
                                PREY90_Target_Lesion_2_segments = st.selectbox(
                                        "PREY90_Target_Lesion_2_segments [Excel : PREY_TL2SEG]",
                                        options=["1","2","3","4a","4b","5","6","7","8","NA"],
                        index=["1","2","3","4a","4b","5","6","7","8","NA"].index(df.iloc[0]["PREY_TL2SEG"]) if df.iloc[0]["PREY_TL2SEG"] else None,
                        placeholder="Choose an option",
                                )
                                PREY90_Target_Lesion_2_LAD = st.number_input(
                                    "PREY90_Target_Lesion_2_LAD",step=0.1,
                                    value = float(df.iloc[0]["PREY_TL2LAD"]) if pd.notnull(df.iloc[0]["PREY_TL2LAD"]) and df.iloc[0]["PREY_TL2LAD"] != "" else 0.0
                                )
                                PREY90_Target_Lesion_2_PAD = st.number_input(
                                    "PREY90_Target Lesion 2 PAD",
                                    step=0.1,value = float(df.iloc[0]["PREY_TL2PAD"]) if pd.notnull(df.iloc[0]["PREY_TL2PAD"]) and df.iloc[0]["PREY_TL2PAD"] != "" else 0.0
                                )
                                PREY90_Target_Lesion_2_CCD = st.number_input(
                                    "PREY90_Target Lesion 2 CCD",
                                    step=0.1,value = float(df.iloc[0]["PREY_TL2CCD"]) if pd.notnull(df.iloc[0]["PREY_TL2CCD"]) and df.iloc[0]["PREY_TL2CCD"] != "" else 0.0
                                )
                        
                                PREY90_Target_Lesion_2_VOL = calculate_value_v2(PREY90_Target_Lesion_2_segments, PREY90_Target_Lesion_2_LAD, PREY90_Target_Lesion_2_PAD, PREY90_Target_Lesion_2_CCD)
                                st.write("PREY90_Target Lesion 2 VOL",PREY90_Target_Lesion_2_VOL)
                                
                                PREY90_pretx_targeted_Lesion_Dia_Sum = max(PREY90_TL1_LAD,PREY90_Target_Lesion_1_PAD,PREY90_Target_Lesion_1_CCD)+max(PREY90_Target_Lesion_2_PAD,PREY90_Target_Lesion_2_LAD,PREY90_Target_Lesion_2_CCD)
                                st.write("PREY90_ pretx targeted Lesion Dia Sum",PREY90_pretx_targeted_Lesion_Dia_Sum)
                                PREY90_Non_Target_Lesion_Location = st.selectbox( 
                                    "PREY90_Non-Target Lesion Location [Excel : PREY_NTLOC]" , options=["1","2","3","4a","4b","5","6","7","8","NA"],
                                index=["1","2","3","4a","4b","5","6","7","8","NA"].index(df.iloc[0]["PREY_NTLOC"]) if df.iloc[0]["PREY_NTLOC"] else None,
                                placeholder="Choose an option",
                                )
                                PREY90_Non_Target_Lesion_2_LAD_Art_Enhanc = st.number_input(
                                    "PREY90_Non_Target_Lesion_2_LAD_Art_Enhanc",
                                    step=0.1,value = float(df.iloc[0]["PREY_NTL1LAD"]) if pd.notnull(df.iloc[0]["PREY_NTL1LAD"]) and df.iloc[0]["PREY_NTL1LAD"] != "" else 0.0
                                )
                                PREY90_Non_Target_Lesion_2_PAD_Art_Enhanc = st.number_input(
                                    "PREY90_Non_Target_Lesion_2_PAD_Art_Enhanc",
                                    step=0.1,value = float(df.iloc[0]["PREY_NTL1PAD"]) if pd.notnull(df.iloc[0]["PREY_NTL1PAD"]) and df.iloc[0]["PREY_NTL1PAD"] != "" else 0.0
                                )
                                PREY90_Non_Target_Lesion_2_CCD_Art_Enhanc = st.number_input(
                                    "PREY90_Non_Target_Lesion_2_CCD_Art_Enhanc",
                                    step=0.1,value = float(df.iloc[0]["PREY_NTL1CCD"]) if pd.notnull(df.iloc[0]["PREY_NTL1CCD"]) and df.iloc[0]["PREY_NTL1CCD"] != "" else 0.0
                                )
                                PREY90_Non_targeted_Lesion_Dia_Sum = 'NA' if PREY90_Non_Target_Lesion_Location == 'NA' or PREY90_Non_Target_Lesion_Location == None else max(PREY90_Non_Target_Lesion_2_PAD_Art_Enhanc,PREY90_Non_Target_Lesion_2_LAD_Art_Enhanc,PREY90_Non_Target_Lesion_2_CCD_Art_Enhanc)
                                st.write("PREY90_Non-targeted Lesion Dia Sum",PREY90_Non_targeted_Lesion_Dia_Sum)
                                PREY90_Reviewers_Initials = st.text_input(
                                    "PREY90_Reviewers Initials",
                                    help="Free-text input for reviewer name",
                                    value = df.iloc[0]["PREY_REVFT"]
                                )
                                PREY90_Pre_Y90_Extrahepatic_Disease = st.selectbox(
                                    "PREY90_Pre Y90 Extrahepatic Disease [Excel : PREY_EHD]\n\n Yes (1), No (0)",
                                    options=["1", "0"],
                                    format_func=lambda x: {
                                            "1": "Yes",
                                            "0": "No",
                                        }[x],
                        index=["1", "0"].index(df.iloc[0]["PREY_EHD"]) if df.iloc[0]["PREY_EHD"] else None,
                        placeholder="Choose an option",
                                )
                                PREY90_Pre_Y90_Extrahepatic_Disease_Location = st.text_input(
                                    "PREY90_Pre Y90 Extrahepatic Disease Location",
                                    help="Free Text",
                                    value=df.iloc[0]["PREY_EHDLOCFT"]
                                )
                                PREY90_PVT = st.selectbox(
                                    "PREY90_PVT [Excel : PREY_PVT]\n\n Yes (1), No (0), NA",
                                    options=["1", "0", "NA"],
                                    format_func=lambda x: {
                                            "1": "Yes",
                                            "0": "No",
                                            "NA": "NA"
                                        }[x],
                        index=["1", "0", "NA"].index(df.iloc[0]["PREY_PVT"]) if df.iloc[0]["PREY_PVT"] else None,
                        placeholder="Choose an option",
                                )
                                PREY90_PVT_Location = st.selectbox(
                                    "PREY90_PVT Location [Excel : PREY_PVTLOC]",
                                    options=["RPV", "LPV"],
                        index=["RPV", "LPV"].index(df.iloc[0]["PREY_PVTLOC"]) if df.iloc[0]["PREY_PVTLOC"] else None,
                        placeholder="Choose an option",
                                )
                                PREY90_Features_of_cirrhosis = st.selectbox(
                                    "PREY90_Features of cirrhosis [Excel : PREY_CIRRH]\n\n\n\n Yes (1), No (0)",
                                    options=["1", "0"],
                                    format_func=lambda x: {
                                            "1": "Yes",
                                            "0": "No",
                                        }[x],
                                    index=["1", "0"].index(df.iloc[0]["PREY_CIRRH"]) if df.iloc[0]["PREY_CIRRH"] else None,
                                    placeholder="Choose an option",
                                )
                                st.subheader("Imaging_1st_Followup")

                                FU_Scan_Modality = st.selectbox(
                                    "1st_FU_Scan Modality[Excel : FU1_MOD]\n\n(1) CT, (2) MRI",
                                        options=["1","2"],
                                        format_func=lambda x: {
                                            "1": "CT",
                                            "2": "MRI",
                                        }[x],
                        index=["1", "2"].index(df.iloc[0]["FU1_MOD"]) if df.iloc[0]["FU1_MOD"] else None,
                        placeholder="Choose an option",
                                )
                                FU_Imaging_Date = st.date_input("1st_FU_Imaging Date",value = datetime.strptime(df.iloc[0]["FU1_IMG_DATE"], "%Y-%m-%d").date() if df.iloc[0]["FU1_IMG_DATE"] else None)
                                FU_Months_Since_Y90 = relativedelta(FU_Imaging_Date, fetch_date).months
                                st.write("1st_FU_Months Since Y90",FU_Months_Since_Y90)
                                FU_Total_number_of_lesions = st.selectbox(
                                   "1st_FU_Total number of lesions [Excel : FU1_TOTLES]\n\n(1) 1,(2) 2,(3) >=3",
                            options=["1", "2", "3"],
                            format_func=lambda x: {
                                            "1": "1",
                                            "2": "2",
                                            "3" : ">=3"
                                        }[x],
                        index=["1", "2", "3"].index(df.iloc[0]["FU1_TOTLES"]) if df.iloc[0]["FU1_TOTLES"] else None, 
                        placeholder="Choose an option",
                                )
                                FU_Target_Lesion_1_LAD_Art_Enhanc = st.number_input(
                                    "1st_FU_Target Lesion 1 LAD Art Enhanc",
                                    step=0.1,value = float(df.iloc[0]["FU1_TL1LAD"]) if pd.notnull(df.iloc[0]["FU1_TL1LAD"]) and df.iloc[0]["FU1_TL1LAD"] != "" else 0.0
                                )
                                FU_Target_Lesion_1_PAD_Art_Enhanc = st.number_input(
                                    "1st_FU_Target Lesion 1 PAD Art Enhanc",
                                    step=0.1,value = float(df.iloc[0]["FU1_TL1PAD"]) if pd.notnull(df.iloc[0]["FU1_TL1PAD"]) and df.iloc[0]["FU1_TL1PAD"] != "" else 0.0
                                )
                                FU_Target_Lesion_1_CCD_Art_Enhanc = st.number_input(
                                    "1st_FU_Target Lesion 1 CCD Art Enhanc",
                                    step=0.1,value = float(df.iloc[0]["FU1_TL1CCD"]) if pd.notnull(df.iloc[0]["FU1_TL1CCD"]) and df.iloc[0]["FU1_TL1CCD"] != "" else 0.0
                                )
                                FU_Target_Lesion_2_Segments = st.selectbox(
                                    "1st_FU_Target Lesion 2 Segments [Excel : 1st_FU_Target Lesion 2 Segments]",
                                    options=["1", "2", "3", "4a", "4b", "5", "6", "7", "8", "NA"],
                        index=["1", "2", "3", "4a", "4b", "5", "6", "7", "8", "NA"].index(df.iloc[0]["FU1_TL2SEG"]) if df.iloc[0]["FU1_TL2SEG"] else None,
                        placeholder="Choose an option",
                                )
                                FU_Target_Lesion_2_LAD_Art_Enhanc = st.number_input(
                                    "1st_FU_Target Lesion 2 LAD Art Enhanc",
                                    step=0.1,value = float(df.iloc[0]["FU1_TL2LAD"]) if pd.notnull(df.iloc[0]["FU1_TL2LAD"]) and df.iloc[0]["FU1_TL2LAD"] != "" else 0.0
                                )
                                FU_Target_Lesion_2_PAD_Art_Enhanc = st.number_input(
                                    "1st_FU_Target Lesion 2 PAD Art Enhanc",
                                    step=0.1,value = float(df.iloc[0]["FU1_TL2PAD"]) if pd.notnull(df.iloc[0]["FU1_TL2PAD"]) and df.iloc[0]["FU1_TL2PAD"] !="" else 0.0
                                )
                                FU_Target_Lesion_2_CCD_Art_Enhanc = st.number_input(
                                    "1st_FU_Target Lesion 2 CCD Art Enhanc",
                                    step=0.1,value = float(df.iloc[0]["FU1_TL2CCD"]) if pd.notnull(df.iloc[0]["FU1_TL2CCD"]) and df.iloc[0]["FU1_TL2CCD"] !="" else 0.0
                                )
                                FU_Follow_up_1_targeted_Lesion_Dia_Sum = max(FU_Target_Lesion_1_CCD_Art_Enhanc,FU_Target_Lesion_1_PAD_Art_Enhanc,FU_Target_Lesion_1_LAD_Art_Enhanc)+max(FU_Target_Lesion_2_CCD_Art_Enhanc,FU_Target_Lesion_2_PAD_Art_Enhanc,FU_Target_Lesion_2_LAD_Art_Enhanc)
                                st.write("1st_FU_Follow up 1 targeted Lesion Dia Sum",FU_Follow_up_1_targeted_Lesion_Dia_Sum)
                                FU_Non_Target_Lesion_2_LAD_Art_Enhanc = st.number_input(
                                    "1st_FU_Non-Target Lesion 2 LAD Art Enhanc",
                                    step=0.1,value = float(df.iloc[0]["FU1_NTL1LAD"]) if pd.notnull(df.iloc[0]["FU1_NTL1LAD"]) and df.iloc[0]["FU1_NTL1LAD"] !="" else 0.0
                                )
                                FU_Non_Target_Lesion_2_PAD_Art_Enhanc = st.number_input(
                                    "1st_FU_Non-Target Lesion 2 PAD Art Enhanc",
                                    step=0.1,value = float(df.iloc[0]["FU1_NTL1PAD"]) if pd.notnull(df.iloc[0]["FU1_NTL1PAD"]) and df.iloc[0]["FU1_NTL1PAD"] !="" else 0.0
                                )
                                FU_Non_Target_Lesion_2_CCD_Art_Enhanc = st.number_input(
                                    "1st_FU_Non-Target Lesion 2 CCD Art Enhanc",
                                    step=0.1,value = float(df.iloc[0]["FU1_NTL1CCD"]) if pd.notnull(df.iloc[0]["FU1_NTL1CCD"]) and df.iloc[0]["FU1_NTL1CCD"] !=""  else 0.0
                                )
                                FU_Non_targeted_Lesion_Dia_Sum = max(FU_Non_Target_Lesion_2_LAD_Art_Enhanc,FU_Non_Target_Lesion_2_PAD_Art_Enhanc,FU_Non_Target_Lesion_2_CCD_Art_Enhanc)
                                st.write("1st_FU_Non-targeted Lesion Dia Sum",FU_Non_targeted_Lesion_Dia_Sum)
                                FU_Lesion_Necrosis = st.selectbox(
                                   "1st_FU_Lesion Necrosis [Excel : FU1_NECROSIS]\n\n Yes (1), No (0), NA",
                                    options=["1", "0", "NA"],
                                    format_func=lambda x: {
                                            "1": "Yes",
                                            "0": "No",
                                            "NA": "NA"
                                        }[x],
                        index=["1", "0", "NA"].index(df.iloc[0]["FU1_NECROSIS"]) if df.iloc[0]["FU1_NECROSIS"] else None,
                        placeholder="Choose an option",
                                )
                                FU_Reviewers_Initials = st.text_input(
                                    "1st_FU_Reviewers Initials",
                                    help="Free-text input for reviewer name",
                                    value = df.iloc[0]["FU1_REVFT"]
                                )
                                FU_Non_target_lesion_response = st.selectbox(
                                    "1st_FU_Non target lesion response[Excel : FU1_NTLRSP]\n\n Yes (1), No (0), NA",
                                    options=["1", "0", "NA"],
                                    format_func=lambda x: {
                                            "1": "Yes",
                                            "0": "No",
                                            "NA": "NA"
                                        }[x],
                        index=["1", "0", "NA"].index(df.iloc[0]["FU1_NTLRSP"]) if df.iloc[0]["FU1_NTLRSP"] else None,
                        placeholder="Choose an option",
                                )
                                FU_New_Lesions = st.selectbox(
                                    "1st_FU_New Lesions[Excel : FU1_NEWLESION]\n\n Yes (1), No (0), NA",
                                    options=["1", "0", "NA"],
                                    format_func=lambda x: {
                                            "1": "Yes",
                                            "0": "No",
                                            "NA": "NA"
                                        }[x],
                        index=["1", "0", "NA"].index(df.iloc[0]["FU1_NEWLESION"]) if df.iloc[0]["FU1_NEWLESION"] else None,
                        placeholder="Choose an option",
                                )
                                FU_NEW_Extrahepatic_Disease = st.selectbox(
                                    "1st_FU_NEW Extrahepatic Disease[Excel : FU1_NEWEHD]\n\n Yes (1), No (0), NA",
                                    options=["1", "0", "NA"],
                                    format_func=lambda x: {
                                            "1": "Yes",
                                            "0": "No",
                                            "NA": "NA"
                                        }[x],
                        index=["1", "0", "NA"].index(df.iloc[0]["FU1_NEWEHD"]) if df.iloc[0]["FU1_NEWEHD"] else None,
                        placeholder="Choose an option",
                                )
                                FU_NEW_Extrahepatic_Dz_Location = st.text_input(
                                    "1st_FU_NEW Extrahepatic Dz Location",
                                    help="Free text",
                                    value=df.iloc[0]["FU1_EHDLOC"]
                                )
                                FU_NEW_Extrahepatic_Dz_Date = st.date_input("1st_FU_NEW Extrahepatic Dz Date",value = datetime.strptime(df.iloc[0]["FU1_EHDDATE"], "%Y-%m-%d").date() if df.iloc[0]["FU1_EHDDATE"] else None)
                                
                                FU_change_non_target_lesion = 0 if PREY90_Non_targeted_Lesion_Dia_Sum == "NA" else ((PREY90_Non_targeted_Lesion_Dia_Sum - FU_Non_targeted_Lesion_Dia_Sum)/max(1,PREY90_pretx_targeted_Lesion_Dia_Sum))*100
                                st.write("1st_FU_% change for non target lesion",FU_change_non_target_lesion)
                                FU_change_target_lesion = ((PREY90_pretx_targeted_Lesion_Dia_Sum - FU_Follow_up_1_targeted_Lesion_Dia_Sum)/max(1,PREY90_pretx_targeted_Lesion_Dia_Sum))*100
                                st.write("1st_FU_% Change Target Dia",FU_change_target_lesion)
                                first_fu_mrecist_localized = mrecist_local(FU_change_target_lesion)
                                st.write("1st_FU_mRECIST LOCALIZED",first_fu_mrecist_localized)
                                
                                first_fu_mrecist_overall = mrecist_overall(FU_New_Lesions, FU_NEW_Extrahepatic_Disease, FU_change_non_target_lesion, FU_change_target_lesion)
                                st.write("1st_FU_mRECIST Overall",first_fu_mrecist_overall)

                                FU_Free_Text = st.text_area(
                                    "1st_FU_Free Text",
                                    help="Free text",
                                    value = df.iloc[0]["FU1_FT"]
                                )
                                st.subheader("Imaging_2nd_Followup")
                               
                                FU2_Scan_Modality = st.selectbox(
                                    "2nd_FU_Scan Modality Excel : FU2_MOD]\n\n(1) CT, (2) MRI",
                                        options=["1","2"],
                                        format_func=lambda x: {
                                            "1": "CT",
                                            "2": "MRI",
                                        }[x],
                                    index=["1", "2"].index(df.iloc[0]["FU2_MOD"]) if df.iloc[0]["FU2_MOD"] else None,
                                    placeholder="Choose an option",
                                )
                                FU2_Imaging_Date = st.date_input(
                                        "2nd_FU_Imaging Date",
                                        value=datetime.strptime(df.iloc[0]["FU2_IMG_DATE"], "%Y-%m-%d").date() if df.iloc[0]["FU2_IMG_DATE"] else None,
                                    )

                                FU2_Months_Since_Y90 = relativedelta(FU2_Imaging_Date, fetch_date).months
                                st.write("2nd_FU_Months Since Y90",FU2_Months_Since_Y90)

                                FU2_Total_number_of_lesions = st.selectbox(
                                    "2nd_FU_Total number of lesions[Excel : FU2_TOTLES]\n\n(1) 1,(2) 2,(3) >=3",
                                 options=["1", "2", "3"],
                            format_func=lambda x: {
                                            "1": "1",
                                            "2": "2",
                                            "3" : ">=3"
                                        }[x],
                                    index=["1", "2", "3"].index(df.iloc[0]["FU2_TOTLES"]) if df.iloc[0]["FU2_TOTLES"] else None,
                                    placeholder="Choose an option",
                                )
                                FU2_Target_Lesion_1_LAD_Art_Enhanc = st.number_input(
                                    "2nd_FU_Target Lesion 1 LAD Art Enhanc",
                                    step=0.1,
                                    value=float(df.iloc[0]["FU2_TL1LAD"]) if pd.notnull(df.iloc[0]["FU2_TL1LAD"]) and df.iloc[0]["FU2_TL1LAD"] != "" else 0.0,
                                )
                                FU2_Target_Lesion_1_PAD_Art_Enhanc = st.number_input(
                                    "2nd_FU_Target Lesion 1 PAD Art Enhanc",
                                    step=0.1,
                                    value=float(df.iloc[0]["FU2_TL1PAD"]) if pd.notnull(df.iloc[0]["FU2_TL1PAD"]) and df.iloc[0]["FU2_TL1PAD"] != "" else 0.0,
                                )

                                FU2_Target_Lesion_1_CCD_Art_Enhanc = st.number_input(
                                    "2nd_FU_Target Lesion 1 CCD Art Enhanc",
                                    step=0.1,
                                    value=float(df.iloc[0]["FU2_TL1CCD"]) if pd.notnull(df.iloc[0]["FU2_TL1CCD"]) and df.iloc[0]["FU2_TL1CCD"] != "" else 0.0,
                                )
                                FU2_Target_Lesion_2_Segments = st.selectbox(
                                   "2nd_FU_Target Lesion 2 Segments [Excel : FU2_TL2SEG]",
                                    options=["1", "2", "3", "4a", "4b", "5", "6", "7", "8", "NA"],
                                    index=["1", "2", "3", "4a", "4b", "5", "6", "7", "8", "NA"].index(df.iloc[0]["FU2_TL2SEG"]) if df.iloc[0]["FU2_TL2SEG"] else None,
                                    placeholder="Choose an option",
                                )

                                FU2_Target_Lesion_2_LAD_Art_Enhanc = st.number_input(
                                    "2nd_FU_Target Lesion 2 LAD Art Enhanc",
                                    step=0.1,
                                    value=float(df.iloc[0]["FU2_TL2LAD"]) if pd.notnull(df.iloc[0]["FU2_TL2LAD"]) and df.iloc[0]["FU2_TL2LAD"] != "" else 0.0,
                                )

                                FU2_Target_Lesion_2_PAD_Art_Enhanc = st.number_input(
                                    "2nd_FU_Target Lesion 2 PAD Art Enhanc",
                                    step=0.1,
                                    value=float(df.iloc[0]["FU2_TL2PAD"]) if pd.notnull(df.iloc[0]["FU2_TL2PAD"]) and df.iloc[0]["FU2_TL2PAD"] != "" else 0.0,
                                )

                                FU2_Target_Lesion_2_CCD_Art_Enhanc = st.number_input(
                                    "2nd_FU_Target Lesion 2 CCD Art Enhanc",
                                    step=0.1,
                                    value=float(df.iloc[0]["FU2_TL2CCD"]) if pd.notnull(df.iloc[0]["FU2_TL2CCD"]) and df.iloc[0]["FU2_TL2CCD"] != "" else 0.0,
                                )

                                FU2_Follow_up_2_targeted_Lesion_Dia_Sum = max(FU2_Target_Lesion_1_CCD_Art_Enhanc, FU2_Target_Lesion_1_PAD_Art_Enhanc, FU2_Target_Lesion_1_LAD_Art_Enhanc) + max(FU2_Target_Lesion_2_CCD_Art_Enhanc, FU2_Target_Lesion_2_PAD_Art_Enhanc, FU2_Target_Lesion_2_LAD_Art_Enhanc)
                                st.write("2nd_FU_Follow up 2 targeted Lesion Dia Sum",FU2_Follow_up_2_targeted_Lesion_Dia_Sum)
                                
                                FU2_Non_Target_Lesion_1_LAD_Art_Enhanc = st.number_input(
                                    "2nd_FU_Non-Target Lesion 1 LAD Art Enhanc",
                                    step=0.1,
                                    value=float(df.iloc[0]["FU2_NTL1LAD"]) if pd.notnull(df.iloc[0]["FU2_NTL1LAD"]) and df.iloc[0]["FU2_NTL1LAD"] != "" else 0.0,
                                )

                                FU2_Non_Target_Lesion_1_PAD_Art_Enhanc = st.number_input(
                                    "2nd_FU_Non-Target Lesion 1 PAD Art Enhanc",
                                    step=0.1,
                                    value=float(df.iloc[0]["FU2_NTL1PAD"]) if pd.notnull(df.iloc[0]["FU2_NTL1PAD"]) and df.iloc[0]["FU2_NTL1PAD"] != "" else 0.0,
                                )

                                FU2_Non_Target_Lesion_1_CCD_Art_Enhanc = st.number_input(
                                    "2nd_FU_Non-Target Lesion 1 CCD Art Enhanc",
                                    step=0.1,
                                    value=float(df.iloc[0]["FU2_NTL1CCD"]) if pd.notnull(df.iloc[0]["FU2_NTL1CCD"]) and df.iloc[0]["FU2_NTL1CCD"] != "" else 0.0,
                                )

                                FU2_Non_targeted_Lesion_Dia_Sum = max(FU2_Non_Target_Lesion_1_LAD_Art_Enhanc, FU2_Non_Target_Lesion_1_PAD_Art_Enhanc, FU2_Non_Target_Lesion_1_CCD_Art_Enhanc)
                                st.write("2nd_FU_Non-targeted Lesion Dia Sum",FU2_Non_targeted_Lesion_Dia_Sum)
                                
                                FU2_Lesion_Necrosis = st.selectbox(
                                    "2nd_FU_Lesion Necrosis  [Excel : FU2_NEC]\n\n Yes (1), No (0), NA",
                                    options=["1", "0", "NA"],
                                    format_func=lambda x: {
                                            "1": "Yes",
                                            "0": "No",
                                            "NA": "NA"
                                        }[x],
                                    index=["1", "0", "NA"].index(df.iloc[0]["FU2_NECROSIS"]) if df.iloc[0]["FU2_NECROSIS"] else None,
                                    placeholder="Choose an option",
                                )

                                FU2_Reviewers_Initials = st.text_input(
                                    "2nd_FU_Reviewers Initials",
                                    help="Free-text input for reviewer name",
                                    value=df.iloc[0]["FU2_REV"],
                                )

                                
                                FU2_Non_target_lesion_response = st.selectbox(
                                    "2nd_FU_Non target lesion response[Excel : FU2_NTLRSP]\n\n Yes (1), No (0), NA",
                                    options=["1", "0", "NA"],
                                    format_func=lambda x: {
                                            "1": "Yes",
                                            "0": "No",
                                            "NA": "NA"
                                        }[x],
                                    index=["1", "0", "NA"].index(df.iloc[0]["FU2_NTLRSP"]) if df.iloc[0]["FU2_NTLRSP"] else None,
                                    placeholder="Choose an option",
                                )

                                FU2_New_Lesions = st.selectbox(
                                    "2nd_FU_New Lesions[Excel : FU2_NEWLES]\n\n Yes (1), No (0), NA",
                                    options=["1", "0", "NA"],
                                    format_func=lambda x: {
                                            "1": "Yes",
                                            "0": "No",
                                            "NA": "NA"
                                        }[x],
                                    index=["1", "0", "NA"].index(df.iloc[0]["FU2_NEWLES"]) if df.iloc[0]["FU2_NEWLES"] else None,
                                    placeholder="Choose an option",
                                )

                                FU2_NEW_Extrahepatic_Disease = st.selectbox(
                                    "2nd_FU_NEW Extrahepatic Disease[Excel : FU2_EHD]\n\n Yes (1), No (0), NA",
                                    options=["1", "0", "NA"],
                                    format_func=lambda x: {
                                            "1": "Yes",
                                            "0": "No",
                                            "NA": "NA"
                                        }[x],
                                    index=["1", "0", "NA"].index(df.iloc[0]["FU2_EHD"]) if df.iloc[0]["FU2_EHD"] else None,
                                    placeholder="Choose an option",
                                )

                                FU2_NEW_Extrahepatic_Dz_Location = st.text_input(
                                    "2nd_FU_NEW Extrahepatic Dz Location",
                                    help="Free text",
                                    value=df.iloc[0]["FU2_EHDLOC"],
                                )

                                FU2_NEW_Extrahepatic_Dz_Date = st.date_input(
                                    "2nd_FU_NEW Extrahepatic Dz Date",
                                    value=datetime.strptime(df.iloc[0]["FU2_EHDDATE"], "%Y-%m-%d").date() if df.iloc[0]["FU2_EHDDATE"] else None,
                                )

                                FU2_change_non_target_lesion = 0 if PREY90_Non_targeted_Lesion_Dia_Sum == "NA" else ((PREY90_Non_targeted_Lesion_Dia_Sum - FU2_Non_targeted_Lesion_Dia_Sum) / max(1,PREY90_pretx_targeted_Lesion_Dia_Sum))*100
                                st.write("2nd_FU_% change for non target lesion",FU2_change_non_target_lesion)
                                FU2_change_target_lesion = ((PREY90_pretx_targeted_Lesion_Dia_Sum - FU2_Follow_up_2_targeted_Lesion_Dia_Sum) / max(1,PREY90_pretx_targeted_Lesion_Dia_Sum)) * 100
                                st.write("2nd_FU_% Change Target Dia",FU2_change_target_lesion)
                                
                                second_fu_mrecist_calc = mrecist_local(FU2_change_target_lesion)
                                st.write("2nd_FU_mRECIST Calc", second_fu_mrecist_calc)
                                second_fu_mrecist_localized = mrecist_calc(FU2_change_target_lesion, FU2_Follow_up_2_targeted_Lesion_Dia_Sum, FU_Follow_up_1_targeted_Lesion_Dia_Sum)
                                st.write("2nd_FU_mRECIST LOCALIZED", second_fu_mrecist_localized)
                                second_fu_mrecist_overall = mrecist_overall(FU2_New_Lesions, FU2_NEW_Extrahepatic_Disease, FU2_change_non_target_lesion, FU2_change_target_lesion)
                                st.write("2nd_FU_mRECIST Overall", second_fu_mrecist_overall)

                                FU2_Free_Text = st.text_area(
                                    "2nd_FU_Free Text",
                                    help="Free text",
                                    value = df.iloc[0]["FU2_FT"]
                                )
                                st.subheader("Imaging_3rd_Followup")
                                FU3_Scan_Modality = st.selectbox(
                                    "3rd_FU_Scan Modality[Excel : FU3_MOD]\n\n(1) CT, (2) MRI",
                                        options=["1","2"],
                                        format_func=lambda x: {
                                            "1": "CT",
                                            "2": "MRI",
                                        }[x],
                                    index=["1", "2"].index(df.iloc[0]["FU3_MOD"]) if df.iloc[0]["FU3_MOD"] else None,
                                    placeholder="Choose an option",
                                )

                                FU3_Imaging_Date = st.date_input(
                                    "3rd_FU_Imaging Date",
                                    value=datetime.strptime(df.iloc[0]["FU3_IMG_DATE"], "%Y-%m-%d").date()
                                    if df.iloc[0]["FU3_IMG_DATE"] else None
                                )
                                FU3_Months_Since_Y90 = relativedelta(FU3_Imaging_Date, fetch_date).months
                                st.write("3rd_FU_Months Since Y90",FU3_Months_Since_Y90)
                                
                                FU3_Total_number_of_lesions = st.selectbox(
                                    "3rd_FU_Total number of lesions[Excel : FU3_TOTLES]\n\n(1) 1,(2) 2,(3) >=3",
                                 options=["1", "2", "3"],
                            format_func=lambda x: {
                                            "1": "1",
                                            "2": "2",
                                            "3" : ">=3"
                                        }[x],
                                    index=["1", "2", "3"].index(df.iloc[0]["FU3_TOTLES"]) if df.iloc[0]["FU3_TOTLES"] else None,
                                    placeholder="Choose an option",
                                )

                                FU3_Target_Lesion_1_LAD_Art_Enhanc = st.number_input(
                                    "3rd_FU_Target Lesion 1 LAD Art Enhanc",
                                    step=0.1,
                                    value=float(df.iloc[0]["FU3_TL1LAD"]) if pd.notnull(df.iloc[0]["FU3_TL1LAD"]) and df.iloc[0]["FU3_TL1LAD"] != "" else 0.0
                                )

                                FU3_Target_Lesion_1_PAD_Art_Enhanc = st.number_input(
                                    "3rd_FU_Target Lesion 1 PAD Art Enhanc",
                                    step=0.1,
                                    value=float(df.iloc[0]["FU3_TL1PAD"]) if pd.notnull(df.iloc[0]["FU3_TL1PAD"]) and df.iloc[0]["FU3_TL1PAD"] != "" else 0.0
                                )

                                FU3_Target_Lesion_1_CCD_Art_Enhanc = st.number_input(
                                    "3rd_FU_Target Lesion 1 CCD Art Enhanc",
                                    step=0.1,
                                    value=float(df.iloc[0]["FU3_TL1CCD"]) if pd.notnull(df.iloc[0]["FU3_TL1CCD"]) and df.iloc[0]["FU3_TL1CCD"] != "" else 0.0
                                )

                                FU3_Target_Lesion_2_Segments = st.selectbox(
                                    "3rd_FU_Target Lesion 2 Segments [Excel : FU3_TL2SEG]",
                                    options=["1", "2", "3", "4a", "4b", "5", "6", "7", "8", "NA"],
                                    index=["1", "2", "3", "4a", "4b", "5", "6", "7", "8", "NA"].index(df.iloc[0]["FU3_TL2SEG"]) if df.iloc[0]["FU3_TL2SEG"] else None,
                                    placeholder="Choose an option",
                                )

                                FU3_Target_Lesion_2_LAD_Art_Enhanc = st.number_input(
                                    "3rd_FU_Target Lesion 2 LAD Art Enhanc",
                                    step=0.1,
                                    value=float(df.iloc[0]["FU3_TL2LAD"]) if pd.notnull(df.iloc[0]["FU3_TL2LAD"]) and df.iloc[0]["FU3_TL2LAD"] != "" else 0.0
                                )

                                FU3_Target_Lesion_2_PAD_Art_Enhanc = st.number_input(
                                    "3rd_FU_Target Lesion 2 PAD Art Enhanc",
                                    step=0.1,
                                    value=float(df.iloc[0]["FU3_TL2PAD"]) if pd.notnull(df.iloc[0]["FU3_TL2PAD"]) and df.iloc[0]["FU3_TL2PAD"] != "" else 0.0
                                )

                                FU3_Target_Lesion_2_CCD_Art_Enhanc = st.number_input(
                                    "3rd_FU_Target Lesion 2 CCD Art Enhanc",
                                    step=0.1,
                                    value=float(df.iloc[0]["FU3_TL2CCD"]) if pd.notnull(df.iloc[0]["FU3_TL2CCD"]) and df.iloc[0]["FU3_TL2CCD"] != "" else 0.0
                                )

                                FU3_Follow_up_2_targeted_Lesion_Dia_Sum = max(FU3_Target_Lesion_1_CCD_Art_Enhanc, FU3_Target_Lesion_1_PAD_Art_Enhanc, FU3_Target_Lesion_1_LAD_Art_Enhanc) + max(FU3_Target_Lesion_2_CCD_Art_Enhanc, FU3_Target_Lesion_2_PAD_Art_Enhanc, FU3_Target_Lesion_2_LAD_Art_Enhanc)
                                st.write("3rd_FU_Follow up 3 targeted Lesion Dia Sum",FU3_Follow_up_2_targeted_Lesion_Dia_Sum)
                                
                                FU3_Non_Target_Lesion_1_LAD_Art_Enhanc = st.number_input(
                                    "3rd_FU_Non-Target Lesion 1 LAD Art Enhanc",
                                    step=0.1,
                                    value=float(df.iloc[0]["FU3_NTL1LAD"]) if pd.notnull(df.iloc[0]["FU3_NTL1LAD"]) and df.iloc[0]["FU3_NTL1LAD"] != "" else 0.0
                                )

                                FU3_Non_Target_Lesion_1_PAD_Art_Enhanc = st.number_input(
                                    "3rd_FU_Non-Target Lesion 1 PAD Art Enhanc",
                                    step=0.1,
                                    value=float(df.iloc[0]["FU3_NTL1PAD"]) if pd.notnull(df.iloc[0]["FU3_NTL1PAD"]) and df.iloc[0]["FU3_NTL1PAD"] != "" else 0.0
                                )

                                FU3_Non_Target_Lesion_1_CCD_Art_Enhanc = st.number_input(
                                    "3rd_FU_Non-Target Lesion 1 CCD Art Enhanc",
                                    step=0.1,
                                    value=float(df.iloc[0]["FU3_NTL1CCD"]) if pd.notnull(df.iloc[0]["FU3_NTL1CCD"]) and df.iloc[0]["FU3_NTL1CCD"] != "" else 0.0
                                )

                                FU3_Non_targeted_Lesion_Dia_Sum = max(FU3_Non_Target_Lesion_1_LAD_Art_Enhanc, FU3_Non_Target_Lesion_1_PAD_Art_Enhanc, FU3_Non_Target_Lesion_1_CCD_Art_Enhanc)
                                st.write("3rd_FU_Non-targeted Lesion Dia Sum",FU3_Non_targeted_Lesion_Dia_Sum)

                                FU3_Lesion_Necrosis = st.selectbox(
                                    "3rd_FU_Lesion Necrosis[Excel : FU3_NEC]\n\n Yes (1), No (0), NA",
                                    options=["1", "0", "NA"],
                                    format_func=lambda x: {
                                            "1": "Yes",
                                            "0": "No",
                                            "NA": "NA"
                                        }[x],
                                         index=["1", "0", "NA"].index(df.iloc[0]["FU3_NEC"]) if df.iloc[0]["FU3_NEC"] else None,
                                    placeholder="Choose an option",
                                )

                                FU3_Reviewers_Initials = st.text_input(
                                    "3rd_FU_Reviewers Initials",
                                    help="Free-text input for reviewer name",
                                    value=df.iloc[0]["FU3_REV"]
                                )

                                FU3_Non_target_lesion_response = st.selectbox(
                                    "3rd_FU_Non target lesion response[Excel : FU3_NTLRSP]\n\n Yes (1), No (0), NA",
                                    options=["1", "0", "NA"],
                                    format_func=lambda x: {
                                            "1": "Yes",
                                            "0": "No",
                                            "NA": "NA"
                                        }[x],
                                    index=["1", "0", "NA"].index(df.iloc[0]["FU3_NTLRSP"]) if df.iloc[0]["FU3_NTLRSP"] else None,
                                    placeholder="Choose an option",
                                )

                                FU3_New_Lesions = st.selectbox(
                                    "3rd_FU_New Lesions[Excel : FU3_NEWLES]\n\n Yes (1), No (0), NA",
                                    options=["1", "0", "NA"],
                                    format_func=lambda x: {
                                            "1": "Yes",
                                            "0": "No",
                                            "NA": "NA"
                                        }[x],
                                    index=["1", "0", "NA"].index(df.iloc[0]["FU3_NEWLES"]) if df.iloc[0]["FU3_NEWLES"] else None,
                                    placeholder="Choose an option",
                                )

                                FU3_NEW_Extrahepatic_Disease = st.selectbox(
                                     "3rd_FU_NEW Extrahepatic Disease[Excel : FU3_EHD]\n\n Yes (1), No (0), NA",
                                    options=["1", "0", "NA"],
                                    format_func=lambda x: {
                                            "1": "Yes",
                                            "0": "No",
                                            "NA": "NA"
                                        }[x],
                                    index=["1", "0", "NA"].index(df.iloc[0]["FU3_EHD"]) if df.iloc[0]["FU3_EHD"] else None,
                                    placeholder="Choose an option",
                                )

                                FU3_NEW_Extrahepatic_Dz_Location = st.text_input(
                                    "3rd_FU_NEW Extrahepatic Dz Location",
                                    help="Free text",
                                    value=df.iloc[0]["FU3_EHDLOC"]
                                )

                                FU3_NEW_Extrahepatic_Dz_Date = st.date_input(
                                    "3rd_FU_NEW Extrahepatic Dz Date",
                                    value=datetime.strptime(df.iloc[0]["FU3_EHDDATE"], "%Y-%m-%d").date() if df.iloc[0]["FU3_EHDDATE"] else None
                                )

                                FU3_change_non_target_lesion = 0 if PREY90_Non_targeted_Lesion_Dia_Sum == 'NA' else ((PREY90_Non_targeted_Lesion_Dia_Sum - FU3_Non_targeted_Lesion_Dia_Sum) / max(1,PREY90_pretx_targeted_Lesion_Dia_Sum))*100
                                st.write("3rd_FU_% change for non target lesion",FU3_change_non_target_lesion)
                                FU3_change_target_lesion = ((PREY90_pretx_targeted_Lesion_Dia_Sum - FU3_Follow_up_2_targeted_Lesion_Dia_Sum) / max(1,PREY90_pretx_targeted_Lesion_Dia_Sum)) * 100
                                st.write("3rd_FU_% Change Target Dia",FU3_change_target_lesion)
                                third_fu_mrecist_calc = mrecist_local(FU3_change_target_lesion)
                                st.write("3rd_FU_mRECIST Calc",third_fu_mrecist_calc)

                                third_fu_mrecist_localized = mrecist_calc(FU3_change_target_lesion, FU3_Follow_up_2_targeted_Lesion_Dia_Sum, FU_Follow_up_1_targeted_Lesion_Dia_Sum)
                                st.write("3rd_FU_mRECIST LOCALIZED",third_fu_mrecist_localized)
                                third_fu_mrecist_overall = mrecist_overall (FU3_New_Lesions, FU3_NEW_Extrahepatic_Disease, FU3_change_non_target_lesion, FU3_change_target_lesion)
                                st.write("3rd_FU_mRECIST Overall", third_fu_mrecist_overall)

                                FU3_Free_Text = st.text_area(
                                    "3rd_FU_Free Text",
                                    help="Free text",
                                    value=df.iloc[0]["FU3_FT"]
                                )
                                # 4th Imaging Follow-up
                                st.subheader("Imaging_4th_Followup")

                                FU4_Scan_Modality = st.selectbox(
                                    "4th_FU_Scan Modality [Excel : FU4_MOD]\n\n(1) CT, (2) MRI",
                                        options=["1","2"],
                                        format_func=lambda x: {
                                            "1": "CT",
                                            "2": "MRI",
                                        }[x],
                        index=["1", "2"].index(df.iloc[0]["FU4_MOD"]) if df.iloc[0]["FU4_MOD"] else None, 
                        placeholder="Choose an option",
                                )

                                FU4_Imaging_Date = st.date_input("4th_FU_Imaging Date",value = datetime.strptime(df.iloc[0]["FU4_IMG_DATE"], "%Y-%m-%d").date() if df.iloc[0]["FU4_IMG_DATE"] else None)

                                FU4_Months_Since_Y90 = relativedelta(FU4_Imaging_Date, fetch_date).months
                                st.write("4th_FU_Months Since Y90",FU4_Months_Since_Y90)
                                FU4_Total_number_of_lesions = st.selectbox(
                                    "4th_FU_Total number of lesions [Excel : FU4_TOTLES]\n\n(1) 1,(2) 2,(3) >=3",
                                 options=["1", "2", "3"],
                            format_func=lambda x: {
                                            "1": "1",
                                            "2": "2",
                                            "3" : ">=3"
                                        }[x],
                        index=["1", "2", "3"].index(df.iloc[0]["FU4_TOTLES"]) if df.iloc[0]["FU4_TOTLES"] else None,  # No default selection
                        placeholder="Choose an option",
                                )
                                FU4_Target_Lesion_1_LAD_Art_Enhanc = st.number_input(
                                    "4th_FU_Target Lesion 1 LAD Art Enhanc",
                                    step=0.1,value = float(df.iloc[0]["FU4_TL1LAD"]) if pd.notnull(df.iloc[0]["FU4_TL1LAD"]) and df.iloc[0]["FU4_TL1LAD"]!="" else 0.0
                                )
                                FU4_Target_Lesion_1_PAD_Art_Enhanc = st.number_input(
                                    "4th_FU_Target Lesion 1 PAD Art Enhanc",
                                    step=0.1,value = float(df.iloc[0]["FU4_TL1PAD"]) if pd.notnull(df.iloc[0]["FU4_TL1PAD"]) and df.iloc[0]["FU4_TL1PAD"] !="" else 0.0
                                )
                                FU4_Target_Lesion_1_CCD_Art_Enhanc = st.number_input(
                                    "4th_FU_Target Lesion 1 CCD Art Enhanc",
                                    step=0.1,value = float(df.iloc[0]["FU4_TL1CCD"]) if pd.notnull(df.iloc[0]["FU4_TL1CCD"]) and df.iloc[0]["FU4_TL1CCD"] !="" else 0.0
                                )
                                FU4_Target_Lesion_2_Segments = st.selectbox(
                                    "4th_FU_Target Lesion 2 Segments [Excel : FU4_TL2SEG]",
                                    options=["1", "2", "3", "4a", "4b", "5", "6", "7", "8", "NA"],
                        index=["1", "2", "3", "4a", "4b", "5", "6", "7", "8", "NA"].index(df.iloc[0]["FU4_TL2SEG"]) if df.iloc[0]["FU4_TL2SEG"] else None,
                        placeholder="Choose an option",
                                )
                                FU4_Target_Lesion_2_LAD_Art_Enhanc = st.number_input(
                                    "4th_FU_Target Lesion 2 LAD Art Enhanc",
                                    step=0.1,value = float(df.iloc[0]["FU4_TL2LAD"]) if pd.notnull(df.iloc[0]["FU4_TL2LAD"]) and df.iloc[0]["FU4_TL2LAD"] !="" else 0.0
                                )
                                FU4_Target_Lesion_2_PAD_Art_Enhanc = st.number_input(
                                    "4th_FU_Target Lesion 2 PAD Art Enhanc",
                                    step=0.1,value = float(df.iloc[0]["FU4_TL2PAD"]) if pd.notnull(df.iloc[0]["FU4_TL2PAD"]) and df.iloc[0]["FU4_TL2PAD"] !="" else 0.0
                                )

                                FU4_Target_Lesion_2_CCD_Art_Enhanc = st.number_input(
                                    "4th_FU_Target Lesion 2 CCD Art Enhanc",
                                    step=0.1,value = float(df.iloc[0]["FU4_TL2CCD"]) if pd.notnull(df.iloc[0]["FU4_TL2CCD"]) and df.iloc[0]["FU4_TL2CCD"] !="" else 0.0
                                )

                                FU4_Follow_up_2_targeted_Lesion_Dia_Sum = max(FU4_Target_Lesion_1_CCD_Art_Enhanc, FU4_Target_Lesion_1_PAD_Art_Enhanc, FU4_Target_Lesion_1_LAD_Art_Enhanc) + max(FU4_Target_Lesion_2_CCD_Art_Enhanc, FU4_Target_Lesion_2_PAD_Art_Enhanc, FU4_Target_Lesion_2_LAD_Art_Enhanc)
                                st.write("4th_FU_Follow up 4 targeted Lesion Dia Sum",FU4_Follow_up_2_targeted_Lesion_Dia_Sum)
                                FU4_Non_Target_Lesion_1_LAD_Art_Enhanc = st.number_input(
                                    "4th_FU_Non-Target Lesion 1 LAD Art Enhanc",
                                    step=0.1, value=float(df.iloc[0]["FU4_NTL1LAD"]) if pd.notnull(df.iloc[0]["FU4_NTL1LAD"]) and df.iloc[0]["FU4_NTL1LAD"] != "" else 0.0
                                )

                                FU4_Non_Target_Lesion_1_PAD_Art_Enhanc = st.number_input(
                                    "4th_FU_Non-Target Lesion 1 PAD Art Enhanc",
                                    step=0.1, value=float(df.iloc[0]["FU4_NTL1PAD"]) if pd.notnull(df.iloc[0]["FU4_NTL1PAD"]) and df.iloc[0]["FU4_NTL1PAD"] != "" else 0.0
                                )

                                FU4_Non_Target_Lesion_1_CCD_Art_Enhanc = st.number_input(
                                    "4th_FU_Non-Target Lesion 1 CCD Art Enhanc",
                                    step=0.1, value=float(df.iloc[0]["FU4_NTL1CCD"]) if pd.notnull(df.iloc[0]["FU4_NTL1CCD"]) and df.iloc[0]["FU4_NTL1CCD"] != "" else 0.0
                                )

                                FU4_Non_targeted_Lesion_Dia_Sum = max(FU4_Non_Target_Lesion_1_LAD_Art_Enhanc, FU4_Non_Target_Lesion_1_PAD_Art_Enhanc, FU4_Non_Target_Lesion_1_CCD_Art_Enhanc)
                                st.write("4th_FU_Non-targeted Lesion Dia Sum",FU4_Non_targeted_Lesion_Dia_Sum)
                                FU4_Lesion_Necrosis = st.selectbox(
                                    "4th_FU_Lesion Necrosis  [Excel : FU4_NECROSIS]\n\n Yes (1), No (0), NA",
                                    options=["1", "0", "NA"],
                                    format_func=lambda x: {"1": "Yes", "0": "No", "NA": "NA"}[x],
                                    index=["1", "0", "NA"].index(df.iloc[0]["FU4_NECROSIS"]) if df.iloc[0]["FU4_NECROSIS"] else None,
                                    placeholder="Choose an option",
                                )

                                FU4_Reviewers_Initials = st.text_input(
                                    "4th_FU_Reviewers Initials",
                                    help="Free-text input for reviewer name",
                                    value=df.iloc[0]["FU4_REVFT"]
                                )

                                FU4_Non_target_lesion_response = st.selectbox(
                                    "4th_FU_Non target lesion response  [Excel : FU4_NTLRSP]\n\n Yes (1), No (0), NA",
                                    options=["1", "0", "NA"],
                                    format_func=lambda x: {"1": "Yes", "0": "No", "NA": "NA"}[x],
                                    index=["1", "0", "NA"].index(df.iloc[0]["FU4_NTLRSP"]) if df.iloc[0]["FU4_NTLRSP"] else None,
                                    placeholder="Choose an option",
                                )

                                FU4_New_Lesions = st.selectbox(
                                    "4th_FU_New Lesions  [Excel : FU4_NEWLESION]\n\n Yes (1), No (0), NA",
                                    options=["1", "0", "NA"],
                                    format_func=lambda x: {"1": "Yes", "0": "No", "NA": "NA"}[x],
                                    index=["1", "0", "NA"].index(df.iloc[0]["FU4_NEWLESION"]) if df.iloc[0]["FU4_NEWLESION"] else None,
                                    placeholder="Choose an option",
                                )

                                FU4_NEW_Extrahepatic_Disease = st.selectbox(
                                    "4th_FU_NEW Extrahepatic Disease  [Excel : FU4_NEWEHD]\n\n Yes (1), No (0), NA",
                                    options=["1", "0", "NA"],
                                    format_func=lambda x: {"1": "Yes", "0": "No", "NA": "NA"}[x],
                                    index=["1", "0", "NA"].index(df.iloc[0]["FU4_NEWEHD"]) if df.iloc[0]["FU4_NEWEHD"] else None,
                                    placeholder="Choose an option",
                                )

                                FU4_NEW_Extrahepatic_Dz_Location = st.text_input(
                                    "4th_FU_NEW Extrahepatic Dz Location",
                                    help="Free text",
                                    value=df.iloc[0]["FU4_EHDLOC"]
                                )

                                FU4_NEW_Extrahepatic_Dz_Date = st.date_input(
                                    "4th_FU_NEW Extrahepatic Dz Date",
                                    value=datetime.strptime(df.iloc[0]["FU4_EHDDATE"], "%Y-%m-%d").date() if df.iloc[0]["FU4_EHDDATE"] else None
                                )

                                FU4_change_non_target_lesion = 0 if PREY90_Non_targeted_Lesion_Dia_Sum == "NA" else ((PREY90_Non_targeted_Lesion_Dia_Sum - FU4_Non_targeted_Lesion_Dia_Sum) / max(1,PREY90_pretx_targeted_Lesion_Dia_Sum)) * 100
                                st.write("4th_FU_% change non target lesion",FU4_change_non_target_lesion)
                                FU4_change_target_lesion = ((PREY90_pretx_targeted_Lesion_Dia_Sum - FU4_Follow_up_2_targeted_Lesion_Dia_Sum) / max(1,PREY90_pretx_targeted_Lesion_Dia_Sum)) * 100
                                st.write("4th_FU_% Change target dia",FU4_change_target_lesion)
                                fourth_fu_mrecist_calc = mrecist_local(FU4_change_target_lesion)
                                st.write("4th_FU_mRECIST Calc",fourth_fu_mrecist_calc)
                                fourth_fu_mrecist_localized = mrecist_calc(FU4_change_target_lesion, FU4_Follow_up_2_targeted_Lesion_Dia_Sum, FU_Follow_up_1_targeted_Lesion_Dia_Sum)
                                st.write("4th_FU_mRECIST LOCALIZED",fourth_fu_mrecist_localized)
                                fourth_fu_mrecist_overall = mrecist_overall (FU4_New_Lesions, FU4_NEW_Extrahepatic_Disease, FU4_change_non_target_lesion, FU4_change_target_lesion)
                                st.write("4th_FU_mRECIST Overall", fourth_fu_mrecist_overall)
                                
                                FU4_Free_Text = st.text_area(
                                    "4th_FU_Free Text",
                                    help="Free text", value = df.iloc[0]["FU4_FT"]
                                )

                                # 5th Imaging Follow-up

                                st.subheader("Imaging_5th_Followup")
                                FU5_Scan_Modality = st.selectbox(
                                    "5th_FU_Scan Modality [Excel : FU5_MOD]\n\n(1) CT, (2) MRI",
                                    options=["1", "2"],
                                    format_func=lambda x: {"1": "CT", "2": "MRI"}[x],
                                    index=["1", "2"].index(df.iloc[0]["FU5_MOD"]) if df.iloc[0]["FU5_MOD"] else None,
                                    placeholder="Choose an option",
                                )

                                FU5_Imaging_Date = st.date_input("5th_FU_Imaging Date", value=datetime.strptime(df.iloc[0]["FU5_IMG_DATE"], "%Y-%m-%d").date() if df.iloc[0]["FU5_IMG_DATE"] else None)

                                FU5_Months_Since_Y90 = relativedelta(FU5_Imaging_Date, fetch_date).months
                                st.write("5th_FU_Months Since Y90",FU5_Months_Since_Y90)

                                FU5_Total_number_of_lesions = st.selectbox(
                                    "5th_FU_Total number of lesions [Excel : FU5_TOTLES]\n\n(1) 1, (2) 2, (3) >=3",
                                    options=["1", "2", "3"],
                                    format_func=lambda x: {"1": "1", "2": "2", "3": ">=3"}[x],
                                    index=["1", "2", "3"].index(df.iloc[0]["FU5_TOTLES"]) if df.iloc[0]["FU5_TOTLES"] else None,
                                    placeholder="Choose an option",
                                )

                                FU5_Target_Lesion_1_LAD_Art_Enhanc = st.number_input(
                                    "5th_FU_Target Lesion 1 LAD Art Enhanc",
                                    step=0.1, value=float(df.iloc[0]["FU5_TL1LAD"]) if pd.notnull(df.iloc[0]["FU5_TL1LAD"]) and df.iloc[0]["FU5_TL1LAD"] != "" else 0.0
                                )

                                FU5_Target_Lesion_1_PAD_Art_Enhanc = st.number_input(
                                    "5th_FU_Target Lesion 1 PAD Art Enhanc",
                                    step=0.1, value=float(df.iloc[0]["FU5_TL1PAD"]) if pd.notnull(df.iloc[0]["FU5_TL1PAD"]) and df.iloc[0]["FU5_TL1PAD"] != "" else 0.0
                                )

                                FU5_Target_Lesion_1_CCD_Art_Enhanc = st.number_input(
                                    "5th_FU_Target Lesion 1 CCD Art Enhanc",
                                    step=0.1, value=float(df.iloc[0]["FU5_TL1CCD"]) if pd.notnull(df.iloc[0]["FU5_TL1CCD"]) and df.iloc[0]["FU5_TL1CCD"] != "" else 0.0
                                )

                                FU5_Target_Lesion_2_Segments = st.selectbox(
                                    "5th_FU_Target Lesion 2 Segments [Excel : FU5_TL2SEG]",
                                    options=["1", "2", "3", "4a", "4b", "5", "6", "7", "8", "NA"],
                                    index=["1", "2", "3", "4a", "4b", "5", "6", "7", "8", "NA"].index(df.iloc[0]["FU5_TL2SEG"]) if df.iloc[0]["FU5_TL2SEG"] else None,
                                    placeholder="Choose an option",
                                )

                                FU5_Target_Lesion_2_LAD_Art_Enhanc = st.number_input(
                                    "5th_FU_Target Lesion 2 LAD Art Enhanc",
                                    step=0.1, value=float(df.iloc[0]["FU5_TL2LAD"]) if pd.notnull(df.iloc[0]["FU5_TL2LAD"]) and df.iloc[0]["FU5_TL2LAD"] != "" else 0.0
                                )

                                FU5_Target_Lesion_2_PAD_Art_Enhanc = st.number_input(
                                    "5th_FU_Target Lesion 2 PAD Art Enhanc",
                                    step=0.1, value=float(df.iloc[0]["FU5_TL2PAD"]) if pd.notnull(df.iloc[0]["FU5_TL2PAD"]) and df.iloc[0]["FU5_TL2PAD"] != "" else 0.0
                                )

                                FU5_Target_Lesion_2_CCD_Art_Enhanc = st.number_input(
                                    "5th_FU_Target Lesion 2 CCD Art Enhanc",
                                    step=0.1, value=float(df.iloc[0]["FU5_TL2CCD"]) if pd.notnull(df.iloc[0]["FU5_TL2CCD"]) and df.iloc[0]["FU5_TL2CCD"] != "" else 0.0
                                )

                                FU5_Follow_up_2_targeted_Lesion_Dia_Sum = max(FU5_Target_Lesion_1_CCD_Art_Enhanc, FU5_Target_Lesion_1_PAD_Art_Enhanc, FU5_Target_Lesion_1_LAD_Art_Enhanc) + max(FU5_Target_Lesion_2_CCD_Art_Enhanc, FU5_Target_Lesion_2_PAD_Art_Enhanc, FU5_Target_Lesion_2_LAD_Art_Enhanc)
                                st.write("5th_FU_Follow up 4 targeted Lesion Dia Sum",FU5_Follow_up_2_targeted_Lesion_Dia_Sum)

                                FU5_Non_Target_Lesion_1_LAD_Art_Enhanc = st.number_input(
                                    "5th_FU_Non-Target Lesion 1 LAD Art Enhanc",
                                    step=0.1, value=float(df.iloc[0]["FU5_NTL1LAD"]) if pd.notnull(df.iloc[0]["FU5_NTL1LAD"]) and df.iloc[0]["FU5_NTL1LAD"] != "" else 0.0
                                )

                                FU5_Non_Target_Lesion_1_PAD_Art_Enhanc = st.number_input(
                                    "5th_FU_Non-Target Lesion 1 PAD Art Enhanc",
                                    step=0.1, value=float(df.iloc[0]["FU5_NTL1PAD"]) if pd.notnull(df.iloc[0]["FU5_NTL1PAD"]) and df.iloc[0]["FU5_NTL1PAD"] != "" else 0.0
                                )

                                FU5_Non_Target_Lesion_1_CCD_Art_Enhanc = st.number_input(
                                    "5th_FU_Non-Target Lesion 1 CCD Art Enhanc",
                                    step=0.1, value=float(df.iloc[0]["FU5_NTL1CCD"]) if pd.notnull(df.iloc[0]["FU5_NTL1CCD"]) and df.iloc[0]["FU5_NTL1CCD"] != "" else 0.0
                                )
                                FU5_Non_targeted_Lesion_Dia_Sum = max(FU5_Non_Target_Lesion_1_LAD_Art_Enhanc, FU5_Non_Target_Lesion_1_PAD_Art_Enhanc, FU5_Non_Target_Lesion_1_CCD_Art_Enhanc)
                                st.write("5th_FU_Non-targeted Lesion Dia Sum",FU5_Non_targeted_Lesion_Dia_Sum)
                                
                                FU5_Non_target_lesion_response = st.selectbox(
                                    "5th_FU_Non target lesion response [Excel : FU5_NTLRSP]\n\n Yes (1), No (0), NA",
                                    options=["1", "0", "NA"],
                                    format_func=lambda x: {"1": "Yes", "0": "No", "NA": "NA"}[x],
                                    index=["1", "0", "NA"].index(df.iloc[0]["FU5_NTLRSP"]) if df.iloc[0]["FU5_NTLRSP"] else None,
                                    placeholder="Choose an option",
                                )

                                FU5_New_Lesions = st.selectbox(
                                    "5th_FU_New Lesions [Excel : FU5_NEWLESION]\n\n Yes (1), No (0), NA",
                                    options=["1", "0", "NA"],
                                    format_func=lambda x: {"1": "Yes", "0": "No", "NA": "NA"}[x],
                                    index=["1", "0", "NA"].index(df.iloc[0]["FU5_NEWLESION"]) if df.iloc[0]["FU5_NEWLESION"] else None,
                                    placeholder="Choose an option",
                                )

                                FU5_NEW_Extrahepatic_Disease = st.selectbox(
                                    "5th_FU_NEW Extrahepatic Disease  [Excel : FU5_NEWEHD]\n\n Yes (1), No (0), NA",
                                    options=["1", "0", "NA"],
                                    format_func=lambda x: {"1": "Yes", "0": "No", "NA": "NA"}[x],
                                    index=["1", "0", "NA"].index(df.iloc[0]["FU5_NEWEHD"]) if df.iloc[0]["FU5_NEWEHD"] else None,
                                    placeholder="Choose an option",
                                )

                                FU5_NEW_Extrahepatic_Dz_Location = st.text_input(
                                    "5th_FU_NEW Extrahepatic Dz Location",
                                    help="Free text",
                                    value=df.iloc[0]["FU5_EHDLOC"]
                                )

                                FU5_NEW_Extrahepatic_Dz_Date = st.date_input(
                                    "5th_FU_NEW Extrahepatic Dz Date",
                                    value=datetime.strptime(df.iloc[0]["FU5_EHDDATE"], "%Y-%m-%d").date() if df.iloc[0]["FU5_EHDDATE"] else None
                                )

                                FU5_change_non_target_lesion = 0 if PREY90_Non_targeted_Lesion_Dia_Sum == 'NA' else ((PREY90_Non_targeted_Lesion_Dia_Sum - FU5_Non_targeted_Lesion_Dia_Sum) / max(0.1,PREY90_pretx_targeted_Lesion_Dia_Sum)) * 100
                                st.write("5th_FU_% change non target lesion ",FU5_change_non_target_lesion)
                                FU5_change_target_lesion = ((PREY90_pretx_targeted_Lesion_Dia_Sum - FU5_Follow_up_2_targeted_Lesion_Dia_Sum) / max(0.1,PREY90_pretx_targeted_Lesion_Dia_Sum)) * 100
                                st.write("5th_FU_% Change target dia",FU5_change_target_lesion)
                                fifth_fu_mrecist_calc = mrecist_local(FU5_change_target_lesion)
                                st.write("5th_FU_mRECIST Calc",fifth_fu_mrecist_calc)

                                fifth_fu_mrecist_localized = mrecist_calc(FU5_change_target_lesion, FU5_Follow_up_2_targeted_Lesion_Dia_Sum, FU_Follow_up_1_targeted_Lesion_Dia_Sum)
                                st.write("5th_FU_mRECIST LOCALIZED",fifth_fu_mrecist_localized)
                                fifth_fu_mrecist_overall = mrecist_overall (FU5_New_Lesions, FU5_NEW_Extrahepatic_Disease, FU5_change_non_target_lesion, FU5_change_target_lesion)
                                st.write("5th_FU_mRECIST Overall", fifth_fu_mrecist_overall)
                                
                                FU5_Free_Text = st.text_area(
                                    "5th_FU_Free Text",
                                    help="Free text", value = df.iloc[0]["FU5_FT"]
                                )
                               
                                st.subheader("Imaging_Dates for OS or PFS")

                                dead = st.selectbox(
                                        "Dead [Excel : DEAD]\n\n Yes (1), No (0)",
                                options=[0, 1],
                                format_func=lambda x:{
                                        0:"No",
                                        1:"Yes"
                                }[x],
                                        index=[0, 1].index(int(df.iloc[0]["DEAD"])) if df.iloc[0]["DEAD"] else None,
                                        placeholder="Choose an option",
                                )

                                Date_of_Death = st.date_input("Date of Death",value = datetime.strptime(df.iloc[0]["DATE_DEAD"], "%Y-%m-%d").date() if df.iloc[0]["DATE_DEAD"] != "NA" and df.iloc[0]["DATE_DEAD"] != "" else None)
                                Time_to_Death = None
                                if dead == 0:
                                    Date_of_Death = 'NA'
                                    Time_to_Death = 'NA'
                                else :
                                    Time_to_Death = relativedelta(Date_of_Death, fetch_date).months
                                st.write("Time to Death",Time_to_Death)

                                OLT = st.selectbox(
                                        "OLT [Excel : OLT]\n\n Yes (1), No (0)",
                                options=[0, 1],
                                format_func=lambda x:{
                                        0:"No",
                                        1:"Yes"
                                }[x],
                                        index=[0, 1].index(int(df.iloc[0]["OLT"])) if df.iloc[0]["OLT"] else None, 
                                        placeholder="Choose an option",
                                )

                                Date_of_OLT = st.date_input("Date of OLT",value = datetime.strptime(df.iloc[0]["DATE_OLT"], "%Y-%m-%d").date() if df.iloc[0]["DATE_OLT"] != "NA" and df.iloc[0]["DATE_OLT"] != "" else None)
                                Time_to_OLT = None
                                if OLT == 0:
                                    Date_of_OLT = 'NA'
                                    Time_to_OLT = 'NA'
                                else:
                                    Time_to_OLT = relativedelta(Date_of_OLT, fetch_date).months
                                st.write("Time to OLT",Time_to_OLT)

                                Repeat_tx_post_Y90 = st.selectbox(
                                        "Repeat tx post Y90 [Excel : RTX]\n\n Yes (1), No (0)",
                                options=[0, 1],
                                format_func=lambda x:{
                                        0:"No",
                                        1:"Yes"
                                }[x],
                                        index=[0, 1].index(int(df.iloc[0]["RTX"])) if df.iloc[0]["RTX"] else None,  # No default selection
                                        placeholder="Choose an option",
                                )

                                Date_of_Repeat_tx_Post_Y90 = st.date_input("Date of Repeat tx Post Y90",value = datetime.strptime(df.iloc[0]["DATE_RTX"], "%Y-%m-%d").date() if df.iloc[0]["DATE_RTX"] != "NA" and df.iloc[0]["DATE_RTX"] != "" else None)
                                Time_to_Repeat_Tx_Post_Y90 = None
                                if Repeat_tx_post_Y90 == 0:
                                    Date_of_Repeat_tx_Post_Y90 = 'NA'
                                    Time_to_Repeat_Tx_Post_Y90 = 'NA'
                                else:
                                    Time_to_Repeat_Tx_Post_Y90 = relativedelta(Date_of_Repeat_tx_Post_Y90, fetch_date).months
                                st.write("Time to Repeat Tx Post Y90",Time_to_Repeat_Tx_Post_Y90)

                                Date_of_Localized_Progression = detect_first_progression(first_fu_mrecist_localized, second_fu_mrecist_localized, third_fu_mrecist_localized, fourth_fu_mrecist_localized, fifth_fu_mrecist_localized, FU2_Imaging_Date, FU3_Imaging_Date, FU4_Imaging_Date, FU5_Imaging_Date)
                                st.write("Date of Localized Progression",Date_of_Localized_Progression)
                                Time_to_localized_progression = None
                                if Date_of_Localized_Progression == "No Progression":
                                        Time_to_localized_progression = 'NA'
                                else:
                                        Time_to_localized_progression = relativedelta(Date_of_Localized_Progression, fetch_date).years
                                st.write("Time to localized progression",Time_to_localized_progression)

                                Date_of_Overall_Progression = detect_overall_progression(first_fu_mrecist_localized, first_fu_mrecist_overall, second_fu_mrecist_localized, second_fu_mrecist_overall, third_fu_mrecist_localized, third_fu_mrecist_overall, fourth_fu_mrecist_localized, fourth_fu_mrecist_overall, fifth_fu_mrecist_localized, fifth_fu_mrecist_overall, FU_Imaging_Date, FU2_Imaging_Date, FU3_Imaging_Date, FU4_Imaging_Date, FU5_Imaging_Date)
                                st.write("Date of Overall Progression", Date_of_Overall_Progression)
                                Time_to_overall_progression = None
                                if Date_of_Overall_Progression == "No Progression":
                                        Time_to_overall_progression = 'NA'
                                else:
                                        Time_to_overall_progression = relativedelta(Date_of_Overall_Progression, fetch_date).years
                                st.write("Time to Overall (Local or systemic) Progression",Time_to_overall_progression)
                                lfu = st.selectbox("Last Follow up [Excel : LFU]\n\n(1) Yes, (0) No", options=["0", "1"],
                                format_func=lambda x:{
                                        "0":"No",
                                        "1":"Yes"
                                    }[x],
                                index=None,  # No default selection
                                placeholder="Choose an option",)
                                Date_of_Last_Follow_up_last_imaging_date = st.date_input("Date of Last Follow-up/last imaging date",value = datetime.strptime(df.iloc[0]["DATE_LFU"], "%Y-%m-%d").date() if df.iloc[0]["DATE_LFU"] != "NA" and df.iloc[0]["DATE_LFU"] != ""else None)
                                Time_to_Last_Follow_up_last_imaging_date = None
                                if dead == 1 and OLT == 1 and Repeat_tx_post_Y90 == 1 and lfu == "0":
                                    Date_of_Last_Follow_up_last_imaging_date = 'NA'
                                    Time_to_Last_Follow_up_last_imaging_date = "NA"
                                else:
                                    Time_to_Last_Follow_up_last_imaging_date = relativedelta(Date_of_Last_Follow_up_last_imaging_date, fetch_date).years 

                                st.write("Time to Last follow up",Time_to_Last_Follow_up_last_imaging_date)
                                notes_free_text = st.text_input("Notes Free Text",value=df.iloc[0]["NOTES_FT"])

                                bestm_recist = determine_bestmrecist(first_fu_mrecist_localized, second_fu_mrecist_localized, third_fu_mrecist_localized, fourth_fu_mrecist_localized, fifth_fu_mrecist_localized)
                                st.write("BestmRECIST", bestm_recist)
                                date_bestm_recist = determine_bestmrecist_date(fifth_fu_mrecist_overall, first_fu_mrecist_overall, second_fu_mrecist_overall, third_fu_mrecist_overall, fourth_fu_mrecist_overall, fifth_fu_mrecist_localized, FU_Imaging_Date, FU2_Imaging_Date, FU3_Imaging_Date, FU4_Imaging_Date, FU5_Imaging_Date)
                                st.write("Date BestmRECIST",date_bestm_recist)
                                time_to_bestm_recist = "No Time" if date_bestm_recist == "No Date" else relativedelta(date_bestm_recist, fetch_date).months
                                st.write("Timeto_bestmRECIST", time_to_bestm_recist)
                                PERCHANGE_BEST_TTR = st.number_input("Percent change till best mRECIST 1st",step=0.1, value=float(df.iloc[0]["PERCHANGE_BEST_TTR"]) if pd.notnull(df.iloc[0]["PERCHANGE_BEST_TTR"]) and df.iloc[0]["PERCHANGE_BEST_TTR"] != "" else 0.0 )
                                def best_cr_noncr(value):
                                    if value == "CR":
                                            return 1
                                    elif value in ["PR", "PD", "SD"]:
                                        return 2
                                    else:
                                        return ""
                                bestm_recist_cr_vs_non_cr = best_cr_noncr(bestm_recist)
                                st.write("BestmRECISTCRvsNonCR", bestm_recist_cr_vs_non_cr)
                                def best_responce(value):
                                    if value in ["CR", "PR"]:
                                        return 1
                                    elif value in ["SD", "PD"]:
                                        return 2
                                    else:
                                        return ""
                                bestm_recist_r_vs_nr = best_responce(bestm_recist)
                                st.write("BestmRECISTRvsNR" ,bestm_recist_r_vs_nr)

                                DATE_BEST_MTR = st.date_input("Date of Best percent change (2)",value = datetime.strptime(df.iloc[0]["DATE_BEST_MTR"], "%Y-%m-%d").date() if df.iloc[0]["DATE_BEST_MTR"] != "NA" and df.iloc[0]["DATE_BEST_MTR"] != "" else None)
                                TIME_BEST_MRT = relativedelta(DATE_BEST_MTR, fetch_date).months
                                PERCHANGE_BEST_MTR = st.number_input("Best Overall percent change (2) ",step=0.1, value=float(df.iloc[0]["PERCHANGE_BEST_MTR"]) if pd.notnull(df.iloc[0]["PERCHANGE_BEST_MTR"]) and df.iloc[0]["PERCHANGE_BEST_MTR"] != "" else 0.0)

                                OS_Date = st.date_input("Overall Survival Date" ,value = datetime.strptime(df.iloc[0]["OS_Date"], "%Y-%m-%d").date() if df.iloc[0]["OS_Date"] != "NA" and df.iloc[0]["OS_Date"] != "" else None)
                                OS_Events = st.selectbox("Overall Survival Events [Excel : OS_Events]\n\n(1) Event: Death, (0) Censored: OLT, RTx, LFU",
                                    options=["1","0"],
                                    format_func=lambda x:{
                                                "0":"Event: Death",
                                                "1":"Censored: OLT, RTx, LFU"
                                        }[x],
                                index=["1","0"].index(df.iloc[0]["OS_Events"]) if df.iloc[0]["OS_Events"] else None,  # No default selection
                                placeholder="Choose an option",
                                )
                                OS_Time = relativedelta(OS_Date, fetch_date).months
                                OS_Reason = st.selectbox("Overall Survival Reaons [Excel : OS_Reason]\n\nDead = dead, OLT = liver transplant, RTx = repeat treatment, LFU = Loss to Follow up",
                                    options=["Dead","OLT", "RTx", "LFU"],
                                    format_func=lambda x:{
                                                "Dead":"dead",
                                                "OLT":"liver transplant",
                                                "RTx":"repeat treatment",
                                                "LFU":"Loss to Follow up"
                                        }[x],
                                index=["Dead","OLT", "RTx", "LFU"].index(df.iloc[0]["OS_Reason"]) if df.iloc[0]["OS_Reason"] else None,  # No default selection
                                placeholder="Choose an option",
                                )
                                #LPFS
                                LPFS_Date = st.date_input("Local Progression Free Survival Date",value = datetime.strptime(df.iloc[0]["LPFS_Date"], "%Y-%m-%d").date() if df.iloc[0]["LPFS_Date"] != "NA" and df.iloc[0]["LPFS_Date"] != "" else None)
                                LPFS_Events = st.selectbox("Local Progression Free Survival Event [Excel : LPFS_Events]\n\n(1) Event: Death, (0) Censored: OLT, RTx, LFU",
                                    options=["1","0"],
                                    format_func=lambda x:{
                                                "1":"Event: Death, LP(Local progression)",
                                                "0":"Censored: OLT, RTx, LFU"
                                        }[x],
                                index=["1","0"].index(df.iloc[0]["LPFS_Events"]) if df.iloc[0]["LPFS_Events"] else None,  # No default selection
                                placeholder="Choose an option",
                                )
                                LPFS_Time = relativedelta(LPFS_Date, fetch_date).months
                                LPFS_Reason = st.selectbox("Local Progression Free Survival Reason [Excel : LPFS_Reason]",
                                    options=["Dead"," LP(Local progression)", "OLT", "RTx", "LFU"],
                                index=["Dead"," LP(Local progression)", "OLT", "RTx", "LFU"].index(df.iloc[0]["LPFS_Reason"]) if df.iloc[0]["LPFS_Reason"] else None,  # No default selection
                                placeholder="Choose an option",
                                )
                                #PFS
                                PFS_Date = st.date_input("Progression Free Survival Date",value = datetime.strptime(df.iloc[0]["PFS_Date"], "%Y-%m-%d").date() if df.iloc[0]["PFS_Date"] != "NA" and df.iloc[0]["PFS_Date"] != "" else None)
                                PFS_Events = st.selectbox("Progression Free Survival Event [Excel : PFS_Events]\n\n(1) Event: Death, (0) Censored: OLT, RTx, LFU",
                                    options=["1","0"],
                                    format_func=lambda x:{
                                                "1":"Event: Death , OP (first time they progression)",
                                                "0":"Censored: OLT, RTx, LFU"
                                        }[x],
                                index=["1","0"].index(df.iloc[0]["PFS_Events"]) if df.iloc[0]["PFS_Events"] else None,  # No default selection
                                placeholder="Choose an option",
                                )
                                PFS_Time = relativedelta(PFS_Date, fetch_date).months
                                PFS_Reason = st.selectbox("Progression Free Survival Reason [Excel : PFS_Reason]\n\nDead = dead, OLT = liver transplant, RTx = repeat treatment, LFU = Loss to Follow up",
                                    options=["Dead","OP(Overall progression)" ,"OLT", "RTx", "LFU"],
                                index=["Dead","OP(Overall progression)" ,"OLT", "RTx", "LFU"].index(df.iloc[0]["PFS_Reason"]) if df.iloc[0]["PFS_Reason"] else None,  # No default selection
                                placeholder="Choose an option",
                                )
                                DOR = LPFS_Time if time_to_bestm_recist == "No Time" else LPFS_Time - time_to_bestm_recist



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
                                if Date_of_Last_Follow_up_last_imaging_date != None and Date_of_Last_Follow_up_last_imaging_date != "NA" :
                                    Date_of_Last_Follow_up_last_imaging_date = Date_of_Last_Follow_up_last_imaging_date.strftime("%Y-%m-%d")
                                if Date_of_Overall_Progression != None and Date_of_Overall_Progression != "No Progression" :
                                    Date_of_Overall_Progression = Date_of_Overall_Progression.strftime("%Y-%m-%d")
                                if Date_of_Localized_Progression != None and Date_of_Localized_Progression != "No Progression" :
                                    Date_of_Localized_Progression = Date_of_Localized_Progression.strftime("%Y-%m-%d")
                                if date_bestm_recist != None and date_bestm_recist != "No Date" :
                                    date_bestm_recist = date_bestm_recist.strftime("%Y-%m-%d")
                                if DATE_BEST_MTR != None and DATE_BEST_MTR != "":
                                    DATE_BEST_MTR = DATE_BEST_MTR.strftime("%Y-%m-%d")
                                if OS_Date != None and OS_Date != "":
                                    OS_Date = OS_Date.strftime("%Y-%m-%d")
                                if LPFS_Date != None and LPFS_Date != "":
                                    LPFS_Date = LPFS_Date.strftime("%Y-%m-%d")
                                if PFS_Date != None and PFS_Date != "":
                                    PFS_Date = PFS_Date.strftime("%Y-%m-%d")
                                submit_tab10 = st.form_submit_button("Submit")

                                if submit_tab10:
                                    
                                    data10={
                                    "PREY_MOD": PREY90_prescan_modality,
                                    "PREY_IMG_DATE": PREY90_Imaging_Date,
                                    "PREY_TOTLES": PREY90_total_number_of_lesions,
                                    "PREY_LOBES": PREY90_Number_Involved_Lobes,
                                    "PREY_TL1SEG": PREY90_target_lesion_1_segments,
                                    "PREY_TL1LAD": PREY90_TL1_LAD,
                                    "PREY_TL1PAD": PREY90_Target_Lesion_1_PAD,
                                    "PREY_TL1CCD": PREY90_Target_Lesion_1_CCD,
                                    "PREY_TL1VOL": PREY90_Target_Lesion_1_VOL,
                                    "PREY_TL2SEG": PREY90_Target_Lesion_2_segments,
                                    "PREY_TL2LAD": PREY90_Target_Lesion_2_LAD,
                                    "PREY_TL2PAD": PREY90_Target_Lesion_2_PAD,
                                    "PREY_TL2CCD": PREY90_Target_Lesion_2_CCD,
                                    "PREY_TL2VOL": PREY90_Target_Lesion_2_VOL,
                                    "PREY_TLDIA": PREY90_pretx_targeted_Lesion_Dia_Sum,
                                    "PREY_NTLOC": PREY90_Non_Target_Lesion_Location,
                                    "PREY_NTL1LAD": PREY90_Non_Target_Lesion_2_LAD_Art_Enhanc,
                                    "PREY_NTL1PAD": PREY90_Non_Target_Lesion_2_PAD_Art_Enhanc,
                                    "PREY_NTL1CCD": PREY90_Non_Target_Lesion_2_CCD_Art_Enhanc,
                                    "PREY_NTLDIA": PREY90_Non_targeted_Lesion_Dia_Sum,
                                    "PREY_REVFT": PREY90_Reviewers_Initials,
                                    "PREY_EHD": PREY90_Pre_Y90_Extrahepatic_Disease,
                                    "PREY_EHDLOCFT": PREY90_Pre_Y90_Extrahepatic_Disease_Location,
                                    "PREY_PVT": PREY90_PVT,
                                    "PREY_PVTLOC": PREY90_PVT_Location,
                                    "PREY_CIRRH": PREY90_Features_of_cirrhosis,
                                    "FU1_MOD": FU_Scan_Modality,
                                    "FU1_IMG_DATE": FU_Imaging_Date,
                                    "FU1_MS_Y90": FU_Months_Since_Y90,
                                    "FU1_TOTLES": FU_Total_number_of_lesions,
                                    "FU1_TL1LAD": FU_Target_Lesion_1_LAD_Art_Enhanc,
                                    "FU1_TL1PAD": FU_Target_Lesion_1_PAD_Art_Enhanc,
                                    "FU1_TL1CCD": FU_Target_Lesion_1_CCD_Art_Enhanc,
                                    "FU1_TL2SEG": FU_Target_Lesion_2_Segments,
                                    "FU1_TL2LAD": FU_Target_Lesion_2_LAD_Art_Enhanc,
                                    "FU1_TL2PAD": FU_Target_Lesion_2_PAD_Art_Enhanc,
                                    "FU1_TL2CCD": FU_Target_Lesion_2_CCD_Art_Enhanc,
                                    "FU1_TLDIA": FU_Follow_up_1_targeted_Lesion_Dia_Sum,
                                    "FU1_NTL1LAD": FU_Non_Target_Lesion_2_LAD_Art_Enhanc,
                                    "FU1_NTL1PAD": FU_Non_Target_Lesion_2_PAD_Art_Enhanc,
                                    "FU1_NTL1CCD": FU_Non_Target_Lesion_2_CCD_Art_Enhanc,
                                    "FU1_NTLDIA": FU_Non_targeted_Lesion_Dia_Sum,
                                    "FU1_NECROSIS": FU_Lesion_Necrosis,
                                    "FU1_REVFT": FU_Reviewers_Initials,
                                    "FU1_NTLRSP": FU_Non_target_lesion_response,
                                    "FU1_NEWLESION": FU_New_Lesions,
                                    "FU1_NEWEHD": FU_NEW_Extrahepatic_Disease,
                                    "FU1_EHDLOC": FU_NEW_Extrahepatic_Dz_Location,
                                    "FU1_EHDDATE": FU_NEW_Extrahepatic_Dz_Date,
                                    "FU1_NTCHG": FU_change_non_target_lesion,
                                    "FU1_TDCHG": FU_change_target_lesion,
                                    "FU1_MREC_LOCAL": first_fu_mrecist_localized,
                                    "FU1_MREC_OVERALL": first_fu_mrecist_overall,
                                    "FU1_FT": FU_Free_Text,
                                    "FU2_MOD": FU2_Scan_Modality,
                                    "FU2_IMG_DATE": FU2_Imaging_Date,
                                    "FU2_MS_Y90": FU2_Months_Since_Y90,
                                    "FU2_TOTLES": FU2_Total_number_of_lesions,
                                    "FU2_TL1LAD": FU2_Target_Lesion_1_LAD_Art_Enhanc,
                                    "FU2_TL1PAD": FU2_Target_Lesion_1_PAD_Art_Enhanc,
                                    "FU2_TL1CCD": FU2_Target_Lesion_1_CCD_Art_Enhanc,
                                    "FU2_TL2SEG": FU2_Target_Lesion_2_Segments,
                                    "FU2_TL2LAD": FU2_Target_Lesion_2_LAD_Art_Enhanc,
                                    "FU2_TL2PAD": FU2_Target_Lesion_2_PAD_Art_Enhanc,
                                    "FU2_TL2CCD": FU2_Target_Lesion_2_CCD_Art_Enhanc,
                                    "FU2_TLDIA": FU2_Follow_up_2_targeted_Lesion_Dia_Sum,
                                    "FU2_NTL1LAD": FU2_Non_Target_Lesion_1_LAD_Art_Enhanc,
                                    "FU2_NTL1PAD": FU2_Non_Target_Lesion_1_PAD_Art_Enhanc,
                                    "FU2_NTL1CCD": FU2_Non_Target_Lesion_1_CCD_Art_Enhanc,
                                    "FU2_NTLDIA": FU2_Non_targeted_Lesion_Dia_Sum,
                                    "FU2_NECROSIS": FU2_Lesion_Necrosis,
                                    "FU2_REV": FU2_Reviewers_Initials,
                                    "FU2_NTLRSP": FU2_Non_target_lesion_response,
                                    "FU2_NEWLES": FU2_New_Lesions,
                                    "FU2_EHD": FU2_NEW_Extrahepatic_Disease,
                                    "FU2_EHDLOC": FU2_NEW_Extrahepatic_Dz_Location,
                                    "FU2_EHDDATE": FU2_NEW_Extrahepatic_Dz_Date,
                                    "FU2_NTCHG": FU2_change_non_target_lesion,
                                    "FU2_TDCHG": FU2_change_target_lesion,
                                    "FU2_MREC_CALC": second_fu_mrecist_calc,
                                    "FU2_MREC_LOCAL": second_fu_mrecist_localized,
                                    "FU2_MREC_OVERALL": second_fu_mrecist_overall,
                                    "FU2_FT": FU2_Free_Text,
                                    "FU3_MOD": FU3_Scan_Modality,
                                    "FU3_IMG_DATE": FU3_Imaging_Date,
                                    "FU3_MS_Y90": FU3_Months_Since_Y90,
                                    "FU3_TOTLES": FU3_Total_number_of_lesions,
                                    "FU3_TL1LAD": FU3_Target_Lesion_1_LAD_Art_Enhanc,
                                    "FU3_TL1PAD": FU3_Target_Lesion_1_PAD_Art_Enhanc,
                                    "FU3_TL1CCD": FU3_Target_Lesion_1_CCD_Art_Enhanc,
                                    "FU3_TL2SEG": FU3_Target_Lesion_2_Segments,
                                    "FU3_TL2LAD": FU3_Target_Lesion_2_LAD_Art_Enhanc,
                                    "FU3_TL2PAD": FU3_Target_Lesion_2_PAD_Art_Enhanc,
                                    "FU3_TL2CCD": FU3_Target_Lesion_2_CCD_Art_Enhanc,
                                    "FU3_TLDIA": FU3_Follow_up_2_targeted_Lesion_Dia_Sum,
                                    "FU3_NTL1LAD": FU3_Non_Target_Lesion_1_LAD_Art_Enhanc,
                                    "FU3_NTL1PAD": FU3_Non_Target_Lesion_1_PAD_Art_Enhanc,
                                    "FU3_NTL1CCD": FU3_Non_Target_Lesion_1_CCD_Art_Enhanc,
                                    "FU3_NTLDIA": FU3_Non_targeted_Lesion_Dia_Sum,
                                    "FU3_NEC": FU3_Lesion_Necrosis,
                                    "FU3_REV": FU3_Reviewers_Initials,
                                    "FU3_NTLRSP": FU3_Non_target_lesion_response,
                                    "FU3_NEWLES": FU3_New_Lesions,
                                    "FU3_EHD": FU3_NEW_Extrahepatic_Disease,
                                    "FU3_EHDLOC": FU3_NEW_Extrahepatic_Dz_Location,
                                    "FU3_EHDDATE": FU3_NEW_Extrahepatic_Dz_Date,
                                    "FU3_NTCHG": FU3_change_non_target_lesion,
                                    "FU3_TDCHG": FU3_change_target_lesion,
                                    "FU3_MREC_CALC": third_fu_mrecist_calc,
                                    "FU3_MREC_LOCAL": third_fu_mrecist_localized,
                                    "FU3_MREC_OVERALL": third_fu_mrecist_overall,
                                    "FU3_FT": FU3_Free_Text,
                                    "FU4_MOD": FU4_Scan_Modality,
                                    "FU4_IMG_DATE": FU4_Imaging_Date,
                                    "FU4_MONTHS_Y90": FU4_Months_Since_Y90,
                                    "FU4_TOTLES": FU4_Total_number_of_lesions,
                                    "FU4_TL1LAD": FU4_Target_Lesion_1_LAD_Art_Enhanc,
                                    "FU4_TL1PAD": FU4_Target_Lesion_1_PAD_Art_Enhanc,
                                    "FU4_TL1CCD": FU4_Target_Lesion_1_CCD_Art_Enhanc,
                                    "FU4_TL2SEG": FU4_Target_Lesion_2_Segments,
                                    "FU4_TL2LAD": FU4_Target_Lesion_2_LAD_Art_Enhanc,
                                    "FU4_TL2PAD": FU4_Target_Lesion_2_PAD_Art_Enhanc,
                                    "FU4_TL2CCD": FU4_Target_Lesion_2_CCD_Art_Enhanc,
                                    "FU4_TL_DIASUM": FU4_Follow_up_2_targeted_Lesion_Dia_Sum,
                                    "FU4_NTL1LAD": FU4_Non_Target_Lesion_1_LAD_Art_Enhanc,
                                    "FU4_NTL1PAD": FU4_Non_Target_Lesion_1_PAD_Art_Enhanc,
                                    "FU4_NTL1CCD": FU4_Non_Target_Lesion_1_CCD_Art_Enhanc,
                                    "FU4_NTL_DIASUM": FU4_Non_targeted_Lesion_Dia_Sum,
                                    "FU4_NECROSIS": FU4_Lesion_Necrosis,
                                    "FU4_REVFT": FU4_Reviewers_Initials,
                                    "FU4_NTLRSP": FU4_Non_target_lesion_response,
                                    "FU4_NEWLESION": FU4_New_Lesions,
                                    "FU4_NEWEHD": FU4_NEW_Extrahepatic_Disease,
                                    "FU4_EHDLOC": FU4_NEW_Extrahepatic_Dz_Location,
                                    "FU4_EHDDATE": FU4_NEW_Extrahepatic_Dz_Date,
                                    "FU4_NTL_CHANGE": FU4_change_non_target_lesion,
                                    "FU4_TL_CHANGE": FU4_change_target_lesion,
                                    "FU4_MREC_CALC": fourth_fu_mrecist_calc,
                                    "FU4_MREC_LOCAL": fourth_fu_mrecist_localized,
                                    "FU4_MREC_OVERALL": fourth_fu_mrecist_overall,
                                    "FU4_FT": FU4_Free_Text,
                                    "FU5_MOD": FU5_Scan_Modality,
                                    "FU5_IMG_DATE": FU5_Imaging_Date,
                                    "FU5_MONTHS_Y90": FU5_Months_Since_Y90,
                                    "FU5_TOTLES": FU5_Total_number_of_lesions,
                                    "FU5_TL1LAD": FU5_Target_Lesion_1_LAD_Art_Enhanc,
                                    "FU5_TL1PAD": FU5_Target_Lesion_1_PAD_Art_Enhanc,
                                    "FU5_TL1CCD": FU5_Target_Lesion_1_CCD_Art_Enhanc,
                                    "FU5_TL2SEG": FU5_Target_Lesion_2_Segments,
                                    "FU5_TL2LAD": FU5_Target_Lesion_2_LAD_Art_Enhanc,
                                    "FU5_TL2PAD": FU5_Target_Lesion_2_PAD_Art_Enhanc,
                                    "FU5_TL2CCD": FU5_Target_Lesion_2_CCD_Art_Enhanc,
                                    "FU5_TL_DIASUM": FU5_Follow_up_2_targeted_Lesion_Dia_Sum,
                                    "FU5_NTL1LAD": FU5_Non_Target_Lesion_1_LAD_Art_Enhanc,
                                    "FU5_NTL1PAD": FU5_Non_Target_Lesion_1_PAD_Art_Enhanc,
                                    "FU5_NTL1CCD": FU5_Non_Target_Lesion_1_CCD_Art_Enhanc,
                                    "FU5_NTL_DIASUM": FU5_Non_targeted_Lesion_Dia_Sum,
                                    "FU5_NTLRSP": FU5_Non_target_lesion_response,
                                    "FU5_NEWLESION": FU5_New_Lesions,
                                    "FU5_NEWEHD": FU5_NEW_Extrahepatic_Disease,
                                    "FU5_EHDLOC": FU5_NEW_Extrahepatic_Dz_Location,
                                    "FU5_EHDDATE": FU5_NEW_Extrahepatic_Dz_Date,
                                    "FU5_NTL_CHANGE": FU5_change_non_target_lesion,
                                    "FU5_TL_CHANGE": FU5_change_target_lesion,
                                    "FU5_MREC_CALC": fifth_fu_mrecist_calc,
                                    "FU5_MREC_LOCAL": fifth_fu_mrecist_localized,
                                    "FU5_MREC_OVERALL": fifth_fu_mrecist_overall,
                                    "FU5_FT": FU5_Free_Text,
                                    
                                    "DEAD": dead,
                                    "DATE_DEAD": Date_of_Death if Date_of_Death != "NA" else Date_of_Death,
                                    "TIME_DEAD": Time_to_Death,
                                    "OLT": OLT,
                                    "DATE_OLT": Date_of_OLT if Date_of_OLT != "NA" else Date_of_OLT,
                                    "TIME_OLT": Time_to_OLT,
                                    "RTX": Repeat_tx_post_Y90,
                                    "DATE_RTX": Date_of_Repeat_tx_Post_Y90 if Date_of_Repeat_tx_Post_Y90 != 'NA' else Date_of_Repeat_tx_Post_Y90,
                                    "TIME_RTX": Time_to_Repeat_Tx_Post_Y90,
                                    "DATE_LOCALP": Date_of_Localized_Progression,
                                    "TIME_LOCALP" : Time_to_localized_progression,
                                    "DATE_OVERALLP" :Date_of_Overall_Progression,
                                    "TIME__OVERALLP" :Time_to_overall_progression,
                                    "LFU":lfu,
                                    "DATE_LFU": Date_of_Last_Follow_up_last_imaging_date,
                                    "TIME_LFU": Time_to_Last_Follow_up_last_imaging_date,
                                    "NOTES_FT" : notes_free_text,
                                    "BMRECIST" :bestm_recist,
                                    "DATE_BMREC_TTR":date_bestm_recist,
                                    "TIME_BMREC_TTR":time_to_bestm_recist,
                                    "PERCHANGE_BEST_TTR": PERCHANGE_BEST_TTR,
                                    "BM_CRVSNON":bestm_recist_cr_vs_non_cr,
                                    "MR_RVSNR":bestm_recist_r_vs_nr,
                                    "DATE_BEST_MTR":DATE_BEST_MTR,
                                    "TIME_BEST_MRT":TIME_BEST_MRT,
                                    "PERCHANGE_BEST_MTR":PERCHANGE_BEST_MTR,
                                    "OS_Date":OS_Date,
                                    "OS_Events":OS_Events,
                                    "OS_Time": OS_Time,
                                    "OS_Reason":OS_Reason,
                                    "LPFS_Date":LPFS_Date,
                                    "LPFS_Events":LPFS_Events,
                                    "LPFS_Time":LPFS_Time,
                                    "LPFS_Reason":LPFS_Reason,
                                    "PFS_Date" : PFS_Date,
                                    "PFS_Events":PFS_Events,
                                    "PFS_Time": PFS_Time,
                                    "PFS_Reason" : PFS_Reason,
                                    "DOR" : DOR,
                                    }
                                    update_google_sheet(data10, mrn)
                                            
                    elif st.session_state.selected_tab == "Dosimetry Data":
                        st.subheader("Dosimetry Data")
                        with st.form("dosimetry_data_form"):
                            trlnkid = st.selectbox(
                                "TRLNKID [Excel : TRLNKID]\n\n Tumor 1 (1), Tumor 2 (2)",
                                    options=["1", "2"],
                                    format_func=lambda x: {
                                            "1": "Tumor 1",
                                            "2": "Tumor 2",
                                        }[x],
                               
                                index=["1","2"].index(df.iloc[0]["TRLNKID"]) if df.iloc[0]["TRLNKID"] else None,
                            placeholder="Choose an option",
                            )
                            input_GTV_mean_dose = st.text_input("GTV mean dose",value = df.iloc[0]["GTV_MEANDOSE"])
                            input_Tx_vol_mean_dose = st.text_input("Tx vol mean dose",value = df.iloc[0]["TXVOL_MEANDOSE"])
                            input_Liver_Vol_Mean_dose = st.text_input("Liver Vol Mean dose",value = df.iloc[0]["LIVVOL__MEANDOSE"])
                            input_Healthy_Liver_mean_dose = st.text_input("Healthy Liver mean dose",value = df.iloc[0]["HEALTHYLIV_MEANDOSE"])
                            input_GTV_Vol = st.number_input("GTV Vol",step=0.1,value = float(df.iloc[0]["GTV_VOL"]) if pd.notnull(df.iloc[0]["GTV_VOL"]) and df.iloc[0]["GTV_VOL"] != "" else 0.0 )
                            input_Tx_vol = st.number_input("Tx vol",step=0.1,value = float(df.iloc[0]["TX_VOL"]) if pd.notnull(df.iloc[0]["TX_VOL"]) and df.iloc[0]["TX_VOL"] != "" else 0.0)
                            input_Liver_vol = st.number_input("Liver vol",step=0.1, min_value=0.1,value = float(df.iloc[0]["LIVER_VOL"]) if pd.notnull(df.iloc[0]["LIVER_VOL"]) and df.iloc[0]["LIVER_VOL"] != "" else 0.10)
                            input_Healthy_Liver_Vol = st.text_input("Healthy Liver Vol",value = df.iloc[0]["HEALTHYLIV_VOL"])
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
                            input_ActivityBq = st.number_input("ActivityBq",step=0.1, value = float(df.iloc[0]["ACTIVITYBQ"]) if pd.notnull(df.iloc[0]["ACTIVITYBQ"]) and df.iloc[0]["ACTIVITYBQ"] != "" else 0.0)
                            input_ActivityCi = (input_ActivityBq/37000000000.0)
                            input_Tx_vol_Activity_Density = (input_ActivityCi/max(0.10,input_Tx_vol))
                            input_ActivityCi = format(input_ActivityCi, ".5E")
                            st.write("ActivityCi", input_ActivityCi)
                            input_Tx_vol_Activity_Density = format(input_Tx_vol_Activity_Density, ".5E")
                            st.write("Tx vol Activity Density",input_Tx_vol_Activity_Density)
                            input_GTV_less_D95_Vol_ml = st.text_input("GTV < D95 Vol_ml",value = df.iloc[0]["GTVLT_D95VOL"])
                            input_GTV_less_D95_Mean_Dose = st.text_input("GTV < D95 Mean Dose",value = df.iloc[0]["GTVLT_D95MEAN"])
                            input_GTV_less_D95_Mx_Dose = st.text_input("GTV < D95 Max Dose",value = df.iloc[0]["GTVLT_D95MAX"])
                            input_GTV_less_D95_Min_Dose = st.text_input("GTV < D95 Min Dose",value = df.iloc[0]["GTVLT_D95MIN"])
                            input_GTV_less_D95_SD = st.text_input("GTV < D95 SD",value = df.iloc[0]["GTVLT_D95SD"])
                            input_GTV_less_D95_Vol_1 = st.text_input("GTV < D95 Vol_1",value = df.iloc[0]["V1_GTVLT_D95VOL"])
                            input_GTV_less_D95_Mean_Dose_1 = st.text_input("GTV < D95 Mean Dose_1",value = df.iloc[0]["V1_GTVLT_D95MEAN"])
                            input_GTV_less_D95_Min_Dose_1 = st.text_input("GTV < D95 Min Dose_1",value = df.iloc[0]["V1_GTVLT_D95MIN"])
                            input_GTV_less_D95_SD_1 = st.text_input("GTV < D95 SD_1",value = df.iloc[0]["V1_GTVLT_D95SD"])
                            input_GTV_less_D95_Vol_2 = st.text_input("GTV < D95 Vol_2",value = df.iloc[0]["V2_GTVLT_D95VOL"])
                            input_GTV_less_D95_Mean_Dose_2 = st.text_input("GTV < D95 Mean Dose_2",value = df.iloc[0]["V2_GTVLT_D95MEAN"])
                            input_GTV_less_D95_Min_Dose_2 = st.text_input("GTV < D95 Min Dose_2",value = df.iloc[0]["V2_GTVLT_D95MIN"])
                            input_GTV_less_D95_SD_2 = st.text_input("GTV < D95 SD_2",value = df.iloc[0]["V2_GTVLT_D95SD"])
                            input_GTV_less_100_Gy_Vol = st.text_input("GTV < 100 Gy Vol",value = df.iloc[0]["GTVLT_100VOL"])
                            input_GTV_less_100_Gy_Mean_Dose = st.text_input("GTV < 100 Gy Mean Dose",value = df.iloc[0]["GTVLT_100MEAN"])
                            input_GTV_less_100_Gy_Max_Dose = st.text_input("GTV < 100 Gy Max Dose",value = df.iloc[0]["GTVLT_100MAX"])
                            input_GTV_less_100_Gy_Min_Dose = st.text_input("GTV < 100 Gy Min Dose",value = df.iloc[0]["GTVLT_100MIN"])
                            input_GTV_less_100_Gy_SD = st.text_input("GTV < 100 Gy SD",value = df.iloc[0]["GTVLT_100SD"])

                            submit_dosimetry_data = st.form_submit_button("Submit")

                            if submit_dosimetry_data:
                                data11 = {
                                    "TRLNKID": trlnkid,
                                    "GTV_MEANDOSE": input_GTV_mean_dose,
                                    "TXVOL_MEANDOSE": input_Tx_vol_mean_dose,
                                    "LIVVOL__MEANDOSE": input_Liver_Vol_Mean_dose,
                                    "HEALTHYLIV_MEANDOSE": input_Healthy_Liver_mean_dose,
                                    "GTV_VOL": input_GTV_Vol,
                                    "TX_VOL": input_Tx_vol,
                                    "LIVER_VOL": input_Liver_vol,
                                    "HEALTHYLIV_VOL": input_Healthy_Liver_Vol,
                                    "GTVLIV_FRAC": input_GTV_Liver,
                                    "D98": input_D98,
                                    "D95": input_D95,
                                    "D90": input_D90,
                                    "D80": input_D80,
                                    "D70": input_D70,
                                    "V100": input_V100,
                                    "V200": input_V200,
                                    "V300": input_V300,
                                    "V400": input_V400,
                                    "ACTIVITYBQ": input_ActivityBq,
                                    "ACTIVITYCI": input_ActivityCi,
                                    "ACTIVITY_TXVOL": input_Tx_vol_Activity_Density,
                                    "GTVLT_D95VOL": input_GTV_less_D95_Vol_ml,
                                    "GTVLT_D95MEAN": input_GTV_less_D95_Mean_Dose,
                                    "GTVLT_D95MAX": input_GTV_less_D95_Mx_Dose,
                                    "GTVLT_D95MIN": input_GTV_less_D95_Min_Dose,
                                    "GTVLT_D95SD": input_GTV_less_D95_SD,
                                    "V1_GTVLT_D95VOL": input_GTV_less_D95_Vol_1,
                                    "V1_GTVLT_D95MEAN": input_GTV_less_D95_Mean_Dose_1,
                                    "V1_GTVLT_D95MIN": input_GTV_less_D95_Min_Dose_1,
                                    "V1_GTVLT_D95SD": input_GTV_less_D95_SD_1,
                                    "V2_GTVLT_D95VOL": input_GTV_less_D95_Vol_2,
                                    "V2_GTVLT_D95MEAN": input_GTV_less_D95_Mean_Dose_2,
                                    "V2_GTVLT_D95MIN": input_GTV_less_D95_Min_Dose_2,
                                    "V2_GTVLT_D95SD": input_GTV_less_D95_SD_2,
                                    "GTVLT_100VOL": input_GTV_less_100_Gy_Vol,
                                    "GTVLT_100MEAN": input_GTV_less_100_Gy_Mean_Dose,
                                    "GTVLT_100MAX": input_GTV_less_100_Gy_Max_Dose,
                                    "GTVLT_100MIN": input_GTV_less_100_Gy_Min_Dose,
                                    "GTVLT_100SD": input_GTV_less_100_Gy_SD
                                }
                                update_google_sheet(data11, mrn)

                    elif st.session_state.selected_tab == "AFP":
                        st.subheader("Dosimetry Data")
                        with st.form("dosimetry_data_form"):
                            
                                input_1AFP_DATE = st.text_area("1AFP Date",value = df.iloc[0]["1AFPDATE"])
                                input_1AFP = st.text_area("1AFP",value = df.iloc[0]["1AFP"])
                                input_2AFP_DATE = st.text_area("2AFP Date",value = df.iloc[0]["2AFPDATE"])
                                input_2AFP = st.text_area("2AFP",value = df.iloc[0]["2AFP"])
                                input_3AFP_DATE = st.text_area("3AFP Date",value = df.iloc[0]["3AFPDATE"])
                                input_3AFP = st.text_area("3AFP",value = df.iloc[0]["3AFP"])
                                input_4AFP_DATE = st.text_area("4AFP Date",value = df.iloc[0]["4AFPDATE"])
                                input_4AFP = st.text_area("4AFP",value = df.iloc[0]["4AFP"])
                                input_5AFP_DATE = st.text_area("5AFP Date",value = df.iloc[0]["5AFPDATE"])
                                input_5AFP = st.text_area("5AFP",value = df.iloc[0]["5AFP"])
                                input_6AFP_DATE = st.text_area("6AFP Date",value = df.iloc[0]["6AFPDATE"])
                                input_6AFP = st.text_area("6AFP",value = df.iloc[0]["6AFP"])
                                input_7AFP_DATE = st.text_area("7AFP Date",value = df.iloc[0]["7AFPDATE"])
                                input_7AFP = st.text_area("7AFP",value = df.iloc[0]["7AFP"])
                                input_8AFP_DATE = st.text_area("8AFP Date",value = df.iloc[0]["8AFPDATE"])
                                input_8AFP = st.text_area("8AFP",value = df.iloc[0]["8AFP"])
                                input_9AFP_DATE = st.text_area("9AFP Date",value = df.iloc[0]["9AFPDATE"])
                                input_9AFP = st.text_area("9AFP",value = df.iloc[0]["9AFP"])
                                input_10AFP_DATE = st.text_area("10AFP Date",value = df.iloc[0]["10AFPDATE"])
                                input_10AFP = st.text_area("10AFP",value = df.iloc[0]["10AFPDATE"])
                                input_11AFP_DATE = st.text_area("11AFP Date",value = df.iloc[0]["11AFPDATE"])
                                input_11AFP = st.text_area("11AFP",value = df.iloc[0]["11AFP"])
                                input_12AFP_DATE = st.text_area("12AFP Date",value = df.iloc[0]["12AFPDATE"])
                                input_12AFP = st.text_area("12AFP",value = df.iloc[0]["12AFP"])
                                input_13AFP_DATE = st.text_area("13AFP Date",value = df.iloc[0]["13AFPDATE"])
                                input_13AFP = st.text_area("13AFP",value = df.iloc[0]["13AFP"])
                                input_14AFP_DATE = st.text_area("14AFP Date",value = df.iloc[0]["14AFPDATE"])
                                input_14AFP = st.text_area("14AFP",value = df.iloc[0]["14AFP"])
                                input_15AFP_DATE = st.text_area("15AFP Date",value = df.iloc[0]["15AFPDATE"])
                                input_15AFP = st.text_area("15AFP",value = df.iloc[0]["15AFP"])
                                input_16AFP_DATE = st.text_area("16AFP Date",value = df.iloc[0]["16AFPDATE"])
                                input_16AFP = st.text_area("16AFP",value = df.iloc[0]["16AFP"])
                                input_17AFP_DATE = st.text_area("17AFP Date",value = df.iloc[0]["17AFPDATE"])
                                input_17AFP = st.text_area("17AFP",value = df.iloc[0]["17AFP"])
                                input_18AFP_DATE = st.text_area("18AFP DATE",value = df.iloc[0]["18AFPDATE"])
                                input_18AFP = st.text_area("18AFP",value = df.iloc[0]["18AFP"])
                                input_19AFP_DATE = st.text_area("19AFP DATE",value = df.iloc[0]["19AFPDATE"])
                                input_19AFP = st.text_area("19AFP",value = df.iloc[0]["19AFP"])
                                input_20AFP_DATE = st.text_area("20AFP DATE",value = df.iloc[0]["20AFPDATE"])
                                input_20AFP = st.text_area("20AFP",value = df.iloc[0]["20AFP"])
                                input_21AFP_DATE = st.text_area("21AFP DATE",value = df.iloc[0]["21AFPDATE"])
                                input_21AFP = st.text_area("21AFP",value = df.iloc[0]["21AFP"])
                                input_22AFP_DATE = st.text_area("22AFP DATE",value = df.iloc[0]["22AFPDATE"])
                                input_22AFP = st.text_area("22AFP",value = df.iloc[0]["22AFP"])
                                input_23AFP_DATE = st.text_area("23AFP DATE",value = df.iloc[0]["23AFPDATE"])
                                input_23AFP = st.text_area("23AFP",value = df.iloc[0]["23AFP"])
                                input_24AFP_DATE = st.text_area("24AFP DATE",value = df.iloc[0]["24AFPDATE"])
                                input_24AFP = st.text_area("24AFP",value = df.iloc[0]["24AFP"])
                                input_25AFP_DATE = st.text_area("25AFP DATE",value = df.iloc[0]["25AFPDATE"])
                                input_25AFP = st.text_area("25AFP",value = df.iloc[0]["25AFP"])
                                input_26AFP_DATE = st.text_area("26AFP DATE",value = df.iloc[0]["26AFPDATE"])
                                input_26AFP = st.text_area("26AFP",value = df.iloc[0]["26AFP"])
                                input_27AFP_DATE = st.text_area("27AFP DATE",value = df.iloc[0]["27AFPDATE"])
                                input_27AFP = st.text_area("27AFP",value = df.iloc[0]["27AFP"])
                                input_28AFP_DATE = st.text_area("28AFP DATE",value = df.iloc[0]["28AFPDATE"])
                                input_28AFP = st.text_area("28AFP",value = df.iloc[0]["28AFP"])
                                input_29AFP_DATE = st.text_area("29AFP DATE",value = df.iloc[0]["29AFPDATE"])
                                input_29AFP = st.text_area("29AFP",value = df.iloc[0]["29AFP"])
                                input_30AFP_DATE = st.text_area("30AFP DATE",value = df.iloc[0]["30AFPDATE"])
                                input_30AFP = st.text_area("30AFP",value = df.iloc[0]["30AFP"])
                                input_31AFP_DATE = st.text_area("31AFP Date",value = df.iloc[0]["31AFPDATE"])
                                input_31AFP = st.text_area("31AFP",value = df.iloc[0]["31AFP"])
                                input_32AFP_DATE = st.text_area("32AFP DATE",value = df.iloc[0]["32AFPDATE"])
                                input_32AFP = st.text_area("32AFP",value = df.iloc[0]["32AFP"])
                                input_33AFP_DATE = st.text_area("33AFP DATE",value = df.iloc[0]["33AFPDATE"])
                                input_33AFP = st.text_area("33AFP",value = df.iloc[0]["33AFP"])
                                input_34AFP_DATE = st.text_area("34AFP DATE",value = df.iloc[0]["34AFPDATE"])
                                input_34AFP = st.text_area("34AFP",value = df.iloc[0]["34AFP"])

                                submit_afp = st.form_submit_button("Submit")

                                if submit_afp:
                                    data12 = {
                                    "1AFPDATE": input_1AFP_DATE, "1AFP": input_1AFP,
                                    "2AFPDATE": input_2AFP_DATE, "2AFP": input_2AFP,
                                    "3AFPDATE": input_3AFP_DATE, "3AFP": input_3AFP,
                                    "4AFPDATE": input_4AFP_DATE, "4AFP": input_4AFP,
                                    "5AFPDATE": input_5AFP_DATE, "5AFP": input_5AFP,
                                    "6AFPDATE": input_6AFP_DATE, "6AFP": input_6AFP,
                                    "7AFPDATE": input_7AFP_DATE, "7AFP": input_7AFP,
                                    "8AFPDATE": input_8AFP_DATE, "8AFP": input_8AFP,
                                    "9AFPDATE": input_9AFP_DATE, "9AFP": input_9AFP,
                                    "10AFPDATE": input_10AFP_DATE, "10AFP": input_10AFP,
                                    "11AFPDATE": input_11AFP_DATE, "11AFP": input_11AFP,
                                    "12AFPDATE": input_12AFP_DATE, "12AFP": input_12AFP,
                                    "13AFPDATE": input_13AFP_DATE, "13AFP": input_13AFP,
                                    "14AFPDATE": input_14AFP_DATE, "14AFP": input_14AFP,
                                    "15AFPDATE": input_15AFP_DATE, "15AFP": input_15AFP,
                                    "16AFPDATE": input_16AFP_DATE, "16AFP": input_16AFP,
                                    "17AFPDATE": input_17AFP_DATE, "17AFP": input_17AFP,
                                    "18AFPDATE": input_18AFP_DATE, "18AFP": input_18AFP,
                                    "19AFPDATE": input_19AFP_DATE, "19AFP": input_19AFP,
                                    "20AFPDATE": input_20AFP_DATE, "20AFP": input_20AFP,
                                    "21AFPDATE": input_21AFP_DATE, "21AFP": input_21AFP,
                                    "22AFPDATE": input_22AFP_DATE, "22AFP": input_22AFP,
                                    "23AFPDATE": input_23AFP_DATE, "23AFP": input_23AFP,
                                    "24AFPDATE": input_24AFP_DATE, "24AFP": input_24AFP,
                                    "25AFPDATE": input_25AFP_DATE, "25AFP": input_25AFP,
                                    "26AFPDATE": input_26AFP_DATE, "26AFP": input_26AFP,
                                    "27AFPDATE": input_27AFP_DATE, "27AFP": input_27AFP,
                                    "28AFPDATE": input_28AFP_DATE, "28AFP": input_28AFP,
                                    "29AFPDATE": input_29AFP_DATE, "29AFP": input_29AFP,
                                    "30AFPDATE": input_30AFP_DATE, "30AFP": input_30AFP,
                                    "31AFPDATE": input_31AFP_DATE, "31AFP": input_31AFP,
                                    "32AFPDATE": input_32AFP_DATE, "32AFP": input_32AFP,
                                    "33AFPDATE": input_33AFP_DATE, "33AFP": input_33AFP,
                                    "34AFPDATE": input_34AFP_DATE, "34AFP": input_34AFP
                                    }
                                    update_google_sheet(data12,mrn)
if st.session_state.logged_in:
    # Navigation options
    st.sidebar.title("Navigation")
    options = st.sidebar.radio("Select an option", ["Add New Data", "Edit Existing Data","Export Excel", "Logout"])
    
    if options == "Add New Data":
        add_new_data()
    elif options == "Edit Existing Data":
        edit_existing_data()
    elif options == "Export Excel":
        st.session_state.page = "home"
        st.switch_page("pages/export_data.py")
        
    elif options == "Logout":
        st.session_state.logged_in = False
        st.rerun()
else:
    login_page()        




