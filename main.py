import streamlit as st
import pandas as pd
import math
from datetime import datetime

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(
        columns=["Name",
    "MRN",
    "TARE Tx Date",
    "Procedure Technique",
    "Age at time of Tare",
    "Gender",
    "Ethnicity",
    "PMHx Hypertension",
    "PMHx Diabetes (T1 or T2)",
    "Hypercholesterolemia",
    "Hx of Smoking",
    "Obesity",
    "Comorbitieis Total Count",
    "Comorbitieis Binary",
    "Cir_PMH_HBV Status",
    "Cir_PMH_HBV Free Text",
    "Cir_PMH_HBV ART",
    "Cir_PMH_HCV Status",
    "Cir_PMH_HCV Free Text",
    "Cir_PMH_HCV ART",
    "Cir_PMH_Alcohol Use Disorder",
    "Cir_PMH_Duration of Alcohol Use Years",
    "Cir_PMH_Alcohol Free Text",
    "Cir_PMH_IVDU Status",
    "Cir_PMH_Duration of IVDU Years",
    "Cir_PMH_IVDU Free Text",
    "Cir_PMH_Other Contributing Factors",
    "Cirrhosis_Dx_Diagnosis Date",
    "Cirrhosis_Dx_Diagnosis Method",
    "Cirrhosis_Dx_HPI EMR Note Free Text",
    "Cirrhosis_Dx_Imaging Findings EMR Note Free Text",
    "Cirrhosis_Dx_Metavir Score",
    "Cirrhosis_Dx_Complications at Time of Diagnosis",
    "Cirrhosis_Dx_Complications at Time of Diagnosis Binary",
    "Cirrhosis_Dx_Complications Free Text",
    "Cirrhosis_Dx_Date of Labs in Window",
    "Cirrhosis_Dx_AFP",
    "Cirrhosis_Dx_AFP_L3",
    "Cirrhosis_Dx_Child-Pugh Class EMR",
    "Cirrhosis_Dx_Child-Pugh Points EMR",
    "Cirrhosis_Dx_MELD Score EMR",
    "Cirrhosis_Dx_MELD-Na Score EMR",
    "Cirrhosis_Dx_Ascites",
    "Cirrhosis_Dx_Ascites Binary Classification",
    "Cirrhosis_Dx_Ascites Free Text",
    "Cirrhosis_Dx_Ascites Labs Free Text",
    "Cirrhosis_Dx_Hepatic Encephalopathy",
    "HCC_Dx_HCC Diagnosis Date",
    "HCC_Dx_Method of Diagnosis",
    "HCC_Dx_Date of Labs in Window",
    "HCC_Dx_AFP",
    "HCC_Dx_AFP L3 & Date Free Text",
    "HCC_Dx_Bilirubin",
    "HCC_Dx_Albumin",
    "HCC_Dx_INR",
    "HCC_Dx_Creatinine",
    "HCC_Dx_Sodium",
    "HCC_Dx_Ascites",
    "HCC_Dx_Ascites Binary Classification",
    "HCC_Dx_Ascites Free Text",
    "HCC_Dx_Ascites Labs Free Text",
    "HCC_Dx_Hepatic Encephalopathy",
    "HCC_Dx_ECOG Performance Status",
    "HCC_Dx_LIRADS Score",
    "HCC_Dx_Child-Pugh Class EMR",
    "HCC_Dx_Child-Pugh Points EMR",
    "HCC_Dx_BCLC Stage EMR",
    "HCC_Dx_MELD Score EMR",
    "HCC_Dx_MELD-Na Score EMR",
    "HCC_Dx_ALBI Score EMR",
    "HCC_Dx_Child-Pugh Class calc",
    "HCC_Dx_Child-Pugh Points calc",
    "HCC_Dx_BCLC Stage calc",
    "HCC_Dx_MELD Score calc",
    "HCC_Dx_MELD-Na Score calc",
    "HCC_Dx_ALBI Score calc",
    "PRVTHER_Prior LDT Therapy",
    "PRVTHER_Prior RFA Therapy",
    "PRVTHER_Prior TARE Therapy",
    "PRVTHER_Prior SBRT Therapy",
    "PRVTHER_Prior TACE Therapy",
    "PRVTHER_Prior MWA Therapy",
    "PRVTHER_Previous Therapy Sum",
    "PRVTHER_Previous Therapy Date(s)",
    "PRVTHER_Total Recurrences HCC",
    "PRVTHER_Binary for ANY Recurrences HCC Binary",
    "PRVTHER_Location of Previous Treatment HCC",
    "PRVTHER_Recurrence Date/Location Free Text",
    "PRVTHER_New HCC Outside Previous Treatment Site",
    "PRVTHER_New HCC Adjacent to Previous Treatment Site",
    "PRVTHER_Residual HCC",
    "PRVTHER_Systemic Therapy Free Text",
    "PRVTHER_Date of Labs in Window",
    "PRVTHER_AFP",
    "PREY90_symptoms",
    "PREY90_date of labs in window",
    "PREY90_AFP",
    "PRE90_AFP Prior to TARE",
    "PREY90_Bilirubin",
    "PREY90_Albumin",
    "PREY90_inr",
    "PREY90_creatinine",
    "PREY90_sodium",
    "PREY90_AST",
    "PREY90_ALT",
    "PREY90_Alkaline Phosphatase",
    "PREY90_potassium",
    "PREY90_Ascites",
    "PREY90_Ascites Binary Classification",
    "PREY90_Ascites Free Text",
    "PREY90_he",
    "PREY90_ecog",
    "PREY90_Child-Pugh Class Emr",
    "PREY90_Child-Pugh Points Emr",
    "PREY90_BCLC Stage EMR",
    "PREY90_MELD Score EMR",
    "PREY90_MELD-Na Score EMR",
    "PREY90_ALBI Score EMR",
    "PREY90_Child-Pugh Class calc",
    "PREY90_Child-Pugh Points calc",
    "PREY90_BCLC Stage calc",
    "PREY90_MELD Score calc",
    "PREY90_MELD-Na Score calc",
    "PREY90_ALBI Score calc",
    "MY90_date",
    "MY90_Lung_shunt",
    "DAYY90_AFP",
    "DAYY90_AFP Prior to TARE",
    "AFP_PreY90 or DAYY90",
    "DAYY90_sodium",
    "DAYY90_creatinine",
    "DAYY90_inr",
    "DAYY90_albumin",
    "DAYY90_bilirubin",
    "DAYY90_AST",
    "DAYY90_ALT",
    "DAYY90_Alkaline Phosphatase",
    "DAYY90_leukocytes",
    "DAYY90_platelets",
    "DAYY90_ascities",
    "DAYY90_Hepatic Encephalopathy",
    "DAYY90_Child-Pugh class EMR",
    "DAYY90_Child-Pugh points EMR",
    "DAYY90_BCLC EMR",
    "DAYY90_MELD EMR",
    "DAYY90_MELD Na EMR",
    "DAYY90_Albi EMR",
    "PREY90_ECOG",
    "DAYY90_Child-Pugh class Calc",
    "DAYY90_Child-Pugh points calc",
    "DAYY90_BCLC calc",
    "DAYY90_MELD calc",
    "DAYY90_MELD Na calc",
    "DAYY90_Albi calc",
    "DAYY90_Type of Sphere",
    "DAYY90_LT_notes_ftx",
    "ken_ChildPughscore",
    "ken_MELDpreTARE",
    "POSTY90_30DY_date_labs",
    "POSTY90_30DY_afp",
    "POSTY90_30DY_afp DATE",
    "POSTY90_30DY_Sodium",
    "POSTY90_30DY_creatinine",
    "POSTY90_30DY_INR",
    "POSTY90_30DY_albumin",
    "POSTY90_30DY_bilirubin",
    "POSTY90_30DY_AST",
    "POSTY90_30DY_ALT",
    "POSTY90_30DY_Alkaline Phosphatase",
    "POSTY90_30DY_leukocytes",
    "POSTY90_30DY_platelets",
    "POSTY90_30DY_potassium",
    "POSTY90_30DY_ECOG",
    "POSTY90_30DY_Child-Pugh Class EMR",
    "POSTY90_30DY_Child-Pugh Points EMR",
    "POSTY90_30DY_BCLC EMR",
    "POSTY90_30DY_MELD EMR",
    "POSTY90_30DY_MELD Na EMR",
    "POSTY90_30DY_ALBI EMR",
    "POSTY90_30DY_Child-Pugh Class calc",
    "POSTY90_30DY_Child-Pugh Points calc",
    "POSTY90_30DY_BCLC calc",
    "POSTY90_30DY_MELD calc",
    "POSTY90_30DY_MELD Na calc",
    "POSTY90_30DY_ALBI calc",
    "Ken_BCLCStagepost90",
    "Ken_MELD_Stagepost90",
    "30DYAE_CTCAE_portal_htn",
    "30DYAE_CTCAE_Vascular comp",
    "30DYAE_CTCAE_fatigue",
    "30DYAE_CTCAE_diarrhea",
    "30DYAE_CTCAE_hypoalbuminemia emr",
    "30DYAE_CTCAE_hyperbilirubinemia emr",
    "30DYAE_CTCAE_Increase_creatinine emr",
    "30DYAE_CTCAE_abdominal pain",
    "30DYAE_CTCAE_sepsis",
    "30DYAE_CTCAE_ascites",
    "30DYAE_CTCAE_ascites Binary classification",
    "30DYAE_CTCAE_ascites_ftx",
    "30DYAE_CTCAE_bacterial_peritonitis",
    "30DYAE_CTCAE_hemorrhage",
    "30DYAE_CTCAE_anorexia",
    "30DYAE_CTCAE_intrahepatic_fistula",
    "30DYAE_CTCAE_constipation",
    "30DYAE_CTCAE_nausea",
    "30DYAE_CTCAE_vomiting",
    "30DYAE_CTCAE_Hepatic Encephalopathy",
    "30DYAE_CTCAE_he_ftx",
    "30DYAE_CTCAE_cholecystitis",
    "30DYAE_CTCAE_gastric_ulcers",
    "30DYAE_CTCAE_hyperkalemia",
    "30DYAE_CTCAE_respiratory_failure",
    "30DYAE_CTCAE_AKI",
    "30DYAE_CTCAE_Radiation_pneumonitis",
    "30DY_AE_other",
    "90DY_AE_date_of_AE",
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
    "PREY90_ pretx targeted Lesion Dia Sum",
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
    "1st_FU_NEW Extrahepatic Dz Localtion",
    "1st_FU_NEW Extrahepatic Dz Date",
    "1st_FU_% change non target lesion",
    "1st_FU_% Change target dia",
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
    "2nd_FU_NEW Extrahepatic Dz Localtion",
    "2nd_FU_NEW Extrahepatic Dz Date",
    "2nd_FU_% change non target lesion",
    "SECFU_% Change Target Dia",
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
    "3rd_FU_NEW Extrahepatic Dz Localtion",
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
    "4th_FU_NEW Extrahepatic Dz Localtion",
    "4th_FU_NEW Extrahepatic Dz Date",
    "4th_FU_% change non target lesion",
    "4th_FU_% Change target dia",
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
    "FOURTHFU_% Change target dia",
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
    "GTV mean dose",
    "Tx vol mean dose",
    "Healthy Liver mean dose (liver - tx vol)",
    "GTV Vol",
    "Tx vol",
    "Liver vol",
    "Healthy Liver Vol",
    "GTV/ Liver (%)",
    "D98 (Gy)",
    "D90 (Gy)",
    "D95 (Gy)",
    "D80 (Gy)",
    "D70 (Gy)",
    "V100(%)",
    "V200(%)",
    "V300(%)",
    "V400(%)",
    "Activity(Bq)",
    "Activity(Ci)",
    "Tx vol Activity Density (Ci/cc)"]
    )
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
    st.title("Patient Information System")

    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs(["Patient Info", "Patient Demographics", "Cirrhosis PMH","HCC Diagnosis", "Previous Therapy for HCC", "Pre Y90", "Day_Y90", "Post Y90 Within 30 Days Labs"])
    with tab1:
        st.subheader("Patient Information")
        with st.form("patient_info_form"):
            # Patient Info Section
            col1, col2 = st.columns(2)
            last_name = col1.text_input("Last Name")
            first_name = col2.text_input("First Name")
            
            mrn = st.text_input("MRN", help="Enter patient's Medical Record Number")
            
            tare_date = st.date_input("TARE Tx Date", help="Select the treatment date")
            
            procedure_technique = st.selectbox(
                "Procedure Technique",
                options=["Lobar", "Segmental"],
                format_func=lambda x: f"{x} ({1 if x == 'Lobar' else 2})"
            )
            
            age = st.number_input("Age at time of TARE", min_value=0, max_value=150, step=1)
        
            submit_tab1 = st.form_submit_button("Submit Patient Info")
            if submit_tab1:
                if mrn in st.session_state.data["MRN"].values:
                    st.error(f"MRN {mrn} already exists. Please enter a unique MRN.")
                else:
                    st.session_state.data = pd.concat(
                    [st.session_state.data, pd.DataFrame([{
                        "Name": f"{last_name}, {first_name}",
                        "MRN": mrn,
                        "TARE Tx Date": tare_date.strftime("%Y-%m-%d"),
                        "Procedure Technique": procedure_technique,
                        "Age at time of Tare": age
                        } ])], ignore_index=True)
                    st.session_state.temp_mrn = mrn
                    st.success("Patient Information saved. Proceed to Patient Description tab.")
                    st.dataframe(st.session_state.data)
                    #st.dataframe(st.session_state.data)
                   
    with tab2:
        st.subheader("Patient Demographics")
        with st.form("demographics_form"):
            st.subheader("Patient Description")
            if "MRN" not in st.session_state.data:
                st.warning("Please complete the Patient Information tab first.")
            else:
                gender = st.selectbox(
                    "Gender",
                    options=["Male", "Female"],
                    format_func=lambda x: f"{x} ({1 if x == 'Male' else 2})"
                )

                # Ethnicity dropdown
                ethnicity = st.selectbox(
                    "Ethnicity",
                    options=["White", "Asian", "Hispanic", "Other", "NA"],
                    format_func=lambda x: {
                        "White": "White (3)",
                        "Asian": "Asian (4)",
                        "Hispanic": "Hispanic (5)",
                        "Other": "Other (6)",
                        "NA": "NA (can't find information)"
                    }[x]
                )

                # Medical History - Yes/No dropdowns
                st.subheader("Medical History")
                
                hypertension = st.selectbox(
                    "PMHx Hypertension",
                    options=["No", "Yes"],
                    format_func=lambda x: f"{x} ({1 if x == 'Yes' else 0})"
                )

                diabetes = st.selectbox(
                    "PMHx Diabetes (T1 or T2)",
                    options=["No", "Yes"],
                    format_func=lambda x: f"{x} ({1 if x == 'Yes' else 0})"
                )

                hypercholesterolemia = st.selectbox(
                    "Hypercholesterolemia",
                    options=["No", "Yes"],
                    format_func=lambda x: f"{x} ({1 if x == 'Yes' else 0})"
                )

                smoking = st.selectbox(
                    "Hx of Smoking",
                    options=["No", "Yes"],
                    format_func=lambda x: f"{x} ({1 if x == 'Yes' else 0})"
                )

                obesity = st.selectbox(
                    "Obesity",
                    options=["No", "Yes"],
                    format_func=lambda x: f"{x} ({1 if x == 'Yes' else 0})"
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
                submit_tab2 = st.form_submit_button("Submit Patient Description")
                if submit_tab2:
                    index = st.session_state.data[st.session_state.data["MRN"] == st.session_state.temp_mrn].index[0]
                    st.session_state.data.at[index, "Gender"] = gender
                    st.session_state.data.at[index, "Ethnicity"] = ethnicity
                    st.session_state.data.at[index, "PMHx Hypertension"] = hypertension
                    st.session_state.data.at[index, "PMHx Diabetes (T1 or T2)"] = diabetes
                    st.session_state.data.at[index, "Hypercholesterolemia"] = hypercholesterolemia
                    st.session_state.data.at[index, "Hx of Smoking"] = smoking
                    st.session_state.data.at[index, "Obesity"] = obesity
                    st.session_state.data.at[index, "Comorbitieis Total Count"] = total_count
                    st.session_state.data.at[index, "Comorbitieis Binary"] = binary_value
                    st.success("Patient Description added successfully.")
                    st.write("Updated Data:")
                    st.dataframe(st.session_state.data)

    with tab3:
        st.subheader("Cirrhosis PMH")
        with st.form("cirrhosis_pmh_form"):
            
            if "MRN" not in st.session_state.data:
                st.warning("Please complete the Patient Information tab first.")
            else:
            # Cirrhosis PMH Fields
                cir_pmh_hbv_status = st.selectbox(
                    "Cir_PMH_HBV Status",
                    options=["Yes", "No"],
                # format_func=lambda x: f"{x} ({1 if x == 'Yes' else 0})",
                    help="Select HBV Status"
                )

                cir_pmh_hbv_free_text = "0" if cir_pmh_hbv_status == "No" else st.text_input(
                    "Cir_PMH_HBV Free Text",
                    help="Provide additional details for HBV Status"
                )
                
                cir_pmh_hbv_art = "0" if cir_pmh_hbv_status == "No" else st.selectbox(
                    "Cir_PMH_HBV ART",
                    options=["Entecavir", "Tenofovir", "NA"],
                )

                cir_pmh_hcv_status = st.selectbox(
                    "Cir_PMH_HCV Status",
                    options=["Yes", "No"],
                # format_func=lambda x: f"{x} ({1 if x == 'Yes' else 0})",
                    help="Select HCV Status"
                )

                cir_pmh_hcv_free_text = "0" if cir_pmh_hcv_status == "No" else st.text_input(
                    "Cir_PMH_HCV Free Text",
                    help="Provide additional details for HCV Status",
                )

                cir_pmh_hcv_art = "0" if cir_pmh_hcv_status == "No" else st.selectbox(
                    "Cir_PMH_HBV ART",
                    options=["sofosbuvir/velpatasvir", "ledipasvir/sofosbuvir", "NA", "Glecaprevir/pibrentasvi"],
                    help="Select ART treatment for HCV",
            
                )

                cir_pmh_alcohol_use_disorder = st.selectbox( 
                    "Cir_PMH_Alcohol Use Disorder",
                    options=["Yes", "No"],
                    #format_func=lambda x: f"{x} ({1 if x == 'Yes' else 0})",
                    help="Select Alcohol Disorder"
                )

                cir_pmh_duration_of_alcohol_use_years = "0" if cir_pmh_alcohol_use_disorder == "No" else st.number_input(
                    "Cir_PMH_Duration of Alcohol Use Years",
                    help="Provide Duration of Alchohol Use Years",
                )

                cir_pmh_alcohol_free_text = "0" if cir_pmh_alcohol_use_disorder == "No" else st.text_input(
                    "Cir_PMH_HCV Free Text",
                    help="Provide additional details for Alcohol Disorder",
                )

                cir_pmh_ivdu_status = st.selectbox(
                    "Cir_PMH_IVDU Status",
                    options=["Yes", "No"],
                    #format_func=lambda x: f"{x} ({1 if x == 'Yes' else 0})",
                    help="Select IVDU Status"
                )

                cir_pmh_duration_of_ivdu_years = "0" if cir_pmh_ivdu_status == "No" else st.number_input(
                    "Cir_PMH_Duration of IVDU Years",
                    help="Provide Duration of IVDU Disorder",
                )

                cir_pmh_ivdu_free_text = "0" if cir_pmh_ivdu_status == "No" else st.text_input(
                    "Cir_PMH_HCV Free Text",
                    help="Provide additional details for IVDU"
            
                )

                cir_pmh_other_contributing_factors = st.selectbox(
                    "Cir_PMH_Other Contributing Factors",
                    options=["NAFLD", "MAFLD", "NASH", "Autoimmune Hepatitis", "Hereditary Hemochromatosis","none"],
                    help="Select Other Contributing Factors"
                )
        
                st.subheader("Cirrhosis Dx")
                Cirrhosis_Dx_Diagnosis_Date = st.date_input("Cirrhosis_Dx_Diagnosis Date",help="Select Diagnosis date")

                Cirrhosis_Dx_Diagnosis_Method = st.selectbox(
                    "Cirrhosis_Dx_Diagnosis Method",
                    options=["Biopsy", "Imaging"],
                    help="Select Diagnosis Method"
                ) 
                Cirrhosis_Dx_HPI_EMR_Note_Free_Text = st.text_input(
                    "Cirrhosis_Dx_HPI EMR Note Free Text",
                    help="Provide details of HPI EMR"
                )
                Cirrhosis_Dx_Imaging_Findings_EMR_Note_Free_Text = st.text_input(
                    "Cirrhosis_Dx_Imaging Findings EMR Note Free Text",
                    help="Provide details of Imaging Findings"
                )

                Cirrhosis_Dx_Metavir_Score = st.selectbox (
                    "Cirrhosis_Dx_Metavir Score",
                    options=["F0/F1", "F2","F3","F4","NA"],
                    help="Select Metavir_score"
                ) 

                Cirrhosis_Dx_Complications_at_Time_of_Diagnosis = st.multiselect(
                    "Cirrhosis_Dx_Complications at Time of Diagnosis",
                    options=["ascites", " variceal hemorrhage","hepatic encephalopathy","jaundice","SBP", "Hepatorenal Syndrome", "Coagulopathy", "Portal HTN", "PVT", "PVTT", "none"],
                    help="Provide details of Compilications at time of Diagnosis"
                )

                Cirrhosis_Dx_Complications_at_Time_of_Diagnosis_Binary = st.selectbox(
                    "Cirrhosis_Dx_Complications at Time of Diagnosis Binary",
                    options=["0","1"],
                    format_func=lambda x: {
                        "1": " >1 ",
                        "0": "None",
                    }[x],
                    help="Provide details of Complications_at_Time_of_Diagnosis_Binary"
                )

                Cirrhosis_Dx_Complications_Free_Text =  st.text_input(
                    "Cirrhosis_Dx_Complications Free Text",
                    help="Provide details of Complications"
                )

                Cirrhosis_Dx_Date_of_Labs_in_Window = st.date_input(" Cirrhosis_Dx_Date of Labs in Window",help="Select the date of lab test")

                Cirrhosis_Dx_AFP = st.text_input(
                    "Cirrhosis_Dx_AFP",
                    help="Enter AFP value in ng/dl"
                    
                )

                Cirrhosis_Dx_AFP_L3 = st.text_input(
                    "Cirrhosis_Dx_AFP_L3",
                    help="Enter AFP_L3 value in ng/dl"
                    
                )

                Cirrhosis_Dx_Child_Pugh_class_EMR = st.selectbox(
                    "Cirrhosis_Dx_Child-Pugh Class EMR",
                    options=["Class A","Class B","Class C","NA"]

                )
                
                    
                # Validation for Cirrhosis_Dx_Child-Pugh Points EMR
                def validate_input(value):
                    if value.isdigit() and 5 <= int(value) <= 15:
                        return value  # Valid number
                    elif value.upper() == "NA":
                        return "NA"  # Valid 'NA'
                    else:
                        return "NA" 

                input_value = st.text_input(
                    "Cirrhosis_Dx_Child-Pugh Points EMR",
                    help="Specify the Child-Pugh points if in EMR 'number 5-15 or NA"                
                )

                Cirrhosis_Dx_Child_Pugh_Points_EMR = validate_input(input_value)

    # Validation for MELD Score EMR

                def validate_input_EMR(value):
                    if value.isdigit() and 6 <= int(value) <= 40:
                        return value  # Valid number
                    elif value.upper() == "NA":
                        return "NA"  # Valid 'NA'
                    else:
                        return "NA" 
                                
                input_value1 = st.text_input(
                    "Cirrhosis_Dx_MELD Score EMR",
                    help="Specify the MELD Score if in EMR 'number 6-40 or NA"                
                )

                Cirrhosis_Dx_MELD_Score_EMR = validate_input_EMR(input_value1)

                input_value2 = st.text_input(
                    "Cirrhosis_Dx_MELD-NA_Score_EMR",
                    help="Specify the MELD Score NA if in EMR 'number 6-40 or NA"                
                )

                Cirrhosis_Dx_MELD_NA_Score_EMR = validate_input_EMR(input_value2)

                Cirrhosis_Dx_Ascites = st.selectbox (
                    "Cirrhosis_Dx_Ascites",
                    options=["none", "Asymptomatic","Minimal ascities/Mild abd distension","Symptomatic"," moderate ascities/Symptomatic medical intervention", "Severe symptoms, invasive intervention indicated", "Life Threatening: Urgent operation intervention indicated"],
                    help="Select Metavir_score"
                ) 

                Cirrhosis_Dx_Ascites_Binary_Classification = "NA" if Cirrhosis_Dx_Ascites == "none" else st.selectbox(
                    "Cirrhosis_Dx_Ascites_Binary_Classification",
                    options=["0","1"],
                    format_func=lambda x: {
                        "1": " Other than 1 ",
                        "0": "None",
                    }[x],
                
                )
                
                Cirrhosis_Dx_Ascites_Free_Text = "NA" if Cirrhosis_Dx_Ascites == "none" else st.text_area(
                    "Cirrhosis_Dx_Ascites Free Text",
                    "Hospitalized (yes/no): \nDiuretics (yes/no): \nParacentesis (yes/no): \nAny other complications (free_text):",
                
                )

                Cirrhosis_Dx_Ascites_Labs_Free_Text = "NA" if Cirrhosis_Dx_Ascites == "none" else st.text_area(
                    "Cirrhosis_Dx_Ascites Labs Free Text",
                    "Bilirubin (mg/dl): \nAlbumin (g/dl): \nINR: \nCreatinine (mg/dl): \nSodium (mmol/L): \nAST (U/L): \nALT (U/L): \nAlk Phos: \nPlatelets:",
                    
                )

                Cirrhosis_Dx_Hepatic_Encephalopathy = st.selectbox(
                    "Cirrhosis_Dx_Hepatic_Encephalopathy",
                    options=["Yes", "No"],
                    #format_func=lambda x: f"{x} ({1 if x == 'Yes' else 0})",
                    help="Hepatic_Encephalopathy"
            
                )

                submit_tab3 = st.form_submit_button("Submit Cirrhosis PMH")
                if submit_tab3:

                    index = st.session_state.data[st.session_state.data["MRN"] == st.session_state.temp_mrn].index[0]
                    st.session_state.data.at[index, "Cir_PMH_HBV Status"] = cir_pmh_hbv_status
                    st.session_state.data.at[index, "Cir_PMH_HBV Free Text"] = cir_pmh_hbv_free_text
                    st.session_state.data.at[index, "Cir_PMH_HBV ART"] = cir_pmh_hbv_art
                    st.session_state.data.at[index, "Cir_PMH_HCV Status"] = cir_pmh_hcv_status
                    st.session_state.data.at[index, "Cir_PMH_HCV Free Text"] = cir_pmh_hcv_free_text
                    st.session_state.data.at[index, "Cir_PMH_HCV ART"] = cir_pmh_hcv_art
                    st.session_state.data.at[index, "Cir_PMH_Alcohol Use Disorder"] = cir_pmh_alcohol_use_disorder
                    st.session_state.data.at[index, "Cir_PMH_Duration of Alcohol Use Years"] = cir_pmh_duration_of_alcohol_use_years
                    st.session_state.data.at[index, "Cir_PMH_Alcohol Free Text"] = cir_pmh_alcohol_free_text
                    st.session_state.data.at[index, "Cir_PMH_IVDU Status"] = cir_pmh_ivdu_status
                    st.session_state.data.at[index, "Cir_PMH_Duration of IVDU Years"] = cir_pmh_duration_of_ivdu_years
                    st.session_state.data.at[index, "Cir_PMH_IVDU Free Text"] = cir_pmh_ivdu_free_text
                    st.session_state.data.at[index, "Cir_PMH_Other Contributing Factors"] = cir_pmh_other_contributing_factors
                    st.session_state.data.at[index, "Cirrhosis_Dx_Diagnosis Date"] = Cirrhosis_Dx_Diagnosis_Date
                    st.session_state.data.at[index, "Cirrhosis_Dx_Diagnosis Method"] = Cirrhosis_Dx_Diagnosis_Method
                    st.session_state.data.at[index, "Cirrhosis_Dx_HPI EMR Note Free Text"] = Cirrhosis_Dx_HPI_EMR_Note_Free_Text
                    st.session_state.data.at[index, "Cirrhosis_Dx_Imaging Findings EMR Note Free Text"] = Cirrhosis_Dx_Imaging_Findings_EMR_Note_Free_Text
                    st.session_state.data.at[index, "Cirrhosis_Dx_Metavir Score"] = Cirrhosis_Dx_Metavir_Score
                    st.session_state.data.at[index, "Cirrhosis_Dx_Complications at Time of Diagnosis"] = Cirrhosis_Dx_Complications_at_Time_of_Diagnosis
                    st.session_state.data.at[index, "Cirrhosis_Dx_Complications at Time of Diagnosis Binary"] = Cirrhosis_Dx_Complications_at_Time_of_Diagnosis_Binary
                    st.session_state.data.at[index, "Cirrhosis_Dx_Complications Free Text"] = Cirrhosis_Dx_Complications_Free_Text
                    st.session_state.data.at[index, "Cirrhosis_Dx_Date of Labs in Window"] = Cirrhosis_Dx_Date_of_Labs_in_Window
                    st.session_state.data.at[index, "Cirrhosis_Dx_AFP"] = Cirrhosis_Dx_AFP
                    st.session_state.data.at[index, "Cirrhosis_Dx_AFP_L3"] = Cirrhosis_Dx_AFP_L3
                    st.session_state.data.at[index, "Cirrhosis_Dx_Child-Pugh Class EMR"] = Cirrhosis_Dx_Child_Pugh_class_EMR
                    st.session_state.data.at[index, "Cirrhosis_Dx_Child-Pugh Points EMR"] = Cirrhosis_Dx_Child_Pugh_Points_EMR
                    st.session_state.data.at[index, "Cirrhosis_Dx_MELD Score EMR"] = Cirrhosis_Dx_MELD_Score_EMR
                    st.session_state.data.at[index, "Cirrhosis_Dx_MELD-Na Score EMR"] = Cirrhosis_Dx_MELD_NA_Score_EMR
                    st.session_state.data.at[index, "Cirrhosis_Dx_Ascites"] = Cirrhosis_Dx_Ascites
                    st.session_state.data.at[index, "Cirrhosis_Dx_Ascites Binary Classification"] = Cirrhosis_Dx_Ascites_Binary_Classification
                    st.session_state.data.at[index, "Cirrhosis_Dx_Ascites Free Text"] = Cirrhosis_Dx_Ascites_Free_Text
                    st.session_state.data.at[index, "Cirrhosis_Dx_Ascites Labs Free Text"] = Cirrhosis_Dx_Ascites_Labs_Free_Text
                    st.session_state.data.at[index, "Cirrhosis_Dx_Hepatic Encephalopathy"] = Cirrhosis_Dx_Hepatic_Encephalopathy
                    
                    st.success("Patient Description added successfully.")
                    st.write("Updated Data:")
                    st.dataframe(st.session_state.data)

    with tab4:
        st.subheader("HCC Diagnosis")
        with st.form("hcc_dx_form"): 
            if "MRN" not in st.session_state.data:
                st.warning("Please complete the Patient Information tab first.")
            else:
                hcc_dx_hcc_diagnosis_date = st.date_input("HCC_Dx_HCC Diagnosis Date", help="Enter the HCC diagnosis date")

                hcc_dx_method_of_diagnosis = st.selectbox(
                    "HCC_Dx_Method of Diagnosis",   
                    options=["Biopsy", "Imaging", "Unknown"],
                    #format_func=lambda x: f"{x} ({1 if x == 'Biopsy' else 2 if x == 'Imaging' else 'NA'})"
                )

                hcc_dx_date_of_labs = st.date_input("HCC_Dx_Date of Labs in Window")

                hcc_dx_afp = st.number_input("HCC_Dx_AFP", help="Enter AFP value in ng/dl")
                hcc_dx_afp_l3_date_free_text = st.text_area("HCC_Dx_AFP L3 & Date Free Text", help="Enter AFP L3 and date details")

                hcc_dx_bilirubin = st.number_input("HCC_Dx_Bilirubin", help="Enter the bilirubin value in mg/dl", min_value=1)
                hcc_dx_albumin = st.number_input("HCC_Dx_Albumin", help="Enter the albumin value in g/dl")
                hcc_dx_inr = st.number_input("HCC_Dx_INR", help="Enter the INR value")
                hcc_dx_creatinine = st.number_input("HCC_Dx_Creatinine", help="Enter the creatinine value in mg/dl")
                hcc_dx_sodium = st.number_input("HCC_Dx_Sodium", help="Enter the sodium value in mmol/L")

                hcc_dx_ascites = st.selectbox(
                    "HCC_Dx_Ascites",
                    options=["none", "Asymptomatic", "Minimal ascities/Mild abd distension, no sx",
                            "Symptomatic", "moderate ascities/Symptomatic medical intervention",
                            "Severe symptoms, invasive intervention indicated",
                            "Life Threatening: Urgent operation intervention indicated"]
                )

                hcc_dx_ascites_binary_classification = 1 if hcc_dx_ascites != "none" else 0
                #st.info(f"HCC_Dx_Ascites Binary Classification: {ascites_binary}")

                hcc_dx_ascites_free_text = "NA" if hcc_dx_ascites == 'none' else st.text_area(
                    "HCC_Dx_Ascites Free Text",
                    "Hospitalized (yes/no): \nDiuretics (yes/no): \nParacentesis (yes/no): \nAny other complications (free_text):",
                    
                )

                hcc_dx_ascites_labs_free_text = "NA" if hcc_dx_ascites == 'none' else st.text_area(
                    "HCC_Dx_Ascites Labs Free Text",
                    """Bilirubin (mg/dl): \nAlbumin (g/dl): \nINR: \nCreatinine (mg/dl): \nSodium (mmol/L): 
                    AST (U/L): \nALT (U/L): \nAlk Phos: \nPlatelets:""",
            
                )

                hcc_dx_hepatic_encephalopathy = st.selectbox(
                    "HCC_Dx_Hepatic Encephalopathy",
                    options=["Yes", "No"],
                    #format_func=lambda x: f"{x} ({1 if x == 'Yes' else 0})"
                )

                hcc_dx_ecog_performance_status = st.selectbox("HCC_Dx_ECOG Performance Status", options=["0", "1", "2", "3", "4", "NA"])

                hcc_dx_lirads_score = st.selectbox(
                    "HCC_Dx_LIRADS Score",
                    options=["LR-1", "LR-2", "LR-3", "LR-4", "LR-5", "LR-5V", "LR-M"]
                )

                hcc_dx_child_pugh_class_emr = st.selectbox(
                    "HCC_Dx_Child-Pugh Class EMR",
                    options=["Class A", "Class B", "Class C", "NA"]
                )

                # Validation of hcc_dx_child_pugh_points_emr

                def validate_input(value):
                    if value.isdigit() and 5 <= int(value) <= 15:
                        return value  # Valid number
                    elif value.upper() == "NA":
                        return "NA"  # Valid 'NA'
                    else:
                        return "NA" 

                input_value3 = st.text_input(
                    "HCC_Dx_Child-Pugh Points EMR",
                    help="Specify the Child-Pugh points if in EMR number 5-15 or NA"                
                )

                hcc_dx_child_pugh_points_emr = validate_input(input_value3)


                hcc_dx_bclc_stage_emr = st.selectbox(
                    "HCC_Dx_BCLC Stage EMR",
                    options=["0", "A", "B", "C", "D"]
                )

                # Validating hcc_dx_meld/na score
                def validate_input2(value):
                    if value.isdigit() and 6 <= int(value) <= 40:
                        return value  # Valid number
                    elif value.upper() == "NA":
                        return "NA"  # Valid 'NA'
                    else:
                        return "NA" 

                input_value4 = st.text_input(
                    "HCC_Dx_MELD Score EMR",
                    help="Write in number in range 6-40, or NA"
                )

                hcc_dx_meld_score_emr = validate_input2(input_value4)

                input_value5 = st.text_input(
                    "HCC_Dx_MELD-Na Score EMR",
                    help="Write in number in range 6-40, or NA"
                )

                hcc_dx_meld_na_score_emr = validate_input2(input_value5)

                hcc_dx_albi_score_emr = st.number_input("HCC_Dx_ALBI Score EMR")

                #  calculation of child_pugh_points_clac

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

                hcc_dx_child_pugh_points_calc = calculatepoints(hcc_dx_bilirubin,hcc_dx_albumin,hcc_dx_inr,hcc_dx_ascites,hcc_dx_hepatic_encephalopathy)

                # Calculations for classses

                def calculate_class(poin):
                    if 5 <= poin <= 6:
                        return 'A'
                    elif 7 <= poin <= 9:
                        return 'B'
                    elif 10 <= poin <= 15:
                        return 'C'
                    else:
                        return "Invalid points: must be between 5 and 15."
        
                hcc_dx_child_pugh_class_calc = calculate_class(hcc_dx_child_pugh_points_calc)
            
                #bclc_stage_calc = st.text_input("HCC_Dx_BCLC Stage calc")
                hcc_dx_meld_score_calc = (3.78*(int(hcc_dx_bilirubin)))+(11.2*(int(hcc_dx_inr)))+(9.57*(int(hcc_dx_creatinine)))+6.43
                hcc_dx_meld_na_score_calc = hcc_dx_meld_score_calc + 1.32*(137-int(hcc_dx_sodium)) - (0.033*hcc_dx_meld_score_calc*(137-int(hcc_dx_sodium)))
                def albi_calc(a,b):
                    a=int(a)
                    b=int(b)
                    t = math.log(a, 10)
                    answer = (t * 0.66) + (b * -0.085)
                    return answer
                
                hcc_dx_albi_score_calc = albi_calc(hcc_dx_bilirubin, hcc_dx_albumin)
            

                submit_tab4 = st.form_submit_button("Save HCC Diagnosis")
                if submit_tab4:
                        index = st.session_state.data[st.session_state.data["MRN"] == st.session_state.temp_mrn].index[0]
                        st.session_state.data.at[index, "HCC_Dx_HCC Diagnosis Date"] = hcc_dx_hcc_diagnosis_date.strftime("%Y-%m-%d")
                        st.session_state.data.at[index, "HCC_Dx_Method of Diagnosis"] = hcc_dx_method_of_diagnosis
                        st.session_state.data.at[index, "HCC_Dx_Date of Labs in Window"] = hcc_dx_date_of_labs.strftime("%Y-%m-%d")
                        st.session_state.data.at[index, "HCC_Dx_AFP"] = hcc_dx_afp
                        st.session_state.data.at[index, "HCC_Dx_AFP L3 & Date Free Text"] = hcc_dx_afp_l3_date_free_text
                        st.session_state.data.at[index, "HCC_Dx_Bilirubin"] = hcc_dx_bilirubin
                        st.session_state.data.at[index, "HCC_Dx_Albumin"] = hcc_dx_albumin
                        st.session_state.data.at[index, "HCC_Dx_INR"] = hcc_dx_inr
                        st.session_state.data.at[index, "HCC_Dx_Creatinine"] = hcc_dx_creatinine
                        st.session_state.data.at[index, "HCC_Dx_Sodium"] = hcc_dx_sodium
                        st.session_state.data.at[index, "HCC_Dx_Ascites"] = hcc_dx_ascites
                        st.session_state.data.at[index, "HCC_Dx_Ascites Binary Classification"] = hcc_dx_ascites_binary_classification
                        st.session_state.data.at[index, "HCC_Dx_Ascites Free Text"] = hcc_dx_ascites_free_text
                        st.session_state.data.at[index, "HCC_Dx_Ascites Labs Free Text"] = hcc_dx_ascites_labs_free_text
                        st.session_state.data.at[index, "HCC_Dx_Hepatic Encephalopathy"] = hcc_dx_hepatic_encephalopathy
                        st.session_state.data.at[index, "HCC_Dx_ECOG Performance Status"] = hcc_dx_ecog_performance_status
                        st.session_state.data.at[index, "HCC_Dx_LIRADS Score"] = hcc_dx_lirads_score
                        st.session_state.data.at[index, "HCC_Dx_Child-Pugh Class EMR"] = hcc_dx_child_pugh_class_emr
                        st.session_state.data.at[index, "HCC_Dx_Child-Pugh Points EMR"] = hcc_dx_child_pugh_points_emr
                        st.session_state.data.at[index, "HCC_Dx_BCLC Stage EMR"] = hcc_dx_bclc_stage_emr
                        st.session_state.data.at[index, "HCC_Dx_MELD Score EMR"] = hcc_dx_meld_score_emr
                        st.session_state.data.at[index, "HCC_Dx_MELD-Na Score EMR"] = hcc_dx_meld_na_score_emr
                        st.session_state.data.at[index, "HCC_Dx_ALBI Score EMR"] = hcc_dx_albi_score_emr
                        st.session_state.data.at[index, "HCC_Dx_Child-Pugh Class calc"] = hcc_dx_child_pugh_class_calc
                        st.session_state.data.at[index, "HCC_Dx_Child-Pugh Points calc"] = hcc_dx_child_pugh_points_calc
                        st.session_state.data.at[index, "HCC_Dx_MELD Score calc"] = hcc_dx_meld_score_calc
                        st.session_state.data.at[index, "HCC_Dx_MELD-Na Score calc"] = hcc_dx_meld_na_score_calc
                        st.session_state.data.at[index, "HCC_Dx_ALBI Score calc"] = hcc_dx_albi_score_calc

                        st.success("HCC Dx added successfully.")
                        st.write("Updated Data:")
                        st.dataframe(st.session_state.data)
  
    with tab5:
        if "MRN" not in st.session_state.data:
                st.warning("Please complete the Patient Information tab first.")
        else:
            st.subheader("Previous Therapy for HCC")
            with st.form("previous_therapy_form"):

                PRVTHER_Prior_LDT_Therapy = st.selectbox(
                    "PRVTHER_Prior_LDT_Therapy",
                    options=["Yes", "No","NA"],
                    #format_func=lambda x: f"{x} ({1 if x == 'Yes' else 0})",
                    help="Prior LDT Therapy"
                )
                PRVTHER_Prior_RFA_Therapy = st.selectbox(
                    "PRVTHER_Prior RFA Therapy",
                    options=["Yes", "No", "NA"],
                    #format_func=lambda x: f"{x} ({1 if x == 'Yes' else 0})",
                    help="Prior RFA Therapy"
                )
            
                PRVTHER_Prior_TARE_Therapy = st.selectbox(
                    "PRVTHER_Prior TARE Therapy",
                    options=["Yes", "No","NA"],
                    #format_func=lambda x: f"{x} ({1 if x == 'Yes' else 0})",
                    help="Prior TARE Therapy"
                )
            
                PRVTHER_Prior_SBRT_Therapy = st.selectbox(
                    "PRVTHER_Prior SBRT Therapy",
                    options=["Yes", "No","NA"],
                    #format_func=lambda x: f"{x} ({1 if x == 'Yes' else 0})",
                    help="Prior SBRT Therapy"
                )
            
                PRVTHER_Prior_TACE_Therapy = st.selectbox(
                    "PRVTHER_Prior TACE Therapy",
                    options=["Yes", "No","NA"],
                    #format_func=lambda x: f"{x} ({1 if x == 'Yes' else 0})",
                    help="Prior TACE Therapy"
                )
                PRVTHER_Prior_MWA_Therapy = st.selectbox(
                    "PRVTHER_Prior MWA Therapy",
                    options=["Yes", "No","NA"],
                    #format_func=lambda x: f"{x} ({1 if x == 'Yes' else 0})",
                    help="Prior MWA Therapy"
                )

                list1=[PRVTHER_Prior_LDT_Therapy, PRVTHER_Prior_RFA_Therapy, PRVTHER_Prior_TARE_Therapy, PRVTHER_Prior_SBRT_Therapy, PRVTHER_Prior_TACE_Therapy, PRVTHER_Prior_MWA_Therapy]
                sum=0
                for item in list1:
                    if item == "Yes" :
                        sum+=1
                    else:
                        continue
                
                PRVTHER_Previous_Therapy_Sum = sum

            # PRVTHER_Previous_Therapy_Sum = PRVTHER_Prior_LDT_Therapy + PRVTHER_Prior_RFA_Therapy + PRVTHER_Prior_TARE_Therapy + PRVTHER_Prior_SBRT_Therapy + PRVTHER_Prior_TACE_Therapy + PRVTHER_Prior_MWA_Therapy

                PRVTHER_Previous_Therapy_Dates = st.text_area(
                "PRVTHER_Previous Therapy Date(s) ",
                help=" Enter previous therapy date or NA"
                )

                PRVTHER_Total_Recurrences_HCC = st.selectbox(
                    "PRVTHER_Total Recurrences HCC",
                    options=["0","1","2","3","4","NA"],
                    help="select total recurrences of HCC"
                )
            
                PRVTHER_Binary_for_ANY_Recurrences_HCC_Binary = 1 if PRVTHER_Previous_Therapy_Sum == "YES" or PRVTHER_Prior_LDT_Therapy == "Yes" or PRVTHER_Prior_RFA_Therapy == "Yes" or PRVTHER_Prior_TARE_Therapy == "Yes" or PRVTHER_Prior_SBRT_Therapy == "Yes" or PRVTHER_Prior_TACE_Therapy == "Yes" or PRVTHER_Prior_MWA_Therapy == "Yes" else 0

                PRVTHER_Location_of_Previous_Treatment_HCC = st.text_input(
                    "PRVTHER_Location of Previous Treatment HCC",
                    help="Provide Location of Previous HCC treatment"
                )

                PRVTHER_Recurrence_Date_Location_Free_Text = st.text_input(
                    "PRVTHER_Recurrence Date/Location Free Text",
                    help="Provide Date and Location on Recurrence"
                )   
                PRVTHER_New_HCC_Outside_Previous_Treatment_Site = st.text_input(
                    "PRVTHER_New HCC Outside Previous Treatment Site",
                    help="new HCC occurrence that has developed in a diff location in the liver, separate from the area that was previously tx"
                )   
                PRVTHER_New_HCC_Adjacent_to_Previous_Treatment_Site = st.text_input(
                    "PRVTHER_New HCC Adjacent to Previous Treatment Site",
                    help=" new HCC occurrence that has developed close to, but not directly in, the area that was previously treated"
                )   
                PRVTHER_Residual_HCC = st.text_input(
                    "PRVTHER_Residual HCC",
                    help="Provide information of Residual HCC"
                ) 

                PRVTHER_Systemic_Therapy_Free_Text = st.selectbox(
                    "PRVTHER_Systemic Therapy Free Text",
                    options=["Yes", "No","NA"],
                    #format_func=lambda x: f"{x} ({1 if x == 'Yes' else 0})",
                    help="Prior TACE Therapy"
                )

                PRVTHER_Date_of_Labs_in_Window = st.date_input(
                    "PRVTHER_Date of Labs in Window",
                    help="select date of labs in window"
                )

                PRVTHER_AFP = st.text_input(
                    "PRVTHER_AFP",
                    help="Enter AFP value in ng/dl or NA"
                )

                submit_tab5 = st.form_submit_button("Submit Previous Therapy Form")

                if submit_tab5:
                        index = st.session_state.data[st.session_state.data["MRN"] == st.session_state.temp_mrn].index[0]
                        st.session_state.data.at[index, "PRVTHER_Prior LDT Therapy"] = PRVTHER_Prior_LDT_Therapy
                        st.session_state.data.at[index, "PRVTHER_Prior RFA Therapy"] = PRVTHER_Prior_RFA_Therapy
                        st.session_state.data.at[index, "PRVTHER_Prior TARE Therapy"] = PRVTHER_Prior_TARE_Therapy
                        st.session_state.data.at[index, "PRVTHER_Prior SBRT Therapy"] = PRVTHER_Prior_SBRT_Therapy
                        st.session_state.data.at[index, "PRVTHER_Prior TACE Therapy"] = PRVTHER_Prior_TACE_Therapy
                        st.session_state.data.at[index, "PRVTHER_Prior MWA Therapy"] = PRVTHER_Prior_MWA_Therapy
                        st.session_state.data.at[index, "PRVTHER_Previous Therapy Sum"] = PRVTHER_Previous_Therapy_Sum
                        st.session_state.data.at[index, "PRVTHER_Previous Therapy Date(s) "] = PRVTHER_Previous_Therapy_Dates
                        st.session_state.data.at[index, "PRVTHER_Total Recurrences HCC"] = PRVTHER_Total_Recurrences_HCC
                        st.session_state.data.at[index, "PRVTHER_Binary for ANY Recurrences HCC Binary"] = PRVTHER_Binary_for_ANY_Recurrences_HCC_Binary
                        st.session_state.data.at[index, "PRVTHER_Location of Previous Treatment HCC"] = PRVTHER_Location_of_Previous_Treatment_HCC
                        st.session_state.data.at[index, "PRVTHER_Recurrence Date/Location Free Text"] = PRVTHER_Recurrence_Date_Location_Free_Text
                        st.session_state.data.at[index, "PRVTHER_New HCC Outside Previous Treatment Site"] = PRVTHER_New_HCC_Outside_Previous_Treatment_Site
                        st.session_state.data.at[index, "PRVTHER_New HCC Adjacent to Previous Treatment Site"] = PRVTHER_New_HCC_Adjacent_to_Previous_Treatment_Site
                        st.session_state.data.at[index, "PRVTHER_Residual HCC"] = PRVTHER_Residual_HCC
                        st.session_state.data.at[index, "PRVTHER_Systemic Therapy Free Text"] = PRVTHER_Systemic_Therapy_Free_Text
                        st.session_state.data.at[index, "PRVTHER_Date of Labs in Window"] = PRVTHER_Date_of_Labs_in_Window
                        st.session_state.data.at[index, "PRVTHER_AFP"] = PRVTHER_AFP
                        
                        st.success("Previous Therapy for HCC added successfully.")
                        st.write("Updated Data:")
                        st.dataframe(st.session_state.data)

    with tab6:
        if "MRN" not in st.session_state.data:
                st.warning("Please complete the Patient Information tab first.")
        else:
            st.subheader("Pre Y90")
            with st.form("pre_y90_form"):
                # Fields for Pre Y90
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
                    help="Select all that apply"
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
                
                prey90_ascites = st.selectbox(
                    "PREY90_Ascites",
                    options=[
                        "none", 
                        "Asymptomatic", 
                        "Minimal ascities/Mild abd distension, no sx", 
                        "Symptomatic", 
                        "moderate ascities/Symptomatic medical intervention", 
                        "Severe symptoms, invasive intervention indicated", 
                        "Life Threatening: Urgent operation intervention indicated"
                    ],
                    help="Select the appropriate ascites classification"
                )
                
                prey90_ascites_binary = 1 if prey90_ascites != "none" else 0
                st.info(f"PREY90_Ascites Binary Classification: {prey90_ascites_binary}")
                
                prey90_ascites_free_text = st.text_area(
                    "PREY90_Ascites Free Text",
                    "Hospitalized (yes/no): \nDiuretics (yes/no): \nParacentesis (yes/no): \nAny other complications (free_text):",
                    help="Provide details about hospitalization, diuretics, paracentesis, and other complications"
                )
                
                prey90_he = st.selectbox(
                    "PREY90_he", 
                    options=["No", "Yes", "NA (not in chart)"], 
                    help="Select hepatic encephalopathy status"
                )
                
                prey90_ecog = st.selectbox(
                    "PREY90_ecog",
                    options=["0", "1", "2", "3", "4", "NA"],
                    help="Select ECOG Performance Status"
                )
                
                prey90_child_pugh_class = st.selectbox(
                    "PREY90_Child-Pugh Class Emr",
                    options=["Class A", "Class B", "Class C", "NA"],
                    help="Select the Child-Pugh class"
                )
                def validate_inputt(value):
                    if value.isdigit() and 5 <= int(value) <= 15:
                        return value  # Valid number
                    elif value.upper() == "NA":
                        return "NA"  # Valid 'NA'
                    else:
                        return "NA" 

                input_value3t = st.text_input(
                    "PREY90_Child-Pugh Points Emr",
                    help="Write in number in range 5-15, or NA"              
                )

                prey90_child_pugh_points = validate_inputt(input_value3t)

                prey90_bclc_stage = st.selectbox(
                    "PREY90_BCLC Stage EMR",
                    options=["0", "A", "B", "C", "D"],
                    help="Select the BCLC stage"
                )

                def validate_input2t(value):
                    if value.isdigit() and 6 <= int(value) <= 40:
                        return value  # Valid number
                    elif value.upper() == "NA":
                        return "NA"  # Valid 'NA'
                    else:
                        return "NA" 

                input_value4t = st.text_input(
                    "PREY90_MELD Score EMR",
                    help="Write in number in range 6-40, or NA"                
                )

                prey90_meld_score = validate_input2t(input_value4t)

                input_value5t = st.text_input(
                    "PREY90_MELD-Na Score EMR",
                    help="Write in number in range 6-40, or NA"               
                )

                prey90_meld_na_score = validate_input2t(input_value5t)
                
                prey90_albi_score = st.text_input(
                    "PREY90_ALBI Score EMR",
                    help="Enter ALBI score"
                )
                
                # Claculation of class and points
                prey90_child_pugh_points_calc = calculatepoints(prey90_bilirubin,prey90_albumin,prey90_inr,prey90_ascites,prey90_he)
        
                prey90_child_pugh_class_calc = calculate_class(prey90_child_pugh_points_calc)
                # Additional Calculated Fields
                
                #prey90_bclc_stage_calc = st.text_input("PREY90_BCLC Stage calc", help="Enter calculated BCLC stage")
                prey90_meld_score_calc = (3.78*(int(prey90_bilirubin)))+(11.2*(int(prey90_inr)))+(9.57*(int(prey90_creatinine)))+6.43
                prey90_meld_na_score_calc = prey90_meld_score_calc + 1.32*(137-int(prey90_sodium)) - (0.033*prey90_meld_score_calc*(137-int(prey90_sodium)))
                
                prey90_albi_score_calc = albi_calc(prey90_bilirubin,prey90_albumin)
            
                st.subheader("Mapping Y90")
                my90_date = st.date_input("MY90_date", help="Enter the date")
                my90_lung_shunt = st.number_input("MY90_Lung_shunt", min_value=0, step=1, help="Enter the lung shunt value")

                submit_tab4 = st.form_submit_button("Save Pre Y90")

                if submit_tab4:
                    index = st.session_state.data[st.session_state.data["MRN"] == st.session_state.temp_mrn].index[0]

                    st.session_state.data.at[index, "PREY90_symptoms"] = prey90_symptoms
                    st.session_state.data.at[index, "PREY90_date of labs in window"] = prey90_date_of_labs.strftime("%Y-%m-%d")
                    st.session_state.data.at[index, "PREY90_AFP"] = prey90_afp
                    st.session_state.data.at[index, "PRE90_AFP Prior to TARE"] = prey90_afp_prior_to_tare
                    st.session_state.data.at[index, "PREY90_Bilirubin"] = prey90_bilirubin
                    st.session_state.data.at[index, "PREY90_Albumin"] = prey90_albumin
                    st.session_state.data.at[index, "PREY90_inr"] = prey90_inr
                    st.session_state.data.at[index, "PREY90_creatinine"] = prey90_creatinine
                    st.session_state.data.at[index, "PREY90_sodium"] = prey90_sodium
                    st.session_state.data.at[index, "PREY90_AST"] = prey90_ast
                    st.session_state.data.at[index, "PREY90_ALT"] = prey90_alt
                    st.session_state.data.at[index, "PREY90_Alkaline Phosphatase"] = prey90_alkaline_phosphatase
                    st.session_state.data.at[index, "PREY90_potassium"] = prey90_potassium
                    st.session_state.data.at[index, "PREY90_Ascites"] = prey90_ascites
                    st.session_state.data.at[index, "PREY90_Ascites Binary Classification"] = prey90_ascites_binary
                    st.session_state.data.at[index, "PREY90_Ascites Free Text"] = prey90_ascites_free_text
                    st.session_state.data.at[index, "PREY90_he"] = prey90_he
                    st.session_state.data.at[index, "PREY90_ecog"] = prey90_ecog
                    st.session_state.data.at[index, "PREY90_Child-Pugh Class Emr"] = prey90_child_pugh_class
                    st.session_state.data.at[index, "PREY90_Child-Pugh Points Emr"] = prey90_child_pugh_points
                    st.session_state.data.at[index, "PREY90_BCLC Stage EMR"] = prey90_bclc_stage
                    st.session_state.data.at[index, "PREY90_MELD Score EMR"] = prey90_meld_score
                    st.session_state.data.at[index, "PREY90_MELD-Na Score EMR"] = prey90_meld_na_score
                    st.session_state.data.at[index, "PREY90_ALBI Score EMR"] = prey90_albi_score
                    st.session_state.data.at[index, "PREY90_Child-Pugh Class calc"] = prey90_child_pugh_class_calc
                    st.session_state.data.at[index, "PREY90_Child-Pugh Points calc"] = prey90_child_pugh_points_calc
                    st.session_state.data.at[index, "PREY90_MELD Score calc"] = prey90_meld_score_calc
                    st.session_state.data.at[index, "PREY90_MELD-Na Score calc"] = prey90_meld_na_score_calc
                    st.session_state.data.at[index, "PREY90_ALBI Score calc"] = prey90_albi_score_calc
                    st.session_state.data.at[index, "MY90_date"] = my90_date
                    st.session_state.data.at[index, "MY90_Lung_shunt"] = my90_lung_shunt

                    st.success("Pre Y90 added successfully.")
                    st.write("Updated Data:")
                    st.dataframe(st.session_state.data)             

    with tab7:
        st.subheader("Day_Y90")
        with st.form("day_y90_form"):
            if "MRN" not in st.session_state.data:
                st.warning("Please complete the Patient Information tab first.")
            else:

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

                if dayy90_afp_prior_to_tare != 'NA':
                    afp_prey90 = dayy90_afp_prior_to_tare      
                elif prey90_afp_prior_to_tare != 'NA':
                    afp_prey90 = prey90_afp_prior_to_tare
                else:
                    afp_prey90 = "NA"
            
            # Inputs for other variables
                dayy90_sodium = st.number_input("DAYY90_sodium (mmol/L)")
                dayy90_creatinine = st.number_input("DAYY90_creatinine (mg/dl)")
                dayy90_inr = st.number_input("DAYY90_inr")
                dayy90_albumin = st.number_input("DAYY90_albumin (g/dl)")
                dayy90_bilirubin = st.number_input("DAYY90_bilirubin (mg/dl)",min_value=1)
                dayy90_ast = st.number_input("DAYY90_AST (U/L)")
                dayy90_alt = st.number_input("DAYY90_ALT (U/L)")
                dayy90_alkaline_phosphatase = st.number_input(
                    "DAYY90_Alkaline Phosphatase (U/L)"
                )
                dayy90_leukocytes = st.number_input("DAYY90_leukocytes (value in x10^3/µL)")
                dayy90_platelets = st.number_input("DAYY90_platelets (value in x10^3/µL)")

                dayy90_ascites = st.selectbox("DAYY90_ascites", options=["Grade 1", "Grade 2", "Grade 3", "Grade 4", "Grade 5"])
                dayy90_hepatic_encephalopathy = st.selectbox(
                    "DAYY90_Hepatic Encephalopathy", options=["Grade 1", "Grade 2", "Grade 3", "Grade 4", "Grade 5"]
                )
                dayy90_child_pugh_class_emr = st.selectbox(
                    "DAYY90_Child-Pugh class EMR", options=["Class A", "Class B", "Class C", "NA"]
                )

                def validate_input(value):
                    if value.isdigit() and 5 <= int(value) <= 15:
                        return value  # Valid number
                    elif value.upper() == "NA":
                        return "NA"  # Valid 'NA'
                    else:
                        return "NA" 

                input_value3 = st.text_input(
                    "Cirrhosis_Dx_Child-Pugh Points EMR",
                    help="Specify the Child-Pugh points if in EMR 'number 5-15 or NA"                
                )

                dayy90_child_pugh_points_emr = validate_input(input_value3)
        
                dayy90_bclc_emr = st.selectbox("DAYY90_BCLC EMR", options=["0","A", "B", "C", "D"])

                def validate_input2(value):
                    if value.isdigit() and 6 <= int(value) <= 40:
                        return value  # Valid number
                    elif value.upper() == "NA":
                        return "NA"  # Valid 'NA'
                    else:
                        return "NA" 

                input_value4 = st.text_input(
                    "DAYY90_MELD EMR",
                    help="Specify MELD EMR if in EMR 'number 6-40 or NA"                
                )

                dayy90_meld_emr = validate_input2(input_value4)

                input_value5 = st.text_input(
                    "DAYY90_MELD Na EMR",
                    help="Specify DAYY90_MELD Na EMR if in EMR 'number 6-40 or NA"                
                )
                dayy90_meld_na_emr = validate_input2(input_value5)

                dayy90_albi_emr = st.number_input("DAYY90_Albi EMR")

                prey90_ecog = st.selectbox("PREY90_ECOG", options=["0", "1", "2", "3", "4", "NA"])
                dayy90_child_pugh_points_calc = calculatepoints(dayy90_bilirubin,dayy90_albumin,dayy90_inr,dayy90_ascites,dayy90_hepatic_encephalopathy)
                dayy90_child_pugh_class_calc = calculate_class(dayy90_child_pugh_points_calc)
                # Formula Calculation
                dayy90_meld_calc = (3.78*(int(dayy90_bilirubin)))+(11.2*(int(dayy90_inr)))+(9.57*(int(dayy90_creatinine)))+6.43
                dayy90_meld_na_calc = dayy90_meld_calc + 1.32*(137-int(dayy90_sodium)) - (0.033*dayy90_meld_calc*(137-int(dayy90_sodium)))
                
                def albi_calc(a,b):
                    a=int(a)
                    b=int(b)
                    t = math.log(a, 10)
                    answer = (t * 0.66) + (b * -0.085)
                    return answer
                
                dayy90_albi_calc = albi_calc(dayy90_bilirubin,dayy90_albumin)
                

                dayy90_type_of_sphere = st.selectbox(
                    "DAYY90_Type of Sphere", options=["Therasphere-1", "SIR-2"]
                )

                dayy90_lt_notes_ftx = st.text_area("DAYY90_LT Notes (Free Text)")

                ken_childpughscore = st.number_input("ken_ChildPughscore")
                ken_meldpretare = st.number_input("ken_MELDpreTARE")


            # Submit button
                submit_tab7 = st.form_submit_button("Submit")
            
                if submit_tab7:
                    index = st.session_state.data[st.session_state.data["MRN"] == st.session_state.temp_mrn].index[0]

                    st.session_state.data.at[index, "DAYY90_AFP"] = dayy90_afp
                    st.session_state.data.at[index, "DAYY90_AFP Prior to TARE"] = dayy90_afp_prior_to_tare
                    st.session_state.data.at[index, "AFP_PreY90 or DAYY90"] = afp_prey90
                    st.session_state.data.at[index, "DAYY90_sodium"] = dayy90_sodium
                    st.session_state.data.at[index, "DAYY90_creatinine"] = dayy90_creatinine
                    st.session_state.data.at[index, "DAYY90_inr"] = dayy90_inr
                    st.session_state.data.at[index, "DAYY90_albumin"] = dayy90_albumin
                    st.session_state.data.at[index, "DAYY90_bilirubin"] = dayy90_bilirubin
                    st.session_state.data.at[index, "DAYY90_AST"] = dayy90_ast
                    st.session_state.data.at[index, "DAYY90_ALT"] = dayy90_alt
                    st.session_state.data.at[index, "DAYY90_Alkaline Phosphatase"] = dayy90_alkaline_phosphatase
                    st.session_state.data.at[index, "DAYY90_leukocytes"] = dayy90_leukocytes
                    st.session_state.data.at[index, "DAYY90_platelets"] = dayy90_platelets
                    st.session_state.data.at[index, "DAYY90_ascities"] = dayy90_ascites
                    st.session_state.data.at[index, "DAYY90_Hepatic Encephalopathy"] = dayy90_hepatic_encephalopathy
                    st.session_state.data.at[index, "DAYY90_Child-Pugh class EMR"] = dayy90_child_pugh_class_emr
                    st.session_state.data.at[index, "DAYY90_Child-Pugh points EMR"] = dayy90_child_pugh_points_emr
                    st.session_state.data.at[index, "DAYY90_BCLC EMR"] = dayy90_bclc_emr
                    st.session_state.data.at[index, "DAYY90_MELD EMR"] = dayy90_meld_emr
                    st.session_state.data.at[index, "DAYY90_MELD Na EMR"] = dayy90_meld_na_emr
                    st.session_state.data.at[index, "DAYY90_Albi EMR"] = dayy90_albi_emr
                    st.session_state.data.at[index, "PREY90_ECOG"] = prey90_ecog
                    st.session_state.data.at[index, "DAYY90_Child-Pugh class Calc"] = dayy90_child_pugh_class_calc
                    st.session_state.data.at[index, "DAYY90_Child-Pugh points calc"] = dayy90_child_pugh_points_calc
                    st.session_state.data.at[index, "DAYY90_MELD calc"] = dayy90_meld_calc
                    st.session_state.data.at[index, "DAYY90_MELD Na calc"] = dayy90_meld_na_calc
                    st.session_state.data.at[index, "DAYY90_Albi calc"] = dayy90_albi_calc
                    st.session_state.data.at[index, "DAYY90_Type of Sphere"] = dayy90_type_of_sphere
                    st.session_state.data.at[index, "DAYY90_LT_notes_ftx"] = dayy90_lt_notes_ftx
                    st.session_state.data.at[index, "ken_ChildPughscore"] = ken_childpughscore
                    st.session_state.data.at[index, "ken_MELDpreTARE"] = ken_meldpretare
                    
                    st.success("DAYY90 added successfully.")
                    st.write("Updated Data:")
                    st.dataframe(st.session_state.data)
    
    with tab8:
        st.subheader("Post Y90 Within 30 Days Labs")
        with st.form("post_y90_form"):
                if "MRN" not in st.session_state.data:
                    st.warning("Please complete the Patient Information tab first.")
                else:
                    
                    # Post Y90 Fields
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

                    posty90_ecog = st.selectbox(
                        "POSTY90_30DY_ECOG",
                        options=["0", "1", "2", "3", "4", "NA"],
                        help="Select ECOG Performance Status"
                    )

                    posty90_child_pugh_class = st.selectbox(
                        "POSTY90_30DY_Child-Pugh Class EMR",
                        options=["Class A", "Class B", "Class C", "NA"],
                        help="Select the Child-Pugh class"
                    )

                    inputp90 = st.text_input(
                        "POSTY90_30DY_Child-Pugh Points EMR",
                        help="Write in number in range 5-15, or NA"
                    )
                    posty90_child_pugh_points = validate_input(inputp90)

                    posty90_bclc_emr = st.selectbox(
                        "POSTY90_30DY_BCLC EMR",
                        options=["0", "A", "B", "C", "D"],
                        help="Select the BCLC stage"
                    )

                    input_meld = st.text_input(
                        "POSTY90_30DY_MELD EMR",
                        help="Write in number in range 6-40, or NA"
                    )
                    posty90_meld_emr = validate_input2(input_meld)


                    input_meld_na = st.text_input(
                        "POSTY90_30DY_MELD Na EMR",
                        help="Write in number in range 6-40, or NA"
                    )
                    posty90_meld_na_emr = validate_input2(input_meld_na)

                    posty90_albi_emr = st.number_input(
                        "POSTY90_30DY_ALBI EMR",
                        help="Enter ALBI score"
                    )


                    posty90_child_pugh_points_calc = calculatepoints(posty90_bilirubin,posty90_albumin,posty90_inr,prey90_ascites,prey90_he)
                    posty90_child_pugh_class_calc = calculate_class(posty90_child_pugh_points_calc)
                    #posty90_bclc_calc = st.text_input(
                        #"POSTY90_30DY_BCLC calc",
                        #help="Enter calculated BCLC stage"
                    #)

                    posty90_meld_calc = (3.78*(int(posty90_bilirubin)))+(11.2*(int(posty90_inr)))+(9.57*(int(posty90_creatinine)))+6.43
                    posty90_meld_na_calc = posty90_meld_calc + 1.32*(137-int(posty90_sodium)) - (0.033*posty90_meld_calc*(137-int(posty90_sodium)))

                    posty90_albi_calc = albi_calc(posty90_bilirubin,posty90_albumin)

                    ken_bclc_stage_post90 = st.text_input(
                        "Ken_BCLCStagepost90",
                        help="Enter BCLC Stage Post-90"
                    )

                    ken_meld_stage_post90 = st.text_input(
                        "Ken_MELD_Stagepost90",
                        help="Enter MELD Score Pre-TARE"
                    )

                    st.subheader("Post_Y90_within_30_days_adverse_events")
                    DYAE_CTCAE_portal_htn = st.selectbox(
                        "30DYAE_CTCAE_portal_htn",
                        options=["0","1","2","3","4","5"]
                    )
                    DYAE_CTCAE_Vascular_comp = st.selectbox(
                        "30DYAE_CTCAE_Vascular comp",
                        options=["0","1","2","3","4","5"]
                    )
                    DYAE_CTCAE_fatigue = st.selectbox(
                        "30DYAE_CTCAE_fatigue",
                        options=["0","1","2"]
                    )
                    DYAE_CTCAE_diarrhea = st.selectbox(
                        "30DYAE_CTCAE_diarrhea",
                        options=["0","1","2","3","4","5"]
                    )

                    DYAE_CTCAE_hypoalbuminemia_emr = st.text_input(
                        "30DYAE_CTCAE_hypoalbuminemia emr"
                    )
                    DYAE_CTCAE_hyperbilirubinemia_emr = st.text_input(
                        "30DYAE_CTCAE_hyperbilirubinemia emr"
                    )
                    DYAE_CTCAE_Increase_creatinine_emr = st.text_input(
                        "30DYAE_CTCAE_Increase_creatinine emr"
                    )
                    DYAE_CTCAE_abdominal_pain = st.selectbox(
                        "30DYAE_CTCAE_abdominal pain",
                        options=["0","1","2","3"]
                    )
                    DYAE_CTCAE_sepsis = st.selectbox(
                        "30DYAE_CTCAE_sepsis",
                        options=["0","3","4","5"]
                    )
                    DYAE_CTCAE_ascites = st.selectbox(
                    "30DYAE_CTCAE_ascites",
                    options=["none", "Asymptomatic", "Minimal ascities/Mild abd distension, no sx",
                            "Symptomatic", "moderate ascities/Symptomatic medical intervention",
                            "Severe symptoms, invasive intervention indicated",
                            "Life Threatening: Urgent operation intervention indicated"]
                    )
                    DYAE_CTCAE_ascites_binary_classification = 1 if DYAE_CTCAE_ascites != "none" else 0
                    DYAE_CTCAE_ascites_ftx = st.text_area(
                        "30DYAE_CTCAE_ascites_ftx",
                    )

                    DYAE_CTCAE_bacterial_peritonitis = st.selectbox(
                        "30DYAE_CTCAE_bacterial_peritonitis",
                        options=["0", "3", "4", "5"]
                    )

                    DYAE_CTCAE_hemorrhage = st.selectbox(
                    "30DYAE_CTCAE_hemorrhage",
                    options=["0", "3", "4", "5"]
                    )

                    DYAE_CTCAE_anorexia = st.selectbox(
                        "30DYAE_CTCAE_anorexia",
                        options=["0", "1", "2", "3"]
                    )

                    DYAE_CTCAE_intrahepatic_fistula = st.selectbox(
                        "30DYAE_CTCAE_intrahepatic_fistula",
                        options=["0","2", "3", "4", "5"]
                    )

                    DYAE_CTCAE_constipation = st.selectbox(
                        "30DYAE_CTCAE_constipation",
                        options=["0", "1", "2", "3"]
                    )

                    DYAE_CTCAE_nausea = st.selectbox(
                        "30DYAE_CTCAE_nausea",
                        options=["0", "1", "2", "3"]
                    )

                    DYAE_CTCAE_vomiting = st.selectbox(
                        "30DYAE_CTCAE_vomiting",
                        options=["0","1","2", "3", "4", "5"]
                    )

                    DYAE_CTCAE_Hepatic_Encephalopathy = st.selectbox(
                        "30DYAE_CTCAE_Hepatic Encephalopathy",
                        options=["0","1","2", "3", "4", "5"]
                    )

                    DYAE_CTCAE_he_ftx = st.text_area(
                        "30DYAE_CTCAE_he_ftx",
                        help="provide additional details of he"
                    )

                    DYAE_CTCAE_cholecystitis = st.selectbox(
                        "30DYAE_CTCAE_cholecystitis",
                        options=["0", "2","3", "4", "5"]
                    )

                    DYAE_CTCAE_gastric_ulcers = st.selectbox(
                        "30DYAE_CTCAE_gastric_ulcers",
                        options=["0","1","2", "3", "4", "5"]
                    )

                    DYAE_CTCAE_hyperkalemia = st.selectbox(
                        "30DYAE_CTCAE_hyperkalemia",
                        options=["NA"]
                    )

                    DYAE_CTCAE_respiratory_failure = st.selectbox(
                        "30DYAE_CTCAE_respiratory_failure",
                        options=["0", "4", "5"]
                    )

                    DYAE_CTCAE_AKI = st.selectbox(
                        "30DYAE_CTCAE_AKI",
                        options=["0", "3", "4", "5"]
                    )

                    DYAE_CTCAE_Radiation_pneumonitis = st.selectbox(
                        "30DYAE_CTCAE_Radiation_pneumonitis",
                        options=["0","1","2", "3", "4", "5"]
                    )

                    DYAE_AE_other = st.text_area(
                        "30DY_AE_other",
                        help="Other Adverse Events (Free Text)"
                    )

                    DYAE_AE_date_of_AE = st.text_input(
                        "90DY_AE_date_of_AE",
                        help="(if AE is present after 30 days but before 90 write it here and the date)"
                    )

                    submit_tab8 = st.form_submit_button("Save Post POST90 Labs")

                    if submit_tab8:
                            
                            index = st.session_state.data[st.session_state.data["MRN"] == st.session_state.temp_mrn].index[0]
                        
                            st.session_state.data.at[index, "POSTY90_30DY_date_labs"] = posty90_date_labs.strftime("%Y-%m-%d")
                            st.session_state.data.at[index, "POSTY90_30DY_afp"] = posty90_afp
                            st.session_state.data.at[index, "POSTY90_30DY_afp DATE"] = posty90_afp_date.strftime("%Y-%m-%d")
                            st.session_state.data.at[index, "POSTY90_30DY_Sodium"] = posty90_sodium
                            st.session_state.data.at[index, "POSTY90_30DY_creatinine"] = posty90_creatinine
                            st.session_state.data.at[index, "POSTY90_30DY_INR"] = posty90_inr
                            st.session_state.data.at[index, "POSTY90_30DY_albumin"] = posty90_albumin
                            st.session_state.data.at[index, "POSTY90_30DY_bilirubin"] = posty90_bilirubin
                            st.session_state.data.at[index, "POSTY90_30DY_AST"] = posty90_ast
                            st.session_state.data.at[index, "POSTY90_30DY_ALT"] = posty90_alt
                            st.session_state.data.at[index, "POSTY90_30DY_Alkaline Phosphatase"] = posty90_alkaline_phosphatase
                            st.session_state.data.at[index, "POSTY90_30DY_leukocytes"] = posty90_leukocytes
                            st.session_state.data.at[index, "POSTY90_30DY_platelets"] = posty90_platelets
                            st.session_state.data.at[index, "POSTY90_30DY_potassium"] = posty90_potassium
                            st.session_state.data.at[index, "POSTY90_30DY_ECOG"] = posty90_ecog
                            st.session_state.data.at[index, "POSTY90_30DY_Child-Pugh Class EMR"] = posty90_child_pugh_class
                            st.session_state.data.at[index, "POSTY90_30DY_Child-Pugh Points EMR"] = posty90_child_pugh_points
                            st.session_state.data.at[index, "POSTY90_30DY_BCLC EMR"] = posty90_bclc_emr
                            st.session_state.data.at[index, "POSTY90_30DY_MELD EMR"] = posty90_meld_emr
                            st.session_state.data.at[index, "POSTY90_30DY_MELD Na EMR"] = posty90_meld_na_emr
                            st.session_state.data.at[index, "POSTY90_30DY_ALBI EMR"] = posty90_albi_emr
                            st.session_state.data.at[index, "POSTY90_30DY_Child-Pugh Class calc"] = posty90_child_pugh_class_calc
                            st.session_state.data.at[index, "POSTY90_30DY_Child-Pugh Points calc"] = posty90_child_pugh_points_calc
                            st.session_state.data.at[index, "POSTY90_30DY_MELD calc"] = posty90_meld_calc
                            st.session_state.data.at[index, "POSTY90_30DY_MELD Na calc"] = posty90_meld_na_calc
                            st.session_state.data.at[index, "POSTY90_30DY_ALBI calc"] = posty90_albi_calc
                            st.session_state.data.at[index, "Ken_BCLCStagepost90"] = ken_bclc_stage_post90
                            st.session_state.data.at[index, "Ken_MELD_Stagepost90"] = ken_meld_stage_post90
                            st.session_state.data.at[index, "30DYAE_CTCAE_portal_htn"] = DYAE_CTCAE_portal_htn
                            st.session_state.data.at[index, "30DYAE_CTCAE_Vascular_comp"] = DYAE_CTCAE_Vascular_comp
                            st.session_state.data.at[index, "30DYAE_CTCAE_fatigue"] = DYAE_CTCAE_fatigue
                            st.session_state.data.at[index, "30DYAE_CTCAE_diarrhea"] = DYAE_CTCAE_diarrhea
                            st.session_state.data.at[index, "30DYAE_CTCAE_hypoalbuminemia_emr"] = DYAE_CTCAE_hypoalbuminemia_emr
                            st.session_state.data.at[index, "30DYAE_CTCAE_hyperbilirubinemia_emr"] = DYAE_CTCAE_hyperbilirubinemia_emr
                            st.session_state.data.at[index, "30DYAE_CTCAE_Increase_creatinine_emr"] = DYAE_CTCAE_Increase_creatinine_emr
                            st.session_state.data.at[index, "30DYAE_CTCAE_abdominal_pain"] = DYAE_CTCAE_abdominal_pain
                            st.session_state.data.at[index, "30DYAE_CTCAE_sepsis"] = DYAE_CTCAE_sepsis
                            st.session_state.data.at[index, "30DYAE_CTCAE_ascites"] = DYAE_CTCAE_ascites
                            st.session_state.data.at[index, "30DYAE_CTCAE_ascites_Binary_classification"] = DYAE_CTCAE_ascites_binary_classification
                            st.session_state.data.at[index, "30DYAE_CTCAE_ascites_ftx"] = DYAE_CTCAE_ascites_ftx
                            st.session_state.data.at[index, "30DYAE_CTCAE_bacterial_peritonitis"] = DYAE_CTCAE_bacterial_peritonitis
                            st.session_state.data.at[index, "30DYAE_CTCAE_hemorrhage"] = DYAE_CTCAE_hemorrhage
                            st.session_state.data.at[index, "30DYAE_CTCAE_anorexia"] = DYAE_CTCAE_anorexia
                            st.session_state.data.at[index, "30DYAE_CTCAE_intrahepatic_fistula"] = DYAE_CTCAE_intrahepatic_fistula
                            st.session_state.data.at[index, "30DYAE_CTCAE_constipation"] = DYAE_CTCAE_constipation
                            st.session_state.data.at[index, "30DYAE_CTCAE_nausea"] = DYAE_CTCAE_nausea
                            st.session_state.data.at[index, "30DYAE_CTCAE_vomiting"] = DYAE_CTCAE_vomiting
                            st.session_state.data.at[index, "30DYAE_CTCAE_Hepatic_Encephalopathy"] = DYAE_CTCAE_Hepatic_Encephalopathy
                            st.session_state.data.at[index, "30DYAE_CTCAE_he_ftx"] = DYAE_CTCAE_he_ftx
                            st.session_state.data.at[index, "30DYAE_CTCAE_cholecystitis"] = DYAE_CTCAE_cholecystitis
                            st.session_state.data.at[index, "30DYAE_CTCAE_gastric_ulcers"] = DYAE_CTCAE_gastric_ulcers
                            st.session_state.data.at[index, "30DYAE_CTCAE_hyperkalemia"] = DYAE_CTCAE_hyperkalemia
                            st.session_state.data.at[index, "30DYAE_CTCAE_respiratory_failure"] = DYAE_CTCAE_respiratory_failure
                            st.session_state.data.at[index, "30DYAE_CTCAE_AKI"] = DYAE_CTCAE_AKI
                            st.session_state.data.at[index, "30DYAE_CTCAE_Radiation_pneumonitis"] = DYAE_CTCAE_Radiation_pneumonitis
                            st.session_state.data.at[index, "30DY_AE_other"] = DYAE_AE_other
                            st.session_state.data.at[index, "90DY_AE_date_of_AE"] = DYAE_AE_date_of_AE

                            st.success("DAYY90 added successfully.")
                            st.write("Updated Data:")
                            st.dataframe(st.session_state.data)
                            
# Edit Existing Data Page
def edit_existing_data():
    st.title("Edit Existing Data")
    if st.session_state.data.empty:
        st.warning("No data available. Please add new data first.")
        return
    else:

        st.write("Current Data:")
        st.dataframe(st.session_state.data)

        mrn = st.text_input("Enter MRN to edit")
        #load_button = st.button("Load Data")
        #if load_button:
        if mrn not in st.session_state.data["MRN"].values:
            st.error(f"No data found for MRN {mrn}.")
        else:
            st.subheader("Cahnge_Data")
            
            st.write(f"Editing data for MRN: {mrn}")

            record = st.session_state.data[st.session_state.data["MRN"] == mrn]
            index = st.session_state.data[st.session_state.data["MRN"] == mrn].index[0]
            tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs(["Patient Demographics", "Cirrhosis PMH","HCC Diagnosis", "Previous Therapy for HCC", "Pre Y90", "Day_Y90", "Post Y90 Within 30 Days Labs"])
           
            with tab2:
                st.subheader("Patient Demographics")
                with st.form("demographics_form"):
                    st.subheader("Patient Description")
                    
                    gender = st.selectbox(
                        "Gender",
                        options=["Male", "Female"],
                        format_func=lambda x: f"{x} ({1 if x == 'Male' else 2})"
                    )

                    # Ethnicity dropdown
                    ethnicity = st.selectbox(
                        "Ethnicity",
                        options=["White", "Asian", "Hispanic", "Other", "NA"],
                        format_func=lambda x: {
                            "White": "White (3)",
                            "Asian": "Asian (4)",
                            "Hispanic": "Hispanic (5)",
                            "Other": "Other (6)",
                            "NA": "NA (can't find information)"
                        }[x]
                    )

                    # Medical History - Yes/No dropdowns
                    st.subheader("Medical History")
                    
                    hypertension = st.selectbox(
                        "PMHx Hypertension",
                        options=["No", "Yes"],
                        format_func=lambda x: f"{x} ({1 if x == 'Yes' else 0})"
                    )

                    diabetes = st.selectbox(
                        "PMHx Diabetes (T1 or T2)",
                        options=["No", "Yes"],
                        format_func=lambda x: f"{x} ({1 if x == 'Yes' else 0})"
                    )

                    hypercholesterolemia = st.selectbox(
                        "Hypercholesterolemia",
                        options=["No", "Yes"],
                        format_func=lambda x: f"{x} ({1 if x == 'Yes' else 0})"
                    )

                    smoking = st.selectbox(
                        "Hx of Smoking",
                        options=["No", "Yes"],
                        format_func=lambda x: f"{x} ({1 if x == 'Yes' else 0})"
                    )

                    obesity = st.selectbox(
                        "Obesity",
                        options=["No", "Yes"],
                        format_func=lambda x: f"{x} ({1 if x == 'Yes' else 0})"
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
                    submit_tab2 = st.form_submit_button("Submit Patient Description")
                    if submit_tab2:
                        index = st.session_state.data[st.session_state.data["MRN"] == st.session_state.temp_mrn].index[0]
                        st.session_state.data.loc[index, "Gender"] = gender
                        st.session_state.data.loc[index, "Ethnicity"] = ethnicity
                        st.session_state.data.loc[index, "PMHx Hypertension"] = hypertension
                        st.session_state.data.loc[index, "PMHx Diabetes (T1 or T2)"] = diabetes
                        st.session_state.data.loc[index, "Hypercholesterolemia"] = hypercholesterolemia
                        st.session_state.data.loc[index, "Hx of Smoking"] = smoking
                        st.session_state.data.loc[index, "Obesity"] = obesity
                        st.session_state.data.loc[index, "Comorbitieis Total Count"] = total_count
                        st.session_state.data.loc[index, "Comorbitieis Binary"] = binary_value
                        st.success("Patient Description added successfully.")
                        st.write("Updated Data:")
                        st.dataframe(st.session_state.data)

            with tab3:
                st.subheader("Cirrhosis PMH")
                with st.form("cirrhosis_pmh_form"):
                    
                    
                        cir_pmh_hbv_status = st.selectbox(
                            "Cir_PMH_HBV Status",
                            options=["Yes", "No"],
                        # format_func=lambda x: f"{x} ({1 if x == 'Yes' else 0})",
                            help="Select HBV Status"
                        )

                        cir_pmh_hbv_free_text = "0" if cir_pmh_hbv_status == "No" else st.text_input(
                            "Cir_PMH_HBV Free Text",
                            help="Provide additional details for HBV Status"
                        )
                        
                        cir_pmh_hbv_art = "0" if cir_pmh_hbv_status == "No" else st.selectbox(
                            "Cir_PMH_HBV ART",
                            options=["Entecavir", "Tenofovir", "NA"],
                        )

                        cir_pmh_hcv_status = st.selectbox(
                            "Cir_PMH_HCV Status",
                            options=["Yes", "No"],
                        # format_func=lambda x: f"{x} ({1 if x == 'Yes' else 0})",
                            help="Select HCV Status"
                        )

                        cir_pmh_hcv_free_text = "0" if cir_pmh_hcv_status == "No" else st.text_input(
                            "Cir_PMH_HCV Free Text",
                            help="Provide additional details for HCV Status",
                        )

                        cir_pmh_hcv_art = "0" if cir_pmh_hcv_status == "No" else st.selectbox(
                            "Cir_PMH_HBV ART",
                            options=["sofosbuvir/velpatasvir", "ledipasvir/sofosbuvir", "NA", "Glecaprevir/pibrentasvi"],
                            help="Select ART treatment for HCV",
                    
                        )

                        cir_pmh_alcohol_use_disorder = st.selectbox( 
                            "Cir_PMH_Alcohol Use Disorder",
                            options=["Yes", "No"],
                            #format_func=lambda x: f"{x} ({1 if x == 'Yes' else 0})",
                            help="Select Alcohol Disorder"
                        )

                        cir_pmh_duration_of_alcohol_use_years = "0" if cir_pmh_alcohol_use_disorder == "No" else st.number_input(
                            "Cir_PMH_Duration of Alcohol Use Years",
                            help="Provide Duration of Alchohol Use Years",
                        )

                        cir_pmh_alcohol_free_text = "0" if cir_pmh_alcohol_use_disorder == "No" else st.text_input(
                            "Cir_PMH_HCV Free Text",
                            help="Provide additional details for Alcohol Disorder",
                        )

                        cir_pmh_ivdu_status = st.selectbox(
                            "Cir_PMH_IVDU Status",
                            options=["Yes", "No"],
                            #format_func=lambda x: f"{x} ({1 if x == 'Yes' else 0})",
                            help="Select IVDU Status"
                        )

                        cir_pmh_duration_of_ivdu_years = "0" if cir_pmh_ivdu_status == "No" else st.number_input(
                            "Cir_PMH_Duration of IVDU Years",
                            help="Provide Duration of IVDU Disorder",
                        )

                        cir_pmh_ivdu_free_text = "0" if cir_pmh_ivdu_status == "No" else st.text_input(
                            "Cir_PMH_HCV Free Text",
                            help="Provide additional details for IVDU"
                    
                        )

                        cir_pmh_other_contributing_factors = st.selectbox(
                            "Cir_PMH_Other Contributing Factors",
                            options=["NAFLD", "MAFLD", "NASH", "Autoimmune Hepatitis", "Hereditary Hemochromatosis","none"],
                            help="Select Other Contributing Factors"
                        )
                
                        st.subheader("Cirrhosis Dx")
                        Cirrhosis_Dx_Diagnosis_Date = st.date_input("Cirrhosis_Dx_Diagnosis Date",help="Select Diagnosis date")

                        Cirrhosis_Dx_Diagnosis_Method = st.selectbox(
                            "Cirrhosis_Dx_Diagnosis Method",
                            options=["Biopsy", "Imaging"],
                            help="Select Diagnosis Method"
                        ) 
                        Cirrhosis_Dx_HPI_EMR_Note_Free_Text = st.text_input(
                            "Cirrhosis_Dx_HPI EMR Note Free Text",
                            help="Provide details of HPI EMR"
                        )
                        Cirrhosis_Dx_Imaging_Findings_EMR_Note_Free_Text = st.text_input(
                            "Cirrhosis_Dx_Imaging Findings EMR Note Free Text",
                            help="Provide details of Imaging Findings"
                        )

                        Cirrhosis_Dx_Metavir_Score = st.selectbox (
                            "Cirrhosis_Dx_Metavir Score",
                            options=["F0/F1", "F2","F3","F4","NA"],
                            help="Select Metavir_score"
                        ) 

                        Cirrhosis_Dx_Complications_at_Time_of_Diagnosis = st.multiselect(
                            "Cirrhosis_Dx_Complications at Time of Diagnosis",
                            options=["ascites", " variceal hemorrhage","hepatic encephalopathy","jaundice","SBP", "Hepatorenal Syndrome", "Coagulopathy", "Portal HTN", "PVT", "PVTT", "none"],
                            help="Provide details of Compilications at time of Diagnosis"
                        )

                        Cirrhosis_Dx_Complications_at_Time_of_Diagnosis_Binary = st.selectbox(
                            "Cirrhosis_Dx_Complications at Time of Diagnosis Binary",
                            options=["0","1"],
                            format_func=lambda x: {
                                "1": " >1 ",
                                "0": "None",
                            }[x],
                            help="Provide details of Complications_at_Time_of_Diagnosis_Binary"
                        )

                        Cirrhosis_Dx_Complications_Free_Text =  st.text_input(
                            "Cirrhosis_Dx_Complications Free Text",
                            help="Provide details of Complications"
                        )

                        Cirrhosis_Dx_Date_of_Labs_in_Window = st.date_input(" Cirrhosis_Dx_Date of Labs in Window",help="Select the date of lab test")

                        Cirrhosis_Dx_AFP = st.text_input(
                            "Cirrhosis_Dx_AFP",
                            help="Enter AFP value in ng/dl"
                            
                        )

                        Cirrhosis_Dx_AFP_L3 = st.text_input(
                            "Cirrhosis_Dx_AFP_L3",
                            help="Enter AFP_L3 value in ng/dl"
                            
                        )

                        Cirrhosis_Dx_Child_Pugh_class_EMR = st.selectbox(
                            "Cirrhosis_Dx_Child-Pugh Class EMR",
                            options=["Class A","Class B","Class C","NA"]

                        )
                        # Validation for Cirrhosis_Dx_Child-Pugh Points EMR
                        def validate_input(value):
                            if value.isdigit() and 5 <= int(value) <= 15:
                                return value  # Valid number
                            elif value.upper() == "NA":
                                return "NA"  # Valid 'NA'
                            else:
                                return "NA" 

                        input_value = st.text_input(
                            "Cirrhosis_Dx_Child-Pugh Points EMR",
                            help="Specify the Child-Pugh points if in EMR 'number 5-15 or NA"                
                        )

                        Cirrhosis_Dx_Child_Pugh_Points_EMR = validate_input(input_value)


                        def validate_input_EMR(value):
                            if value.isdigit() and 6 <= int(value) <= 40:
                                return value  # Valid number
                            elif value.upper() == "NA":
                                return "NA"  # Valid 'NA'
                            else:
                                return "NA" 
                        
                        input_value1 = st.text_input(
                            "Cirrhosis_Dx_MELD Score EMR",
                            help="Specify the MELD Score if in EMR 'number 6-40 or NA"                
                        )

                        Cirrhosis_Dx_MELD_Score_EMR = validate_input_EMR(input_value1)

                
                        input_value2 = st.text_input(
                            "Cirrhosis_Dx_MELD-NA_Score_EMR",
                            help="Specify the MELD Score NA if in EMR 'number 6-40 or NA"                
                        )

                        Cirrhosis_Dx_MELD_NA_Score_EMR = validate_input_EMR(input_value2)

                
                        
                        Cirrhosis_Dx_Ascites = st.selectbox (
                            "Cirrhosis_Dx_Ascites",
                            options=["none", "Asymptomatic","Minimal ascities/Mild abd distension","Symptomatic"," moderate ascities/Symptomatic medical intervention", "Severe symptoms, invasive intervention indicated", "Life Threatening: Urgent operation intervention indicated"],
                            help="Select Metavir_score"
                        ) 

                        Cirrhosis_Dx_Ascites_Binary_Classification = "NA" if Cirrhosis_Dx_Ascites == "none" else st.selectbox(
                            "Cirrhosis_Dx_Ascites_Binary_Classification",
                            options=["0","1"],
                            format_func=lambda x: {
                                "1": " Other than 1 ",
                                "0": "None",
                            }[x],
                        
                        )
                        
                        Cirrhosis_Dx_Ascites_Free_Text = "NA" if Cirrhosis_Dx_Ascites == "none" else st.text_area(
                            "Cirrhosis_Dx_Ascites Free Text",
                            "Hospitalized (yes/no): \nDiuretics (yes/no): \nParacentesis (yes/no): \nAny other complications (free_text):",
                        
                        )

                        Cirrhosis_Dx_Ascites_Labs_Free_Text = "NA" if Cirrhosis_Dx_Ascites == "none" else st.text_area(
                            "Cirrhosis_Dx_Ascites Labs Free Text",
                            "Bilirubin (mg/dl): \nAlbumin (g/dl): \nINR: \nCreatinine (mg/dl): \nSodium (mmol/L): \nAST (U/L): \nALT (U/L): \nAlk Phos: \nPlatelets:",
                            
                        )

                        Cirrhosis_Dx_Hepatic_Encephalopathy = st.selectbox(
                            "Cirrhosis_Dx_Hepatic_Encephalopathy",
                            options=["Yes", "No"],
                            #format_func=lambda x: f"{x} ({1 if x == 'Yes' else 0})",
                            help="Hepatic_Encephalopathy"
                    
                        )


                        submit_tab3 = st.form_submit_button("Submit Cirrhosis PMH")
                        if submit_tab3:

                            #index = st.session_state.data[st.session_state.data["MRN"] == st.session_state.temp_mrn].index[0]
                            st.session_state.data.at[index, "Cir_PMH_HBV Status"] = cir_pmh_hbv_status
                            st.session_state.data.at[index, "Cir_PMH_HBV Free Text"] = cir_pmh_hbv_free_text
                            st.session_state.data.at[index, "Cir_PMH_HBV ART"] = cir_pmh_hbv_art
                            st.session_state.data.at[index, "Cir_PMH_HCV Status"] = cir_pmh_hcv_status
                            st.session_state.data.at[index, "Cir_PMH_HCV Free Text"] = cir_pmh_hcv_free_text
                            st.session_state.data.at[index, "Cir_PMH_HCV ART"] = cir_pmh_hcv_art
                            st.session_state.data.at[index, "Cir_PMH_Alcohol Use Disorder"] = cir_pmh_alcohol_use_disorder
                            st.session_state.data.at[index, "Cir_PMH_Duration of Alcohol Use Years"] = cir_pmh_duration_of_alcohol_use_years
                            st.session_state.data.at[index, "Cir_PMH_Alcohol Free Text"] = cir_pmh_alcohol_free_text
                            st.session_state.data.at[index, "Cir_PMH_IVDU Status"] = cir_pmh_ivdu_status
                            st.session_state.data.at[index, "Cir_PMH_Duration of IVDU Years"] = cir_pmh_duration_of_ivdu_years
                            st.session_state.data.at[index, "Cir_PMH_IVDU Free Text"] = cir_pmh_ivdu_free_text
                            st.session_state.data.at[index, "Cir_PMH_Other Contributing Factors"] = cir_pmh_other_contributing_factors
                            st.session_state.data.at[index, "Cirrhosis_Dx_Diagnosis Date"] = Cirrhosis_Dx_Diagnosis_Date
                            st.session_state.data.at[index, "Cirrhosis_Dx_Diagnosis Method"] = Cirrhosis_Dx_Diagnosis_Method
                            st.session_state.data.at[index, "Cirrhosis_Dx_HPI EMR Note Free Text"] = Cirrhosis_Dx_HPI_EMR_Note_Free_Text
                            st.session_state.data.at[index, "Cirrhosis_Dx_Imaging Findings EMR Note Free Text"] = Cirrhosis_Dx_Imaging_Findings_EMR_Note_Free_Text
                            st.session_state.data.at[index, "Cirrhosis_Dx_Metavir Score"] = Cirrhosis_Dx_Metavir_Score
                            st.session_state.data.at[index, "Cirrhosis_Dx_Complications at Time of Diagnosis"] = Cirrhosis_Dx_Complications_at_Time_of_Diagnosis
                            st.session_state.data.at[index, "Cirrhosis_Dx_Complications at Time of Diagnosis Binary"] = Cirrhosis_Dx_Complications_at_Time_of_Diagnosis_Binary
                            st.session_state.data.at[index, "Cirrhosis_Dx_Complications Free Text"] = Cirrhosis_Dx_Complications_Free_Text
                            st.session_state.data.at[index, "Cirrhosis_Dx_Date of Labs in Window"] = Cirrhosis_Dx_Date_of_Labs_in_Window
                            st.session_state.data.at[index, "Cirrhosis_Dx_AFP"] = Cirrhosis_Dx_AFP
                            st.session_state.data.at[index, "Cirrhosis_Dx_AFP_L3"] = Cirrhosis_Dx_AFP_L3
                            st.session_state.data.at[index, "Cirrhosis_Dx_Child-Pugh Class EMR"] = Cirrhosis_Dx_Child_Pugh_class_EMR
                            st.session_state.data.at[index, "Cirrhosis_Dx_Child-Pugh Points EMR"] = Cirrhosis_Dx_Child_Pugh_Points_EMR
                            st.session_state.data.at[index, "Cirrhosis_Dx_MELD Score EMR"] = Cirrhosis_Dx_MELD_Score_EMR
                            st.session_state.data.at[index, "Cirrhosis_Dx_MELD-Na Score EMR"] = Cirrhosis_Dx_MELD_NA_Score_EMR
                            st.session_state.data.at[index, "Cirrhosis_Dx_Ascites"] = Cirrhosis_Dx_Ascites
                            st.session_state.data.at[index, "Cirrhosis_Dx_Ascites Binary Classification"] = Cirrhosis_Dx_Ascites_Binary_Classification
                            st.session_state.data.at[index, "Cirrhosis_Dx_Ascites Free Text"] = Cirrhosis_Dx_Ascites_Free_Text
                            st.session_state.data.at[index, "Cirrhosis_Dx_Ascites Labs Free Text"] = Cirrhosis_Dx_Ascites_Labs_Free_Text
                            st.session_state.data.at[index, "Cirrhosis_Dx_Hepatic Encephalopathy"] = Cirrhosis_Dx_Hepatic_Encephalopathy
                            
                            st.success("Patient Description added successfully.")
                            st.write("Updated Data:")
                            st.dataframe(st.session_state.data)

            with tab4:
                st.subheader("HCC Diagnosis")
                with st.form("hcc_dx_form"): 
                    
                        hcc_dx_hcc_diagnosis_date = st.date_input("HCC_Dx_HCC Diagnosis Date", help="Enter the HCC diagnosis date")

                        hcc_dx_method_of_diagnosis = st.selectbox(
                            "HCC_Dx_Method of Diagnosis",   
                            options=["Biopsy", "Imaging", "Unknown"],
                            #format_func=lambda x: f"{x} ({1 if x == 'Biopsy' else 2 if x == 'Imaging' else 'NA'})"
                        )

                        hcc_dx_date_of_labs = st.date_input("HCC_Dx_Date of Labs in Window")

                        hcc_dx_afp = st.number_input("HCC_Dx_AFP", help="Enter AFP value in ng/dl")
                        hcc_dx_afp_l3_date_free_text = st.text_area("HCC_Dx_AFP L3 & Date Free Text", help="Enter AFP L3 and date details")

                        hcc_dx_bilirubin = st.number_input("HCC_Dx_Bilirubin", help="Enter the bilirubin value in mg/dl", min_value=1)
                        hcc_dx_albumin = st.number_input("HCC_Dx_Albumin", help="Enter the albumin value in g/dl")
                        hcc_dx_inr = st.number_input("HCC_Dx_INR", help="Enter the INR value")
                        hcc_dx_creatinine = st.number_input("HCC_Dx_Creatinine", help="Enter the creatinine value in mg/dl")
                        hcc_dx_sodium = st.number_input("HCC_Dx_Sodium", help="Enter the sodium value in mmol/L")

                        hcc_dx_ascites = st.selectbox(
                            "HCC_Dx_Ascites",
                            options=["none", "Asymptomatic", "Minimal ascities/Mild abd distension, no sx",
                                    "Symptomatic", "moderate ascities/Symptomatic medical intervention",
                                    "Severe symptoms, invasive intervention indicated",
                                    "Life Threatening: Urgent operation intervention indicated"]
                        )

                        hcc_dx_ascites_binary_classification = 1 if hcc_dx_ascites != "none" else 0
                        #st.info(f"HCC_Dx_Ascites Binary Classification: {ascites_binary}")

                        hcc_dx_ascites_free_text = "NA" if hcc_dx_ascites == 'none' else st.text_area(
                            "HCC_Dx_Ascites Free Text",
                            "Hospitalized (yes/no): \nDiuretics (yes/no): \nParacentesis (yes/no): \nAny other complications (free_text):",
                            
                        )

                        hcc_dx_ascites_labs_free_text = "NA" if hcc_dx_ascites == 'none' else st.text_area(
                            "HCC_Dx_Ascites Labs Free Text",
                            """Bilirubin (mg/dl): \nAlbumin (g/dl): \nINR: \nCreatinine (mg/dl): \nSodium (mmol/L): 
                            AST (U/L): \nALT (U/L): \nAlk Phos: \nPlatelets:""",
                    
                        )

                        hcc_dx_hepatic_encephalopathy = st.selectbox(
                            "HCC_Dx_Hepatic Encephalopathy",
                            options=["Yes", "No"],
                            #format_func=lambda x: f"{x} ({1 if x == 'Yes' else 0})"
                        )

                        hcc_dx_ecog_performance_status = st.selectbox("HCC_Dx_ECOG Performance Status", options=["0", "1", "2", "3", "4", "NA"])

                        hcc_dx_lirads_score = st.selectbox(
                            "HCC_Dx_LIRADS Score",
                            options=["LR-1", "LR-2", "LR-3", "LR-4", "LR-5", "LR-5V", "LR-M"]
                        )

                        hcc_dx_child_pugh_class_emr = st.selectbox(
                            "HCC_Dx_Child-Pugh Class EMR",
                            options=["Class A", "Class B", "Class C", "NA"]
                        )

                        # Validation of hcc_dx_child_pugh_points_emr

                        def validate_input(value):
                            if value.isdigit() and 5 <= int(value) <= 15:
                                return value  # Valid number
                            elif value.upper() == "NA":
                                return "NA"  # Valid 'NA'
                            else:
                                return "NA" 

                        input_value3 = st.text_input(
                            "HCC_Dx_Child-Pugh Points EMR",
                            help="Specify the Child-Pugh points if in EMR number 5-15 or NA"                
                        )

                        hcc_dx_child_pugh_points_emr = validate_input(input_value3)


                        hcc_dx_bclc_stage_emr = st.selectbox(
                            "HCC_Dx_BCLC Stage EMR",
                            options=["0", "A", "B", "C", "D"]
                        )

                        # Validating hcc_dx_meld/na score
                        def validate_input2(value):
                            if value.isdigit() and 6 <= int(value) <= 40:
                                return value  # Valid number
                            elif value.upper() == "NA":
                                return "NA"  # Valid 'NA'
                            else:
                                return "NA" 

                
                        input_value4 = st.text_input(
                            "HCC_Dx_MELD Score EMR",
                            help="Write in number in range 6-40, or NA"
                        )


                        hcc_dx_meld_score_emr = validate_input2(input_value4)

                        input_value5 = st.text_input(
                            "HCC_Dx_MELD-Na Score EMR",
                            help="Write in number in range 6-40, or NA"
                        )

                        hcc_dx_meld_na_score_emr = validate_input2(input_value5)


                        hcc_dx_albi_score_emr = st.number_input("HCC_Dx_ALBI Score EMR")

                        #  calculation of child_pugh_points_clac

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

                # Points for INR
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


                        hcc_dx_child_pugh_points_calc = calculatepoints(hcc_dx_bilirubin,hcc_dx_albumin,hcc_dx_inr,hcc_dx_ascites,hcc_dx_hepatic_encephalopathy)

                        # Calculations for classses

                        def calculate_class(poin):
                            if 5 <= poin <= 6:
                                return 'A'
                            elif 7 <= poin <= 9:
                                return 'B'
                            elif 10 <= poin <= 15:
                                return 'C'
                            else:
                                return "Invalid points: must be between 5 and 15."
                
                        hcc_dx_child_pugh_class_calc = calculate_class(hcc_dx_child_pugh_points_calc)
                    
                        #bclc_stage_calc = st.text_input("HCC_Dx_BCLC Stage calc")
                        hcc_dx_meld_score_calc = (3.78*(int(hcc_dx_bilirubin)))+(11.2*(int(hcc_dx_inr)))+(9.57*(int(hcc_dx_creatinine)))+6.43
                        hcc_dx_meld_na_score_calc = hcc_dx_meld_score_calc + 1.32*(137-int(hcc_dx_sodium)) - (0.033*hcc_dx_meld_score_calc*(137-int(hcc_dx_sodium)))
                        def albi_calc(a,b):
                            a=int(a)
                            b=int(b)
                            t = math.log(a, 10)
                            answer = (t * 0.66) + (b * -0.085)
                            return answer
                        
                        hcc_dx_albi_score_calc = albi_calc(hcc_dx_bilirubin, hcc_dx_albumin)
                    

                        submit_tab4 = st.form_submit_button("Save HCC Diagnosis")
                        if submit_tab4:
                                #index = st.session_state.data[st.session_state.data["MRN"] == st.session_state.temp_mrn].index[0]
                                st.session_state.data.at[index, "HCC_Dx_HCC Diagnosis Date"] = hcc_dx_hcc_diagnosis_date.strftime("%Y-%m-%d")
                                st.session_state.data.at[index, "HCC_Dx_Method of Diagnosis"] = hcc_dx_method_of_diagnosis
                                st.session_state.data.at[index, "HCC_Dx_Date of Labs in Window"] = hcc_dx_date_of_labs.strftime("%Y-%m-%d")
                                st.session_state.data.at[index, "HCC_Dx_AFP"] = hcc_dx_afp
                                st.session_state.data.at[index, "HCC_Dx_AFP L3 & Date Free Text"] = hcc_dx_afp_l3_date_free_text
                                st.session_state.data.at[index, "HCC_Dx_Bilirubin"] = hcc_dx_bilirubin
                                st.session_state.data.at[index, "HCC_Dx_Albumin"] = hcc_dx_albumin
                                st.session_state.data.at[index, "HCC_Dx_INR"] = hcc_dx_inr
                                st.session_state.data.at[index, "HCC_Dx_Creatinine"] = hcc_dx_creatinine
                                st.session_state.data.at[index, "HCC_Dx_Sodium"] = hcc_dx_sodium
                                st.session_state.data.at[index, "HCC_Dx_Ascites"] = hcc_dx_ascites
                                st.session_state.data.at[index, "HCC_Dx_Ascites Binary Classification"] = hcc_dx_ascites_binary_classification
                                st.session_state.data.at[index, "HCC_Dx_Ascites Free Text"] = hcc_dx_ascites_free_text
                                st.session_state.data.at[index, "HCC_Dx_Ascites Labs Free Text"] = hcc_dx_ascites_labs_free_text
                                st.session_state.data.at[index, "HCC_Dx_Hepatic Encephalopathy"] = hcc_dx_hepatic_encephalopathy
                                st.session_state.data.at[index, "HCC_Dx_ECOG Performance Status"] = hcc_dx_ecog_performance_status
                                st.session_state.data.at[index, "HCC_Dx_LIRADS Score"] = hcc_dx_lirads_score
                                st.session_state.data.at[index, "HCC_Dx_Child-Pugh Class EMR"] = hcc_dx_child_pugh_class_emr
                                st.session_state.data.at[index, "HCC_Dx_Child-Pugh Points EMR"] = hcc_dx_child_pugh_points_emr
                                st.session_state.data.at[index, "HCC_Dx_BCLC Stage EMR"] = hcc_dx_bclc_stage_emr
                                st.session_state.data.at[index, "HCC_Dx_MELD Score EMR"] = hcc_dx_meld_score_emr
                                st.session_state.data.at[index, "HCC_Dx_MELD-Na Score EMR"] = hcc_dx_meld_na_score_emr
                                st.session_state.data.at[index, "HCC_Dx_ALBI Score EMR"] = hcc_dx_albi_score_emr
                                st.session_state.data.at[index, "HCC_Dx_Child-Pugh Class calc"] = hcc_dx_child_pugh_class_calc
                                st.session_state.data.at[index, "HCC_Dx_Child-Pugh Points calc"] = hcc_dx_child_pugh_points_calc
                                st.session_state.data.at[index, "HCC_Dx_MELD Score calc"] = hcc_dx_meld_score_calc
                                st.session_state.data.at[index, "HCC_Dx_MELD-Na Score calc"] = hcc_dx_meld_na_score_calc
                                st.session_state.data.at[index, "HCC_Dx_ALBI Score calc"] = hcc_dx_albi_score_calc

                                st.success("HCC Dx added successfully.")
                                st.write("Updated Data:")
                                st.dataframe(st.session_state.data)
        
            with tab5:
                
                    st.subheader("Previous Therapy for HCC")
                    with st.form("previous_therapy_form"):

                        PRVTHER_Prior_LDT_Therapy = st.selectbox(
                            "PRVTHER_Prior_LDT_Therapy",
                            options=["Yes", "No","NA"],
                            #format_func=lambda x: f"{x} ({1 if x == 'Yes' else 0})",
                            help="Prior LDT Therapy"
                        )
                        PRVTHER_Prior_RFA_Therapy = st.selectbox(
                            "PRVTHER_Prior RFA Therapy",
                            options=["Yes", "No", "NA"],
                            #format_func=lambda x: f"{x} ({1 if x == 'Yes' else 0})",
                            help="Prior RFA Therapy"
                        )
                    
                        PRVTHER_Prior_TARE_Therapy = st.selectbox(
                            "PRVTHER_Prior TARE Therapy",
                            options=["Yes", "No","NA"],
                            #format_func=lambda x: f"{x} ({1 if x == 'Yes' else 0})",
                            help="Prior TARE Therapy"
                        )
                    
                        PRVTHER_Prior_SBRT_Therapy = st.selectbox(
                            "PRVTHER_Prior SBRT Therapy",
                            options=["Yes", "No","NA"],
                            #format_func=lambda x: f"{x} ({1 if x == 'Yes' else 0})",
                            help="Prior SBRT Therapy"
                        )
                    
                        PRVTHER_Prior_TACE_Therapy = st.selectbox(
                            "PRVTHER_Prior TACE Therapy",
                            options=["Yes", "No","NA"],
                            #format_func=lambda x: f"{x} ({1 if x == 'Yes' else 0})",
                            help="Prior TACE Therapy"
                        )
                        PRVTHER_Prior_MWA_Therapy = st.selectbox(
                            "PRVTHER_Prior MWA Therapy",
                            options=["Yes", "No","NA"],
                            #format_func=lambda x: f"{x} ({1 if x == 'Yes' else 0})",
                            help="Prior MWA Therapy"
                        )

                        list1=[PRVTHER_Prior_LDT_Therapy, PRVTHER_Prior_RFA_Therapy, PRVTHER_Prior_TARE_Therapy, PRVTHER_Prior_SBRT_Therapy, PRVTHER_Prior_TACE_Therapy, PRVTHER_Prior_MWA_Therapy]
                        sum=0
                        for item in list1:
                            if item == "Yes" :
                                sum+=1
                            else:
                                continue
                        
                        PRVTHER_Previous_Therapy_Sum = sum

                    
                    # PRVTHER_Previous_Therapy_Sum = PRVTHER_Prior_LDT_Therapy + PRVTHER_Prior_RFA_Therapy + PRVTHER_Prior_TARE_Therapy + PRVTHER_Prior_SBRT_Therapy + PRVTHER_Prior_TACE_Therapy + PRVTHER_Prior_MWA_Therapy

                        PRVTHER_Previous_Therapy_Dates = st.text_area(
                        "PRVTHER_Previous Therapy Date(s) ",
                        help=" Enter previous therapy date or NA"
                        )

                        PRVTHER_Total_Recurrences_HCC = st.selectbox(
                            "PRVTHER_Total Recurrences HCC",
                            options=["0","1","2","3","4","NA"],
                            help="select total recurrences of HCC"
                        )
                    
                        PRVTHER_Binary_for_ANY_Recurrences_HCC_Binary = 1 if PRVTHER_Previous_Therapy_Sum == "YES" or PRVTHER_Prior_LDT_Therapy == "Yes" or PRVTHER_Prior_RFA_Therapy == "Yes" or PRVTHER_Prior_TARE_Therapy == "Yes" or PRVTHER_Prior_SBRT_Therapy == "Yes" or PRVTHER_Prior_TACE_Therapy == "Yes" or PRVTHER_Prior_MWA_Therapy == "Yes" else 0

                        PRVTHER_Location_of_Previous_Treatment_HCC = st.text_input(
                            "PRVTHER_Location of Previous Treatment HCC",
                            help="Provide Location of Previous HCC treatment"
                        )

                        PRVTHER_Recurrence_Date_Location_Free_Text = st.text_input(
                            "PRVTHER_Recurrence Date/Location Free Text",
                            help="Provide Date and Location on Recurrence"
                        )   
                        PRVTHER_New_HCC_Outside_Previous_Treatment_Site = st.text_input(
                            "PRVTHER_New HCC Outside Previous Treatment Site",
                            help="new HCC occurrence that has developed in a diff location in the liver, separate from the area that was previously tx"
                        )   
                        PRVTHER_New_HCC_Adjacent_to_Previous_Treatment_Site = st.text_input(
                            "PRVTHER_New HCC Adjacent to Previous Treatment Site",
                            help=" new HCC occurrence that has developed close to, but not directly in, the area that was previously treated"
                        )   
                        PRVTHER_Residual_HCC = st.text_input(
                            "PRVTHER_Residual HCC",
                            help="Provide information of Residual HCC"
                        ) 

                        PRVTHER_Systemic_Therapy_Free_Text = st.selectbox(
                            "PRVTHER_Systemic Therapy Free Text",
                            options=["Yes", "No","NA"],
                            #format_func=lambda x: f"{x} ({1 if x == 'Yes' else 0})",
                            help="Prior TACE Therapy"
                        )

                        PRVTHER_Date_of_Labs_in_Window = st.date_input(
                            "PRVTHER_Date of Labs in Window",
                            help="select date of labs in window"
                        )

                        PRVTHER_AFP = st.text_input(
                            "PRVTHER_AFP",
                            help="Enter AFP value in ng/dl or NA"
                        )

                        submit_tab5 = st.form_submit_button("Submit Previous Therapy Form")

                        if submit_tab5:
                                #index = st.session_state.data[st.session_state.data["MRN"] == st.session_state.temp_mrn].index[0]
                                st.session_state.data.at[index, "PRVTHER_Prior LDT Therapy"] = PRVTHER_Prior_LDT_Therapy
                                st.session_state.data.at[index, "PRVTHER_Prior RFA Therapy"] = PRVTHER_Prior_RFA_Therapy
                                st.session_state.data.at[index, "PRVTHER_Prior TARE Therapy"] = PRVTHER_Prior_TARE_Therapy
                                st.session_state.data.at[index, "PRVTHER_Prior SBRT Therapy"] = PRVTHER_Prior_SBRT_Therapy
                                st.session_state.data.at[index, "PRVTHER_Prior TACE Therapy"] = PRVTHER_Prior_TACE_Therapy
                                st.session_state.data.at[index, "PRVTHER_Prior MWA Therapy"] = PRVTHER_Prior_MWA_Therapy
                                st.session_state.data.at[index, "PRVTHER_Previous Therapy Sum"] = PRVTHER_Previous_Therapy_Sum
                                st.session_state.data.at[index, "PRVTHER_Previous Therapy Date(s) "] = PRVTHER_Previous_Therapy_Dates
                                st.session_state.data.at[index, "PRVTHER_Total Recurrences HCC"] = PRVTHER_Total_Recurrences_HCC
                                st.session_state.data.at[index, "PRVTHER_Binary for ANY Recurrences HCC Binary"] = PRVTHER_Binary_for_ANY_Recurrences_HCC_Binary
                                st.session_state.data.at[index, "PRVTHER_Location of Previous Treatment HCC"] = PRVTHER_Location_of_Previous_Treatment_HCC
                                st.session_state.data.at[index, "PRVTHER_Recurrence Date/Location Free Text"] = PRVTHER_Recurrence_Date_Location_Free_Text
                                st.session_state.data.at[index, "PRVTHER_New HCC Outside Previous Treatment Site"] = PRVTHER_New_HCC_Outside_Previous_Treatment_Site
                                st.session_state.data.at[index, "PRVTHER_New HCC Adjacent to Previous Treatment Site"] = PRVTHER_New_HCC_Adjacent_to_Previous_Treatment_Site
                                st.session_state.data.at[index, "PRVTHER_Residual HCC"] = PRVTHER_Residual_HCC
                                st.session_state.data.at[index, "PRVTHER_Systemic Therapy Free Text"] = PRVTHER_Systemic_Therapy_Free_Text
                                st.session_state.data.at[index, "PRVTHER_Date of Labs in Window"] = PRVTHER_Date_of_Labs_in_Window
                                st.session_state.data.at[index, "PRVTHER_AFP"] = PRVTHER_AFP
                                
                                st.success("Previous Therapy for HCC added successfully.")
                                st.write("Updated Data:")
                                st.dataframe(st.session_state.data)

            with tab6:
                
                    st.subheader("Pre Y90")
                    with st.form("pre_y90_form"):
                        # Fields for Pre Y90
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
                            help="Select all that apply"
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
                        
                        prey90_ascites = st.selectbox(
                            "PREY90_Ascites",
                            options=[
                                "none", 
                                "Asymptomatic", 
                                "Minimal ascities/Mild abd distension, no sx", 
                                "Symptomatic", 
                                "moderate ascities/Symptomatic medical intervention", 
                                "Severe symptoms, invasive intervention indicated", 
                                "Life Threatening: Urgent operation intervention indicated"
                            ],
                            help="Select the appropriate ascites classification"
                        )
                        
                        prey90_ascites_binary = 1 if prey90_ascites != "none" else 0
                        st.info(f"PREY90_Ascites Binary Classification: {prey90_ascites_binary}")
                        
                        prey90_ascites_free_text = st.text_area(
                            "PREY90_Ascites Free Text",
                            "Hospitalized (yes/no): \nDiuretics (yes/no): \nParacentesis (yes/no): \nAny other complications (free_text):",
                            help="Provide details about hospitalization, diuretics, paracentesis, and other complications"
                        )
                        
                        prey90_he = st.selectbox(
                            "PREY90_he", 
                            options=["No", "Yes", "NA (not in chart)"], 
                            help="Select hepatic encephalopathy status"
                        )
                        
                        prey90_ecog = st.selectbox(
                            "PREY90_ecog",
                            options=["0", "1", "2", "3", "4", "NA"],
                            help="Select ECOG Performance Status"
                        )
                        
                        prey90_child_pugh_class = st.selectbox(
                            "PREY90_Child-Pugh Class Emr",
                            options=["Class A", "Class B", "Class C", "NA"],
                            help="Select the Child-Pugh class"
                        )
                        def validate_inputt(value):
                            if value.isdigit() and 5 <= int(value) <= 15:
                                return value  # Valid number
                            elif value.upper() == "NA":
                                return "NA"  # Valid 'NA'
                            else:
                                return "NA" 

                        input_value3t = st.text_input(
                            "PREY90_Child-Pugh Points Emr",
                            help="Write in number in range 5-15, or NA"              
                        )

                        prey90_child_pugh_points = validate_inputt(input_value3t)
                        prey90_bclc_stage = st.selectbox(
                            "PREY90_BCLC Stage EMR",
                            options=["0", "A", "B", "C", "D"],
                            help="Select the BCLC stage"
                        )

                        def validate_input2t(value):
                            if value.isdigit() and 6 <= int(value) <= 40:
                                return value  # Valid number
                            elif value.upper() == "NA":
                                return "NA"  # Valid 'NA'
                            else:
                                return "NA" 

                        input_value4t = st.text_input(
                            "PREY90_MELD Score EMR",
                            help="Write in number in range 6-40, or NA"                
                        )

                        prey90_meld_score = validate_input2t(input_value4t)

                        input_value5t = st.text_input(
                            "PREY90_MELD-Na Score EMR",
                            help="Write in number in range 6-40, or NA"               
                        )

                        prey90_meld_na_score = validate_input2t(input_value5t)
                        
                        prey90_albi_score = st.text_input(
                            "PREY90_ALBI Score EMR",
                            help="Enter ALBI score"
                        )
                        
                        # Claculation of class and points
                        prey90_child_pugh_points_calc = calculatepoints(prey90_bilirubin,prey90_albumin,prey90_inr,prey90_ascites,prey90_he)
                
                        prey90_child_pugh_class_calc = calculate_class(prey90_child_pugh_points_calc)
                        # Additional Calculated Fields
                        
                        #prey90_bclc_stage_calc = st.text_input("PREY90_BCLC Stage calc", help="Enter calculated BCLC stage")
                        prey90_meld_score_calc = (3.78*(int(prey90_bilirubin)))+(11.2*(int(prey90_inr)))+(9.57*(int(prey90_creatinine)))+6.43
                        prey90_meld_na_score_calc = prey90_meld_score_calc + 1.32*(137-int(prey90_sodium)) - (0.033*prey90_meld_score_calc*(137-int(prey90_sodium)))
                        
                        prey90_albi_score_calc = albi_calc(prey90_bilirubin,prey90_albumin)
                    
                        st.subheader("Mapping Y90")
                        my90_date = st.date_input("MY90_date", help="Enter the date")
                        my90_lung_shunt = st.number_input("MY90_Lung_shunt", min_value=0, step=1, help="Enter the lung shunt value")


                        submit_tab4 = st.form_submit_button("Save Pre Y90")

                        if submit_tab4:
                            #index = st.session_state.data[st.session_state.data["MRN"] == st.session_state.temp_mrn].index[0]

                            st.session_state.data.at[index, "PREY90_symptoms"] = prey90_symptoms
                            st.session_state.data.at[index, "PREY90_date of labs in window"] = prey90_date_of_labs.strftime("%Y-%m-%d")
                            st.session_state.data.at[index, "PREY90_AFP"] = prey90_afp
                            st.session_state.data.at[index, "PRE90_AFP Prior to TARE"] = prey90_afp_prior_to_tare
                            st.session_state.data.at[index, "PREY90_Bilirubin"] = prey90_bilirubin
                            st.session_state.data.at[index, "PREY90_Albumin"] = prey90_albumin
                            st.session_state.data.at[index, "PREY90_inr"] = prey90_inr
                            st.session_state.data.at[index, "PREY90_creatinine"] = prey90_creatinine
                            st.session_state.data.at[index, "PREY90_sodium"] = prey90_sodium
                            st.session_state.data.at[index, "PREY90_AST"] = prey90_ast
                            st.session_state.data.at[index, "PREY90_ALT"] = prey90_alt
                            st.session_state.data.at[index, "PREY90_Alkaline Phosphatase"] = prey90_alkaline_phosphatase
                            st.session_state.data.at[index, "PREY90_potassium"] = prey90_potassium
                            st.session_state.data.at[index, "PREY90_Ascites"] = prey90_ascites
                            st.session_state.data.at[index, "PREY90_Ascites Binary Classification"] = prey90_ascites_binary
                            st.session_state.data.at[index, "PREY90_Ascites Free Text"] = prey90_ascites_free_text
                            st.session_state.data.at[index, "PREY90_he"] = prey90_he
                            st.session_state.data.at[index, "PREY90_ecog"] = prey90_ecog
                            st.session_state.data.at[index, "PREY90_Child-Pugh Class Emr"] = prey90_child_pugh_class
                            st.session_state.data.at[index, "PREY90_Child-Pugh Points Emr"] = prey90_child_pugh_points
                            st.session_state.data.at[index, "PREY90_BCLC Stage EMR"] = prey90_bclc_stage
                            st.session_state.data.at[index, "PREY90_MELD Score EMR"] = prey90_meld_score
                            st.session_state.data.at[index, "PREY90_MELD-Na Score EMR"] = prey90_meld_na_score
                            st.session_state.data.at[index, "PREY90_ALBI Score EMR"] = prey90_albi_score
                            st.session_state.data.at[index, "PREY90_Child-Pugh Class calc"] = prey90_child_pugh_class_calc
                            st.session_state.data.at[index, "PREY90_Child-Pugh Points calc"] = prey90_child_pugh_points_calc
                            st.session_state.data.at[index, "PREY90_MELD Score calc"] = prey90_meld_score_calc
                            st.session_state.data.at[index, "PREY90_MELD-Na Score calc"] = prey90_meld_na_score_calc
                            st.session_state.data.at[index, "PREY90_ALBI Score calc"] = prey90_albi_score_calc
                            st.session_state.data.at[index, "MY90_date"] = my90_date
                            st.session_state.data.at[index, "MY90_Lung_shunt"] = my90_lung_shunt

                            st.success("Pre Y90 added successfully.")
                            st.write("Updated Data:")
                            st.dataframe(st.session_state.data)             

            with tab7:
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

            # Process the input
                        dayy90_afp_prior_to_tare = process_input(dayy90_afp)

                        if dayy90_afp_prior_to_tare != 'NA':
                            afp_prey90 = dayy90_afp_prior_to_tare      
                        elif prey90_afp_prior_to_tare != 'NA':
                            afp_prey90 = prey90_afp_prior_to_tare
                        else:
                            afp_prey90 = "NA"
                    
          
                        dayy90_sodium = st.number_input("DAYY90_sodium (mmol/L)")
                        dayy90_creatinine = st.number_input("DAYY90_creatinine (mg/dl)")
                        dayy90_inr = st.number_input("DAYY90_inr")
                        dayy90_albumin = st.number_input("DAYY90_albumin (g/dl)")
                        dayy90_bilirubin = st.number_input("DAYY90_bilirubin (mg/dl)",min_value=1)
                        dayy90_ast = st.number_input("DAYY90_AST (U/L)")
                        dayy90_alt = st.number_input("DAYY90_ALT (U/L)")
                        dayy90_alkaline_phosphatase = st.number_input(
                            "DAYY90_Alkaline Phosphatase (U/L)"
                        )
                        dayy90_leukocytes = st.number_input("DAYY90_leukocytes (value in x10^3/µL)")
                        dayy90_platelets = st.number_input("DAYY90_platelets (value in x10^3/µL)")

                        dayy90_ascites = st.selectbox("DAYY90_ascites", options=["Grade 1", "Grade 2", "Grade 3", "Grade 4", "Grade 5"])
                        dayy90_hepatic_encephalopathy = st.selectbox(
                            "DAYY90_Hepatic Encephalopathy", options=["Grade 1", "Grade 2", "Grade 3", "Grade 4", "Grade 5"]
                        )
                        dayy90_child_pugh_class_emr = st.selectbox(
                            "DAYY90_Child-Pugh class EMR", options=["Class A", "Class B", "Class C", "NA"]
                        )

                        def validate_input(value):
                            if value.isdigit() and 5 <= int(value) <= 15:
                                return value  # Valid number
                            elif value.upper() == "NA":
                                return "NA"  # Valid 'NA'
                            else:
                                return "NA" 

                        input_value3 = st.text_input(
                            "Cirrhosis_Dx_Child-Pugh Points EMR",
                            help="Specify the Child-Pugh points if in EMR 'number 5-15 or NA"                
                        )

                        dayy90_child_pugh_points_emr = validate_input(input_value3)

                        dayy90_bclc_emr = st.selectbox("DAYY90_BCLC EMR", options=["0","A", "B", "C", "D"])

                        def validate_input2(value):
                            if value.isdigit() and 6 <= int(value) <= 40:
                                return value  # Valid number
                            elif value.upper() == "NA":
                                return "NA"  # Valid 'NA'
                            else:
                                return "NA" 

                        input_value4 = st.text_input(
                            "DAYY90_MELD EMR",
                            help="Specify MELD EMR if in EMR 'number 6-40 or NA"                
                        )

                        dayy90_meld_emr = validate_input2(input_value4)

                        input_value5 = st.text_input(
                            "DAYY90_MELD Na EMR",
                            help="Specify DAYY90_MELD Na EMR if in EMR 'number 6-40 or NA"                
                        )
                        dayy90_meld_na_emr = validate_input2(input_value5)

                        dayy90_albi_emr = st.number_input("DAYY90_Albi EMR")

                        prey90_ecog = st.selectbox("PREY90_ECOG", options=["0", "1", "2", "3", "4", "NA"])
                        dayy90_child_pugh_points_calc = calculatepoints(dayy90_bilirubin,dayy90_albumin,dayy90_inr,dayy90_ascites,dayy90_hepatic_encephalopathy)
                        dayy90_child_pugh_class_calc = calculate_class(dayy90_child_pugh_points_calc)
                        # Formula Calculation
                        dayy90_meld_calc = (3.78*(int(dayy90_bilirubin)))+(11.2*(int(dayy90_inr)))+(9.57*(int(dayy90_creatinine)))+6.43
                        dayy90_meld_na_calc = dayy90_meld_calc + 1.32*(137-int(dayy90_sodium)) - (0.033*dayy90_meld_calc*(137-int(dayy90_sodium)))
                        

                        def albi_calc(a,b):
                            a=int(a)
                            b=int(b)
                            t = math.log(a, 10)
                            answer = (t * 0.66) + (b * -0.085)
                            return answer
                        
                        dayy90_albi_calc = albi_calc(dayy90_bilirubin,dayy90_albumin)
                     
                        dayy90_type_of_sphere = st.selectbox(
                            "DAYY90_Type of Sphere", options=["Therasphere-1", "SIR-2"]
                        )

                        dayy90_lt_notes_ftx = st.text_area("DAYY90_LT Notes (Free Text)")

                        ken_childpughscore = st.number_input("ken_ChildPughscore")
                        ken_meldpretare = st.number_input("ken_MELDpreTARE")


                    # Submit button
                        submit_tab7 = st.form_submit_button("Submit")
                    
                        if submit_tab7:
                            #index = st.session_state.data[st.session_state.data["MRN"] == st.session_state.temp_mrn].index[0]

                            st.session_state.data.at[index, "DAYY90_AFP"] = dayy90_afp
                            st.session_state.data.at[index, "DAYY90_AFP Prior to TARE"] = dayy90_afp_prior_to_tare
                            st.session_state.data.at[index, "AFP_PreY90 or DAYY90"] = afp_prey90
                            st.session_state.data.at[index, "DAYY90_sodium"] = dayy90_sodium
                            st.session_state.data.at[index, "DAYY90_creatinine"] = dayy90_creatinine
                            st.session_state.data.at[index, "DAYY90_inr"] = dayy90_inr
                            st.session_state.data.at[index, "DAYY90_albumin"] = dayy90_albumin
                            st.session_state.data.at[index, "DAYY90_bilirubin"] = dayy90_bilirubin
                            st.session_state.data.at[index, "DAYY90_AST"] = dayy90_ast
                            st.session_state.data.at[index, "DAYY90_ALT"] = dayy90_alt
                            st.session_state.data.at[index, "DAYY90_Alkaline Phosphatase"] = dayy90_alkaline_phosphatase
                            st.session_state.data.at[index, "DAYY90_leukocytes"] = dayy90_leukocytes
                            st.session_state.data.at[index, "DAYY90_platelets"] = dayy90_platelets
                            st.session_state.data.at[index, "DAYY90_ascities"] = dayy90_ascites
                            st.session_state.data.at[index, "DAYY90_Hepatic Encephalopathy"] = dayy90_hepatic_encephalopathy
                            st.session_state.data.at[index, "DAYY90_Child-Pugh class EMR"] = dayy90_child_pugh_class_emr
                            st.session_state.data.at[index, "DAYY90_Child-Pugh points EMR"] = dayy90_child_pugh_points_emr
                            st.session_state.data.at[index, "DAYY90_BCLC EMR"] = dayy90_bclc_emr
                            st.session_state.data.at[index, "DAYY90_MELD EMR"] = dayy90_meld_emr
                            st.session_state.data.at[index, "DAYY90_MELD Na EMR"] = dayy90_meld_na_emr
                            st.session_state.data.at[index, "DAYY90_Albi EMR"] = dayy90_albi_emr
                            st.session_state.data.at[index, "PREY90_ECOG"] = prey90_ecog
                            st.session_state.data.at[index, "DAYY90_Child-Pugh class Calc"] = dayy90_child_pugh_class_calc
                            st.session_state.data.at[index, "DAYY90_Child-Pugh points calc"] = dayy90_child_pugh_points_calc
                            st.session_state.data.at[index, "DAYY90_MELD calc"] = dayy90_meld_calc
                            st.session_state.data.at[index, "DAYY90_MELD Na calc"] = dayy90_meld_na_calc
                            st.session_state.data.at[index, "DAYY90_Albi calc"] = dayy90_albi_calc
                            st.session_state.data.at[index, "DAYY90_Type of Sphere"] = dayy90_type_of_sphere
                            st.session_state.data.at[index, "DAYY90_LT_notes_ftx"] = dayy90_lt_notes_ftx
                            st.session_state.data.at[index, "ken_ChildPughscore"] = ken_childpughscore
                            st.session_state.data.at[index, "ken_MELDpreTARE"] = ken_meldpretare
                            
                            st.success("DAYY90 added successfully.")
                            st.write("Updated Data:")
                            st.dataframe(st.session_state.data)
            
            with tab8:
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

                            posty90_ecog = st.selectbox(
                                "POSTY90_30DY_ECOG",
                                options=["0", "1", "2", "3", "4", "NA"],
                                help="Select ECOG Performance Status"
                            )

                            posty90_child_pugh_class = st.selectbox(
                                "POSTY90_30DY_Child-Pugh Class EMR",
                                options=["Class A", "Class B", "Class C", "NA"],
                                help="Select the Child-Pugh class"
                            )

                            inputp90 = st.text_input(
                                "POSTY90_30DY_Child-Pugh Points EMR",
                                help="Write in number in range 5-15, or NA"
                            )
                            posty90_child_pugh_points = validate_input(inputp90)

                            posty90_bclc_emr = st.selectbox(
                                "POSTY90_30DY_BCLC EMR",
                                options=["0", "A", "B", "C", "D"],
                                help="Select the BCLC stage"
                            )

                            input_meld = st.text_input(
                                "POSTY90_30DY_MELD EMR",
                                help="Write in number in range 6-40, or NA"
                            )
                            posty90_meld_emr = validate_input2(input_meld)


                            input_meld_na = st.text_input(
                                "POSTY90_30DY_MELD Na EMR",
                                help="Write in number in range 6-40, or NA"
                            )
                            posty90_meld_na_emr = validate_input2(input_meld_na)

                            posty90_albi_emr = st.number_input(
                                "POSTY90_30DY_ALBI EMR",
                                help="Enter ALBI score"
                            )

                            posty90_child_pugh_points_calc = calculatepoints(posty90_bilirubin,posty90_albumin,posty90_inr,prey90_ascites,prey90_he)
                            posty90_child_pugh_class_calc = calculate_class(posty90_child_pugh_points_calc)
                          
                            posty90_meld_calc = (3.78*(int(posty90_bilirubin)))+(11.2*(int(posty90_inr)))+(9.57*(int(posty90_creatinine)))+6.43
                            posty90_meld_na_calc = posty90_meld_calc + 1.32*(137-int(posty90_sodium)) - (0.033*posty90_meld_calc*(137-int(posty90_sodium)))


                            posty90_albi_calc = albi_calc(posty90_bilirubin,posty90_albumin)

                            ken_bclc_stage_post90 = st.text_input(
                                "Ken_BCLCStagepost90",
                                help="Enter BCLC Stage Post-90"
                            )

                            ken_meld_stage_post90 = st.text_input(
                                "Ken_MELD_Stagepost90",
                                help="Enter MELD Score Pre-TARE"
                            )

                            st.subheader("Post_Y90_within_30_days_adverse_events")
                            DYAE_CTCAE_portal_htn = st.selectbox(
                                "30DYAE_CTCAE_portal_htn",
                                options=["0","1","2","3","4","5"]
                            )
                            DYAE_CTCAE_Vascular_comp = st.selectbox(
                                "30DYAE_CTCAE_Vascular comp",
                                options=["0","1","2","3","4","5"]
                            )
                            DYAE_CTCAE_fatigue = st.selectbox(
                                "30DYAE_CTCAE_fatigue",
                                options=["0","1","2"]
                            )
                            DYAE_CTCAE_diarrhea = st.selectbox(
                                "30DYAE_CTCAE_diarrhea",
                                options=["0","1","2","3","4","5"]
                            )

                            DYAE_CTCAE_hypoalbuminemia_emr = st.text_input(
                                "30DYAE_CTCAE_hypoalbuminemia emr"
                            )
                            DYAE_CTCAE_hyperbilirubinemia_emr = st.text_input(
                                "30DYAE_CTCAE_hyperbilirubinemia emr"
                            )
                            DYAE_CTCAE_Increase_creatinine_emr = st.text_input(
                                "30DYAE_CTCAE_Increase_creatinine emr"
                            )
                            DYAE_CTCAE_abdominal_pain = st.selectbox(
                                "30DYAE_CTCAE_abdominal pain",
                                options=["0","1","2","3"]
                            )
                            DYAE_CTCAE_sepsis = st.selectbox(
                                "30DYAE_CTCAE_sepsis",
                                options=["0","3","4","5"]
                            )
                            DYAE_CTCAE_ascites = st.selectbox(
                            "30DYAE_CTCAE_ascites",
                            options=["none", "Asymptomatic", "Minimal ascities/Mild abd distension, no sx",
                                    "Symptomatic", "moderate ascities/Symptomatic medical intervention",
                                    "Severe symptoms, invasive intervention indicated",
                                    "Life Threatening: Urgent operation intervention indicated"]
                            )
                            DYAE_CTCAE_ascites_binary_classification = 1 if DYAE_CTCAE_ascites != "none" else 0
                            DYAE_CTCAE_ascites_ftx = st.text_area(
                                "30DYAE_CTCAE_ascites_ftx",
                            )

                            DYAE_CTCAE_bacterial_peritonitis = st.selectbox(
                                "30DYAE_CTCAE_bacterial_peritonitis",
                                options=["0", "3", "4", "5"]
                            )

                            DYAE_CTCAE_hemorrhage = st.selectbox(
                            "30DYAE_CTCAE_hemorrhage",
                            options=["0", "3", "4", "5"]
                            )

                            DYAE_CTCAE_anorexia = st.selectbox(
                                "30DYAE_CTCAE_anorexia",
                                options=["0", "1", "2", "3"]
                            )

                            DYAE_CTCAE_intrahepatic_fistula = st.selectbox(
                                "30DYAE_CTCAE_intrahepatic_fistula",
                                options=["0","2", "3", "4", "5"]
                            )

                            DYAE_CTCAE_constipation = st.selectbox(
                                "30DYAE_CTCAE_constipation",
                                options=["0", "1", "2", "3"]
                            )

                            DYAE_CTCAE_nausea = st.selectbox(
                                "30DYAE_CTCAE_nausea",
                                options=["0", "1", "2", "3"]
                            )

                            DYAE_CTCAE_vomiting = st.selectbox(
                                "30DYAE_CTCAE_vomiting",
                                options=["0","1","2", "3", "4", "5"]
                            )

                            DYAE_CTCAE_Hepatic_Encephalopathy = st.selectbox(
                                "30DYAE_CTCAE_Hepatic Encephalopathy",
                                options=["0","1","2", "3", "4", "5"]
                            )

                            DYAE_CTCAE_he_ftx = st.text_area(
                                "30DYAE_CTCAE_he_ftx",
                                help="provide additional details of he"
                            )

                            DYAE_CTCAE_cholecystitis = st.selectbox(
                                "30DYAE_CTCAE_cholecystitis",
                                options=["0", "2","3", "4", "5"]
                            )

                            DYAE_CTCAE_gastric_ulcers = st.selectbox(
                                "30DYAE_CTCAE_gastric_ulcers",
                                options=["0","1","2", "3", "4", "5"]
                            )

                            DYAE_CTCAE_hyperkalemia = st.selectbox(
                                "30DYAE_CTCAE_hyperkalemia",
                                options=["NA"]
                            )

                            DYAE_CTCAE_respiratory_failure = st.selectbox(
                                "30DYAE_CTCAE_respiratory_failure",
                                options=["0", "4", "5"]
                            )

                            DYAE_CTCAE_AKI = st.selectbox(
                                "30DYAE_CTCAE_AKI",
                                options=["0", "3", "4", "5"]
                            )

                            DYAE_CTCAE_Radiation_pneumonitis = st.selectbox(
                                "30DYAE_CTCAE_Radiation_pneumonitis",
                                options=["0","1","2", "3", "4", "5"]
                            )

                            DYAE_AE_other = st.text_area(
                                "30DY_AE_other",
                                help="Other Adverse Events (Free Text)"
                            )

                            DYAE_AE_date_of_AE = st.text_input(
                                "90DY_AE_date_of_AE",
                                help="(if AE is present after 30 days but before 90 write it here and the date)"
                            )
                            


                            submit_tab8 = st.form_submit_button("Save Post POST90 Labs")

                            if submit_tab8:
                                    
                                    #index = st.session_state.data[st.session_state.data["MRN"] == st.session_state.temp_mrn].index[0]
                                
                                    st.session_state.data.at[index, "POSTY90_30DY_date_labs"] = posty90_date_labs.strftime("%Y-%m-%d")
                                    st.session_state.data.at[index, "POSTY90_30DY_afp"] = posty90_afp
                                    st.session_state.data.at[index, "POSTY90_30DY_afp DATE"] = posty90_afp_date.strftime("%Y-%m-%d")
                                    st.session_state.data.at[index, "POSTY90_30DY_Sodium"] = posty90_sodium
                                    st.session_state.data.at[index, "POSTY90_30DY_creatinine"] = posty90_creatinine
                                    st.session_state.data.at[index, "POSTY90_30DY_INR"] = posty90_inr
                                    st.session_state.data.at[index, "POSTY90_30DY_albumin"] = posty90_albumin
                                    st.session_state.data.at[index, "POSTY90_30DY_bilirubin"] = posty90_bilirubin
                                    st.session_state.data.at[index, "POSTY90_30DY_AST"] = posty90_ast
                                    st.session_state.data.at[index, "POSTY90_30DY_ALT"] = posty90_alt
                                    st.session_state.data.at[index, "POSTY90_30DY_Alkaline Phosphatase"] = posty90_alkaline_phosphatase
                                    st.session_state.data.at[index, "POSTY90_30DY_leukocytes"] = posty90_leukocytes
                                    st.session_state.data.at[index, "POSTY90_30DY_platelets"] = posty90_platelets
                                    st.session_state.data.at[index, "POSTY90_30DY_potassium"] = posty90_potassium
                                    st.session_state.data.at[index, "POSTY90_30DY_ECOG"] = posty90_ecog
                                    st.session_state.data.at[index, "POSTY90_30DY_Child-Pugh Class EMR"] = posty90_child_pugh_class
                                    st.session_state.data.at[index, "POSTY90_30DY_Child-Pugh Points EMR"] = posty90_child_pugh_points
                                    st.session_state.data.at[index, "POSTY90_30DY_BCLC EMR"] = posty90_bclc_emr
                                    st.session_state.data.at[index, "POSTY90_30DY_MELD EMR"] = posty90_meld_emr
                                    st.session_state.data.at[index, "POSTY90_30DY_MELD Na EMR"] = posty90_meld_na_emr
                                    st.session_state.data.at[index, "POSTY90_30DY_ALBI EMR"] = posty90_albi_emr
                                    st.session_state.data.at[index, "POSTY90_30DY_Child-Pugh Class calc"] = posty90_child_pugh_class_calc
                                    st.session_state.data.at[index, "POSTY90_30DY_Child-Pugh Points calc"] = posty90_child_pugh_points_calc
                                    st.session_state.data.at[index, "POSTY90_30DY_MELD calc"] = posty90_meld_calc
                                    st.session_state.data.at[index, "POSTY90_30DY_MELD Na calc"] = posty90_meld_na_calc
                                    st.session_state.data.at[index, "POSTY90_30DY_ALBI calc"] = posty90_albi_calc
                                    st.session_state.data.at[index, "Ken_BCLCStagepost90"] = ken_bclc_stage_post90
                                    st.session_state.data.at[index, "Ken_MELD_Stagepost90"] = ken_meld_stage_post90
                                    st.session_state.data.at[index, "30DYAE_CTCAE_portal_htn"] = DYAE_CTCAE_portal_htn
                                    st.session_state.data.at[index, "30DYAE_CTCAE_Vascular_comp"] = DYAE_CTCAE_Vascular_comp
                                    st.session_state.data.at[index, "30DYAE_CTCAE_fatigue"] = DYAE_CTCAE_fatigue
                                    st.session_state.data.at[index, "30DYAE_CTCAE_diarrhea"] = DYAE_CTCAE_diarrhea
                                    st.session_state.data.at[index, "30DYAE_CTCAE_hypoalbuminemia_emr"] = DYAE_CTCAE_hypoalbuminemia_emr
                                    st.session_state.data.at[index, "30DYAE_CTCAE_hyperbilirubinemia_emr"] = DYAE_CTCAE_hyperbilirubinemia_emr
                                    st.session_state.data.at[index, "30DYAE_CTCAE_Increase_creatinine_emr"] = DYAE_CTCAE_Increase_creatinine_emr
                                    st.session_state.data.at[index, "30DYAE_CTCAE_abdominal_pain"] = DYAE_CTCAE_abdominal_pain
                                    st.session_state.data.at[index, "30DYAE_CTCAE_sepsis"] = DYAE_CTCAE_sepsis
                                    st.session_state.data.at[index, "30DYAE_CTCAE_ascites"] = DYAE_CTCAE_ascites
                                    st.session_state.data.at[index, "30DYAE_CTCAE_ascites_Binary_classification"] = DYAE_CTCAE_ascites_binary_classification
                                    st.session_state.data.at[index, "30DYAE_CTCAE_ascites_ftx"] = DYAE_CTCAE_ascites_ftx
                                    st.session_state.data.at[index, "30DYAE_CTCAE_bacterial_peritonitis"] = DYAE_CTCAE_bacterial_peritonitis
                                    st.session_state.data.at[index, "30DYAE_CTCAE_hemorrhage"] = DYAE_CTCAE_hemorrhage
                                    st.session_state.data.at[index, "30DYAE_CTCAE_anorexia"] = DYAE_CTCAE_anorexia
                                    st.session_state.data.at[index, "30DYAE_CTCAE_intrahepatic_fistula"] = DYAE_CTCAE_intrahepatic_fistula
                                    st.session_state.data.at[index, "30DYAE_CTCAE_constipation"] = DYAE_CTCAE_constipation
                                    st.session_state.data.at[index, "30DYAE_CTCAE_nausea"] = DYAE_CTCAE_nausea
                                    st.session_state.data.at[index, "30DYAE_CTCAE_vomiting"] = DYAE_CTCAE_vomiting
                                    st.session_state.data.at[index, "30DYAE_CTCAE_Hepatic_Encephalopathy"] = DYAE_CTCAE_Hepatic_Encephalopathy
                                    st.session_state.data.at[index, "30DYAE_CTCAE_he_ftx"] = DYAE_CTCAE_he_ftx
                                    st.session_state.data.at[index, "30DYAE_CTCAE_cholecystitis"] = DYAE_CTCAE_cholecystitis
                                    st.session_state.data.at[index, "30DYAE_CTCAE_gastric_ulcers"] = DYAE_CTCAE_gastric_ulcers
                                    st.session_state.data.at[index, "30DYAE_CTCAE_hyperkalemia"] = DYAE_CTCAE_hyperkalemia
                                    st.session_state.data.at[index, "30DYAE_CTCAE_respiratory_failure"] = DYAE_CTCAE_respiratory_failure
                                    st.session_state.data.at[index, "30DYAE_CTCAE_AKI"] = DYAE_CTCAE_AKI
                                    st.session_state.data.at[index, "30DYAE_CTCAE_Radiation_pneumonitis"] = DYAE_CTCAE_Radiation_pneumonitis
                                    st.session_state.data.at[index, "30DY_AE_other"] = DYAE_AE_other
                                    st.session_state.data.at[index, "90DY_AE_date_of_AE"] = DYAE_AE_date_of_AE

                                    st.success("DAYY90 added successfully.")
                                    st.write("Updated Data:")
                                    st.dataframe(st.session_state.data)
                    
  
# Main App Logic
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


