import streamlit as st
import pandas as pd
import math
from datetime import datetime
from dateutil.relativedelta import relativedelta
import numpy as np

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


#st.set_page_config(layout="wide")

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

    # Different functions created for inputs
    
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
    
    # start main page
    st.title("Patient Information System")

    tabs = ["Patient Info", "Patient Demographics", "Cirrhosis PMH","HCC Diagnosis", "Previous Therapy for HCC", "Pre Y90", "Day_Y90", "Post Y90 Within 30 Days Labs", "Other Post Tare","Imaging Date","Dosimetry Data","AFP"]
    if "selected_tab" not in st.session_state:
        st.session_state.selected_tab = tabs[0]

    col1, col2 = st.columns([0.3, 0.7],gap="small")

    # Left column for vertical tabs
    with col1:
        st.header("Patient Deatils")
        st.session_state.selected_tab = st.radio("", tabs)

    # Right column for dynamic form
    with col2:
        #st.header(st.session_state.selected_tab)
        
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
                if mrn in st.session_state.data["MRN"].values:
                    st.write("Are you sure this is a duplicate")
                    duplicate_procedure_check = 1
                
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

                age = st.number_input("Age at time of TARE", min_value=0, max_value=150, step=1, format="%d")
            
                submit_tab1 = st.form_submit_button("Submit")
                if submit_tab1:
                    if mrn in st.session_state.data["MRN"].values:
                        st.error(f"MRN {mrn} already exists. Please enter a unique MRN.")
                    else:
                        st.session_state.data = pd.concat(
                        [st.session_state.data, pd.DataFrame([{
                            "Name": f"{last_name}, {first_name}",
                            "MRN": mrn,
                            "Duplicate" : duplicate_procedure_check,
                            "TAREdate": tare_date.strftime("%Y-%m-%d"),
                            "PTech": procedure_technique,
                            "Tareage": age
                            } ])], ignore_index=True)
                        st.session_state.temp_mrn = mrn
                        st.success("Patient Information saved. Proceed to Patient Description tab.")
            
        elif st.session_state.selected_tab == "Patient Demographics":
            st.subheader("Patient_Demographics")
            with st.form("demographics_form"):
                #st.subheader("Patient Description")
                if "MRN" not in st.session_state.data:
                    st.warning("Please complete the Patient Information tab first.")
                else:
                    try:
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
                            index = st.session_state.data[st.session_state.data["MRN"] == st.session_state.temp_mrn].index[0]
                            st.session_state.data.at[index, "Gender"] = gender
                            st.session_state.data.at[index, "Ethnicity"] = ethnicity
                            st.session_state.data.at[index, "PMHxHTN"] = hypertension
                            st.session_state.data.at[index, "PMHxDM"] = diabetes
                            st.session_state.data.at[index, "Hypercholesterolemia"] = hypercholesterolemia
                            st.session_state.data.at[index, "PMHxSmoking"] = smoking
                            st.session_state.data.at[index, "Obesity"] = obesity
                            st.success("Patient Description added successfully.")
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
                                 return "Slight"
                            elif score == "Symptomatic" or score == "moderate ascities/Symptomatic medical intervention":
                                 return "Moderate"
                            elif score == "Severe symptoms, invasive intervention indicated" or score == "Life Threatening: Urgent operation intervention indicated" :
                                 return "Severe"
                        
                        Cirrhosis_Dx_Ascites_Classification = "Absent" if Cirrhosis_Dx_Ascites_CTCAE == "none" else findascitesclass(Cirrhosis_Dx_Ascites_CTCAE)
                        
                        Cirrhosis_Dx_Ascites_Free_Text = "NA" if Cirrhosis_Dx_Ascites_CTCAE == "none" else st.text_area(
                            "Cirrhosis_Dx_Ascites Free Text",
                            "Hospitalized (yes/no): \nDiuretics (yes/no): \nParacentesis (yes/no): \nAny other complications (free_text):",
                        
                        )

                        submit_tab3 = st.form_submit_button("Submit")
                        if submit_tab3:

                            index = st.session_state.data[st.session_state.data["MRN"] == st.session_state.temp_mrn].index[0]
                            st.session_state.data.at[index, "CirPMH_HBV"] = cir_pmh_hbv_status
                            st.session_state.data.at[index, "CirPMH_HBVFT"] = cir_pmh_hbv_free_text
                            st.session_state.data.at[index, "CirPMH_HBVART"] = cir_pmh_hbv_art
                            st.session_state.data.at[index, "CirPMH_HCV"] = cir_pmh_hcv_status
                            st.session_state.data.at[index, "CirPMH_HCVFT"] = cir_pmh_hcv_free_text
                            st.session_state.data.at[index, "CirPMH_HCVART"] = cir_pmh_hcv_art
                            st.session_state.data.at[index, "CirPMH_AUD"] = cir_pmh_alcohol_use_disorder
                            st.session_state.data.at[index, "CirPMH_AUDFT"] = cir_pmh_alcohol_free_text
                            st.session_state.data.at[index, "CirPMH_IVDU"] = cir_pmh_ivdu_status
                            st.session_state.data.at[index, "CirPMH_IVDUFT"] = cir_pmh_ivdu_free_text
                            st.session_state.data.at[index, "CirPMH_Liverfactors"] = cir_pmh_liver_addtional_factor
                            st.session_state.data.at[index, "Cirdx_Dxdate"] = Cirrhosis_Dx_Diagnosis_Date
                            st.session_state.data.at[index, "Cirdx_Dxmethod"] = Cirrhosis_Dx_Diagnosis_Method
                            st.session_state.data.at[index, "Cirdx_HPIFT"] = Cirrhosis_Dx_HPI_EMR_Note_Free_Text
                            st.session_state.data.at[index, "Cirdx_ImageemrFT"] = Cirrhosis_Dx_Imaging_Findings_EMR_Note_Free_Text
                            st.session_state.data.at[index, "Cirdx_Metavir"] = Cirrhosis_Dx_Metavir_Score
                            st.session_state.data.at[index, "Cirdx_Compatdx"] = Cirrhosis_Dx_Complications_at_Time_of_Diagnosis
                            st.session_state.data.at[index, "Cirdx_Compatdxbinary"] = Cirrhosis_Dx_Complications_at_Time_of_Diagnosis_Binary
                            st.session_state.data.at[index, "Cirdx_CompFT"] = Cirrhosis_Dx_Complications_Free_Text
                            st.session_state.data.at[index, "Cirdx_DateLabs"] = Cirrhosis_Dx_Date_of_Labs_in_Window
                            st.session_state.data.at[index, "Cirdx_AFP"] = Cirrhosis_Dx_AFP
                            st.session_state.data.at[index, "Cirdx_AFP L3"] = Cirrhosis_Dx_AFP_L3
                            st.session_state.data.at[index, "Cirdx_AFPL3DateFT"] = Cirrhosis_Dx_AFP_L3_Date_Free_Text
                            st.session_state.data.at[index, "Cirdx_AscitesCTCAE"] = Cirrhosis_Dx_Ascites_CTCAE
                            st.session_state.data.at[index, "Cirdx_AscitesCTCAEnumb"] = Cirrhosis_Dx_Ascites_Classification
                            st.session_state.data.at[index, "Cirdx_AscitesFT"] = Cirrhosis_Dx_Ascites_Free_Text
                            
                            st.success("Patient Description added successfully.")
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
                            "HCC_Dx_Method of Diagnosis",   
                            options=["Biopsy", "Imaging", "Unknown"],
                            index=None,  # No default selection
                            placeholder="Choose an option",
                            #format_func=lambda x: f"{x} ({1 if x == 'Biopsy' else 2 if x == 'Imaging' else 'NA'})"
                        )

                        hcc_dx_date_of_labs = st.date_input("HCC_Dx_Date of Labs in Window")

                        hcc_dx_afp = st.number_input("HCC_Dx_AFP", help="Enter AFP value in ng/dl")
                        hcc_dx_afp_l3 = st.number_input("HCC_Dx_AFP L3", help="Enter AFP L3 and date details")
                        hcc_dx_afp_l3_date_free_text = st.text_area("HCC_Dx_AFP L3 Date Free Text")

                        hcc_dx_bilirubin = st.number_input("HCC_Dx_Bilirubin", help="Enter the bilirubin value in mg/dl", min_value=1)
                        hcc_dx_albumin = st.number_input("HCC_Dx_Albumin", help="Enter the albumin value in g/dl")
                        hcc_dx_inr = st.number_input("HCC_Dx_INR", help="Enter the INR value")
                        hcc_dx_creatinine = st.number_input("HCC_Dx_Creatinine", help="Enter the creatinine value in mg/dl")
                        hcc_dx_sodium = st.number_input("HCC_Dx_Sodium", help="Enter the sodium value in mmol/L")

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

                        hcc_dx_bclc_calc = st.text_area("HCC_Dx_BCLC Stage calc")
                        submit_tab4 = st.form_submit_button("Submit")
                        if submit_tab4:
                                index = st.session_state.data[st.session_state.data["MRN"] == st.session_state.temp_mrn].index[0]
                                st.session_state.data.at[index, "HCCdx_HCCdxdate"] = hcc_dx_hcc_diagnosis_date.strftime("%Y-%m-%d")
                                st.session_state.data.at[index, "HCCdx_Methoddx"] = hcc_dx_method_of_diagnosis
                                st.session_state.data.at[index, "HCCdx_Datelabs"] = hcc_dx_date_of_labs.strftime("%Y-%m-%d")
                                st.session_state.data.at[index, "HCCdx_AFP"] = hcc_dx_afp
                                st.session_state.data.at[index, "HCCdx_AFP L3"] = hcc_dx_afp_l3
                                st.session_state.data.at[index, "HCCdx_AFPL3dateFT"] = hcc_dx_afp_l3_date_free_text
                                st.session_state.data.at[index, "HCCdx_Bilirubin"] = hcc_dx_bilirubin
                                st.session_state.data.at[index, "HCCdx_Albumin"] = hcc_dx_albumin
                                st.session_state.data.at[index, "HCCdx_INR"] = hcc_dx_inr
                                st.session_state.data.at[index, "HCCdx_Creatinine"] = hcc_dx_creatinine
                                st.session_state.data.at[index, "HCCdx_Sodium"] = hcc_dx_sodium
                                st.session_state.data.at[index, "HCCdx_AscitesCTCAE"] = hcc_dx_ascites_CTCAE
                                st.session_state.data.at[index, "HCCdx_AscitesCTCAEnumb"] = hCC_dx_ascites_classification
                                st.session_state.data.at[index, "HCCdx_Ascitesdiruetics"] = hcc_dx_ascites_diruetics
                                st.session_state.data.at[index, "HCCdx_Ascitesparacentesis"] = hcc_dx_ascites_paracentesis
                                st.session_state.data.at[index, "HCCdx_Asciteshospitalization"] = hcc_dx_ascites_hospitalization
                                st.session_state.data.at[index, "HCCdx_HEgrade"] = hcc_dx_he_grade
                                st.session_state.data.at[index, "HCCdx_ECOG"] = hcc_dx_ecog_performance_status
                                st.session_state.data.at[index, "HCCdx_LIRADS"] = hcc_dx_lirads_score
                                st.session_state.data.at[index, "HCCdx_CPcalc"] = hcc_dx_child_pugh_points_calc
                                st.session_state.data.at[index, "HCCdx_CPclass"] = hcc_dx_child_pugh_class_calc
                                st.session_state.data.at[index, "HCCdx_MELD"] = hcc_dx_meld_score_calc
                                st.session_state.data.at[index, "HCCdx_MELDNa"] = hcc_dx_meld_na_score_calc
                                st.session_state.data.at[index, "HCCdx_Albiscore"] = hcc_dx_albi_score_calc
                                st.session_state.data.at[index, "HCCdx_Albigrade"] = hcc_dx_albi_grade
                                st.session_state.data.at[index, "HCCdx_BCLC"] = hcc_dx_bclc_calc
                                st.success("HCC Dx added successfully.")
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
                            help="Enter AFP value in ng/dl or NA"
                        )

                        submit_tab5 = st.form_submit_button("Submit")
                        if submit_tab5:
                                index = st.session_state.data[st.session_state.data["MRN"] == st.session_state.temp_mrn].index[0]

                                st.session_state.data.at[index, "PRVTHER_LDT"] = PRVTHER_Prior_LDT_Therapy
                                st.session_state.data.at[index, "PRVTHER_RFA"] = PRVTHER_Prior_RFA_Therapy
                                st.session_state.data.at[index, "PRVTHER_RFAdate"] = PRVTHER_Prior_RFA_Date
                                st.session_state.data.at[index, "PRVTHER_TARE"] = PRVTHER_Prior_TARE_Therapy
                                st.session_state.data.at[index, "PRVTHER_TAREdate"] = PRVTHER_Prior_TARE_Date
                                st.session_state.data.at[index, "PRVTHER_SBRT"] = PRVTHER_Prior_SBRT_Therapy
                                st.session_state.data.at[index, "PRVTHER_SBRTdate"] = PRVTHER_Prior_SBRT_Date
                                st.session_state.data.at[index, "PRVTHER_TACE"] = PRVTHER_Prior_TACE_Therapy
                                st.session_state.data.at[index, "PRVTHER_TACEdate"] = PRVTHER_Prior_TACE_Date
                                st.session_state.data.at[index, "PRVTHER_MWA"] = PRVTHER_Prior_MWA_Therapy
                                st.session_state.data.at[index, "PRVTHER_MWAdate"] = PRVTHER_Prior_MWA_Date
                                st.session_state.data.at[index, "PRVTHER_Resection"] = PRVTHER_Resection
                                st.session_state.data.at[index, "PRVTHER_Resection date"] = PRVTHER_Resection_Date
                                st.session_state.data.at[index, "PRVTHER_Prevtxsum"] = PRVTHER_Previous_Therapy_Sum
                                st.session_state.data.at[index, "PRVTHER_NotesFT"] = PRVTHER_NotesFT
                                st.session_state.data.at[index, "PRVTHER_Totalrecur"] = PRVTHER_Total_Recurrences_HCC
                                st.session_state.data.at[index, "PRVTHER_Locationprevtxseg"] = PRVTHER_Location_of_Previous_Treatment_segments
                                st.session_state.data.at[index, "PRVTHER_Location of Previous Tx Segments FT"] = PRVTHER_Location_of_Previous_Tx_segments_ft
                                st.session_state.data.at[index, "PRVTHER_RecurLocationFT"] = PRVTHER_recurrence_location_note
                                st.session_state.data.at[index, "PRVTHER_RecurDate"] = PRVTHER_recurrence_date
                                st.session_state.data.at[index, "PRVTHER_Recurrence Seg"] = PRVTHER_recurrence_seg
                                st.session_state.data.at[index, "PRVTHER_NewHCCoutsideprevsite"] = PRVTHER_New_HCC_Outside_Previous_Treatment_Site
                                st.session_state.data.at[index, "PRVTHER_NewHCCadjacentprevsite"] = PRVTHER_New_HCC_Adjacent_to_Previous_Treatment_Site
                                st.session_state.data.at[index, "PRVTHER_ResidualHCCnoteFT"] = PRVTHER_Residual_HCC_Note
                                st.session_state.data.at[index, "PRVTHER_ResidualHCC"] = PRVTHER_Residual_HCC
                                st.session_state.data.at[index, "PRVTHER_SystemictherapyFT"] = PRVTHER_Systemic_Therapy_Free_Text
                                st.session_state.data.at[index, "PRVTHER_DateAFP"] = PRVTHER_Date_of_Labs_in_Window
                                st.session_state.data.at[index, "PRVTHER_AFP"] = PRVTHER_AFP
                                st.success("Previous Therapy for HCC added successfully.")
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
                        help="Select all that apply",
                            placeholder="Select all that apply"
                        )
                        
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
                        
                        
                        prey90_bilirubin = st.number_input("PREY90_Bilirubin", help="Enter the bilirubin value in mg/dl",min_value=1)
                        prey90_albumin = st.number_input("PREY90_Albumin", help="Enter the albumin value in g/dl")
                        prey90_inr = st.number_input("PREY90_inr", help="Enter the INR value")
                        prey90_creatinine = st.number_input("PREY90_creatinine", help="Enter the creatinine value in mg/dl")
                        prey90_sodium = st.number_input("PREY90_sodium", help="Enter the sodium value in mmol/L")
                        prey90_ast = st.number_input("PREY90_AST", help="Enter AST value in U/L")
                        prey90_alt = st.number_input("PREY90_ALT", help="Enter ALT value in U/L")
                        prey90_alkaline_phosphatase = st.number_input("PREY90_Alkaline Phosphatase", help="Enter Alkaline Phosphatase value in U/L")
                        prey90_potassium = st.number_input("PREY90_potassium", help="Enter the potassium value in mmol/L")
                        
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
                
                        prey90_child_pugh_class_calc = calculate_class(prey90_child_pugh_points_calc)
                        # Additional Calculated Fields
                        
                        #prey90_bclc_stage_calc = st.text_input("PREY90_BCLC Stage calc", help="Enter calculated BCLC stage")
                        prey90_meld_score_calc = (3.78*(int(prey90_bilirubin)))+(11.2*(int(prey90_inr)))+(9.57*(int(prey90_creatinine)))+6.43
                        prey90_meld_na_score_calc = prey90_meld_score_calc + 1.32*(137-int(prey90_sodium)) - (0.033*prey90_meld_score_calc*(137-int(prey90_sodium)))
                        
                        prey90_albi_score_calc = albi_calc(prey90_bilirubin,prey90_albumin)
                        prey90_albi_grade = albi_class(prey90_albi_score_calc)

                        prey90_bclc_calc = st.text_area("PREY90_BCLC Stage calc")

                    
                        st.subheader("Mapping Y90")
                        my90_date = st.date_input("MY90_date", help="Enter the date")
                        my90_lung_shunt = st.number_input("MY90_Lung_shunt", min_value=0, step=1, help="Enter the lung shunt value")

                        submit_tab4 = st.form_submit_button("Submit")

                        if submit_tab4:
                            index = st.session_state.data[st.session_state.data["MRN"] == st.session_state.temp_mrn].index[0]

                            st.session_state.data.at[index, "PREY90_sx"] = prey90_symptoms
                            st.session_state.data.at[index, "PREY90_Datelabs"] = prey90_date_of_labs.strftime("%Y-%m-%d")
                            st.session_state.data.at[index, "PREY90_AFP"] = prey90_afp
                            st.session_state.data.at[index, "PRE90_AFPbinary"] = prey90_afp_prior_to_tare
                            st.session_state.data.at[index, "PREY90_Bilirubin"] = prey90_bilirubin
                            st.session_state.data.at[index, "PREY90_Albumin"] = prey90_albumin
                            st.session_state.data.at[index, "PREY90_Inr"] = prey90_inr
                            st.session_state.data.at[index, "PREY90_Ireatinine"] = prey90_creatinine
                            st.session_state.data.at[index, "PREY90_Sodium"] = prey90_sodium
                            st.session_state.data.at[index, "PREY90_AST"] = prey90_ast
                            st.session_state.data.at[index, "PREY90_ALT"] = prey90_alt
                            st.session_state.data.at[index, "PREY90_Alkaline Phosphatase"] = prey90_alkaline_phosphatase
                            st.session_state.data.at[index, "PREY90_Potassium"] = prey90_potassium
                            st.session_state.data.at[index, "PREY90_AscitesCTCAE"] = prey90_ascites_ctcae
                            st.session_state.data.at[index, "PREY90_AscitesCTCAEnumb"] = prey90_ascites_classification
                            st.session_state.data.at[index, "PREY90_AscitesFT"] = prey90_ascites_free_text
                            st.session_state.data.at[index, "PREY90_Ascitesdiruetics"] = prey90_ascites_diruetics
                            st.session_state.data.at[index, "PREY90_Ascitesparacentesis"] = prey90_ascites_paracentesis
                            st.session_state.data.at[index, "PREY90_Asciteshospitalization"] = prey90_ascites_hospitalization
                            st.session_state.data.at[index, "PREY90_HEgrade"] = prey90_he_grade
                            st.session_state.data.at[index, "PREY90_ECOG"] = prey90_ecog
                            st.session_state.data.at[index, "PREY90_CPclass"]= prey90_child_pugh_class_calc
                            st.session_state.data.at[index, "PREY90_CPcalc"] = prey90_child_pugh_points_calc
                            st.session_state.data.at[index, "PREY90_MELD"] = prey90_meld_score_calc
                            st.session_state.data.at[index, "PREY90_MELDNa"] = prey90_meld_na_score_calc
                            st.session_state.data.at[index, "PREY90_Albiscore"] = prey90_albi_score_calc
                            st.session_state.data.at[index, "PREY90_Albigrade"] = prey90_albi_grade
                            st.session_state.data.at[index, "PREY90_BCLC"] = prey90_bclc_calc
                            st.session_state.data.at[index, "MY90_date"] = my90_date
                            st.session_state.data.at[index, "MY90_Lung_shunt"] = my90_lung_shunt

                            st.success("Pre Y90 added successfully.")
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
                        index = st.session_state.data[st.session_state.data["MRN"] == st.session_state.temp_mrn].index[0]


                        prey90_afp_binarydup = st.session_state.data.at[index, "PRE90_AFPbinary"]
                    
                    # Inputs for other variables
                        dayy90_sodium = st.number_input("DAYY90_sodium")
                        dayy90_creatinine = st.number_input("DAYY90_creatinine")
                        dayy90_inr = st.number_input("DAYY90_inr")
                        dayy90_albumin = st.number_input("DAYY90_albumin")
                        dayy90_bilirubin = st.number_input("DAYY90_bilirubin",min_value=1)
                        dayy90_ast = st.number_input("DAYY90_AST")
                        dayy90_alt = st.number_input("DAYY90_ALT")
                        dayy90_alkaline_phosphatase = st.number_input(
                            "DAYY90_Alkaline Phosphatase"
                        )
                        dayy90_leukocytes = st.number_input("DAYY90_leukocytes")
                        dayy90_platelets = st.number_input("DAYY90_platelets")
                        dayy90_potassium = st.number_input("DAY90_Potassium")

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

                        
                        # Claculation of class and points
                        dayy90_child_pugh_points_calc = calculatepoints(dayy90_bilirubin,dayy90_albumin,dayy90_inr,dayy90_ascites_ctcae,dayy90_he_grade)
                
                        dayy90_child_pugh_class_calc = calculate_class(dayy90_child_pugh_points_calc)
                        # Additional Calculated Fields
                        
                        #prey90_bclc_stage_calc = st.text_input("PREY90_BCLC Stage calc", help="Enter calculated BCLC stage")
                        dayy90_meld_score_calc = (3.78*(int(dayy90_bilirubin)))+(11.2*(int(dayy90_inr)))+(9.57*(int(dayy90_creatinine)))+6.43
                        dayy90_meld_na_score_calc = dayy90_meld_score_calc + 1.32*(137-int(dayy90_sodium)) - (0.033*dayy90_meld_score_calc*(137-int(dayy90_sodium)))
                        
                        dayy90_albi_score_calc = albi_calc(dayy90_bilirubin,dayy90_albumin)
                        dayy90_albi_grade = albi_class(dayy90_albi_score_calc)

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
                        ken_meldpretare = st.number_input("ken_MELDpreTARE")


                    # Submit button
                        submit_tab7 = st.form_submit_button("Submit")
                    
                        if submit_tab7:
                            index = st.session_state.data[st.session_state.data["MRN"] == st.session_state.temp_mrn].index[0]

                            st.session_state.data.at[index, "DAYY90_AFP"] = dayy90_afp
                            st.session_state.data.at[index, "DAYY90_AFP Binary"] = dayy90_afp_prior_to_tare
                            st.session_state.data.at[index, "PRE90_AFP BinaryDup"] = prey90_afp_binarydup
                            st.session_state.data.at[index, "DAYY90_Sodium"] = dayy90_sodium
                            st.session_state.data.at[index, "DAYY90_Creatinine"] = dayy90_creatinine
                            st.session_state.data.at[index, "DAYY90_Inr"] = dayy90_inr
                            st.session_state.data.at[index, "DAYY90_Albumin"] = dayy90_albumin
                            st.session_state.data.at[index, "DAYY90_Bilirubin"] = dayy90_bilirubin
                            st.session_state.data.at[index, "DAYY90_AST"] = dayy90_ast
                            st.session_state.data.at[index, "DAYY90_ALT"] = dayy90_alt
                            st.session_state.data.at[index, "DAYY90_Alkphos"] = dayy90_alkaline_phosphatase
                            st.session_state.data.at[index, "DAYY90_Leukocytes"] = dayy90_leukocytes
                            st.session_state.data.at[index, "DAYY90_Platelets"] = dayy90_platelets
                            st.session_state.data.at[index, "DAY90_Potassium"] = dayy90_potassium
                            st.session_state.data.at[index, "Day90_AscitesCTCAE"] = dayy90_ascites_ctcae
                            st.session_state.data.at[index, "Day90_AscitesCTCAEnumb"] = dayy90_ascites_classification
                            st.session_state.data.at[index, "Day90_HEgrade"] = dayy90_he_grade
                            st.session_state.data.at[index, "PREY90_ECOG"] = dayy90_ecog
                            st.session_state.data.at[index, "DAYY90_CPclass"] = dayy90_child_pugh_class_calc
                            st.session_state.data.at[index, "DAYY90_CPcalc"] = dayy90_child_pugh_points_calc
                            st.session_state.data.at[index, "DAYY90_MELD"] = dayy90_meld_score_calc
                            st.session_state.data.at[index, "DAYY90_MELD Na calc"] = dayy90_meld_na_score_calc
                            st.session_state.data.at[index, "DAYY90_Albiscore"] = dayy90_albi_score_calc
                            st.session_state.data.at[index, "DAYY90_Albigrade"] = dayy90_albi_grade
                            st.session_state.data.at[index, "DAYY90_BCLC"] = dayy90_bclc_calc
                            st.session_state.data.at[index, "DAYY90_Sphere"] = dayy90_type_of_sphere
                            st.session_state.data.at[index, "DAYY90_LTnoteFT"] = dayy90_lt_notes_ftx
                            st.session_state.data.at[index, "ken_ChildPughscore"] = ken_childpughscore
                            st.session_state.data.at[index, "ken_MELDpreTARE (MELDpreTARE)"] = ken_meldpretare
                            
                            st.success("DAYY90 added successfully.")
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
                        input90 = st.text_input("POSTY90_30DY_afp", help="Enter AFP value in ng/dl or NA")
                        posty90_afp = process_input(input90)
                        posty90_afp_date = st.date_input("POSTY90_30DY_afp DATE", help="Enter the date for AFP")
                        posty90_sodium = st.number_input("POSTY90_30DY_Sodium", help="Enter the sodium value in mmol/L")
                        posty90_creatinine = st.number_input("POSTY90_30DY_creatinine", help="Enter the creatinine value in mg/dl")
                        posty90_inr = st.number_input("POSTY90_30DY_INR", help="Enter the INR value")
                        posty90_albumin = st.number_input("POSTY90_30DY_albumin", help="Enter the albumin value in g/dl")
                        posty90_bilirubin = st.number_input("POSTY90_30DY_bilirubin", help="Enter the bilirubin value in mg/dl",min_value=1)
                        posty90_ast = st.number_input("POSTY90_30DY_AST", help="Enter AST value in U/L")
                        posty90_alt = st.number_input("POSTY90_30DY_ALT", help="Enter ALT value in U/L")
                        posty90_alkaline_phosphatase = st.number_input("POSTY90_30DY_Alkaline Phosphatase", help="Enter Alkaline Phosphatase value in U/L")
                        posty90_leukocytes = st.number_input("POSTY90_30DY_leukocytes", help="Enter leukocytes value in x10^3/µL")
                        posty90_platelets = st.number_input("POSTY90_30DY_platelets", help="Enter platelets value in x10^3/µL")
                        posty90_potassium = st.number_input("POSTY90_30DY_potassium", help="Enter the potassium value in mmol/L")
                        
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
                            help="Enter ALBI score"
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
                                
                                index = st.session_state.data[st.session_state.data["MRN"] == st.session_state.temp_mrn].index[0]
                            
                                st.session_state.data.at[index, "POSTY90_30DY_Datelabs"] = posty90_date_labs.strftime("%Y-%m-%d")
                                st.session_state.data.at[index, "POSTY90_30DY_AFP"] = posty90_afp
                                st.session_state.data.at[index, "POSTY90_30DY_AFPdate DATE"] = posty90_afp_date.strftime("%Y-%m-%d")
                                st.session_state.data.at[index, "POSTY90_30DY_Sodium"] = posty90_sodium
                                st.session_state.data.at[index, "POSTY90_30DY_Creatinine"] = posty90_creatinine
                                st.session_state.data.at[index, "POSTY90_30DY_INR"] = posty90_inr
                                st.session_state.data.at[index, "POSTY90_30DY_Albumin"] = posty90_albumin
                                st.session_state.data.at[index, "POSTY90_30DY_Bilirubin"] = posty90_bilirubin
                                st.session_state.data.at[index, "POSTY90_30DY_AST"] = posty90_ast
                                st.session_state.data.at[index, "POSTY90_30DY_ALT"] = posty90_alt
                                st.session_state.data.at[index, "POSTY90_30DY_ALP"] = posty90_alkaline_phosphatase
                                st.session_state.data.at[index, "POSTY90_30DY_Leukocytes"] = posty90_leukocytes
                                st.session_state.data.at[index, "POSTY90_30DY_Platelets"] = posty90_platelets
                                st.session_state.data.at[index, "POSTY90_30DY_Potassium"] = posty90_potassium
                                st.session_state.data.at[index, "30DY_AE_AscitesCTCAE"] = posty90_ascites_ctcae
                                st.session_state.data.at[index, "30DY_AE_AscitesCTCAEnumb"] = posty90_ascites_classification
                                st.session_state.data.at[index, "30DY_AE_Ascitesdiruetics"] = posty90_ascites_diruetics
                                st.session_state.data.at[index, "30DY_AE_Ascitesparacentesis"] = posty90_ascites_paracentesis
                                st.session_state.data.at[index, "30DY_AE_Asciteshospitalization"] = posty90_ascites_hospitalization
                                st.session_state.data.at[index, "30DY_AE_HEgrade"] = posty90_he_grade
                                st.session_state.data.at[index, "30DY_AE_ascities_freetext"] = posty90_ascites_free_text
                                st.session_state.data.at[index, "POSTY90_30DY_ECOG"] = posty90_ecog
                                st.session_state.data.at[index, "POSTY90_30DY_CPclass"] = posty90_child_pugh_class
                                st.session_state.data.at[index, "POSTY90_30DY_CPcalc"] = posty90_child_pugh_points
                                st.session_state.data.at[index, "POSTY90_30DY_MELD"] = posty90_meld
                                st.session_state.data.at[index, "POSTY90_30DY_MELDNa"] = posty90_meld_na
                                st.session_state.data.at[index, "POSTY90_30DY_ALBIscore"] = posty90_albi_score
                                st.session_state.data.at[index, "POSTY90_30DY_ALBIgrade"] = posty90_albi_grade
                                st.session_state.data.at[index, "POSTY90_30DY_BCLC"] = posty90_bclc
                                st.session_state.data.at[index, "Ken_BCLCStagepost90"] = ken_bclc_stage_post90
                                st.session_state.data.at[index, "Ken_MELD_Stagepost90"] = ken_meld_stage_post90

                                st.session_state.data.at[index, "30DY_AE_Portalhtn"] = DYAE_CTCAE_portal_htn
                                st.session_state.data.at[index, "30DY_AE_Vascularcomp"] = DYAE_CTCAE_Vascular_comp
                                st.session_state.data.at[index, "30DY_AE_Fatigue"] = DYAE_CTCAE_fatigue
                                st.session_state.data.at[index, "30DY_AE_Diarrhea"] = DYAE_CTCAE_diarrhea
                                st.session_state.data.at[index, "30DY_AE_Hypoalbuminemia"] = DYAE_CTCAE_hypoalbuminemia_emr
                                st.session_state.data.at[index, "30DY_AE_Hyperbilirubinemia"] = DYAE_CTCAE_hyperbilirubinemia_emr
                                st.session_state.data.at[index, "30DY_AE_Increasecreatine"] = DYAE_CTCAE_Increase_creatinine_emr
                                st.session_state.data.at[index, "30DY_AE_Abdominalpain"] = DYAE_CTCAE_abdominal_pain
                                st.session_state.data.at[index, "30DY_AE_Sepsis"] = DYAE_CTCAE_sepsis
                                st.session_state.data.at[index, "30DY_AE_BacterialPer"] = DYAE_CTCAE_bacterial_peritonitis
                                st.session_state.data.at[index, "30DY_AE_Hemorrhage"] = DYAE_CTCAE_hemorrhage
                                st.session_state.data.at[index, "30DY_AE_Anorexia"] = DYAE_CTCAE_anorexia
                                st.session_state.data.at[index, "30DY_AE_Intrahepaticfistula"] = DYAE_CTCAE_intrahepatic_fistula
                                st.session_state.data.at[index, "30DY_AE_Constipation"] = DYAE_CTCAE_constipation
                                st.session_state.data.at[index, "30DY_AE_Nausea"] = DYAE_CTCAE_nausea
                                st.session_state.data.at[index, "30DY_AE_Vomiting"] = DYAE_CTCAE_vomiting
                                st.session_state.data.at[index, "30DY_AE_Cholecystitis"] = DYAE_CTCAE_cholecystitis
                                st.session_state.data.at[index, "30DY_AE_Gastriculcer"] = DYAE_CTCAE_gastric_ulcers
                                st.session_state.data.at[index, "30DY_AE_Hyperkalemia"] = DYAE_CTCAE_hyperkalemia
                                st.session_state.data.at[index, "30DY_AE_Respfailure"] = DYAE_CTCAE_respiratory_failure
                                st.session_state.data.at[index, "30DY_AE_AKI"] = DYAE_CTCAE_AKI
                                st.session_state.data.at[index, "30DY_AE_Radiationpneumonitis"] = DYAE_CTCAE_Radiation_pneumonitis
                                st.session_state.data.at[index, "30DY_AE_Other"] = DYAE_AE_other
                                st.session_state.data.at[index, "90DY_AE_date_of_AE"] = DYAE_AE_date_of_AE
                                st.session_state.data.at[index, "Additional Notes FT"] = ken_grandedtoxicity
                                st.session_state.data.at[index, "90DY_AE_Hosp3mo"] = dy_ae_hospitalization_3
                                st.session_state.data.at[index, "90DY_AE_Datehosp3mo"] = dy_ae_hospitalization_6
                                st.session_state.data.at[index, "90DY_AE_Hosp6mo"] = dy_ae_hosp6mo
                                st.session_state.data.at[index, "90DY_AE_DeathduetoAE"] = dy_ae_death_due

                                st.success("DAYY90 added successfully.")
                    except:
                        st.warning("Please Fill Patient Information Page")
        
        elif st.session_state.selected_tab == "Other Post Tare":
            st.subheader("Other_post_TARE")
            with st.form("other_post_tare_form"):
                if "MRN" not in st.session_state.data:
                    st.warning("Please complete the Patient Information tab first.")
                else:
                    try:
                        oc_liver_transplant = st.radio("OC_Liver_transplant", options=["yes", "no"])
                        oc_liver_transplant_date = st.date_input("OC_Liver_transplant_date")

                        st.subheader("K_other")
            # with st.form("k_other_form"):

                        k_ken_toxgtg3 = st.number_input("K_ken_ToxgtG3")
                        if k_ken_toxgtg3 > 3:
                            k_ken_toxgtg3 = 1
                        else:
                            k_ken_toxgtg3 =0
                                        
                        k_ken_toxgtg2 = st.number_input("K_ken_ToxgtG2")
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
                        
                    # prey90_bilirubin = st.session_state.data.loc[
                        #   st.session_state.data['MRN'] == st.session_state.temp_mrn, 
                        #    'PREY90_Bilirubin'
                        #]
                    # prey90_albumin = st.session_state.data.loc[
                        #   st.session_state.data['MRN'] == st.session_state.temp_mrn, 
                        #   'PREY90_Albumin'
                        #]
                        #prey90_bilirubin = prey90_bilirubin.isnull().all()
                        #prey90_albumin = prey90_albumin.isnull().all()
                    # if posty90_albumin.isnull(np.nan):
                        # st.write("Please enter the albumin value in the Pre Y90 tab.")
                    # else:             
                        #  k_ken_albipretareraw = albi_calc(prey90_bilirubin,prey90_albumin)
                        #  k_ken_albipretaregrade = albigrade(k_ken_albipretareraw)
                        
                        #posty90_bilirubin = st.session_state.data.loc[
                        #   st.session_state.data['MRN'] == st.session_state.temp_mrn, 
                        #   'POSTY90_30DY_bilirubin'
                        #].values[0]

                        #posty90_albumin = st.session_state.data.loc[
                        #    st.session_state.data['MRN'] == st.session_state.temp_mrn, 
                        #    'POSTY90_30DY_albumin'
                        #].values[0]

                        #posty90_bilirubin = posty90_bilirubin.isnull().all()
                        #posty90_albumin = posty90_albumin.isnull.all()
                        #if posty90_albumin.isnull(np.nan):
                            #st.write("Please enter the albumin value in the Pre Y90 tab.")
                        #else:             
                        #  k_ken_albiposttareraw = albi_calc(posty90_bilirubin,posty90_albumin)
                        # k_ken_albiposttaregrade = albigrade(k_ken_albiposttareraw)


                        submit_tab9 = st.form_submit_button("Submit")

                        if submit_tab9:
                            index = st.session_state.data[st.session_state.data["MRN"] == st.session_state.temp_mrn].index[0]

                            st.session_state.data.at[index, "OC_Liver_transplant"] = oc_liver_transplant
                            st.session_state.data.at[index, "OC_Liver_transplant_date"] = oc_liver_transplant_date
                            st.session_state.data.at[index, "K_ken_ToxgtG3"] = k_ken_toxgtg3
                            st.session_state.data.at[index, "K_ken_ToxgtG2"] = k_ken_toxgtg2
                            #st.session_state.data.at[index, "K_ken_AlbiPreTARERaw"] = k_ken_albipretareraw
                            #st.session_state.data.at[index, "K_ken_AlbiPreTAREGrade"] = k_ken_albipretaregrade
                            #st.session_state.data.at[index, "K_ken_AlbiPostTARERaw"] = k_ken_albiposttareraw
                            #st.session_state.data.at[index, "K_ken_AliPostTAREGrade"] = k_ken_albiposttaregrade

                            st.success("Other Post Tare added successfully.")
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
                        PREY90_TL1_LAD = st.number_input(
                            "PREY90_TL1_LAD",
                            format="%.2f"
                        )

                        PREY90_Target_Lesion_1_PAD = st.number_input(
                            "PREY90_Target Lesion 1 PAD",
                            format="%.2f"
                        )

                        PREY90_Target_Lesion_1_CCD = st.number_input(
                            "PREY90_Target Lesion 1 CCD",
                            format="%.2f"
                        )
                        PREY90_Target_Lesion_1_VOL = 4/3*3.14*(PREY90_Target_Lesion_1_PAD)*(PREY90_TL1_LAD)*PREY90_Target_Lesion_1_CCD
                        PREY90_Target_Lesion_2_segments = st.selectbox(
                                "PREY90_Target_Lesion_2_segments",
                                options=["1","2","3","4a","4b","5","6","7","8","NA"],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )
                        PREY90_Target_Lesion_2_LAD = st.number_input(
                            "PREY90_Target_Lesion_2_LAD",
                            format="%.2f"
                        )
                        PREY90_Target_Lesion_2_PAD = st.number_input(
                            "PREY90_Target Lesion 2 PAD",
                            format="%.2f"
                        )

                        PREY90_Target_Lesion_2_CCD = st.number_input(
                            "PREY90_Target Lesion 2 CCD",
                            format="%.2f"
                        )
                        PREY90_Target_Lesion_2_VOL = 4/3*3.14*(PREY90_Target_Lesion_2_PAD)*(PREY90_Target_Lesion_2_LAD)*PREY90_Target_Lesion_2_CCD

                        PREY90_pretx_targeted_Lesion_Dia_Sum = max(PREY90_TL1_LAD,PREY90_Target_Lesion_1_PAD,PREY90_Target_Lesion_1_CCD)+max(PREY90_Target_Lesion_2_PAD,PREY90_Target_Lesion_2_LAD,PREY90_Target_Lesion_2_CCD)

                        PREY90_Non_Target_Lesion_Location = st.selectbox( "PREY90_Non-Target Lesion Location" , options=["1","2","3","4a","4b","5","6","7","8","NA"],
                        index=None,  # No default selection
                        placeholder="Choose an option",)

                        PREY90_Non_Target_Lesion_2_LAD_Art_Enhanc = st.number_input(
                            "PREY90_Non_Target_Lesion_2_LAD_Art_Enhanc",
                            format="%.2f"
                        )
                        PREY90_Non_Target_Lesion_2_PAD_Art_Enhanc = st.number_input(
                            "PREY90_Non_Target_Lesion_2_PAD_Art_Enhanc",
                            format="%.2f"
                        )

                        PREY90_Non_Target_Lesion_2_CCD_Art_Enhanc = st.number_input(
                            "PREY90_Non_Target_Lesion_2_CCD_Art_Enhanc",
                            format="%.2f"
                        )
                        PREY90_Non_targeted_Lesion_Dia_Sum = max(PREY90_Non_Target_Lesion_2_PAD_Art_Enhanc,PREY90_Non_Target_Lesion_2_LAD_Art_Enhanc,PREY90_Non_Target_Lesion_2_CCD_Art_Enhanc)

                        PREY90_Reviewers_Initials = st.text_input(
                            "PREY90_Reviewers Initials",
                            help="Free-text input for reviewer name"
                        )

                        PREY90_Pre_Y90_Extrahepatic_Disease = st.selectbox(
                            "PREY90_Pre Y90 Extrahepatic Disease",
                            options=["Yes", "No", "N/A"],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )

                        PREY90_Pre_Y90_Extrahepatic_Disease_Location = st.text_input(
                            "PREY90_Pre Y90 Extrahepatic Disease Location",
                            help="Free Text"
                        )

                        PREY90_PVT = st.selectbox(
                            "PREY90_PVT",
                            options=["Yes", "No", "N/A"],
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
                            options=["Yes", "No", "N/A"],
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

                        st.session_state.data['TAREdate'] = pd.to_datetime(st.session_state.data['TAREdate'])

                        # Fetch the relevant date for the current MRN
                        
                        fetch_date = st.session_state.data.loc[
                                st.session_state.data['MRN'] == st.session_state.temp_mrn, 
                                'TAREdate'
                            ].values[0]
                        
                        st.write("Enter Patient Entry")

                        # Convert fetch_date to a datetime.date object
                        fetch_date = pd.to_datetime(fetch_date).date()


        
                        FU_Months_Since_Y90 = relativedelta(FU_Imaging_Date, fetch_date).months

                        FU_Total_number_of_lesions = st.selectbox(
                            "1st_FU_Total number of lesions",
                            options=["1", "2", ">3"],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )

                        FU_Target_Lesion_1_LAD_Art_Enhanc = st.number_input(
                            "1st_FU_Target Lesion 1 LAD Art Enhanc",
                            format="%.2f"
                        )

                        FU_Target_Lesion_1_PAD_Art_Enhanc = st.number_input(
                            "1st_FU_Target Lesion 1 PAD Art Enhanc",
                            format="%.2f"
                        )

                        FU_Target_Lesion_1_CCD_Art_Enhanc = st.number_input(
                            "1st_FU_Target Lesion 1 CCD Art Enhanc",
                            format="%.2f"
                        )

                        FU_Target_Lesion_2_Segments = st.selectbox(
                            "1st_FU_Target Lesion 2 Segments",
                            options=["1", "2", "3", "4a", "4b", "5", "6", "7", "8", "NA"],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )

                        FU_Target_Lesion_2_LAD_Art_Enhanc = st.number_input(
                            "1st_FU_Target Lesion 2 LAD Art Enhanc",
                            format="%.2f"
                        )

                        FU_Target_Lesion_2_PAD_Art_Enhanc = st.number_input(
                            "1st_FU_Target Lesion 2 PAD Art Enhanc",
                            format="%.2f"
                        )

                        FU_Target_Lesion_2_CCD_Art_Enhanc = st.number_input(
                            "1st_FU_Target Lesion 2 CCD Art Enhanc",
                            format="%.2f"
                        )

                        # Assuming "Follow up 1 targeted Lesion Dia Sum" is calculated elsewhere in the code
                        # FU_Follow_up_1_targeted_Lesion_Dia_Sum = calculated_value
                        FU_Follow_up_1_targeted_Lesion_Dia_Sum = max(FU_Target_Lesion_1_CCD_Art_Enhanc,FU_Target_Lesion_1_PAD_Art_Enhanc,FU_Target_Lesion_1_LAD_Art_Enhanc)+max(FU_Target_Lesion_2_CCD_Art_Enhanc,FU_Target_Lesion_2_PAD_Art_Enhanc,FU_Target_Lesion_2_LAD_Art_Enhanc)


                        FU_Non_Target_Lesion_2_LAD_Art_Enhanc = st.number_input(
                            "1st_FU_Non-Target Lesion 2 LAD Art Enhanc",
                            format="%.2f"
                        )

                        FU_Non_Target_Lesion_2_PAD_Art_Enhanc = st.number_input(
                            "1st_FU_Non-Target Lesion 2 PAD Art Enhanc",
                            format="%.2f"
                        )

                        FU_Non_Target_Lesion_2_CCD_Art_Enhanc = st.number_input(
                            "1st_FU_Non-Target Lesion 2 CCD Art Enhanc",
                            format="%.2f"
                        )

                        # Assuming "Non-targeted Lesion Dia Sum" is calculated elsewhere in the code
                        FU_Non_targeted_Lesion_Dia_Sum = max(FU_Non_Target_Lesion_2_LAD_Art_Enhanc,FU_Non_Target_Lesion_2_PAD_Art_Enhanc,FU_Non_Target_Lesion_2_CCD_Art_Enhanc)

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

                        FU_change_target_lesion = ((PREY90_pretx_targeted_Lesion_Dia_Sum - FU_Follow_up_1_targeted_Lesion_Dia_Sum)/max(1,PREY90_pretx_targeted_Lesion_Dia_Sum))*100

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

                        FU2_Total_number_of_lesions = st.selectbox(
                            "2nd_FU_Total number of lesions",
                            options=["1", "2", ">3"],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )

                        FU2_Target_Lesion_1_LAD_Art_Enhanc = st.number_input(
                            "2nd_FU_Target Lesion 1 LAD Art Enhanc",
                            format="%.2f"
                        )

                        FU2_Target_Lesion_1_PAD_Art_Enhanc = st.number_input(
                            "2nd_FU_Target Lesion 1 PAD Art Enhanc",
                            format="%.2f"
                        )

                        FU2_Target_Lesion_1_CCD_Art_Enhanc = st.number_input(
                            "2nd_FU_Target Lesion 1 CCD Art Enhanc",
                            format="%.2f"
                        )

                        FU2_Target_Lesion_2_Segments = st.selectbox(
                            "2nd_FU_Target Lesion 2 Segments",
                            options=["1", "2", "3", "4a", "4b", "5", "6", "7", "8", "NA"],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )

                        FU2_Target_Lesion_2_LAD_Art_Enhanc = st.number_input(
                            "2nd_FU_Target Lesion 2 LAD Art Enhanc",
                            format="%.2f"
                        )

                        FU2_Target_Lesion_2_PAD_Art_Enhanc = st.number_input(
                            "2nd_FU_Target Lesion 2 PAD Art Enhanc",
                            format="%.2f"
                        )

                        FU2_Target_Lesion_2_CCD_Art_Enhanc = st.number_input(
                            "2nd_FU_Target Lesion 2 CCD Art Enhanc",
                            format="%.2f"
                        )

                        FU2_Follow_up_2_targeted_Lesion_Dia_Sum = max(FU2_Target_Lesion_1_CCD_Art_Enhanc, FU2_Target_Lesion_1_PAD_Art_Enhanc, FU2_Target_Lesion_1_LAD_Art_Enhanc) + max(FU2_Target_Lesion_2_CCD_Art_Enhanc, FU2_Target_Lesion_2_PAD_Art_Enhanc, FU2_Target_Lesion_2_LAD_Art_Enhanc)

                        FU2_Non_Target_Lesion_1_LAD_Art_Enhanc = st.number_input(
                            "2nd_FU_Non-Target Lesion 1 LAD Art Enhanc",
                            format="%.2f"
                        )

                        FU2_Non_Target_Lesion_1_PAD_Art_Enhanc = st.number_input(
                            "2nd_FU_Non-Target Lesion 1 PAD Art Enhanc",
                            format="%.2f"
                        )

                        FU2_Non_Target_Lesion_1_CCD_Art_Enhanc = st.number_input(
                            "2nd_FU_Non-Target Lesion 1 CCD Art Enhanc",
                            format="%.2f"
                        )

                        FU2_Non_targeted_Lesion_Dia_Sum = max(FU2_Non_Target_Lesion_1_LAD_Art_Enhanc, FU2_Non_Target_Lesion_1_PAD_Art_Enhanc, FU2_Non_Target_Lesion_1_CCD_Art_Enhanc)

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

                        FU2_change_target_lesion = ((PREY90_pretx_targeted_Lesion_Dia_Sum - FU2_Follow_up_2_targeted_Lesion_Dia_Sum) / max(1,PREY90_pretx_targeted_Lesion_Dia_Sum)) * 100

                        FU2_Free_Text = st.text_area(
                            "2nd_FU_Free Text",
                            help="Free text"
                        )

                        # Repeat the same structure for 3rd, 4th, and 5th follow-ups with variable names changed accordingly

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

                        FU3_Total_number_of_lesions = st.selectbox(
                            "3rd_FU_Total number of lesions",
                            options=["1", "2", ">3"],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )

                        FU3_Target_Lesion_1_LAD_Art_Enhanc = st.number_input(
                            "3rd_FU_Target Lesion 1 LAD Art Enhanc",
                            format="%.2f"
                        )

                        FU3_Target_Lesion_1_PAD_Art_Enhanc = st.number_input(
                            "3rd_FU_Target Lesion 1 PAD Art Enhanc",
                            format="%.2f"
                        )

                        FU3_Target_Lesion_1_CCD_Art_Enhanc = st.number_input(
                            "3rd_FU_Target Lesion 1 CCD Art Enhanc",
                            format="%.2f"
                        )

                        FU3_Target_Lesion_2_Segments = st.selectbox(
                            "3rd_FU_Target Lesion 2 Segments",
                            options=["1", "2", "3", "4a", "4b", "5", "6", "7", "8", "NA"],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )

                        FU3_Target_Lesion_2_LAD_Art_Enhanc = st.number_input(
                            "3rd_FU_Target Lesion 2 LAD Art Enhanc",
                            format="%.2f"
                        )

                        FU3_Target_Lesion_2_PAD_Art_Enhanc = st.number_input(
                            "3rd_FU_Target Lesion 2 PAD Art Enhanc",
                            format="%.2f"
                        )

                        FU3_Target_Lesion_2_CCD_Art_Enhanc = st.number_input(
                            "3rd_FU_Target Lesion 2 CCD Art Enhanc",
                            format="%.2f"
                        )

                        FU3_Follow_up_2_targeted_Lesion_Dia_Sum = max(FU3_Target_Lesion_1_CCD_Art_Enhanc, FU3_Target_Lesion_1_PAD_Art_Enhanc, FU3_Target_Lesion_1_LAD_Art_Enhanc) + max(FU3_Target_Lesion_2_CCD_Art_Enhanc, FU3_Target_Lesion_2_PAD_Art_Enhanc, FU3_Target_Lesion_2_LAD_Art_Enhanc)

                        FU3_Non_Target_Lesion_1_LAD_Art_Enhanc = st.number_input(
                            "3rd_FU_Non-Target Lesion 1 LAD Art Enhanc",
                            format="%.2f"
                        )

                        FU3_Non_Target_Lesion_1_PAD_Art_Enhanc = st.number_input(
                            "3rd_FU_Non-Target Lesion 1 PAD Art Enhanc",
                            format="%.2f"
                        )

                        FU3_Non_Target_Lesion_1_CCD_Art_Enhanc = st.number_input(
                            "3rd_FU_Non-Target Lesion 1 CCD Art Enhanc",
                            format="%.2f"
                        )

                        FU3_Non_targeted_Lesion_Dia_Sum = max(FU3_Non_Target_Lesion_1_LAD_Art_Enhanc, FU3_Non_Target_Lesion_1_PAD_Art_Enhanc, FU3_Non_Target_Lesion_1_CCD_Art_Enhanc)

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

                        FU3_change_target_lesion = ((PREY90_pretx_targeted_Lesion_Dia_Sum - FU3_Follow_up_2_targeted_Lesion_Dia_Sum) / max(1,PREY90_pretx_targeted_Lesion_Dia_Sum)) * 100

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

                        FU4_Total_number_of_lesions = st.selectbox(
                            "4th_FU_Total number of lesions",
                            options=["1", "2", ">3"],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )

                        FU4_Target_Lesion_1_LAD_Art_Enhanc = st.number_input(
                            "4th_FU_Target Lesion 1 LAD Art Enhanc",
                            format="%.2f"
                        )

                        FU4_Target_Lesion_1_PAD_Art_Enhanc = st.number_input(
                            "4th_FU_Target Lesion 1 PAD Art Enhanc",
                            format="%.2f"
                        )

                        FU4_Target_Lesion_1_CCD_Art_Enhanc = st.number_input(
                            "4th_FU_Target Lesion 1 CCD Art Enhanc",
                            format="%.2f"
                        )

                        FU4_Target_Lesion_2_Segments = st.selectbox(
                            "4th_FU_Target Lesion 2 Segments",
                            options=["1", "2", "3", "4a", "4b", "5", "6", "7", "8", "NA"],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )

                        FU4_Target_Lesion_2_LAD_Art_Enhanc = st.number_input(
                            "4th_FU_Target Lesion 2 LAD Art Enhanc",
                            format="%.2f"
                        )

                        FU4_Target_Lesion_2_PAD_Art_Enhanc = st.number_input(
                            "4th_FU_Target Lesion 2 PAD Art Enhanc",
                            format="%.2f"
                        )

                        FU4_Target_Lesion_2_CCD_Art_Enhanc = st.number_input(
                            "4th_FU_Target Lesion 2 CCD Art Enhanc",
                            format="%.2f"
                        )

                        FU4_Follow_up_2_targeted_Lesion_Dia_Sum = max(FU4_Target_Lesion_1_CCD_Art_Enhanc, FU4_Target_Lesion_1_PAD_Art_Enhanc, FU4_Target_Lesion_1_LAD_Art_Enhanc) + max(FU4_Target_Lesion_2_CCD_Art_Enhanc, FU4_Target_Lesion_2_PAD_Art_Enhanc, FU4_Target_Lesion_2_LAD_Art_Enhanc)

                        FU4_Non_Target_Lesion_1_LAD_Art_Enhanc = st.number_input(
                            "4th_FU_Non-Target Lesion 1 LAD Art Enhanc",
                            format="%.2f"
                        )

                        FU4_Non_Target_Lesion_1_PAD_Art_Enhanc = st.number_input(
                            "4th_FU_Non-Target Lesion 1 PAD Art Enhanc",
                            format="%.2f"
                        )

                        FU4_Non_Target_Lesion_1_CCD_Art_Enhanc = st.number_input(
                            "4th_FU_Non-Target Lesion 1 CCD Art Enhanc",
                            format="%.2f"
                        )

                        FU4_Non_targeted_Lesion_Dia_Sum = max(FU4_Non_Target_Lesion_1_LAD_Art_Enhanc, FU4_Non_Target_Lesion_1_PAD_Art_Enhanc, FU4_Non_Target_Lesion_1_CCD_Art_Enhanc)

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

                        FU4_change_target_lesion = ((PREY90_pretx_targeted_Lesion_Dia_Sum - FU4_Follow_up_2_targeted_Lesion_Dia_Sum) / max(1,PREY90_pretx_targeted_Lesion_Dia_Sum)) * 100

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

                        FU5_Total_number_of_lesions = st.selectbox(
                            "5th_FU_Total number of lesions",
                            options=["1", "2", ">3"],
                        index=None,  # No default selection
                        placeholder="Choose an option",
                        )

                        FU5_Non_Target_Lesion_1_LAD_Art_Enhanc = st.number_input(
                            "5th_FU_Non-Target Lesion 1 LAD Art Enhanc",
                            format="%.2f"
                        )

                        FU5_Non_Target_Lesion_1_PAD_Art_Enhanc = st.number_input(
                            "5th_FU_Non-Target Lesion 1 PAD Art Enhanc",
                            format="%.2f"
                        )

                        FU5_Non_Target_Lesion_1_CCD_Art_Enhanc = st.number_input(
                            "5th_FU_Non-Target Lesion 1 CCD Art Enhanc",
                            format="%.2f"
                        )

                        FU5_Non_targeted_Lesion_Dia_Sum = max(FU5_Non_Target_Lesion_1_LAD_Art_Enhanc, FU5_Non_Target_Lesion_1_PAD_Art_Enhanc, FU5_Non_Target_Lesion_1_CCD_Art_Enhanc)

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

                        Date_of_Localized_Progression = st.text_input("Date of Localized Progression")

                        if Date_of_Localized_Progression == "No Progression":
                                Time_to_localized_progression = 'NA'
                        else:
                                Time_to_Localized_Progression = relativedelta(Date_of_Localized_Progression, fetch_date).years

                        Date_of_Overall_Progression = st.text_input("Date of Overall Progression")

                        if Date_of_Overall_Progression == "No Progression":
                                Time_to_overall_progression = 'NA'
                        else:
                                Time_to_overall_Progression = relativedelta(Date_of_Overall_Progression, fetch_date).years

                        Date_of_Last_Follow_up_last_imaging_date = 'NA' if dead == 1 and OLT == 1 else st.date_input("Date of Last Follow-up/last imaging date")

                        Time_to_Last_Follow_up_last_imaging_date = 'NA' if dead == 1 and OLT == 1 else relativedelta(Date_of_Last_Follow_up_last_imaging_date, fetch_date).years 

                        submit_tab10 = st.form_submit_button("Submit")

                        if submit_tab10:
                            index = st.session_state.data[st.session_state.data["MRN"] == st.session_state.temp_mrn].index[0]

                            st.session_state.data.at[index, "PREY90_prescan_modality"] = PREY90_prescan_modality
                            st.session_state.data.at[index, "PREY90_Imaging Date"] = PREY90_Imaging_Date
                            st.session_state.data.at[index, "PREY90_total number of lesions"] = PREY90_total_number_of_lesions
                            st.session_state.data.at[index, "PREY90_Number Involved Lobes"] = PREY90_Number_Involved_Lobes
                            st.session_state.data.at[index, "PREY90_target_lesion_1_segments"] = PREY90_target_lesion_1_segments
                            st.session_state.data.at[index, "PREY90_TL1_LAD"] = PREY90_TL1_LAD
                            st.session_state.data.at[index, "PREY90_Target Lesion 1 PAD"] = PREY90_Target_Lesion_1_PAD
                            st.session_state.data.at[index, "PREY90_Target Lesion 1 CCD"] = PREY90_Target_Lesion_1_CCD
                            st.session_state.data.at[index, "PREY90_Target Lesion 1 VOL"] = PREY90_Target_Lesion_1_VOL
                            st.session_state.data.at[index, "PREY90_Target lesion 2 Segments"] = PREY90_Target_Lesion_2_segments
                            st.session_state.data.at[index, "PREY90_Target Lesion 2 LAD"] = PREY90_Target_Lesion_2_LAD
                            st.session_state.data.at[index, "PREY90_Target Lesion 2 PAD"] = PREY90_Target_Lesion_2_PAD
                            st.session_state.data.at[index, "PREY90_Target Lesion 2 CCD"] = PREY90_Target_Lesion_2_CCD
                            st.session_state.data.at[index, "PREY90_Target Lesion 2 VOL"] = PREY90_Target_Lesion_2_VOL
                            st.session_state.data.at[index, "PREY90_pretx targeted Lesion Dia Sum"] = PREY90_pretx_targeted_Lesion_Dia_Sum
                            st.session_state.data.at[index, "PREY90_Non-Target Lesion Location"] = PREY90_Non_Target_Lesion_Location
                            st.session_state.data.at[index, "PREY90_Non-Target Lesion 2 LAD Art Enhanc"] = PREY90_Non_Target_Lesion_2_LAD_Art_Enhanc
                            st.session_state.data.at[index, "PREY90_Non-Target Lesion 2 PAD Art Enhanc"] = PREY90_Non_Target_Lesion_2_PAD_Art_Enhanc
                            st.session_state.data.at[index, "PREY90_Non-Target Lesion 2 CCD Art Enhanc"] = PREY90_Non_Target_Lesion_2_CCD_Art_Enhanc
                            st.session_state.data.at[index, "PREY90_Non-targeted Lesion Dia Sum"] = PREY90_Non_targeted_Lesion_Dia_Sum
                            st.session_state.data.at[index, "PREY90_Reviewers Initials"] = PREY90_Reviewers_Initials
                            st.session_state.data.at[index, "PREY90_Pre Y90 Extrahepatic Disease"] = PREY90_Pre_Y90_Extrahepatic_Disease
                            st.session_state.data.at[index, "PREY90_Pre Y90 Extrahepatic Disease Location"] = PREY90_Pre_Y90_Extrahepatic_Disease_Location
                            st.session_state.data.at[index, "PREY90_PVT"] = PREY90_PVT
                            st.session_state.data.at[index, "PREY90_PVT Location"] = PREY90_PVT_Location
                            st.session_state.data.at[index, "PREY90_Features of cirrhosis"] = PREY90_Features_of_cirrhosis
                            st.session_state.data.at[index, "1st_FU_Scan Modality"] = FU_Scan_Modality
                            st.session_state.data.at[index, "1st_FU_Imaging Date"] = FU_Imaging_Date
                            st.session_state.data.at[index, "1st_FU_Months Since Y90"] = FU_Months_Since_Y90
                            st.session_state.data.at[index, "1st_FU_Total number of lesions"] = FU_Total_number_of_lesions
                            st.session_state.data.at[index, "1st_FU_Target Lesion 1 LAD Art Enhanc"] = FU_Target_Lesion_1_LAD_Art_Enhanc
                            st.session_state.data.at[index, "1st_FU_Target Lesion 1 PAD Art Enhanc"] = FU_Target_Lesion_1_PAD_Art_Enhanc
                            st.session_state.data.at[index, "1st_FU_Target Lesion 1 CCD Art Enhanc"] = FU_Target_Lesion_1_CCD_Art_Enhanc
                            st.session_state.data.at[index, "1st_FU_Target Lesion 2 Segments"] = FU_Target_Lesion_2_Segments
                            st.session_state.data.at[index, "1st_FU_Target Lesion 2 LAD Art Enhanc"] = FU_Target_Lesion_2_LAD_Art_Enhanc
                            st.session_state.data.at[index, "1st_FU_Target Lesion 2 PAD Art Enhanc"] = FU_Target_Lesion_2_PAD_Art_Enhanc
                            st.session_state.data.at[index, "1st_FU_Target Lesion 2 CCD Art Enhanc"] = FU_Target_Lesion_2_CCD_Art_Enhanc
                            st.session_state.data.at[index, "1st_FU_Follow up 1 targeted Lesion Dia Sum"] = FU_Follow_up_1_targeted_Lesion_Dia_Sum
                            st.session_state.data.at[index, "1st_FU_Non-Target Lesion 2 LAD Art Enhanc"] = FU_Non_Target_Lesion_2_LAD_Art_Enhanc
                            st.session_state.data.at[index, "1st_FU_Non-Target Lesion 2 PAD Art Enhanc"] = FU_Non_Target_Lesion_2_PAD_Art_Enhanc
                            st.session_state.data.at[index, "1st_FU_Non-Target Lesion 2 CCD Art Enhanc"] = FU_Non_Target_Lesion_2_CCD_Art_Enhanc
                            st.session_state.data.at[index, "1st_FU_Non-targeted Lesion Dia Sum"] = FU_Non_targeted_Lesion_Dia_Sum
                            st.session_state.data.at[index, "1st_FU_Lesion Necrosis"] = FU_Lesion_Necrosis
                            st.session_state.data.at[index, "1st_FU_Reviewers Initials"] = FU_Reviewers_Initials
                            st.session_state.data.at[index, "1st_FU_Non target lesion response"] = FU_Non_target_lesion_response
                            st.session_state.data.at[index, "1st_FU_New Lesions"] = FU_New_Lesions
                            st.session_state.data.at[index, "1st_FU_NEW Extrahepatic Disease"] = FU_NEW_Extrahepatic_Disease
                            st.session_state.data.at[index, "1st_FU_NEW Extrahepatic Dz Location"] = FU_NEW_Extrahepatic_Dz_Location
                            st.session_state.data.at[index, "1st_FU_NEW Extrahepatic Dz Date"] = FU_NEW_Extrahepatic_Dz_Date
                            st.session_state.data.at[index, "1st_FU_% change non target lesion"] = FU_change_non_target_lesion
                            st.session_state.data.at[index, "1st_FU_% Change Target Dia"] = FU_change_target_lesion
                            st.session_state.data.at[index, "1st_FU_Free Text"] = FU_Free_Text
                            st.session_state.data.at[index, "2nd_FU_Scan Modality"] = FU2_Scan_Modality
                            st.session_state.data.at[index, "2nd_FU_Imaging Date"] = FU2_Imaging_Date
                            st.session_state.data.at[index, "2nd_FU_Months Since Y90"] = FU2_Months_Since_Y90
                            st.session_state.data.at[index, "2nd_FU_Total number of lesions"] = FU2_Total_number_of_lesions
                            st.session_state.data.at[index, "2nd_FU_Target Lesion 1 LAD Art Enhanc"] = FU2_Target_Lesion_1_LAD_Art_Enhanc
                            st.session_state.data.at[index, "2nd_FU_Target Lesion 1 PAD Art Enhanc"] = FU2_Target_Lesion_1_PAD_Art_Enhanc
                            st.session_state.data.at[index, "2nd_FU_Target Lesion 1 CCD Art Enhanc"] = FU2_Target_Lesion_1_CCD_Art_Enhanc
                            st.session_state.data.at[index, "2nd_FU_Target Lesion 2 Segments"] = FU2_Target_Lesion_2_Segments
                            st.session_state.data.at[index, "2nd_FU_Target Lesion 2 LAD Art Enhanc"] = FU2_Target_Lesion_2_LAD_Art_Enhanc
                            st.session_state.data.at[index, "2nd_FU_Target Lesion 2 PAD Art Enhanc"] = FU2_Target_Lesion_2_PAD_Art_Enhanc
                            st.session_state.data.at[index, "2nd_FU_Target Lesion 2 CCD Art Enhanc"] = FU2_Target_Lesion_2_CCD_Art_Enhanc
                            st.session_state.data.at[index, "2nd_FU_Follow up 2 targeted Lesion Dia Sum"] = FU2_Follow_up_2_targeted_Lesion_Dia_Sum
                            st.session_state.data.at[index, "2nd_FU_Non-Target Lesion 1 LAD Art Enhanc"] = FU2_Non_Target_Lesion_1_LAD_Art_Enhanc
                            st.session_state.data.at[index, "2nd_FU_Non-Target Lesion 1 PAD Art Enhanc"] = FU2_Non_Target_Lesion_1_PAD_Art_Enhanc
                            st.session_state.data.at[index, "2nd_FU_Non-Target Lesion 1 CCD Art Enhanc"] = FU2_Non_Target_Lesion_1_CCD_Art_Enhanc
                            st.session_state.data.at[index, "2nd_FU_Non-targeted Lesion Dia Sum"] = FU2_Non_targeted_Lesion_Dia_Sum
                            st.session_state.data.at[index, "2nd_FU_Lesion Necrosis"] = FU2_Lesion_Necrosis
                            st.session_state.data.at[index, "2nd_FU_Reviewers Initials"] = FU2_Reviewers_Initials
                            st.session_state.data.at[index, "2nd_FU_Non target lesion response"] = FU2_Non_target_lesion_response
                            st.session_state.data.at[index, "2nd_FU_New Lesions"] = FU2_New_Lesions
                            st.session_state.data.at[index, "2nd_FU_Extrahepatic Disease"] = FU2_NEW_Extrahepatic_Disease
                            st.session_state.data.at[index, "2nd_FU_NEW Extrahepatic Dz Location"] = FU2_NEW_Extrahepatic_Dz_Location
                            st.session_state.data.at[index, "2nd_FU_NEW Extrahepatic Dz Date"] = FU2_NEW_Extrahepatic_Dz_Date
                            st.session_state.data.at[index, "2nd_FU_% change non target lesion"] = FU2_change_non_target_lesion
                            st.session_state.data.at[index, "2nd_FU_% Change Target Dia"] = FU2_change_target_lesion
                            st.session_state.data.at[index, "2nd_FU_Free Text"] = FU2_Free_Text
                            st.session_state.data.at[index, "3rd_FU_Scan Modality"] = FU3_Scan_Modality
                            st.session_state.data.at[index, "3rd_FU_Imaging Date"] = FU3_Imaging_Date
                            st.session_state.data.at[index, "3rd_FU_Months Since Y90"] = FU3_Months_Since_Y90
                            st.session_state.data.at[index, "3rd_FU_Total number of lesions"] = FU3_Total_number_of_lesions
                            st.session_state.data.at[index, "3rd_FU_Target Lesion 1 LAD Art Enhanc"] = FU3_Target_Lesion_1_LAD_Art_Enhanc
                            st.session_state.data.at[index, "3rd_FU_Target Lesion 1 PAD Art Enhanc"] = FU3_Target_Lesion_1_PAD_Art_Enhanc
                            st.session_state.data.at[index, "3rd_FU_Target Lesion 1 CCD Art Enhanc"] = FU3_Target_Lesion_1_CCD_Art_Enhanc
                            st.session_state.data.at[index, "3rd_FU_Target Lesion 2 Segments"] = FU3_Target_Lesion_2_Segments
                            st.session_state.data.at[index, "3rd_FU_Target Lesion 2 LAD Art Enhanc"] = FU3_Target_Lesion_2_LAD_Art_Enhanc
                            st.session_state.data.at[index, "3rd_FU_Target Lesion 2 PAD Art Enhanc"] = FU3_Target_Lesion_2_PAD_Art_Enhanc
                            st.session_state.data.at[index, "3rd_FU_Target Lesion 2 CCD Art Enhanc"] = FU3_Target_Lesion_2_CCD_Art_Enhanc
                            st.session_state.data.at[index, "3rd_FU_Follow up 2 targeted Lesion Dia Sum"] = FU3_Follow_up_2_targeted_Lesion_Dia_Sum
                            st.session_state.data.at[index, "3rd_FU_Non-Target Lesion 1 LAD Art Enhanc"] = FU3_Non_Target_Lesion_1_LAD_Art_Enhanc
                            st.session_state.data.at[index, "3rd_FU_Non-Target Lesion 1 PAD Art Enhanc"] = FU3_Non_Target_Lesion_1_PAD_Art_Enhanc
                            st.session_state.data.at[index, "3rd_FU_Non-Target Lesion 1 CCD Art Enhanc"] = FU3_Non_Target_Lesion_1_CCD_Art_Enhanc
                            st.session_state.data.at[index, "3rd_FU_Non-targeted Lesion Dia Sum"] = FU3_Non_targeted_Lesion_Dia_Sum
                            st.session_state.data.at[index, "3rd_FU_Lesion Necrosis"] = FU3_Lesion_Necrosis
                            st.session_state.data.at[index, "3rd_FU_Reviewers Initials"] = FU3_Reviewers_Initials
                            st.session_state.data.at[index, "3rd_FU_Non target lesion response"] = FU3_Non_target_lesion_response
                            st.session_state.data.at[index, "3rd_FU_New Lesions"] = FU3_New_Lesions
                            st.session_state.data.at[index, "3rd_FU_Extrahepatic Disease"] = FU3_NEW_Extrahepatic_Disease
                            st.session_state.data.at[index, "3rd_FU_NEW Extrahepatic Dz Location"] = FU3_NEW_Extrahepatic_Dz_Location
                            st.session_state.data.at[index, "3rd_FU_NEW Extrahepatic Dz Date"] = FU3_NEW_Extrahepatic_Dz_Date
                            st.session_state.data.at[index, "3rd_FU_% change for non target lesion"] = FU3_change_non_target_lesion
                            st.session_state.data.at[index, "3rd_FU_% Change Target Dia"] = FU3_change_target_lesion
                            st.session_state.data.at[index, "3rd_FU_Free Text"] = FU3_Free_Text
                            st.session_state.data.at[index, "4th_FU_Scan Modality"] = FU4_Scan_Modality
                            st.session_state.data.at[index, "4th_FU_Imaging Date"] = FU4_Imaging_Date
                            st.session_state.data.at[index, "4th_FU_Months Since Y90"] = FU4_Months_Since_Y90
                            st.session_state.data.at[index, "4th_FU_Total number of lesions"] = FU4_Total_number_of_lesions
                            st.session_state.data.at[index, "4th_FU_Target Lesion 1 LAD Art Enhanc"] = FU4_Target_Lesion_1_LAD_Art_Enhanc
                            st.session_state.data.at[index, "4th_FU_Target Lesion 1 PAD Art Enhanc"] = FU4_Target_Lesion_1_PAD_Art_Enhanc
                            st.session_state.data.at[index, "4th_FU_Target Lesion 1 CCD Art Enhanc"] = FU4_Target_Lesion_1_CCD_Art_Enhanc
                            st.session_state.data.at[index, "4th_FU_Target Lesion 2 Segments"] = FU4_Target_Lesion_2_Segments
                            st.session_state.data.at[index, "4th_FU_Target Lesion 2 LAD Art Enhanc"] = FU4_Target_Lesion_2_LAD_Art_Enhanc
                            st.session_state.data.at[index, "4th_FU_Target Lesion 2 PAD Art Enhanc"] = FU4_Target_Lesion_2_PAD_Art_Enhanc
                            st.session_state.data.at[index, "4th_FU_Target Lesion 2 CCD Art Enhanc"] = FU4_Target_Lesion_2_CCD_Art_Enhanc
                            st.session_state.data.at[index, "4th_FU_Follow up 2 targeted Lesion Dia Sum"] = FU4_Follow_up_2_targeted_Lesion_Dia_Sum
                            st.session_state.data.at[index, "4th_FU_Non-Target Lesion 1 LAD Art Enhanc"] = FU4_Non_Target_Lesion_1_LAD_Art_Enhanc
                            st.session_state.data.at[index, "4th_FU_Non-Target Lesion 1 PAD Art Enhanc"] = FU4_Non_Target_Lesion_1_PAD_Art_Enhanc
                            st.session_state.data.at[index, "4th_FU_Non-Target Lesion 1 CCD Art Enhanc"] = FU4_Non_Target_Lesion_1_CCD_Art_Enhanc
                            st.session_state.data.at[index, "4th_FU_Non-targeted Lesion Dia Sum"] = FU4_Non_targeted_Lesion_Dia_Sum
                            st.session_state.data.at[index, "4th_FU_Lesion Necrosis"] = FU4_Lesion_Necrosis
                            st.session_state.data.at[index, "4th_FU_Reviewers Initials"] = FU4_Reviewers_Initials
                            st.session_state.data.at[index, "4th_FU_Non target lesion response"] = FU4_Non_target_lesion_response
                            st.session_state.data.at[index, "4th_FU_New Lesions"] = FU4_New_Lesions
                            st.session_state.data.at[index, "4th_FU_Extrahepatic Disease"] = FU4_NEW_Extrahepatic_Disease
                            st.session_state.data.at[index, "4th_FU_NEW Extrahepatic Dz Location"] = FU4_NEW_Extrahepatic_Dz_Location
                            st.session_state.data.at[index, "4th_FU_NEW Extrahepatic Dz Date"] = FU4_NEW_Extrahepatic_Dz_Date
                            st.session_state.data.at[index, "4th_FU_% change non target lesion"] = FU4_change_non_target_lesion
                            st.session_state.data.at[index, "4th_FU_% Change Target Dia"] = FU4_change_target_lesion
                            st.session_state.data.at[index, "4th_FU_Free Text"] = FU4_Free_Text
                            st.session_state.data.at[index, "5th_FU_Imaging Date"] = FU5_Imaging_Date
                            st.session_state.data.at[index, "5th_FU_Months Since Y90"] = FU5_Months_Since_Y90
                            st.session_state.data.at[index, "5th_FU_Total number of lesions"] = FU5_Total_number_of_lesions
                            st.session_state.data.at[index, "5th_FU_Non-Target Lesion 1 LAD Art Enhanc"] = FU5_Non_Target_Lesion_1_LAD_Art_Enhanc
                            st.session_state.data.at[index, "5th_FU_Non-Target Lesion 1 PAD Art Enhanc"] = FU5_Non_Target_Lesion_1_PAD_Art_Enhanc
                            st.session_state.data.at[index, "5th_FU_Non-Target Lesion 1 CCD Art Enhanc"] = FU5_Non_Target_Lesion_1_CCD_Art_Enhanc
                            st.session_state.data.at[index, "5th_FU_Non-targeted Lesion Dia Sum"] = FU5_Non_targeted_Lesion_Dia_Sum
                            st.session_state.data.at[index, "5th_FU_Non target lesion response"] = FU5_Non_target_lesion_response
                            st.session_state.data.at[index, "5th_FU_New Lesions"] = FU5_New_Lesions
                            st.session_state.data.at[index, "5th_FU_Extrahepatic Disease"] = FU5_NEW_Extrahepatic_Disease
                            st.session_state.data.at[index, "5th_FU_NEW Extrahepatic Dz Location"] = FU5_NEW_Extrahepatic_Dz_Location
                            st.session_state.data.at[index, "5th_FU_NEW Extrahepatic Dz Date"] = FU5_NEW_Extrahepatic_Dz_Date
                            st.session_state.data.at[index, "5th_FU_% change non target lesion"] = FU5_change_non_target_lesion
                            st.session_state.data.at[index, "Dead"] = dead
                            st.session_state.data.at[index, "Date of Death"] = Date_of_Death
                            st.session_state.data.at[index, "Time to Death"] = Time_to_Death
                            st.session_state.data.at[index, "OLT"] = OLT
                            st.session_state.data.at[index, "Date of OLT"] = Date_of_OLT
                            st.session_state.data.at[index, "Time to OLT"] = Time_to_OLT
                            st.session_state.data.at[index, "Repeat tx post Y90"] = Repeat_tx_post_Y90
                            st.session_state.data.at[index, "Date of Repeat tx Post Y90"] = Date_of_Repeat_tx_Post_Y90
                            st.session_state.data.at[index, "Time to Repeat Tx Post Y90"] = Time_to_Repeat_Tx_Post_Y90
                            st.session_state.data.at[index, "Date of Localized Progression"] = Date_of_Localized_Progression
                            
                        
                            st.success("Imagine Data dubmitted")
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
                        input_GTV_Vol = st.number_input("GTV Vol")
                        input_Tx_vol = st.text_input("Tx vol")
                        input_Liver_vol = st.number_input("Liver vol",min_value=1)
                        input_Healthy_Liver_Vol = st.text_input("Healthy Liver Vol")
                        input_GTV_Liver = (input_GTV_Vol)/(input_Liver_vol)*100
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
                            index = st.session_state.data[st.session_state.data["MRN"] == st.session_state.temp_mrn].index[0]

                            # Assign inputs to session state
                            st.session_state.data.at[index, "GTV mean dose"] = input_GTV_mean_dose
                            st.session_state.data.at[index, "Tx vol mean dose"] = input_Tx_vol_mean_dose
                            st.session_state.data.at[index, "Liver Vol Mean dose"] = input_Liver_Vol_Mean_dose
                            st.session_state.data.at[index, "Healthy Liver mean dose"] = input_Healthy_Liver_mean_dose
                            st.session_state.data.at[index, "GTV Vol"] = input_GTV_Vol
                            st.session_state.data.at[index, "Tx vol"] = input_Tx_vol
                            st.session_state.data.at[index, "Liver vol"] = input_Liver_vol
                            st.session_state.data.at[index, "Healthy Liver Vol"] = input_Healthy_Liver_Vol
                            st.session_state.data.at[index, "GTV/Liver"] = input_GTV_Liver
                            st.session_state.data.at[index, "D98"] = input_D98
                            st.session_state.data.at[index, "D95"] = input_D95
                            st.session_state.data.at[index, "D90"] = input_D90
                            st.session_state.data.at[index, "D80"] = input_D80
                            st.session_state.data.at[index, "D70"] = input_D70
                            st.session_state.data.at[index, "V100"] = input_V100
                            st.session_state.data.at[index, "V200"] = input_V200
                            st.session_state.data.at[index, "V300"] = input_V300
                            st.session_state.data.at[index, "V400"] = input_V400
                            st.session_state.data.at[index, "ActivityBq"] = input_ActivityBq
                            st.session_state.data.at[index, "ActivityCi"] = input_ActivityCi
                            st.session_state.data.at[index, "Tx vol Activity Density"] = input_Tx_vol_Activity_Density
                            st.session_state.data.at[index, "NEW"] = input_NEW
                            st.session_state.data.at[index, "GTV < D95 Vol_ml"] = input_GTV_less_D95_Vol_ml
                            st.session_state.data.at[index, "GTV < D95 Mean Dose"] = input_GTV_less_D95_Mean_Dose
                            st.session_state.data.at[index, "GTV < D95 Min Dose"] = input_GTV_less_D95_Min_Dose
                            st.session_state.data.at[index, "GTV < D95 SD"] = input_GTV_less_D95_SD
                            st.session_state.data.at[index, "GTV < D95 Vol_1"] = input_GTV_less_D95_Vol_1
                            st.session_state.data.at[index, "GTV < D95 Mean Dose_1"] = input_GTV_less_D95_Mean_Dose_1
                            st.session_state.data.at[index, "GTV < D95 Min Dose_1"] = input_GTV_less_D95_Min_Dose_1
                            st.session_state.data.at[index, "GTV < D95 SD_1"] = input_GTV_less_D95_SD_1
                            st.session_state.data.at[index, "GTV < D95 Vol_2"] = input_GTV_less_D95_Vol_2
                            st.session_state.data.at[index, "GTV < D95 Mean Dose_2"] = input_GTV_less_D95_Mean_Dose_2
                            st.session_state.data.at[index, "GTV < D95 Min Dose_2"] = input_GTV_less_D95_Min_Dose_2
                            st.session_state.data.at[index, "GTV < D95 SD_2"] = input_GTV_less_D95_SD_2
                            st.session_state.data.at[index, "GTV < 100 Gy Vol"] = input_GTV_less_100_Gy_Vol
                            st.session_state.data.at[index, "GTV < 100 Gy Mean Dose"] = input_GTV_less_100_Gy_Mean_Dose
                            st.session_state.data.at[index, "GTV < 100 Gy Min Dose"] = input_GTV_less_100_Gy_Min_Dose
                            st.session_state.data.at[index, "GTV < 100 Gy SD"] = input_GTV_less_100_Gy_SD


                            st.success("Dosimetry Data added successfully.")
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
                            index = st.session_state.data[st.session_state.data["MRN"] == st.session_state.temp_mrn].index[0]
                            # Assign the input values to st.session_state.data at the specified index
                            st.session_state.data.at[index, "1AFP Date"] = input_1AFP_Date
                            st.session_state.data.at[index, "1AFP"] = input_1AFP
                            st.session_state.data.at[index, "2AFP Date"] = input_2AFP_Date
                            st.session_state.data.at[index, "2AFP"] = input_2AFP
                            st.session_state.data.at[index, "3AFP Date"] = input_3AFP_Date
                            st.session_state.data.at[index, "3AFP"] = input_3AFP
                            st.session_state.data.at[index, "4AFP Date"] = input_4AFP_Date
                            st.session_state.data.at[index, "4AFP"] = input_4AFP
                            st.session_state.data.at[index, "5AFP Date"] = input_5AFP_Date
                            st.session_state.data.at[index, "5AFP"] = input_5AFP
                            st.session_state.data.at[index, "6AFP Date"] = input_6AFP_Date
                            st.session_state.data.at[index, "6AFP"] = input_6AFP
                            st.session_state.data.at[index, "7AFP Date"] = input_7AFP_Date
                            st.session_state.data.at[index, "7AFP"] = input_7AFP
                            st.session_state.data.at[index, "8AFP Date"] = input_8AFP_Date
                            st.session_state.data.at[index, "8AFP"] = input_8AFP
                            st.session_state.data.at[index, "9AFP Date"] = input_9AFP_Date
                            st.session_state.data.at[index, "9AFP"] = input_9AFP
                            st.session_state.data.at[index, "10AFP Date"] = input_10AFP_Date
                            st.session_state.data.at[index, "10AFP"] = input_10AFP
                            st.session_state.data.at[index, "11AFP Date"] = input_11AFP_Date
                            st.session_state.data.at[index, "11AFP"] = input_11AFP
                            st.session_state.data.at[index, "12AFP Date"] = input_12AFP_Date
                            st.session_state.data.at[index, "12AFP"] = input_12AFP
                            st.session_state.data.at[index, "13AFP Date"] = input_13AFP_Date
                            st.session_state.data.at[index, "13AFP"] = input_13AFP
                            st.session_state.data.at[index, "14AFP Date"] = input_14AFP_Date
                            st.session_state.data.at[index, "14AFP"] = input_14AFP
                            st.session_state.data.at[index, "15AFP Date"] = input_15AFP_Date
                            st.session_state.data.at[index, "15AFP"] = input_15AFP
                            st.session_state.data.at[index, "16AFP Date"] = input_16AFP_Date
                            st.session_state.data.at[index, "16AFP"] = input_16AFP
                            st.session_state.data.at[index, "17AFP Date"] = input_17AFP_Date
                            st.session_state.data.at[index, "17AFP"] = input_17AFP
                            st.session_state.data.at[index, "18AFP DATE"] = input_18AFP_DATE
                            st.session_state.data.at[index, "18AFP"] = input_18AFP
                            st.session_state.data.at[index, "19AFP DATE"] = input_19AFP_DATE
                            st.session_state.data.at[index, "19AFP"] = input_19AFP
                            st.session_state.data.at[index, "20AFP DATE"] = input_20AFP_DATE
                            st.session_state.data.at[index, "20AFP"] = input_20AFP
                            st.session_state.data.at[index, "21AFP DATE"] = input_21AFP_DATE
                            st.session_state.data.at[index, "21AFP"] = input_21AFP
                            st.session_state.data.at[index, "22AFP DATE"] = input_22AFP_DATE
                            st.session_state.data.at[index, "22AFP"] = input_22AFP
                            st.session_state.data.at[index, "23AFP DATE"] = input_23AFP_DATE
                            st.session_state.data.at[index, "23AFP"] = input_23AFP
                            st.session_state.data.at[index, "24AFP DATE"] = input_24AFP_DATE
                            st.session_state.data.at[index, "24AFP"] = input_24AFP
                            st.session_state.data.at[index, "25AFP DATE"] = input_25AFP_DATE
                            st.session_state.data.at[index, "25AFP"] = input_25AFP
                            st.session_state.data.at[index, "26AFP DATE"] = input_26AFP_DATE
                            st.session_state.data.at[index, "26AFP"] = input_26AFP
                            st.session_state.data.at[index, "27AFP DATE"] = input_27AFP_DATE
                            st.session_state.data.at[index, "27AFP"] = input_27AFP
                            st.session_state.data.at[index, "28AFP DATE"] = input_28AFP_DATE
                            st.session_state.data.at[index, "28AFP"] = input_28AFP
                            st.session_state.data.at[index, "29AFP DATE"] = input_29AFP_DATE
                            st.session_state.data.at[index, "29AFP"] = input_29AFP
                            st.session_state.data.at[index, "30AFP DATE"] = input_30AFP_DATE
                            st.session_state.data.at[index, "30AFP"] = input_30AFP
                            st.session_state.data.at[index, "31AFP Date"] = input_31AFP_Date
                            st.session_state.data.at[index, "31AFP"] = input_31AFP
                            st.session_state.data.at[index, "32AFP DATE"] = input_32AFP_DATE
                            st.session_state.data.at[index, "32AFP"] = input_32AFP
                            st.session_state.data.at[index, "33AFP DATE"] = input_33AFP_DATE
                            st.session_state.data.at[index, "33AFP"] = input_33AFP
                            st.session_state.data.at[index, "34AFP DATE"] = input_34AFP_DATE
                            st.session_state.data.at[index, "34AFP"] = input_34AFP
                            st.success("Dosimetry Data added successfully.")
                    except:
                        st.warning("Please Fill Patient Information Page")
    
    st.session_state.data["TAREdate"] = st.session_state.data["TAREdate"].astype(str)               
    st.dataframe(st.session_state.data)

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
    if st.session_state.data.empty:
        st.warning("No data available. Please add new data first.")
        return
    else:

        st.write("Current Data:")
        st.dataframe(st.session_state.data, use_container_width=True)

        mrn = st.text_input("Enter MRN to edit and Press Enter")
        #load_button = st.button("Edit Data")
        #if load_button:
        if mrn not in st.session_state.data["MRN"].values:
            st.error(f"No data found for MRN {mrn}.")
        else:
            st.subheader("Cahnge_Data")
            
            st.write(f"Editing data for MRN: {mrn}")

            record = st.session_state.data[st.session_state.data["MRN"] == mrn]
            #st.session_state.data['TAREdate'] = pd.to_datetime(st.session_state.data['TAREdate'],format="%Y-%m-%d")

            # Fetch the relevant date for the current MRN
            fetch_date = st.session_state.data.loc[
                st.session_state.data['MRN'] == st.session_state.temp_mrn, 
                'TAREdate'
            ].values[0]
            fetch_date = str(fetch_date)

            # Convert fetch_date to a datetime.date object
            fetch_date = pd.to_datetime(fetch_date).date()
            index = st.session_state.data[st.session_state.data["MRN"] == mrn].index[0]
            col1, col2 = st.columns([0.3, 0.7],gap="small")
            tabs = ["Patient Information","Patient Demographics", "Cirrhosis PMH","HCC Diagnosis", "Previous Therapy for HCC", "Pre Y90", "Day_Y90", "Post Y90 Within 30 Days Labs", "Other Post Tare","Imaging Date","Dosimetry Data","AFP"]
            #tare_date = record.loc[index, "TARE Tx Date"]
            #tare_date = datetime.strptime(tare_date, "%Y-%m-%d").date()
            with col1:
                st.header("Patient Deatils")
                st.session_state.selected_tab = st.radio("", tabs)

            with col2:
                if st.session_state.selected_tab == "Patient Information":
                    st.subheader("Patient_Info")
                    with st.form("patient_info_form"):
                        # Patient Info Section
                        col1, col2 = st.columns(2)
                        last_name = col1.text_input("Last Name")
                        last_name = last_name.lower()
                        first_name = col2.text_input("First Name")
                        first_name = first_name.lower()
                        
                        st.write(mrn)
                        
                        duplicate_procedure_check = 0
                        if mrn in st.session_state.data["MRN"].values:
                            st.write("Are you sure this is a duplicate")
                            duplicate_procedure_check = 1
                        
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

                        age = st.number_input("Age at time of TARE", min_value=0, max_value=150, step=1, format="%d")
                    
                        submit_tab1 = st.form_submit_button("Submit")
                        if submit_tab1:
                            st.session_state.data.at[index, "Name"] = f"{last_name}, {first_name}"
                            st.session_state.data.at[index, "Duplicate"] = duplicate_procedure_check
                            st.session_state.data.at[index, "TAREdate"] = tare_date
                            st.session_state.data.at[index, "PTech"] = procedure_technique
                            st.session_state.data.at[index, "Tareage"] = age

                elif st.session_state.selected_tab == "Patient Demographics":
                    st.subheader("Patient Demographics")
                    with st.form("demographics_form"):

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
                            st.session_state.data.at[index, "Gender"] = gender
                            st.session_state.data.at[index, "Ethnicity"] = ethnicity
                            st.session_state.data.at[index, "PMHxHTN"] = hypertension
                            st.session_state.data.at[index, "PMHxDM"] = diabetes
                            st.session_state.data.at[index, "Hypercholesterolemia"] = hypercholesterolemia
                            st.session_state.data.at[index, "PMHxSmoking"] = smoking
                            st.session_state.data.at[index, "Obesity"] = obesity
                            st.success("Patient Description added successfully.")
                        
                    
                elif st.session_state.selected_tab == "Cirrhosis PMH":
                    st.subheader("Cirrhosis PMH")
                    with st.form("cirrhosis_pmh_form"):

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
                        
                        Cirrhosis_Dx_Ascites_Classification = "Absent" if Cirrhosis_Dx_Ascites_CTCAE == "none" else findascitesclass(Cirrhosis_Dx_Ascites_CTCAE)
                        
                        Cirrhosis_Dx_Ascites_Free_Text = "NA" if Cirrhosis_Dx_Ascites_CTCAE == "none" else st.text_area(
                            "Cirrhosis_Dx_Ascites Free Text",
                            "Hospitalized (yes/no): \nDiuretics (yes/no): \nParacentesis (yes/no): \nAny other complications (free_text):",
                        
                        )

                        submit_tab3 = st.form_submit_button("Submit")
                        if submit_tab3:

                            #index = st.session_state.data[st.session_state.data["MRN"] == st.session_state.temp_mrn].index[0]
                            st.session_state.data.at[index, "CirPMH_HBV"] = cir_pmh_hbv_status
                            st.session_state.data.at[index, "CirPMH_HBVFT"] = cir_pmh_hbv_free_text
                            st.session_state.data.at[index, "CirPMH_HBVART"] = cir_pmh_hbv_art
                            st.session_state.data.at[index, "CirPMH_HCV"] = cir_pmh_hcv_status
                            st.session_state.data.at[index, "CirPMH_HCVFT"] = cir_pmh_hcv_free_text
                            st.session_state.data.at[index, "CirPMH_HCVART"] = cir_pmh_hcv_art
                            st.session_state.data.at[index, "CirPMH_AUD"] = cir_pmh_alcohol_use_disorder
                            st.session_state.data.at[index, "CirPMH_AUDFT"] = cir_pmh_alcohol_free_text
                            st.session_state.data.at[index, "CirPMH_IVDU"] = cir_pmh_ivdu_status
                            st.session_state.data.at[index, "CirPMH_IVDUFT"] = cir_pmh_ivdu_free_text
                            st.session_state.data.at[index, "CirPMH_Liverfactors"] = cir_pmh_liver_addtional_factor
                            st.session_state.data.at[index, "Cirdx_Dxdate"] = Cirrhosis_Dx_Diagnosis_Date
                            st.session_state.data.at[index, "Cirdx_Dxmethod"] = Cirrhosis_Dx_Diagnosis_Method
                            st.session_state.data.at[index, "Cirdx_HPIFT"] = Cirrhosis_Dx_HPI_EMR_Note_Free_Text
                            st.session_state.data.at[index, "Cirdx_ImageemrFT"] = Cirrhosis_Dx_Imaging_Findings_EMR_Note_Free_Text
                            st.session_state.data.at[index, "Cirdx_Metavir"] = Cirrhosis_Dx_Metavir_Score
                            st.session_state.data.at[index, "Cirdx_Compatdx"] = Cirrhosis_Dx_Complications_at_Time_of_Diagnosis
                            st.session_state.data.at[index, "Cirdx_Compatdxbinary"] = Cirrhosis_Dx_Complications_at_Time_of_Diagnosis_Binary
                            st.session_state.data.at[index, "Cirdx_CompFT"] = Cirrhosis_Dx_Complications_Free_Text
                            st.session_state.data.at[index, "Cirdx_DateLabs"] = Cirrhosis_Dx_Date_of_Labs_in_Window
                            st.session_state.data.at[index, "Cirdx_AFP"] = Cirrhosis_Dx_AFP
                            st.session_state.data.at[index, "Cirdx_AFP L3"] = Cirrhosis_Dx_AFP_L3
                            st.session_state.data.at[index, "Cirdx_AFPL3DateFT"] = Cirrhosis_Dx_AFP_L3_Date_Free_Text
                            st.session_state.data.at[index, "Cirdx_AscitesCTCAE"] = Cirrhosis_Dx_Ascites_CTCAE
                            st.session_state.data.at[index, "Cirdx_AscitesCTCAEnumb"] = Cirrhosis_Dx_Ascites_Classification
                            st.session_state.data.at[index, "Cirdx_AscitesFT"] = Cirrhosis_Dx_Ascites_Free_Text
                            
                            st.success("Patient Description added successfully.")

                elif st.session_state.selected_tab == "HCC Diagnosis":
                    st.subheader("HCC Diagnosis")
                    with st.form("hcc_dx_form"):

                        hcc_dx_hcc_diagnosis_date = st.date_input("HCC_Dx_HCC Diagnosis Date", help="Enter the HCC diagnosis date")

                        hcc_dx_method_of_diagnosis = st.selectbox(
                            "HCC_Dx_Method of Diagnosis",   
                            options=["Biopsy", "Imaging", "Unknown"],
                            index=None,  # No default selection
                            placeholder="Choose an option",
                            #format_func=lambda x: f"{x} ({1 if x == 'Biopsy' else 2 if x == 'Imaging' else 'NA'})"
                        )

                        hcc_dx_date_of_labs = st.date_input("HCC_Dx_Date of Labs in Window")

                        hcc_dx_afp = st.number_input("HCC_Dx_AFP", help="Enter AFP value in ng/dl")
                        hcc_dx_afp_l3 = st.number_input("HCC_Dx_AFP L3", help="Enter AFP L3 and date details")
                        hcc_dx_afp_l3_date_free_text = st.text_area("HCC_Dx_AFP L3 Date Free Text")

                        hcc_dx_bilirubin = st.number_input("HCC_Dx_Bilirubin", help="Enter the bilirubin value in mg/dl", min_value=1)
                        hcc_dx_albumin = st.number_input("HCC_Dx_Albumin", help="Enter the albumin value in g/dl")
                        hcc_dx_inr = st.number_input("HCC_Dx_INR", help="Enter the INR value")
                        hcc_dx_creatinine = st.number_input("HCC_Dx_Creatinine", help="Enter the creatinine value in mg/dl")
                        hcc_dx_sodium = st.number_input("HCC_Dx_Sodium", help="Enter the sodium value in mmol/L")

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
                            options=[1,2,3],
                            format_func=lambda x: {
                            1: "None",
                            2: "Grade 1-2",
                            3: "Grade 3-4",
                            
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

                        hcc_dx_bclc_calc = st.text_area("HCC_Dx_BCLC Stage calc")
                    

                        submit_tab4 = st.form_submit_button("Submit")
                        if submit_tab4:
                                #index = st.session_state.data[st.session_state.data["MRN"] == st.session_state.temp_mrn].index[0]
                                st.session_state.data.at[index, "HCCdx_HCCdxdate"] = hcc_dx_hcc_diagnosis_date.strftime("%Y-%m-%d")
                                st.session_state.data.at[index, "HCCdx_Methoddx"] = hcc_dx_method_of_diagnosis
                                st.session_state.data.at[index, "HCCdx_Datelabs"] = hcc_dx_date_of_labs.strftime("%Y-%m-%d")
                                st.session_state.data.at[index, "HCCdx_AFP"] = hcc_dx_afp
                                st.session_state.data.at[index, "HCCdx_AFP L3"] = hcc_dx_afp_l3
                                st.session_state.data.at[index, "HCCdx_AFPL3dateFT"] = hcc_dx_afp_l3_date_free_text
                                st.session_state.data.at[index, "HCCdx_Bilirubin"] = hcc_dx_bilirubin
                                st.session_state.data.at[index, "HCCdx_Albumin"] = hcc_dx_albumin
                                st.session_state.data.at[index, "HCCdx_INR"] = hcc_dx_inr
                                st.session_state.data.at[index, "HCCdx_Creatinine"] = hcc_dx_creatinine
                                st.session_state.data.at[index, "HCCdx_Sodium"] = hcc_dx_sodium
                                st.session_state.data.at[index, "HCCdx_AscitesCTCAE"] = hcc_dx_ascites_CTCAE
                                st.session_state.data.at[index, "HCCdx_AscitesCTCAEnumb"] = hCC_dx_ascites_classification
                                st.session_state.data.at[index, "HCCdx_Ascitesdiruetics"] = hcc_dx_ascites_diruetics
                                st.session_state.data.at[index, "HCCdx_Ascitesparacentesis"] = hcc_dx_ascites_paracentesis
                                st.session_state.data.at[index, "HCCdx_Asciteshospitalization"] = hcc_dx_ascites_hospitalization
                                st.session_state.data.at[index, "HCCdx_HEgrade"] = hcc_dx_he_grade
                                st.session_state.data.at[index, "HCCdx_ECOG"] = hcc_dx_ecog_performance_status
                                st.session_state.data.at[index, "HCCdx_LIRADS"] = hcc_dx_lirads_score
                                st.session_state.data.at[index, "HCCdx_CPcalc"] = hcc_dx_child_pugh_points_calc
                                st.session_state.data.at[index, "HCCdx_CPclass"] = hcc_dx_child_pugh_class_calc
                                st.session_state.data.at[index, "HCCdx_MELD"] = hcc_dx_meld_score_calc
                                st.session_state.data.at[index, "HCCdx_MELDNa"] = hcc_dx_meld_na_score_calc
                                st.session_state.data.at[index, "HCCdx_Albiscore"] = hcc_dx_albi_score_calc
                                st.session_state.data.at[index, "HCCdx_Albigrade"] = hcc_dx_albi_grade
                                st.session_state.data.at[index, "HCCdx_BCLC"] = hcc_dx_bclc_calc
                                st.success("HCC Dx added successfully.")
        
                elif st.session_state.selected_tab == "Previous Therapy for HCC":
                    st.subheader("Previous Therapy for HCC")
                    with st.form("previous_therapy_form"):

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
                            help="Enter AFP value in ng/dl or NA"
                        )

                        submit_tab5 = st.form_submit_button("Submit")

                        if submit_tab5:
                                #index = st.session_state.data[st.session_state.data["MRN"] == st.session_state.temp_mrn].index[0]

                                st.session_state.data.at[index, "PRVTHER_LDT"] = PRVTHER_Prior_LDT_Therapy
                                st.session_state.data.at[index, "PRVTHER_RFA"] = PRVTHER_Prior_RFA_Therapy
                                st.session_state.data.at[index, "PRVTHER_RFAdate"] = PRVTHER_Prior_RFA_Date
                                st.session_state.data.at[index, "PRVTHER_TARE"] = PRVTHER_Prior_TARE_Therapy
                                st.session_state.data.at[index, "PRVTHER_TAREdate"] = PRVTHER_Prior_TARE_Date
                                st.session_state.data.at[index, "PRVTHER_SBRT"] = PRVTHER_Prior_SBRT_Therapy
                                st.session_state.data.at[index, "PRVTHER_SBRTdate"] = PRVTHER_Prior_SBRT_Date
                                st.session_state.data.at[index, "PRVTHER_TACE"] = PRVTHER_Prior_TACE_Therapy
                                st.session_state.data.at[index, "PRVTHER_TACEdate"] = PRVTHER_Prior_TACE_Date
                                st.session_state.data.at[index, "PRVTHER_MWA"] = PRVTHER_Prior_MWA_Therapy
                                st.session_state.data.at[index, "PRVTHER_MWAdate"] = PRVTHER_Prior_MWA_Date
                                st.session_state.data.at[index, "PRVTHER_Resection"] = PRVTHER_Resection
                                st.session_state.data.at[index, "PRVTHER_Resection date"] = PRVTHER_Resection_Date
                                st.session_state.data.at[index, "PRVTHER_Prevtxsum"] = PRVTHER_Previous_Therapy_Sum
                                st.session_state.data.at[index, "PRVTHER_NotesFT"] = PRVTHER_NotesFT
                                st.session_state.data.at[index, "PRVTHER_Totalrecur"] = PRVTHER_Total_Recurrences_HCC
                                st.session_state.data.at[index, "PRVTHER_Locationprevtxseg"] = PRVTHER_Location_of_Previous_Treatment_segments
                                st.session_state.data.at[index, "PRVTHER_Location of Previous Tx Segments FT"] = PRVTHER_Location_of_Previous_Tx_segments_ft
                                st.session_state.data.at[index, "PRVTHER_RecurLocationFT"] = PRVTHER_recurrence_location_note
                                st.session_state.data.at[index, "PRVTHER_RecurDate"] = PRVTHER_recurrence_date
                                st.session_state.data.at[index, "PRVTHER_Recurrence Seg"] = PRVTHER_recurrence_seg
                                st.session_state.data.at[index, "PRVTHER_NewHCCoutsideprevsite"] = PRVTHER_New_HCC_Outside_Previous_Treatment_Site
                                st.session_state.data.at[index, "PRVTHER_NewHCCadjacentprevsite"] = PRVTHER_New_HCC_Adjacent_to_Previous_Treatment_Site
                                st.session_state.data.at[index, "PRVTHER_ResidualHCCnoteFT"] = PRVTHER_Residual_HCC_Note
                                st.session_state.data.at[index, "PRVTHER_ResidualHCC"] = PRVTHER_Residual_HCC
                                st.session_state.data.at[index, "PRVTHER_SystemictherapyFT"] = PRVTHER_Systemic_Therapy_Free_Text
                                st.session_state.data.at[index, "PRVTHER_DateAFP"] = PRVTHER_Date_of_Labs_in_Window
                                st.session_state.data.at[index, "PRVTHER_AFP"] = PRVTHER_AFP
                                st.success("Previous Therapy for HCC added successfully.")
            
                elif st.session_state.selected_tab == "Pre Y90":
                    st.subheader("Pre Y90")
                    with st.form("pre_y90_form"):

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
                            placeholder="Select all that apply"
                        )
                        
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
                        
                        
                        prey90_bilirubin = st.number_input("PREY90_Bilirubin", help="Enter the bilirubin value in mg/dl",min_value=1)
                        prey90_albumin = st.number_input("PREY90_Albumin", help="Enter the albumin value in g/dl")
                        prey90_inr = st.number_input("PREY90_inr", help="Enter the INR value")
                        prey90_creatinine = st.number_input("PREY90_creatinine", help="Enter the creatinine value in mg/dl")
                        prey90_sodium = st.number_input("PREY90_sodium", help="Enter the sodium value in mmol/L")
                        prey90_ast = st.number_input("PREY90_AST", help="Enter AST value in U/L")
                        prey90_alt = st.number_input("PREY90_ALT", help="Enter ALT value in U/L")
                        prey90_alkaline_phosphatase = st.number_input("PREY90_Alkaline Phosphatase", help="Enter Alkaline Phosphatase value in U/L")
                        prey90_potassium = st.number_input("PREY90_potassium", help="Enter the potassium value in mmol/L")
                        
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
                
                        prey90_child_pugh_class_calc = calculate_class(prey90_child_pugh_points_calc)
                        # Additional Calculated Fields
                        
                        #prey90_bclc_stage_calc = st.text_input("PREY90_BCLC Stage calc", help="Enter calculated BCLC stage")
                        prey90_meld_score_calc = (3.78*(int(prey90_bilirubin)))+(11.2*(int(prey90_inr)))+(9.57*(int(prey90_creatinine)))+6.43
                        prey90_meld_na_score_calc = prey90_meld_score_calc + 1.32*(137-int(prey90_sodium)) - (0.033*prey90_meld_score_calc*(137-int(prey90_sodium)))
                        
                        prey90_albi_score_calc = albi_calc(prey90_bilirubin,prey90_albumin)
                        prey90_albi_grade = albi_class(prey90_albi_score_calc)

                        prey90_bclc_calc = st.text_area("PREY90_BCLC Stage calc")

                    
                        st.subheader("Mapping Y90")
                        my90_date = st.date_input("MY90_date", help="Enter the date")
                        my90_lung_shunt = st.number_input("MY90_Lung_shunt", min_value=0, step=1, help="Enter the lung shunt value")

                        submit_tab4 = st.form_submit_button("Submit")

                        if submit_tab4:
                            #index = st.session_state.data[st.session_state.data["MRN"] == st.session_state.temp_mrn].index[0]

                            st.session_state.data.at[index, "PREY90_sx"] = prey90_symptoms
                            st.session_state.data.at[index, "PREY90_Datelabs"] = prey90_date_of_labs.strftime("%Y-%m-%d")
                            st.session_state.data.at[index, "PREY90_AFP"] = prey90_afp
                            st.session_state.data.at[index, "PRE90_AFPbinary"] = prey90_afp_prior_to_tare
                            st.session_state.data.at[index, "PREY90_Bilirubin"] = prey90_bilirubin
                            st.session_state.data.at[index, "PREY90_Albumin"] = prey90_albumin
                            st.session_state.data.at[index, "PREY90_Inr"] = prey90_inr
                            st.session_state.data.at[index, "PREY90_Ireatinine"] = prey90_creatinine
                            st.session_state.data.at[index, "PREY90_Sodium"] = prey90_sodium
                            st.session_state.data.at[index, "PREY90_AST"] = prey90_ast
                            st.session_state.data.at[index, "PREY90_ALT"] = prey90_alt
                            st.session_state.data.at[index, "PREY90_Alkaline Phosphatase"] = prey90_alkaline_phosphatase
                            st.session_state.data.at[index, "PREY90_Potassium"] = prey90_potassium
                            st.session_state.data.at[index, "PREY90_AscitesCTCAE"] = prey90_ascites_ctcae
                            st.session_state.data.at[index, "PREY90_AscitesCTCAEnumb"] = prey90_ascites_classification
                            st.session_state.data.at[index, "PREY90_AscitesFT"] = prey90_ascites_free_text
                            st.session_state.data.at[index, "PREY90_Ascitesdiruetics"] = prey90_ascites_diruetics
                            st.session_state.data.at[index, "PREY90_Ascitesparacentesis"] = prey90_ascites_paracentesis
                            st.session_state.data.at[index, "PREY90_Asciteshospitalization"] = prey90_ascites_hospitalization
                            st.session_state.data.at[index, "PREY90_HEgrade"] = prey90_he_grade
                            st.session_state.data.at[index, "PREY90_ECOG"] = prey90_ecog
                            st.session_state.data.at[index, "PREY90_CPclass"]= prey90_child_pugh_class_calc
                            st.session_state.data.at[index, "PREY90_CPcalc"] = prey90_child_pugh_points_calc
                            st.session_state.data.at[index, "PREY90_MELD"] = prey90_meld_score_calc
                            st.session_state.data.at[index, "PREY90_MELDNa"] = prey90_meld_na_score_calc
                            st.session_state.data.at[index, "PREY90_Albiscore"] = prey90_albi_score_calc
                            st.session_state.data.at[index, "PREY90_Albigrade"] = prey90_albi_grade
                            st.session_state.data.at[index, "PREY90_BCLC"] = prey90_bclc_calc
                            st.session_state.data.at[index, "MY90_date"] = my90_date
                            st.session_state.data.at[index, "MY90_Lung_shunt"] = my90_lung_shunt

                            st.success("Pre Y90 added successfully.")
            
                elif st.session_state.selected_tab == "Day_Y90":
                    st.subheader("Day_Y90")
                    with st.form("day_y90_form"):

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

                        prey90_afp_binarydup = st.session_state.data.at[index, "PRE90_AFPbinary"]
                    
                    # Inputs for other variables
                        dayy90_sodium = st.number_input("DAYY90_sodium")
                        dayy90_creatinine = st.number_input("DAYY90_creatinine")
                        dayy90_inr = st.number_input("DAYY90_inr")
                        dayy90_albumin = st.number_input("DAYY90_albumin")
                        dayy90_bilirubin = st.number_input("DAYY90_bilirubin",min_value=1)
                        dayy90_ast = st.number_input("DAYY90_AST")
                        dayy90_alt = st.number_input("DAYY90_ALT")
                        dayy90_alkaline_phosphatase = st.number_input(
                            "DAYY90_Alkaline Phosphatase"
                        )
                        dayy90_leukocytes = st.number_input("DAYY90_leukocytes")
                        dayy90_platelets = st.number_input("DAYY90_platelets")
                        dayy90_potassium = st.number_input("DAY90_Potassium")

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

                        
                        # Claculation of class and points
                        dayy90_child_pugh_points_calc = calculatepoints(dayy90_bilirubin,dayy90_albumin,dayy90_inr,dayy90_ascites_ctcae,dayy90_he_grade)
                
                        dayy90_child_pugh_class_calc = calculate_class(dayy90_child_pugh_points_calc)
                        # Additional Calculated Fields
                        
                        #prey90_bclc_stage_calc = st.text_input("PREY90_BCLC Stage calc", help="Enter calculated BCLC stage")
                        dayy90_meld_score_calc = (3.78*(int(dayy90_bilirubin)))+(11.2*(int(dayy90_inr)))+(9.57*(int(dayy90_creatinine)))+6.43
                        dayy90_meld_na_score_calc = dayy90_meld_score_calc + 1.32*(137-int(dayy90_sodium)) - (0.033*dayy90_meld_score_calc*(137-int(dayy90_sodium)))
                        
                        dayy90_albi_score_calc = albi_calc(dayy90_bilirubin,dayy90_albumin)
                        dayy90_albi_grade = albi_class(dayy90_albi_score_calc)

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
                        ken_meldpretare = st.number_input("ken_MELDpreTARE")


                    # Submit button
                        submit_tab7 = st.form_submit_button("Submit")
                    
                        if submit_tab7:
                            #index = st.session_state.data[st.session_state.data["MRN"] == st.session_state.temp_mrn].index[0]

                            st.session_state.data.at[index, "DAYY90_AFP"] = dayy90_afp
                            st.session_state.data.at[index, "DAYY90_AFP Binary"] = dayy90_afp_prior_to_tare
                            st.session_state.data.at[index, "PRE90_AFP BinaryDup"] = prey90_afp_binarydup
                            st.session_state.data.at[index, "DAYY90_Sodium"] = dayy90_sodium
                            st.session_state.data.at[index, "DAYY90_Creatinine"] = dayy90_creatinine
                            st.session_state.data.at[index, "DAYY90_Inr"] = dayy90_inr
                            st.session_state.data.at[index, "DAYY90_Albumin"] = dayy90_albumin
                            st.session_state.data.at[index, "DAYY90_Bilirubin"] = dayy90_bilirubin
                            st.session_state.data.at[index, "DAYY90_AST"] = dayy90_ast
                            st.session_state.data.at[index, "DAYY90_ALT"] = dayy90_alt
                            st.session_state.data.at[index, "DAYY90_Alkphos"] = dayy90_alkaline_phosphatase
                            st.session_state.data.at[index, "DAYY90_Leukocytes"] = dayy90_leukocytes
                            st.session_state.data.at[index, "DAYY90_Platelets"] = dayy90_platelets
                            st.session_state.data.at[index, "DAY90_Potassium"] = dayy90_potassium
                            st.session_state.data.at[index, "Day90_AscitesCTCAE"] = dayy90_ascites_ctcae
                            st.session_state.data.at[index, "Day90_AscitesCTCAEnumb"] = dayy90_ascites_classification
                            st.session_state.data.at[index, "Day90_HEgrade"] = dayy90_he_grade
                            st.session_state.data.at[index, "PREY90_ECOG"] = dayy90_ecog
                            st.session_state.data.at[index, "DAYY90_CPclass"] = dayy90_child_pugh_class_calc
                            st.session_state.data.at[index, "DAYY90_CPcalc"] = dayy90_child_pugh_points_calc
                            st.session_state.data.at[index, "DAYY90_MELD"] = dayy90_meld_score_calc
                            st.session_state.data.at[index, "DAYY90_MELD Na calc"] = dayy90_meld_na_score_calc
                            st.session_state.data.at[index, "DAYY90_Albiscore"] = dayy90_albi_score_calc
                            st.session_state.data.at[index, "DAYY90_Albigrade"] = dayy90_albi_grade
                            st.session_state.data.at[index, "DAYY90_BCLC"] = dayy90_bclc_calc
                            st.session_state.data.at[index, "DAYY90_Sphere"] = dayy90_type_of_sphere
                            st.session_state.data.at[index, "DAYY90_LTnoteFT"] = dayy90_lt_notes_ftx
                            st.session_state.data.at[index, "ken_ChildPughscore"] = ken_childpughscore
                            st.session_state.data.at[index, "ken_MELDpreTARE (MELDpreTARE)"] = ken_meldpretare
                            
                            st.success("DAYY90 added successfully.")
            
                elif st.session_state.selected_tab == "Post Y90 Within 30 Days Labs":
                    st.subheader("Post Y90 Within 30 Days Labs")
                    with st.form("post_y90_form"):

                        posty90_date_labs = st.date_input("POSTY90_30DY_date_labs", help="Enter the date of lab tests")
                        input90 = st.text_input("POSTY90_30DY_afp", help="Enter AFP value in ng/dl or NA")
                        posty90_afp = process_input(input90)
                        posty90_afp_date = st.date_input("POSTY90_30DY_afp DATE", help="Enter the date for AFP")
                        posty90_sodium = st.number_input("POSTY90_30DY_Sodium", help="Enter the sodium value in mmol/L")
                        posty90_creatinine = st.number_input("POSTY90_30DY_creatinine", help="Enter the creatinine value in mg/dl")
                        posty90_inr = st.number_input("POSTY90_30DY_INR", help="Enter the INR value")
                        posty90_albumin = st.number_input("POSTY90_30DY_albumin", help="Enter the albumin value in g/dl")
                        posty90_bilirubin = st.number_input("POSTY90_30DY_bilirubin", help="Enter the bilirubin value in mg/dl",min_value=1)
                        posty90_ast = st.number_input("POSTY90_30DY_AST", help="Enter AST value in U/L")
                        posty90_alt = st.number_input("POSTY90_30DY_ALT", help="Enter ALT value in U/L")
                        posty90_alkaline_phosphatase = st.number_input("POSTY90_30DY_Alkaline Phosphatase", help="Enter Alkaline Phosphatase value in U/L")
                        posty90_leukocytes = st.number_input("POSTY90_30DY_leukocytes", help="Enter leukocytes value in x10^3/µL")
                        posty90_platelets = st.number_input("POSTY90_30DY_platelets", help="Enter platelets value in x10^3/µL")
                        posty90_potassium = st.number_input("POSTY90_30DY_potassium", help="Enter the potassium value in mmol/L")
                        
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
                            help="Enter ALBI score"
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
                                
                                #index = st.session_state.data[st.session_state.data["MRN"] == st.session_state.temp_mrn].index[0]
                            
                                st.session_state.data.at[index, "POSTY90_30DY_Datelabs"] = posty90_date_labs.strftime("%Y-%m-%d")
                                st.session_state.data.at[index, "POSTY90_30DY_AFP"] = posty90_afp
                                st.session_state.data.at[index, "POSTY90_30DY_AFPdate DATE"] = posty90_afp_date.strftime("%Y-%m-%d")
                                st.session_state.data.at[index, "POSTY90_30DY_Sodium"] = posty90_sodium
                                st.session_state.data.at[index, "POSTY90_30DY_Creatinine"] = posty90_creatinine
                                st.session_state.data.at[index, "POSTY90_30DY_INR"] = posty90_inr
                                st.session_state.data.at[index, "POSTY90_30DY_Albumin"] = posty90_albumin
                                st.session_state.data.at[index, "POSTY90_30DY_Bilirubin"] = posty90_bilirubin
                                st.session_state.data.at[index, "POSTY90_30DY_AST"] = posty90_ast
                                st.session_state.data.at[index, "POSTY90_30DY_ALT"] = posty90_alt
                                st.session_state.data.at[index, "POSTY90_30DY_ALP"] = posty90_alkaline_phosphatase
                                st.session_state.data.at[index, "POSTY90_30DY_Leukocytes"] = posty90_leukocytes
                                st.session_state.data.at[index, "POSTY90_30DY_Platelets"] = posty90_platelets
                                st.session_state.data.at[index, "POSTY90_30DY_Potassium"] = posty90_potassium
                                st.session_state.data.at[index, "30DY_AE_AscitesCTCAE"] = posty90_ascites_ctcae
                                st.session_state.data.at[index, "30DY_AE_AscitesCTCAEnumb"] = posty90_ascites_classification
                                st.session_state.data.at[index, "30DY_AE_Ascitesdiruetics"] = posty90_ascites_diruetics
                                st.session_state.data.at[index, "30DY_AE_Ascitesparacentesis"] = posty90_ascites_paracentesis
                                st.session_state.data.at[index, "30DY_AE_Asciteshospitalization"] = posty90_ascites_hospitalization
                                st.session_state.data.at[index, "30DY_AE_HEgrade"] = posty90_he_grade
                                st.session_state.data.at[index, "30DY_AE_ascities_freetext"] = posty90_ascites_free_text
                                st.session_state.data.at[index, "POSTY90_30DY_ECOG"] = posty90_ecog
                                st.session_state.data.at[index, "POSTY90_30DY_CPclass"] = posty90_child_pugh_class
                                st.session_state.data.at[index, "POSTY90_30DY_CPcalc"] = posty90_child_pugh_points
                                st.session_state.data.at[index, "POSTY90_30DY_MELD"] = posty90_meld
                                st.session_state.data.at[index, "POSTY90_30DY_MELDNa"] = posty90_meld_na
                                st.session_state.data.at[index, "POSTY90_30DY_ALBIscore"] = posty90_albi_score
                                st.session_state.data.at[index, "POSTY90_30DY_ALBIgrade"] = posty90_albi_grade
                                st.session_state.data.at[index, "POSTY90_30DY_BCLC"] = posty90_bclc
                                st.session_state.data.at[index, "Ken_BCLCStagepost90"] = ken_bclc_stage_post90
                                st.session_state.data.at[index, "Ken_MELD_Stagepost90"] = ken_meld_stage_post90

                                st.session_state.data.at[index, "30DY_AE_Portalhtn"] = DYAE_CTCAE_portal_htn
                                st.session_state.data.at[index, "30DY_AE_Vascularcomp"] = DYAE_CTCAE_Vascular_comp
                                st.session_state.data.at[index, "30DY_AE_Fatigue"] = DYAE_CTCAE_fatigue
                                st.session_state.data.at[index, "30DY_AE_Diarrhea"] = DYAE_CTCAE_diarrhea
                                st.session_state.data.at[index, "30DY_AE_Hypoalbuminemia"] = DYAE_CTCAE_hypoalbuminemia_emr
                                st.session_state.data.at[index, "30DY_AE_Hyperbilirubinemia"] = DYAE_CTCAE_hyperbilirubinemia_emr
                                st.session_state.data.at[index, "30DY_AE_Increasecreatine"] = DYAE_CTCAE_Increase_creatinine_emr
                                st.session_state.data.at[index, "30DY_AE_Abdominalpain"] = DYAE_CTCAE_abdominal_pain
                                st.session_state.data.at[index, "30DY_AE_Sepsis"] = DYAE_CTCAE_sepsis
                                st.session_state.data.at[index, "30DY_AE_BacterialPer"] = DYAE_CTCAE_bacterial_peritonitis
                                st.session_state.data.at[index, "30DY_AE_Hemorrhage"] = DYAE_CTCAE_hemorrhage
                                st.session_state.data.at[index, "30DY_AE_Anorexia"] = DYAE_CTCAE_anorexia
                                st.session_state.data.at[index, "30DY_AE_Intrahepaticfistula"] = DYAE_CTCAE_intrahepatic_fistula
                                st.session_state.data.at[index, "30DY_AE_Constipation"] = DYAE_CTCAE_constipation
                                st.session_state.data.at[index, "30DY_AE_Nausea"] = DYAE_CTCAE_nausea
                                st.session_state.data.at[index, "30DY_AE_Vomiting"] = DYAE_CTCAE_vomiting
                                st.session_state.data.at[index, "30DY_AE_Cholecystitis"] = DYAE_CTCAE_cholecystitis
                                st.session_state.data.at[index, "30DY_AE_Gastriculcer"] = DYAE_CTCAE_gastric_ulcers
                                st.session_state.data.at[index, "30DY_AE_Hyperkalemia"] = DYAE_CTCAE_hyperkalemia
                                st.session_state.data.at[index, "30DY_AE_Respfailure"] = DYAE_CTCAE_respiratory_failure
                                st.session_state.data.at[index, "30DY_AE_AKI"] = DYAE_CTCAE_AKI
                                st.session_state.data.at[index, "30DY_AE_Radiationpneumonitis"] = DYAE_CTCAE_Radiation_pneumonitis
                                st.session_state.data.at[index, "30DY_AE_Other"] = DYAE_AE_other
                                st.session_state.data.at[index, "90DY_AE_date_of_AE"] = DYAE_AE_date_of_AE
                                st.session_state.data.at[index, "Additional Notes FT"] = ken_grandedtoxicity
                                st.session_state.data.at[index, "90DY_AE_Hosp3mo"] = dy_ae_hospitalization_3
                                st.session_state.data.at[index, "90DY_AE_Datehosp3mo"] = dy_ae_hospitalization_6
                                st.session_state.data.at[index, "90DY_AE_Hosp6mo"] = dy_ae_hosp6mo
                                st.session_state.data.at[index, "90DY_AE_DeathduetoAE"] = dy_ae_death_due

                                st.success("DAYY90 added successfully.")                             
                              

                                             
                elif st.session_state.selected_tab == "Other Post Tare":
                    st.subheader("Other_post_TARE")
                    with st.form("other_post_tare_form"):
                        
                            oc_liver_transplant = st.radio("OC_Liver_transplant", options=["yes", "no"])
                            oc_liver_transplant_date = st.date_input("OC_Liver_transplant_date")

                            st.subheader("K_other")
                # with st.form("k_other_form"):

                            k_ken_toxgtg3 = st.number_input("K_ken_ToxgtG3")
                            if k_ken_toxgtg3 > 3:
                                k_ken_toxgtg3 = 1
                            else:
                                k_ken_toxgtg3 =0
                                            
                            k_ken_toxgtg2 = st.number_input("K_ken_ToxgtG2")
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

                            #prey90_bilirubin_verify = st.session_state.data["PREY90_Bilirubin"].isnull()
                            #prey90_albumin_verify = st.session_state.data["PREY90_Albumin"].isnull()
                            #if prey90_bilirubin_verify.bool() == True or prey90_albumin_verify.bool() == True :
                             #   st.write("Fill value PREY90_Bilirubin and PREY90_Albumin")
                            #else:
                            #prey90_bilirubin = st.session_state.data["PREY90_Bilirubin"]
                             #   prey90_albumin = st.session_state.data["PREY90_Albumin"]
                              #  k_ken_albipretareraw = albi_calc(prey90_bilirubin,prey90_albumin)
                               # k_ken_albipretaregrade = albigrade(k_ken_albipretareraw)
                       
                            #posty90_albumin_verify = st.session_state.data["POSTY90_30DY_albumin"].isnull()
                            #posty90_bilirubin_verify = st.session_state.data["POSTY90_30DY_bilirubin"].isnull()
                            #if posty90_albumin_verify.bool() == True or posty90_bilirubin_verify.bool() == True :
                             #   st.write("Fill value POSTY90_30DY_albumin and POSTY90_30DY_bilirubin")
                            #else:
                             #   posty90_albumin = float(st.session_state.data["POSTY90_30DY_albumin"])
                              #  posty90_bilirubin = float(st.session_state.data["POSTY90_30DY_bilirubin"])
                               # k_ken_albiposttareraw = albi_calc(posty90_bilirubin,posty90_albumin)
                                #k_ken_albiposttaregrade = albigrade(k_ken_albiposttareraw)'''

                            submit_tab9 = st.form_submit_button("Submit")

                            if submit_tab9:
                                #index = st.session_state.data[st.session_state.data["MRN"] == st.session_state.temp_mrn].index[0]

                                st.session_state.data.at[index, "OC_Liver_transplant"] = oc_liver_transplant
                                st.session_state.data.at[index, "OC_Liver_transplant_date"] = oc_liver_transplant_date
                                st.session_state.data.at[index, "K_ken_ToxgtG3"] = k_ken_toxgtg3
                                st.session_state.data.at[index, "K_ken_ToxgtG2"] = k_ken_toxgtg2
                                #st.session_state.data.at[index, "K_ken_AlbiPreTARERaw"] = k_ken_albipretareraw
                                #st.session_state.data.at[index, "K_ken_AlbiPreTAREGrade"] = k_ken_albipretaregrade
                                #st.session_state.data.at[index, "K_ken_AlbiPostTARERaw"] = k_ken_albiposttareraw
                                #st.session_state.data.at[index, "K_ken_AliPostTAREGrade"] = k_ken_albiposttaregrade'''

                                st.success("Other Post Tare added successfully.")
                                st.write("Updated Data:")
                                                   
                elif st.session_state.selected_tab == "Imaging Date":
                    st.subheader("Imaging Date")
                    with st.form("imaging_date_form"):
             
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
                            PREY90_TL1_LAD = st.number_input(
                                "PREY90_TL1_LAD",
                                format="%.2f"
                            )

                            PREY90_Target_Lesion_1_PAD = st.number_input(
                                "PREY90_Target Lesion 1 PAD",
                                format="%.2f"
                            )

                            PREY90_Target_Lesion_1_CCD = st.number_input(
                                "PREY90_Target Lesion 1 CCD",
                                format="%.2f"
                            )
                            PREY90_Target_Lesion_1_VOL = 4/3*3.14*(PREY90_Target_Lesion_1_PAD)*(PREY90_TL1_LAD)*PREY90_Target_Lesion_1_CCD
                            PREY90_Target_Lesion_2_segments = st.selectbox(
                                    "PREY90_Target_Lesion_2_segments",
                                    options=["1","2","3","4a","4b","5","6","7","8","NA"],
                    index=None,  # No default selection
                    placeholder="Choose an option",
                            )
                            PREY90_Target_Lesion_2_LAD = st.number_input(
                                "PREY90_Target_Lesion_2_LAD",
                                format="%.2f"
                            )
                            PREY90_Target_Lesion_2_PAD = st.number_input(
                                "PREY90_Target Lesion 2 PAD",
                                format="%.2f"
                            )

                            PREY90_Target_Lesion_2_CCD = st.number_input(
                                "PREY90_Target Lesion 2 CCD",
                                format="%.2f"
                            )
                            PREY90_Target_Lesion_2_VOL = 4/3*3.14*(PREY90_Target_Lesion_2_PAD)*(PREY90_Target_Lesion_2_LAD)*PREY90_Target_Lesion_2_CCD

                            PREY90_pretx_targeted_Lesion_Dia_Sum = max(PREY90_TL1_LAD,PREY90_Target_Lesion_1_PAD,PREY90_Target_Lesion_1_CCD)+max(PREY90_Target_Lesion_2_PAD,PREY90_Target_Lesion_2_LAD,PREY90_Target_Lesion_2_CCD)

                            PREY90_Non_Target_Lesion_Location = st.selectbox( "PREY90_Non-Target Lesion Location" , options=["1","2","3","4a","4b","5","6","7","8","NA"],
                    index=None,  # No default selection
                    placeholder="Choose an option",)

                            PREY90_Non_Target_Lesion_2_LAD_Art_Enhanc = st.number_input(
                                "PREY90_Non_Target_Lesion_2_LAD_Art_Enhanc",
                                format="%.2f"
                            )
                            PREY90_Non_Target_Lesion_2_PAD_Art_Enhanc = st.number_input(
                                "PREY90_Non_Target_Lesion_2_PAD_Art_Enhanc",
                                format="%.2f"
                            )

                            PREY90_Non_Target_Lesion_2_CCD_Art_Enhanc = st.number_input(
                                "PREY90_Non_Target_Lesion_2_CCD_Art_Enhanc",
                                format="%.2f"
                            )
                            PREY90_Non_targeted_Lesion_Dia_Sum = max(PREY90_Non_Target_Lesion_2_PAD_Art_Enhanc,PREY90_Non_Target_Lesion_2_LAD_Art_Enhanc,PREY90_Non_Target_Lesion_2_CCD_Art_Enhanc)

                            PREY90_Reviewers_Initials = st.text_input(
                                "PREY90_Reviewers Initials",
                                help="Free-text input for reviewer name"
                            )

                            PREY90_Pre_Y90_Extrahepatic_Disease = st.selectbox(
                                "PREY90_Pre Y90 Extrahepatic Disease",
                                options=["Yes", "No", "N/A"],
                    index=None,  # No default selection
                    placeholder="Choose an option",
                            )

                            PREY90_Pre_Y90_Extrahepatic_Disease_Location = st.text_input(
                                "PREY90_Pre Y90 Extrahepatic Disease Location",
                                help="Free Text"
                            )

                            PREY90_PVT = st.selectbox(
                                "PREY90_PVT",
                                options=["Yes", "No", "N/A"],
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
                                options=["Yes", "No", "N/A"],
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

                            # Assuming "Months Since Y90" is calculated elsewhere in the code
                            # FU_Months_Since_Y90 = calculated_value
                            
                            FU_Months_Since_Y90 = relativedelta(FU_Imaging_Date, fetch_date).months

                            FU_Total_number_of_lesions = st.selectbox(
                                "1st_FU_Total number of lesions",
                                options=["1", "2", ">3"],
                    index=None,  # No default selection
                    placeholder="Choose an option",
                            )

                            FU_Target_Lesion_1_LAD_Art_Enhanc = st.number_input(
                                "1st_FU_Target Lesion 1 LAD Art Enhanc",
                                format="%.2f"
                            )

                            FU_Target_Lesion_1_PAD_Art_Enhanc = st.number_input(
                                "1st_FU_Target Lesion 1 PAD Art Enhanc",
                                format="%.2f"
                            )

                            FU_Target_Lesion_1_CCD_Art_Enhanc = st.number_input(
                                "1st_FU_Target Lesion 1 CCD Art Enhanc",
                                format="%.2f"
                            )

                            FU_Target_Lesion_2_Segments = st.selectbox(
                                "1st_FU_Target Lesion 2 Segments",
                                options=["1", "2", "3", "4a", "4b", "5", "6", "7", "8", "NA"],
                    index=None,  # No default selection
                    placeholder="Choose an option",
                            )

                            FU_Target_Lesion_2_LAD_Art_Enhanc = st.number_input(
                                "1st_FU_Target Lesion 2 LAD Art Enhanc",
                                format="%.2f"
                            )

                            FU_Target_Lesion_2_PAD_Art_Enhanc = st.number_input(
                                "1st_FU_Target Lesion 2 PAD Art Enhanc",
                                format="%.2f"
                            )

                            FU_Target_Lesion_2_CCD_Art_Enhanc = st.number_input(
                                "1st_FU_Target Lesion 2 CCD Art Enhanc",
                                format="%.2f"
                            )

                            # Assuming "Follow up 1 targeted Lesion Dia Sum" is calculated elsewhere in the code
                            # FU_Follow_up_1_targeted_Lesion_Dia_Sum = calculated_value
                            FU_Follow_up_1_targeted_Lesion_Dia_Sum = max(FU_Target_Lesion_1_CCD_Art_Enhanc,FU_Target_Lesion_1_PAD_Art_Enhanc,FU_Target_Lesion_1_LAD_Art_Enhanc)+max(FU_Target_Lesion_2_CCD_Art_Enhanc,FU_Target_Lesion_2_PAD_Art_Enhanc,FU_Target_Lesion_2_LAD_Art_Enhanc)


                            FU_Non_Target_Lesion_2_LAD_Art_Enhanc = st.number_input(
                                "1st_FU_Non-Target Lesion 2 LAD Art Enhanc",
                                format="%.2f"
                            )

                            FU_Non_Target_Lesion_2_PAD_Art_Enhanc = st.number_input(
                                "1st_FU_Non-Target Lesion 2 PAD Art Enhanc",
                                format="%.2f"
                            )

                            FU_Non_Target_Lesion_2_CCD_Art_Enhanc = st.number_input(
                                "1st_FU_Non-Target Lesion 2 CCD Art Enhanc",
                                format="%.2f"
                            )

                            # Assuming "Non-targeted Lesion Dia Sum" is calculated elsewhere in the code
                            FU_Non_targeted_Lesion_Dia_Sum = max(FU_Non_Target_Lesion_2_LAD_Art_Enhanc,FU_Non_Target_Lesion_2_PAD_Art_Enhanc,FU_Non_Target_Lesion_2_CCD_Art_Enhanc)

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

                            FU_change_target_lesion = ((PREY90_pretx_targeted_Lesion_Dia_Sum - FU_Follow_up_1_targeted_Lesion_Dia_Sum)/max(1,PREY90_pretx_targeted_Lesion_Dia_Sum))*100

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

                            FU2_Total_number_of_lesions = st.selectbox(
                                "2nd_FU_Total number of lesions",
                                options=["1", "2", ">3"],
                    index=None,  # No default selection
                    placeholder="Choose an option",
                            )

                            FU2_Target_Lesion_1_LAD_Art_Enhanc = st.number_input(
                                "2nd_FU_Target Lesion 1 LAD Art Enhanc",
                                format="%.2f"
                            )

                            FU2_Target_Lesion_1_PAD_Art_Enhanc = st.number_input(
                                "2nd_FU_Target Lesion 1 PAD Art Enhanc",
                                format="%.2f"
                            )

                            FU2_Target_Lesion_1_CCD_Art_Enhanc = st.number_input(
                                "2nd_FU_Target Lesion 1 CCD Art Enhanc",
                                format="%.2f"
                            )

                            FU2_Target_Lesion_2_Segments = st.selectbox(
                                "2nd_FU_Target Lesion 2 Segments",
                                options=["1", "2", "3", "4a", "4b", "5", "6", "7", "8", "NA"],
                    index=None,  # No default selection
                    placeholder="Choose an option",
                            )

                            FU2_Target_Lesion_2_LAD_Art_Enhanc = st.number_input(
                                "2nd_FU_Target Lesion 2 LAD Art Enhanc",
                                format="%.2f"
                            )

                            FU2_Target_Lesion_2_PAD_Art_Enhanc = st.number_input(
                                "2nd_FU_Target Lesion 2 PAD Art Enhanc",
                                format="%.2f"
                            )

                            FU2_Target_Lesion_2_CCD_Art_Enhanc = st.number_input(
                                "2nd_FU_Target Lesion 2 CCD Art Enhanc",
                                format="%.2f"
                            )

                            FU2_Follow_up_2_targeted_Lesion_Dia_Sum = max(FU2_Target_Lesion_1_CCD_Art_Enhanc, FU2_Target_Lesion_1_PAD_Art_Enhanc, FU2_Target_Lesion_1_LAD_Art_Enhanc) + max(FU2_Target_Lesion_2_CCD_Art_Enhanc, FU2_Target_Lesion_2_PAD_Art_Enhanc, FU2_Target_Lesion_2_LAD_Art_Enhanc)

                            FU2_Non_Target_Lesion_1_LAD_Art_Enhanc = st.number_input(
                                "2nd_FU_Non-Target Lesion 1 LAD Art Enhanc",
                                format="%.2f"
                            )

                            FU2_Non_Target_Lesion_1_PAD_Art_Enhanc = st.number_input(
                                "2nd_FU_Non-Target Lesion 1 PAD Art Enhanc",
                                format="%.2f"
                            )

                            FU2_Non_Target_Lesion_1_CCD_Art_Enhanc = st.number_input(
                                "2nd_FU_Non-Target Lesion 1 CCD Art Enhanc",
                                format="%.2f"
                            )

                            FU2_Non_targeted_Lesion_Dia_Sum = max(FU2_Non_Target_Lesion_1_LAD_Art_Enhanc, FU2_Non_Target_Lesion_1_PAD_Art_Enhanc, FU2_Non_Target_Lesion_1_CCD_Art_Enhanc)

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

                            FU2_change_target_lesion = ((PREY90_pretx_targeted_Lesion_Dia_Sum - FU2_Follow_up_2_targeted_Lesion_Dia_Sum) / max(1,PREY90_pretx_targeted_Lesion_Dia_Sum)) * 100

                            FU2_Free_Text = st.text_area(
                                "2nd_FU_Free Text",
                                help="Free text"
                            )

                            # Repeat the same structure for 3rd, 4th, and 5th follow-ups with variable names changed accordingly

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

                            FU3_Total_number_of_lesions = st.selectbox(
                                "3rd_FU_Total number of lesions",
                                options=["1", "2", ">3"],
                    index=None,  # No default selection
                    placeholder="Choose an option",
                            )

                            FU3_Target_Lesion_1_LAD_Art_Enhanc = st.number_input(
                                "3rd_FU_Target Lesion 1 LAD Art Enhanc",
                                format="%.2f"
                            )

                            FU3_Target_Lesion_1_PAD_Art_Enhanc = st.number_input(
                                "3rd_FU_Target Lesion 1 PAD Art Enhanc",
                                format="%.2f"
                            )

                            FU3_Target_Lesion_1_CCD_Art_Enhanc = st.number_input(
                                "3rd_FU_Target Lesion 1 CCD Art Enhanc",
                                format="%.2f"
                            )

                            FU3_Target_Lesion_2_Segments = st.selectbox(
                                "3rd_FU_Target Lesion 2 Segments",
                                options=["1", "2", "3", "4a", "4b", "5", "6", "7", "8", "NA"],
                    index=None,  # No default selection
                    placeholder="Choose an option",
                            )

                            FU3_Target_Lesion_2_LAD_Art_Enhanc = st.number_input(
                                "3rd_FU_Target Lesion 2 LAD Art Enhanc",
                                format="%.2f"
                            )

                            FU3_Target_Lesion_2_PAD_Art_Enhanc = st.number_input(
                                "3rd_FU_Target Lesion 2 PAD Art Enhanc",
                                format="%.2f"
                            )

                            FU3_Target_Lesion_2_CCD_Art_Enhanc = st.number_input(
                                "3rd_FU_Target Lesion 2 CCD Art Enhanc",
                                format="%.2f"
                            )

                            FU3_Follow_up_2_targeted_Lesion_Dia_Sum = max(FU3_Target_Lesion_1_CCD_Art_Enhanc, FU3_Target_Lesion_1_PAD_Art_Enhanc, FU3_Target_Lesion_1_LAD_Art_Enhanc) + max(FU3_Target_Lesion_2_CCD_Art_Enhanc, FU3_Target_Lesion_2_PAD_Art_Enhanc, FU3_Target_Lesion_2_LAD_Art_Enhanc)

                            FU3_Non_Target_Lesion_1_LAD_Art_Enhanc = st.number_input(
                                "3rd_FU_Non-Target Lesion 1 LAD Art Enhanc",
                                format="%.2f"
                            )

                            FU3_Non_Target_Lesion_1_PAD_Art_Enhanc = st.number_input(
                                "3rd_FU_Non-Target Lesion 1 PAD Art Enhanc",
                                format="%.2f"
                            )

                            FU3_Non_Target_Lesion_1_CCD_Art_Enhanc = st.number_input(
                                "3rd_FU_Non-Target Lesion 1 CCD Art Enhanc",
                                format="%.2f"
                            )

                            FU3_Non_targeted_Lesion_Dia_Sum = max(FU3_Non_Target_Lesion_1_LAD_Art_Enhanc, FU3_Non_Target_Lesion_1_PAD_Art_Enhanc, FU3_Non_Target_Lesion_1_CCD_Art_Enhanc)

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

                            FU3_change_target_lesion = ((PREY90_pretx_targeted_Lesion_Dia_Sum - FU3_Follow_up_2_targeted_Lesion_Dia_Sum) / max(1,PREY90_pretx_targeted_Lesion_Dia_Sum)) * 100

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

                            FU4_Total_number_of_lesions = st.selectbox(
                                "4th_FU_Total number of lesions",
                                options=["1", "2", ">3"],
                    index=None,  # No default selection
                    placeholder="Choose an option",
                            )

                            FU4_Target_Lesion_1_LAD_Art_Enhanc = st.number_input(
                                "4th_FU_Target Lesion 1 LAD Art Enhanc",
                                format="%.2f"
                            )

                            FU4_Target_Lesion_1_PAD_Art_Enhanc = st.number_input(
                                "4th_FU_Target Lesion 1 PAD Art Enhanc",
                                format="%.2f"
                            )

                            FU4_Target_Lesion_1_CCD_Art_Enhanc = st.number_input(
                                "4th_FU_Target Lesion 1 CCD Art Enhanc",
                                format="%.2f"
                            )

                            FU4_Target_Lesion_2_Segments = st.selectbox(
                                "4th_FU_Target Lesion 2 Segments",
                                options=["1", "2", "3", "4a", "4b", "5", "6", "7", "8", "NA"],
                    index=None,  # No default selection
                    placeholder="Choose an option",
                            )

                            FU4_Target_Lesion_2_LAD_Art_Enhanc = st.number_input(
                                "4th_FU_Target Lesion 2 LAD Art Enhanc",
                                format="%.2f"
                            )

                            FU4_Target_Lesion_2_PAD_Art_Enhanc = st.number_input(
                                "4th_FU_Target Lesion 2 PAD Art Enhanc",
                                format="%.2f"
                            )

                            FU4_Target_Lesion_2_CCD_Art_Enhanc = st.number_input(
                                "4th_FU_Target Lesion 2 CCD Art Enhanc",
                                format="%.2f"
                            )

                            FU4_Follow_up_2_targeted_Lesion_Dia_Sum = max(FU4_Target_Lesion_1_CCD_Art_Enhanc, FU4_Target_Lesion_1_PAD_Art_Enhanc, FU4_Target_Lesion_1_LAD_Art_Enhanc) + max(FU4_Target_Lesion_2_CCD_Art_Enhanc, FU4_Target_Lesion_2_PAD_Art_Enhanc, FU4_Target_Lesion_2_LAD_Art_Enhanc)

                            FU4_Non_Target_Lesion_1_LAD_Art_Enhanc = st.number_input(
                                "4th_FU_Non-Target Lesion 1 LAD Art Enhanc",
                                format="%.2f"
                            )

                            FU4_Non_Target_Lesion_1_PAD_Art_Enhanc = st.number_input(
                                "4th_FU_Non-Target Lesion 1 PAD Art Enhanc",
                                format="%.2f"
                            )

                            FU4_Non_Target_Lesion_1_CCD_Art_Enhanc = st.number_input(
                                "4th_FU_Non-Target Lesion 1 CCD Art Enhanc",
                                format="%.2f"
                            )

                            FU4_Non_targeted_Lesion_Dia_Sum = max(FU4_Non_Target_Lesion_1_LAD_Art_Enhanc, FU4_Non_Target_Lesion_1_PAD_Art_Enhanc, FU4_Non_Target_Lesion_1_CCD_Art_Enhanc)

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

                            FU4_change_target_lesion = ((PREY90_pretx_targeted_Lesion_Dia_Sum - FU4_Follow_up_2_targeted_Lesion_Dia_Sum) / max(1,PREY90_pretx_targeted_Lesion_Dia_Sum)) * 100

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

                            FU5_Total_number_of_lesions = st.selectbox(
                                "5th_FU_Total number of lesions",
                                options=["1", "2", ">3"],
                    index=None,  # No default selection
                    placeholder="Choose an option",
                            )

                            FU5_Non_Target_Lesion_1_LAD_Art_Enhanc = st.number_input(
                                "5th_FU_Non-Target Lesion 1 LAD Art Enhanc",
                                format="%.2f"
                            )

                            FU5_Non_Target_Lesion_1_PAD_Art_Enhanc = st.number_input(
                                "5th_FU_Non-Target Lesion 1 PAD Art Enhanc",
                                format="%.2f"
                            )

                            FU5_Non_Target_Lesion_1_CCD_Art_Enhanc = st.number_input(
                                "5th_FU_Non-Target Lesion 1 CCD Art Enhanc",
                                format="%.2f"
                            )

                            FU5_Non_targeted_Lesion_Dia_Sum = max(FU5_Non_Target_Lesion_1_LAD_Art_Enhanc, FU5_Non_Target_Lesion_1_PAD_Art_Enhanc, FU5_Non_Target_Lesion_1_CCD_Art_Enhanc)

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

                            Date_of_Localized_Progression = st.text_input("Date of Localized Progression")

                            if Date_of_Localized_Progression == "No Progression":
                                    Time_to_localized_progression = 'NA'
                            else:
                                    Time_to_Localized_Progression = relativedelta(Date_of_Localized_Progression, fetch_date).years

                            Date_of_Overall_Progression = st.text_input("Date of Overall Progression")

                            if Date_of_Overall_Progression == "No Progression":
                                    Time_to_overall_progression = 'NA'
                            else:
                                    Time_to_overall_Progression = relativedelta(Date_of_Overall_Progression, fetch_date).years

                            Date_of_Last_Follow_up_last_imaging_date = 'NA' if dead == 1 and OLT == 1 else st.date_input("Date of Last Follow-up/last imaging date")

                            Time_to_Last_Follow_up_last_imaging_date = 'NA' if dead == 1 and OLT == 1 else relativedelta(Date_of_Last_Follow_up_last_imaging_date, fetch_date).years 

                            submit_tab10 = st.form_submit_button("Submit")

                            if submit_tab10:
                                #index = st.session_state.data[st.session_state.data["MRN"] == st.session_state.temp_mrn].index[0]

                                st.session_state.data.at[index, "PREY90_prescan_modality"] = PREY90_prescan_modality
                                st.session_state.data.at[index, "PREY90_Imaging Date"] = PREY90_Imaging_Date
                                st.session_state.data.at[index, "PREY90_total number of lesions"] = PREY90_total_number_of_lesions
                                st.session_state.data.at[index, "PREY90_Number Involved Lobes"] = PREY90_Number_Involved_Lobes
                                st.session_state.data.at[index, "PREY90_target_lesion_1_segments"] = PREY90_target_lesion_1_segments
                                st.session_state.data.at[index, "PREY90_TL1_LAD"] = PREY90_TL1_LAD
                                st.session_state.data.at[index, "PREY90_Target Lesion 1 PAD"] = PREY90_Target_Lesion_1_PAD
                                st.session_state.data.at[index, "PREY90_Target Lesion 1 CCD"] = PREY90_Target_Lesion_1_CCD
                                st.session_state.data.at[index, "PREY90_Target Lesion 1 VOL"] = PREY90_Target_Lesion_1_VOL
                                st.session_state.data.at[index, "PREY90_Target lesion 2 Segments"] = PREY90_Target_Lesion_2_segments
                                st.session_state.data.at[index, "PREY90_Target Lesion 2 LAD"] = PREY90_Target_Lesion_2_LAD
                                st.session_state.data.at[index, "PREY90_Target Lesion 2 PAD"] = PREY90_Target_Lesion_2_PAD
                                st.session_state.data.at[index, "PREY90_Target Lesion 2 CCD"] = PREY90_Target_Lesion_2_CCD
                                st.session_state.data.at[index, "PREY90_Target Lesion 2 VOL"] = PREY90_Target_Lesion_2_VOL
                                st.session_state.data.at[index, "PREY90_pretx targeted Lesion Dia Sum"] = PREY90_pretx_targeted_Lesion_Dia_Sum
                                st.session_state.data.at[index, "PREY90_Non-Target Lesion Location"] = PREY90_Non_Target_Lesion_Location
                                st.session_state.data.at[index, "PREY90_Non-Target Lesion 2 LAD Art Enhanc"] = PREY90_Non_Target_Lesion_2_LAD_Art_Enhanc
                                st.session_state.data.at[index, "PREY90_Non-Target Lesion 2 PAD Art Enhanc"] = PREY90_Non_Target_Lesion_2_PAD_Art_Enhanc
                                st.session_state.data.at[index, "PREY90_Non-Target Lesion 2 CCD Art Enhanc"] = PREY90_Non_Target_Lesion_2_CCD_Art_Enhanc
                                st.session_state.data.at[index, "PREY90_Non-targeted Lesion Dia Sum"] = PREY90_Non_targeted_Lesion_Dia_Sum
                                st.session_state.data.at[index, "PREY90_Reviewers Initials"] = PREY90_Reviewers_Initials
                                st.session_state.data.at[index, "PREY90_Pre Y90 Extrahepatic Disease"] = PREY90_Pre_Y90_Extrahepatic_Disease
                                st.session_state.data.at[index, "PREY90_Pre Y90 Extrahepatic Disease Location"] = PREY90_Pre_Y90_Extrahepatic_Disease_Location
                                st.session_state.data.at[index, "PREY90_PVT"] = PREY90_PVT
                                st.session_state.data.at[index, "PREY90_PVT Location"] = PREY90_PVT_Location
                                st.session_state.data.at[index, "PREY90_Features of cirrhosis"] = PREY90_Features_of_cirrhosis
                                st.session_state.data.at[index, "1st_FU_Scan Modality"] = FU_Scan_Modality
                                st.session_state.data.at[index, "1st_FU_Imaging Date"] = FU_Imaging_Date
                                st.session_state.data.at[index, "1st_FU_Months Since Y90"] = FU_Months_Since_Y90
                                st.session_state.data.at[index, "1st_FU_Total number of lesions"] = FU_Total_number_of_lesions
                                st.session_state.data.at[index, "1st_FU_Target Lesion 1 LAD Art Enhanc"] = FU_Target_Lesion_1_LAD_Art_Enhanc
                                st.session_state.data.at[index, "1st_FU_Target Lesion 1 PAD Art Enhanc"] = FU_Target_Lesion_1_PAD_Art_Enhanc
                                st.session_state.data.at[index, "1st_FU_Target Lesion 1 CCD Art Enhanc"] = FU_Target_Lesion_1_CCD_Art_Enhanc
                                st.session_state.data.at[index, "1st_FU_Target Lesion 2 Segments"] = FU_Target_Lesion_2_Segments
                                st.session_state.data.at[index, "1st_FU_Target Lesion 2 LAD Art Enhanc"] = FU_Target_Lesion_2_LAD_Art_Enhanc
                                st.session_state.data.at[index, "1st_FU_Target Lesion 2 PAD Art Enhanc"] = FU_Target_Lesion_2_PAD_Art_Enhanc
                                st.session_state.data.at[index, "1st_FU_Target Lesion 2 CCD Art Enhanc"] = FU_Target_Lesion_2_CCD_Art_Enhanc
                                st.session_state.data.at[index, "1st_FU_Follow up 1 targeted Lesion Dia Sum"] = FU_Follow_up_1_targeted_Lesion_Dia_Sum
                                st.session_state.data.at[index, "1st_FU_Non-Target Lesion 2 LAD Art Enhanc"] = FU_Non_Target_Lesion_2_LAD_Art_Enhanc
                                st.session_state.data.at[index, "1st_FU_Non-Target Lesion 2 PAD Art Enhanc"] = FU_Non_Target_Lesion_2_PAD_Art_Enhanc
                                st.session_state.data.at[index, "1st_FU_Non-Target Lesion 2 CCD Art Enhanc"] = FU_Non_Target_Lesion_2_CCD_Art_Enhanc
                                st.session_state.data.at[index, "1st_FU_Non-targeted Lesion Dia Sum"] = FU_Non_targeted_Lesion_Dia_Sum
                                st.session_state.data.at[index, "1st_FU_Lesion Necrosis"] = FU_Lesion_Necrosis
                                st.session_state.data.at[index, "1st_FU_Reviewers Initials"] = FU_Reviewers_Initials
                                st.session_state.data.at[index, "1st_FU_Non target lesion response"] = FU_Non_target_lesion_response
                                st.session_state.data.at[index, "1st_FU_New Lesions"] = FU_New_Lesions
                                st.session_state.data.at[index, "1st_FU_NEW Extrahepatic Disease"] = FU_NEW_Extrahepatic_Disease
                                st.session_state.data.at[index, "1st_FU_NEW Extrahepatic Dz Location"] = FU_NEW_Extrahepatic_Dz_Location
                                st.session_state.data.at[index, "1st_FU_NEW Extrahepatic Dz Date"] = FU_NEW_Extrahepatic_Dz_Date
                                st.session_state.data.at[index, "1st_FU_% change non target lesion"] = FU_change_non_target_lesion
                                st.session_state.data.at[index, "1st_FU_% Change Target Dia"] = FU_change_target_lesion
                                st.session_state.data.at[index, "1st_FU_Free Text"] = FU_Free_Text
                                st.session_state.data.at[index, "2nd_FU_Scan Modality"] = FU2_Scan_Modality
                                st.session_state.data.at[index, "2nd_FU_Imaging Date"] = FU2_Imaging_Date
                                st.session_state.data.at[index, "2nd_FU_Months Since Y90"] = FU2_Months_Since_Y90
                                st.session_state.data.at[index, "2nd_FU_Total number of lesions"] = FU2_Total_number_of_lesions
                                st.session_state.data.at[index, "2nd_FU_Target Lesion 1 LAD Art Enhanc"] = FU2_Target_Lesion_1_LAD_Art_Enhanc
                                st.session_state.data.at[index, "2nd_FU_Target Lesion 1 PAD Art Enhanc"] = FU2_Target_Lesion_1_PAD_Art_Enhanc
                                st.session_state.data.at[index, "2nd_FU_Target Lesion 1 CCD Art Enhanc"] = FU2_Target_Lesion_1_CCD_Art_Enhanc
                                st.session_state.data.at[index, "2nd_FU_Target Lesion 2 Segments"] = FU2_Target_Lesion_2_Segments
                                st.session_state.data.at[index, "2nd_FU_Target Lesion 2 LAD Art Enhanc"] = FU2_Target_Lesion_2_LAD_Art_Enhanc
                                st.session_state.data.at[index, "2nd_FU_Target Lesion 2 PAD Art Enhanc"] = FU2_Target_Lesion_2_PAD_Art_Enhanc
                                st.session_state.data.at[index, "2nd_FU_Target Lesion 2 CCD Art Enhanc"] = FU2_Target_Lesion_2_CCD_Art_Enhanc
                                st.session_state.data.at[index, "2nd_FU_Follow up 2 targeted Lesion Dia Sum"] = FU2_Follow_up_2_targeted_Lesion_Dia_Sum
                                st.session_state.data.at[index, "2nd_FU_Non-Target Lesion 1 LAD Art Enhanc"] = FU2_Non_Target_Lesion_1_LAD_Art_Enhanc
                                st.session_state.data.at[index, "2nd_FU_Non-Target Lesion 1 PAD Art Enhanc"] = FU2_Non_Target_Lesion_1_PAD_Art_Enhanc
                                st.session_state.data.at[index, "2nd_FU_Non-Target Lesion 1 CCD Art Enhanc"] = FU2_Non_Target_Lesion_1_CCD_Art_Enhanc
                                st.session_state.data.at[index, "2nd_FU_Non-targeted Lesion Dia Sum"] = FU2_Non_targeted_Lesion_Dia_Sum
                                st.session_state.data.at[index, "2nd_FU_Lesion Necrosis"] = FU2_Lesion_Necrosis
                                st.session_state.data.at[index, "2nd_FU_Reviewers Initials"] = FU2_Reviewers_Initials
                                st.session_state.data.at[index, "2nd_FU_Non target lesion response"] = FU2_Non_target_lesion_response
                                st.session_state.data.at[index, "2nd_FU_New Lesions"] = FU2_New_Lesions
                                st.session_state.data.at[index, "2nd_FU_Extrahepatic Disease"] = FU2_NEW_Extrahepatic_Disease
                                st.session_state.data.at[index, "2nd_FU_NEW Extrahepatic Dz Location"] = FU2_NEW_Extrahepatic_Dz_Location
                                st.session_state.data.at[index, "2nd_FU_NEW Extrahepatic Dz Date"] = FU2_NEW_Extrahepatic_Dz_Date
                                st.session_state.data.at[index, "2nd_FU_% change non target lesion"] = FU2_change_non_target_lesion
                                st.session_state.data.at[index, "2nd_FU_% Change Target Dia"] = FU2_change_target_lesion
                                st.session_state.data.at[index, "2nd_FU_Free Text"] = FU2_Free_Text
                                st.session_state.data.at[index, "3rd_FU_Scan Modality"] = FU3_Scan_Modality
                                st.session_state.data.at[index, "3rd_FU_Imaging Date"] = FU3_Imaging_Date
                                st.session_state.data.at[index, "3rd_FU_Months Since Y90"] = FU3_Months_Since_Y90
                                st.session_state.data.at[index, "3rd_FU_Total number of lesions"] = FU3_Total_number_of_lesions
                                st.session_state.data.at[index, "3rd_FU_Target Lesion 1 LAD Art Enhanc"] = FU3_Target_Lesion_1_LAD_Art_Enhanc
                                st.session_state.data.at[index, "3rd_FU_Target Lesion 1 PAD Art Enhanc"] = FU3_Target_Lesion_1_PAD_Art_Enhanc
                                st.session_state.data.at[index, "3rd_FU_Target Lesion 1 CCD Art Enhanc"] = FU3_Target_Lesion_1_CCD_Art_Enhanc
                                st.session_state.data.at[index, "3rd_FU_Target Lesion 2 Segments"] = FU3_Target_Lesion_2_Segments
                                st.session_state.data.at[index, "3rd_FU_Target Lesion 2 LAD Art Enhanc"] = FU3_Target_Lesion_2_LAD_Art_Enhanc
                                st.session_state.data.at[index, "3rd_FU_Target Lesion 2 PAD Art Enhanc"] = FU3_Target_Lesion_2_PAD_Art_Enhanc
                                st.session_state.data.at[index, "3rd_FU_Target Lesion 2 CCD Art Enhanc"] = FU3_Target_Lesion_2_CCD_Art_Enhanc
                                st.session_state.data.at[index, "3rd_FU_Follow up 2 targeted Lesion Dia Sum"] = FU3_Follow_up_2_targeted_Lesion_Dia_Sum
                                st.session_state.data.at[index, "3rd_FU_Non-Target Lesion 1 LAD Art Enhanc"] = FU3_Non_Target_Lesion_1_LAD_Art_Enhanc
                                st.session_state.data.at[index, "3rd_FU_Non-Target Lesion 1 PAD Art Enhanc"] = FU3_Non_Target_Lesion_1_PAD_Art_Enhanc
                                st.session_state.data.at[index, "3rd_FU_Non-Target Lesion 1 CCD Art Enhanc"] = FU3_Non_Target_Lesion_1_CCD_Art_Enhanc
                                st.session_state.data.at[index, "3rd_FU_Non-targeted Lesion Dia Sum"] = FU3_Non_targeted_Lesion_Dia_Sum
                                st.session_state.data.at[index, "3rd_FU_Lesion Necrosis"] = FU3_Lesion_Necrosis
                                st.session_state.data.at[index, "3rd_FU_Reviewers Initials"] = FU3_Reviewers_Initials
                                st.session_state.data.at[index, "3rd_FU_Non target lesion response"] = FU3_Non_target_lesion_response
                                st.session_state.data.at[index, "3rd_FU_New Lesions"] = FU3_New_Lesions
                                st.session_state.data.at[index, "3rd_FU_Extrahepatic Disease"] = FU3_NEW_Extrahepatic_Disease
                                st.session_state.data.at[index, "3rd_FU_NEW Extrahepatic Dz Location"] = FU3_NEW_Extrahepatic_Dz_Location
                                st.session_state.data.at[index, "3rd_FU_NEW Extrahepatic Dz Date"] = FU3_NEW_Extrahepatic_Dz_Date
                                st.session_state.data.at[index, "3rd_FU_% change for non target lesion"] = FU3_change_non_target_lesion
                                st.session_state.data.at[index, "3rd_FU_% Change Target Dia"] = FU3_change_target_lesion
                                st.session_state.data.at[index, "3rd_FU_Free Text"] = FU3_Free_Text
                                st.session_state.data.at[index, "4th_FU_Scan Modality"] = FU4_Scan_Modality
                                st.session_state.data.at[index, "4th_FU_Imaging Date"] = FU4_Imaging_Date
                                st.session_state.data.at[index, "4th_FU_Months Since Y90"] = FU4_Months_Since_Y90
                                st.session_state.data.at[index, "4th_FU_Total number of lesions"] = FU4_Total_number_of_lesions
                                st.session_state.data.at[index, "4th_FU_Target Lesion 1 LAD Art Enhanc"] = FU4_Target_Lesion_1_LAD_Art_Enhanc
                                st.session_state.data.at[index, "4th_FU_Target Lesion 1 PAD Art Enhanc"] = FU4_Target_Lesion_1_PAD_Art_Enhanc
                                st.session_state.data.at[index, "4th_FU_Target Lesion 1 CCD Art Enhanc"] = FU4_Target_Lesion_1_CCD_Art_Enhanc
                                st.session_state.data.at[index, "4th_FU_Target Lesion 2 Segments"] = FU4_Target_Lesion_2_Segments
                                st.session_state.data.at[index, "4th_FU_Target Lesion 2 LAD Art Enhanc"] = FU4_Target_Lesion_2_LAD_Art_Enhanc
                                st.session_state.data.at[index, "4th_FU_Target Lesion 2 PAD Art Enhanc"] = FU4_Target_Lesion_2_PAD_Art_Enhanc
                                st.session_state.data.at[index, "4th_FU_Target Lesion 2 CCD Art Enhanc"] = FU4_Target_Lesion_2_CCD_Art_Enhanc
                                st.session_state.data.at[index, "4th_FU_Follow up 2 targeted Lesion Dia Sum"] = FU4_Follow_up_2_targeted_Lesion_Dia_Sum
                                st.session_state.data.at[index, "4th_FU_Non-Target Lesion 1 LAD Art Enhanc"] = FU4_Non_Target_Lesion_1_LAD_Art_Enhanc
                                st.session_state.data.at[index, "4th_FU_Non-Target Lesion 1 PAD Art Enhanc"] = FU4_Non_Target_Lesion_1_PAD_Art_Enhanc
                                st.session_state.data.at[index, "4th_FU_Non-Target Lesion 1 CCD Art Enhanc"] = FU4_Non_Target_Lesion_1_CCD_Art_Enhanc
                                st.session_state.data.at[index, "4th_FU_Non-targeted Lesion Dia Sum"] = FU4_Non_targeted_Lesion_Dia_Sum
                                st.session_state.data.at[index, "4th_FU_Lesion Necrosis"] = FU4_Lesion_Necrosis
                                st.session_state.data.at[index, "4th_FU_Reviewers Initials"] = FU4_Reviewers_Initials
                                st.session_state.data.at[index, "4th_FU_Non target lesion response"] = FU4_Non_target_lesion_response
                                st.session_state.data.at[index, "4th_FU_New Lesions"] = FU4_New_Lesions
                                st.session_state.data.at[index, "4th_FU_Extrahepatic Disease"] = FU4_NEW_Extrahepatic_Disease
                                st.session_state.data.at[index, "4th_FU_NEW Extrahepatic Dz Location"] = FU4_NEW_Extrahepatic_Dz_Location
                                st.session_state.data.at[index, "4th_FU_NEW Extrahepatic Dz Date"] = FU4_NEW_Extrahepatic_Dz_Date
                                st.session_state.data.at[index, "4th_FU_% change non target lesion"] = FU4_change_non_target_lesion
                                st.session_state.data.at[index, "4th_FU_% Change Target Dia"] = FU4_change_target_lesion
                                st.session_state.data.at[index, "4th_FU_Free Text"] = FU4_Free_Text
                                st.session_state.data.at[index, "5th_FU_Imaging Date"] = FU5_Imaging_Date
                                st.session_state.data.at[index, "5th_FU_Months Since Y90"] = FU5_Months_Since_Y90
                                st.session_state.data.at[index, "5th_FU_Total number of lesions"] = FU5_Total_number_of_lesions
                                st.session_state.data.at[index, "5th_FU_Non-Target Lesion 1 LAD Art Enhanc"] = FU5_Non_Target_Lesion_1_LAD_Art_Enhanc
                                st.session_state.data.at[index, "5th_FU_Non-Target Lesion 1 PAD Art Enhanc"] = FU5_Non_Target_Lesion_1_PAD_Art_Enhanc
                                st.session_state.data.at[index, "5th_FU_Non-Target Lesion 1 CCD Art Enhanc"] = FU5_Non_Target_Lesion_1_CCD_Art_Enhanc
                                st.session_state.data.at[index, "5th_FU_Non-targeted Lesion Dia Sum"] = FU5_Non_targeted_Lesion_Dia_Sum
                                st.session_state.data.at[index, "5th_FU_Non target lesion response"] = FU5_Non_target_lesion_response
                                st.session_state.data.at[index, "5th_FU_New Lesions"] = FU5_New_Lesions
                                st.session_state.data.at[index, "5th_FU_Extrahepatic Disease"] = FU5_NEW_Extrahepatic_Disease
                                st.session_state.data.at[index, "5th_FU_NEW Extrahepatic Dz Location"] = FU5_NEW_Extrahepatic_Dz_Location
                                st.session_state.data.at[index, "5th_FU_NEW Extrahepatic Dz Date"] = FU5_NEW_Extrahepatic_Dz_Date
                                st.session_state.data.at[index, "5th_FU_% change non target lesion"] = FU5_change_non_target_lesion
                                st.session_state.data.at[index, "Dead"] = dead
                                st.session_state.data.at[index, "Date of Death"] = Date_of_Death
                                st.session_state.data.at[index, "Time to Death"] = Time_to_Death
                                st.session_state.data.at[index, "OLT"] = OLT
                                st.session_state.data.at[index, "Date of OLT"] = Date_of_OLT
                                st.session_state.data.at[index, "Time to OLT"] = Time_to_OLT
                                st.session_state.data.at[index, "Repeat tx post Y90"] = Repeat_tx_post_Y90
                                st.session_state.data.at[index, "Date of Repeat tx Post Y90"] = Date_of_Repeat_tx_Post_Y90
                                st.session_state.data.at[index, "Time to Repeat Tx Post Y90"] = Time_to_Repeat_Tx_Post_Y90
                                st.session_state.data.at[index, "Date of Localized Progression"] = Date_of_Localized_Progression
                                
                            
                                st.success("Imagine Data dubmitted")
                                          
                elif st.session_state.selected_tab == "Dosimetry Data":
                    st.subheader("Dosimetry Data")
                    with st.form("dosimetry_data_form"):
            
                        input_GTV_mean_dose = st.text_input("GTV mean dose")
                        input_Tx_vol_mean_dose = st.text_input("Tx vol mean dose")
                        input_Liver_Vol_Mean_dose = st.text_input("Liver Vol Mean dose")
                        input_Healthy_Liver_mean_dose = st.text_input("Healthy Liver mean dose")
                        input_GTV_Vol = st.number_input("GTV Vol")
                        input_Tx_vol = st.text_input("Tx vol")
                        input_Liver_vol = st.number_input("Liver vol", min_value=1)
                        input_Healthy_Liver_Vol = st.text_input("Healthy Liver Vol")
                        input_GTV_Liver = (input_GTV_Vol)/(input_Liver_vol)*100
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
                            index = st.session_state.data[st.session_state.data["MRN"] == st.session_state.temp_mrn].index[0]

                            # Assign inputs to session state
                            st.session_state.data.at[index, "GTV mean dose"] = input_GTV_mean_dose
                            st.session_state.data.at[index, "Tx vol mean dose"] = input_Tx_vol_mean_dose
                            st.session_state.data.at[index, "Liver Vol Mean dose"] = input_Liver_Vol_Mean_dose
                            st.session_state.data.at[index, "Healthy Liver mean dose"] = input_Healthy_Liver_mean_dose
                            st.session_state.data.at[index, "GTV Vol"] = input_GTV_Vol
                            st.session_state.data.at[index, "Tx vol"] = input_Tx_vol
                            st.session_state.data.at[index, "Liver vol"] = input_Liver_vol
                            st.session_state.data.at[index, "Healthy Liver Vol"] = input_Healthy_Liver_Vol
                            st.session_state.data.at[index, "GTV/Liver"] = input_GTV_Liver
                            st.session_state.data.at[index, "D98"] = input_D98
                            st.session_state.data.at[index, "D95"] = input_D95
                            st.session_state.data.at[index, "D90"] = input_D90
                            st.session_state.data.at[index, "D80"] = input_D80
                            st.session_state.data.at[index, "D70"] = input_D70
                            st.session_state.data.at[index, "V100"] = input_V100
                            st.session_state.data.at[index, "V200"] = input_V200
                            st.session_state.data.at[index, "V300"] = input_V300
                            st.session_state.data.at[index, "V400"] = input_V400
                            st.session_state.data.at[index, "ActivityBq"] = input_ActivityBq
                            st.session_state.data.at[index, "ActivityCi"] = input_ActivityCi
                            st.session_state.data.at[index, "Tx vol Activity Density"] = input_Tx_vol_Activity_Density
                            st.session_state.data.at[index, "NEW"] = input_NEW
                            st.session_state.data.at[index, "GTV < D95 Vol_ml"] = input_GTV_less_D95_Vol_ml
                            st.session_state.data.at[index, "GTV < D95 Mean Dose"] = input_GTV_less_D95_Mean_Dose
                            st.session_state.data.at[index, "GTV < D95 Min Dose"] = input_GTV_less_D95_Min_Dose
                            st.session_state.data.at[index, "GTV < D95 SD"] = input_GTV_less_D95_SD
                            st.session_state.data.at[index, "GTV < D95 Vol_1"] = input_GTV_less_D95_Vol_1
                            st.session_state.data.at[index, "GTV < D95 Mean Dose_1"] = input_GTV_less_D95_Mean_Dose_1
                            st.session_state.data.at[index, "GTV < D95 Min Dose_1"] = input_GTV_less_D95_Min_Dose_1
                            st.session_state.data.at[index, "GTV < D95 SD_1"] = input_GTV_less_D95_SD_1
                            st.session_state.data.at[index, "GTV < D95 Vol_2"] = input_GTV_less_D95_Vol_2
                            st.session_state.data.at[index, "GTV < D95 Mean Dose_2"] = input_GTV_less_D95_Mean_Dose_2
                            st.session_state.data.at[index, "GTV < D95 Min Dose_2"] = input_GTV_less_D95_Min_Dose_2
                            st.session_state.data.at[index, "GTV < D95 SD_2"] = input_GTV_less_D95_SD_2
                            st.session_state.data.at[index, "GTV < 100 Gy Vol"] = input_GTV_less_100_Gy_Vol
                            st.session_state.data.at[index, "GTV < 100 Gy Mean Dose"] = input_GTV_less_100_Gy_Mean_Dose
                            st.session_state.data.at[index, "GTV < 100 Gy Min Dose"] = input_GTV_less_100_Gy_Min_Dose
                            st.session_state.data.at[index, "GTV < 100 Gy SD"] = input_GTV_less_100_Gy_SD
                            st.success("Dosimetry Data added successfully.")

                elif st.session_state.selected_tab == "AFP":
                    st.subheader("Dosimetry Data")
                    with st.form("dosimetry_data_form"):
                        
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
                                index = st.session_state.data[st.session_state.data["MRN"] == st.session_state.temp_mrn].index[0]
                                # Assign the input values to st.session_state.data at the specified index
                                st.session_state.data.at[index, "1AFP Date"] = input_1AFP_Date
                                st.session_state.data.at[index, "1AFP"] = input_1AFP
                                st.session_state.data.at[index, "2AFP Date"] = input_2AFP_Date
                                st.session_state.data.at[index, "2AFP"] = input_2AFP
                                st.session_state.data.at[index, "3AFP Date"] = input_3AFP_Date
                                st.session_state.data.at[index, "3AFP"] = input_3AFP
                                st.session_state.data.at[index, "4AFP Date"] = input_4AFP_Date
                                st.session_state.data.at[index, "4AFP"] = input_4AFP
                                st.session_state.data.at[index, "5AFP Date"] = input_5AFP_Date
                                st.session_state.data.at[index, "5AFP"] = input_5AFP
                                st.session_state.data.at[index, "6AFP Date"] = input_6AFP_Date
                                st.session_state.data.at[index, "6AFP"] = input_6AFP
                                st.session_state.data.at[index, "7AFP Date"] = input_7AFP_Date
                                st.session_state.data.at[index, "7AFP"] = input_7AFP
                                st.session_state.data.at[index, "8AFP Date"] = input_8AFP_Date
                                st.session_state.data.at[index, "8AFP"] = input_8AFP
                                st.session_state.data.at[index, "9AFP Date"] = input_9AFP_Date
                                st.session_state.data.at[index, "9AFP"] = input_9AFP
                                st.session_state.data.at[index, "10AFP Date"] = input_10AFP_Date
                                st.session_state.data.at[index, "10AFP"] = input_10AFP
                                st.session_state.data.at[index, "11AFP Date"] = input_11AFP_Date
                                st.session_state.data.at[index, "11AFP"] = input_11AFP
                                st.session_state.data.at[index, "12AFP Date"] = input_12AFP_Date
                                st.session_state.data.at[index, "12AFP"] = input_12AFP
                                st.session_state.data.at[index, "13AFP Date"] = input_13AFP_Date
                                st.session_state.data.at[index, "13AFP"] = input_13AFP
                                st.session_state.data.at[index, "14AFP Date"] = input_14AFP_Date
                                st.session_state.data.at[index, "14AFP"] = input_14AFP
                                st.session_state.data.at[index, "15AFP Date"] = input_15AFP_Date
                                st.session_state.data.at[index, "15AFP"] = input_15AFP
                                st.session_state.data.at[index, "16AFP Date"] = input_16AFP_Date
                                st.session_state.data.at[index, "16AFP"] = input_16AFP
                                st.session_state.data.at[index, "17AFP Date"] = input_17AFP_Date
                                st.session_state.data.at[index, "17AFP"] = input_17AFP
                                st.session_state.data.at[index, "18AFP DATE"] = input_18AFP_DATE
                                st.session_state.data.at[index, "18AFP"] = input_18AFP
                                st.session_state.data.at[index, "19AFP DATE"] = input_19AFP_DATE
                                st.session_state.data.at[index, "19AFP"] = input_19AFP
                                st.session_state.data.at[index, "20AFP DATE"] = input_20AFP_DATE
                                st.session_state.data.at[index, "20AFP"] = input_20AFP
                                st.session_state.data.at[index, "21AFP DATE"] = input_21AFP_DATE
                                st.session_state.data.at[index, "21AFP"] = input_21AFP
                                st.session_state.data.at[index, "22AFP DATE"] = input_22AFP_DATE
                                st.session_state.data.at[index, "22AFP"] = input_22AFP
                                st.session_state.data.at[index, "23AFP DATE"] = input_23AFP_DATE
                                st.session_state.data.at[index, "23AFP"] = input_23AFP
                                st.session_state.data.at[index, "24AFP DATE"] = input_24AFP_DATE
                                st.session_state.data.at[index, "24AFP"] = input_24AFP
                                st.session_state.data.at[index, "25AFP DATE"] = input_25AFP_DATE
                                st.session_state.data.at[index, "25AFP"] = input_25AFP
                                st.session_state.data.at[index, "26AFP DATE"] = input_26AFP_DATE
                                st.session_state.data.at[index, "26AFP"] = input_26AFP
                                st.session_state.data.at[index, "27AFP DATE"] = input_27AFP_DATE
                                st.session_state.data.at[index, "27AFP"] = input_27AFP
                                st.session_state.data.at[index, "28AFP DATE"] = input_28AFP_DATE
                                st.session_state.data.at[index, "28AFP"] = input_28AFP
                                st.session_state.data.at[index, "29AFP DATE"] = input_29AFP_DATE
                                st.session_state.data.at[index, "29AFP"] = input_29AFP
                                st.session_state.data.at[index, "30AFP DATE"] = input_30AFP_DATE
                                st.session_state.data.at[index, "30AFP"] = input_30AFP
                                st.session_state.data.at[index, "31AFP Date"] = input_31AFP_Date
                                st.session_state.data.at[index, "31AFP"] = input_31AFP
                                st.session_state.data.at[index, "32AFP DATE"] = input_32AFP_DATE
                                st.session_state.data.at[index, "32AFP"] = input_32AFP
                                st.session_state.data.at[index, "33AFP DATE"] = input_33AFP_DATE
                                st.session_state.data.at[index, "33AFP"] = input_33AFP
                                st.session_state.data.at[index, "34AFP DATE"] = input_34AFP_DATE
                                st.session_state.data.at[index, "34AFP"] = input_34AFP
                                st.success("AFP Data added successfully.")
                                   
        st.dataframe(st.session_state.data, use_container_width=True)
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

