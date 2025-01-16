import streamlit as st
import pandas as pd
from datetime import datetime
import math

def calculate_comorbidities_total(hypertension, diabetes, hypercholesterolemia, smoking, obesity):
    """Calculate total number of comorbidities"""
    conditions = [hypertension, diabetes, hypercholesterolemia, smoking, obesity]
    return sum(1 for condition in conditions if condition == 1)

def calculate_comorbidities_binary(total_count):
    """Convert total count to binary (1 if >=1, 0 if 0)"""
    return 1 if total_count >= 1 else 0

def main():
    import math
    st.title("Patient Information System")

    # Initialize session state for form data if it doesn't exist
    if 'form_data' not in st.session_state:
        st.session_state.form_data = []

    # Create tabs
    tab1, tab2, tab3, tab5, tab7, tab9 = st.tabs(["Patient Info", "Patient Demographics", "Cirrhosis PMH", "Previous Therapy for HCC","Day_Y90","Other_post_TARE"])

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
            
            submit_tab1 = st.form_submit_button("Save & Continue")
            
            if submit_tab1:
                if not all([last_name, first_name, mrn, tare_date, age]):
                    st.error("Please fill in all required fields.")
                else:
                    st.session_state['tab1_data'] = {
                        "Name": f"{last_name}, {first_name}",
                        "MRN": mrn,
                        "TARE_Tx_Date": tare_date.strftime("%Y-%m-%d"),
                        "Procedure_Technique": procedure_technique,
                        "Age_at_TARE": age
                    }
                    st.success("Patient information saved! Please proceed to Demographics tab.")

    with tab2:
        st.subheader("Patient Demographics")
        with st.form("demographics_form"):
            # Gender dropdown
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

            submit_tab2 = st.form_submit_button("Submit Demographics")

            if submit_tab2:
                if 'tab1_data' not in st.session_state:
                    st.error("Please fill out Patient Info tab first!")
                else:
                    # Combine data from both tabs
                    combined_data = {
                        **st.session_state['tab1_data'],
                        "Gender": gender,
                        "Ethnicity": ethnicity,
                        "Hypertension": hypertension,
                        "Diabetes": diabetes,
                        "Hypercholesterolemia": hypercholesterolemia,
                        "Smoking_History": smoking,
                        "Obesity": obesity,
                        "Comorbidities_Total": total_count,
                        "Comorbidities_Binary": binary_value
                    }
                    
                    st.session_state.form_data.append(combined_data)
                    st.success("All information submitted successfully!")
   
    with tab3:
        st.subheader("Cirrhosis PMH")
        with st.form("cirrhosis_pmh_form"):
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
                if 'tab1_data' not in st.session_state:
                    st.error("Please fill out Patient Info tab first!")
                else:
                    cirrhosis_pmh_data = {
                        "Cir_PMH_HBV Status": cir_pmh_hbv_status,
                        "Cir_PMH_HBV Free Text": cir_pmh_hbv_free_text,
                        "Cir_PMH_HBV ART": cir_pmh_hbv_art,
                        "Cir_PMH_HCV Status": cir_pmh_hcv_status,
                        "Cir_PMH_HCV Free Text": cir_pmh_hcv_free_text,
                        "Cir_PMH_HCV ART" : cir_pmh_hcv_art,
                        "Cir_PMH_Alcohol Use Disorder" : cir_pmh_alcohol_use_disorder,
                        "Cir_PMH_Duration of Alcohol Use Years" : cir_pmh_duration_of_alcohol_use_years,
                        "Cir_PMH_Alcohol Free Text" : cir_pmh_alcohol_free_text,
                        "Cir_PMH_IVDU Status" : cir_pmh_ivdu_status,
                        "Cir_PMH_Duration of IVDU Years" : cir_pmh_duration_of_ivdu_years,
                        "Cir_PMH_IVDU Free Text" : cir_pmh_ivdu_free_text,
                        "Cir_PMH_Other Contributing Factors" : cir_pmh_other_contributing_factors,
                        "Cirrhosis_Dx_Diagnosis Date" : Cirrhosis_Dx_Diagnosis_Date,
                        "Cirrhosis_Dx_Diagnosis Method" : Cirrhosis_Dx_Diagnosis_Method,
                        "Cirrhosis_Dx_HPI EMR Note Free Text" : Cirrhosis_Dx_HPI_EMR_Note_Free_Text,
                        "Cirrhosis_Dx_Imaging Findings EMR Note Free Text" : Cirrhosis_Dx_Imaging_Findings_EMR_Note_Free_Text,
                        "Cirrhosis_Dx_Metavir Score" : Cirrhosis_Dx_Metavir_Score,
                        "Cirrhosis_Dx_Complications at Time of Diagnosis" : Cirrhosis_Dx_Complications_at_Time_of_Diagnosis,
                        "Cirrhosis_Dx_Complications at Time of Diagnosis Binary" : Cirrhosis_Dx_Complications_at_Time_of_Diagnosis_Binary,
                        "Cirrhosis_Dx_Complications Free Text" : Cirrhosis_Dx_Complications_Free_Text,
                        "Cirrhosis_Dx_Date of Labs in Window" : Cirrhosis_Dx_Date_of_Labs_in_Window,
                        "Cirrhosis_Dx_AFP" : Cirrhosis_Dx_AFP,
                        "Cirrhosis_Dx_AFP_L3" : Cirrhosis_Dx_AFP_L3,
                        "Cirrhosis_Dx_Child-Pugh Class EMR" : Cirrhosis_Dx_Child_Pugh_Class_EMR,
                        "Cirrhosis_Dx_Child-Pugh Points EMR" : Cirrhosis_Dx_Child_Pugh_Points_EMR,
                        "Cirrhosis_Dx_MELD Score EMR" : Cirrhosis_Dx_MELD_Score_EMR,
                        "Cirrhosis_Dx_MELD-Na Score EMR" : Cirrhosis_Dx_MELD_NA_Score_EMR,
                        "Cirrhosis_Dx_Ascites" : Cirrhosis_Dx_Ascites,
                        "Cirrhosis_Dx_Ascites Binary Classification" : Cirrhosis_Dx_Ascites_Binary_Classification,
                        "Cirrhosis_Dx_Ascites Free Text" : Cirrhosis_Dx_Ascites_Free_Text,
                        "Cirrhosis_Dx_Ascites Labs Free Text" : Cirrhosis_Dx_Ascites_Labs_Free_Text,
                        "Cirrhosis_Dx_Hepatic Encephalopathy" : Cirrhosis_Dx_Hepatic_Encephalopathy
                    }
                    st.session_state.form_data.append(cirrhosis_pmh_data)
                    st.success("Cirrhosis PMH information saved successfully!")
    
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
                if 'tab1_data' not in st.session_state:
                    st.error("Please fill out Patient Info tab first!")
                else:
                    previous_therapy_data = {
                        "PRVTHER_Prior LDT Therapy": PRVTHER_Prior_LDT_Therapy,
                        "PRVTHER_Prior RFA Therapy" : PRVTHER_Prior_RFA_Therapy,
                        "PRVTHER_Prior TARE Therapy" : PRVTHER_Prior_TARE_Therapy,
                        "PRVTHER_Prior SBRT Therapy" : PRVTHER_Prior_SBRT_Therapy,
                        "PRVTHER_Prior TACE Therapy" : PRVTHER_Prior_TACE_Therapy,
                        "PRVTHER_Prior MWA Therapy" : PRVTHER_Prior_MWA_Therapy,
                        "PRVTHER_Previous Therapy Sum" : PRVTHER_Previous_Therapy_Sum,
                        "PRVTHER_Previous Therapy Date(s) " : PRVTHER_Previous_Therapy_Dates,
                        "PRVTHER_Total Recurrences HCC" : PRVTHER_Total_Recurrences_HCC,
                        "PRVTHER_Binary for ANY Recurrences HCC Binary" : PRVTHER_Binary_for_ANY_Recurrences_HCC_Binary,
                        "PRVTHER_Location of Previous Treatment HCC" : PRVTHER_Location_of_Previous_Treatment_HCC,
                        "PRVTHER_Recurrence Date/Location Free Text" : PRVTHER_Recurrence_Date_Location_Free_Text,
                        "PRVTHER_New HCC Outside Previous Treatment Site" : PRVTHER_New_HCC_Outside_Previous_Treatment_Site,
                        "PRVTHER_New HCC Adjacent to Previous Treatment Site" : PRVTHER_New_HCC_Adjacent_to_Previous_Treatment_Site,
                        "PRVTHER_Residual HCC" : PRVTHER_Residual_HCC,
                        "PRVTHER_Systemic Therapy Free Text" : PRVTHER_Systemic_Therapy_Free_Text,
                        "PRVTHER_Date of Labs in Window" : PRVTHER_Date_of_Labs_in_Window,
                        "PRVTHER_AFP" : PRVTHER_AFP
                    }
                    st.session_state.form_data.append(previous_therapy_data)
                    st.success("Previous therapy information saved successfully!")

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

            inputx = st.text_input("DAYY90_AFP", placeholder="Enter AFP value in ng/dl or NA")
           

# Calucation of DAYY90_AFP Prior to TARE 
            

# Process the input
            dayy90_afp_prior_to_tare = process_input(inputx)
           
            
            
   

# Calculation of AFP_PreY90 or DAYY90
            if dayy90_afp_prior_to_tare != 'NA':
                afp_prey90 = dayy90_afp_prior_to_tare      
            elif pre90_afp_prior_to_tare != 'NA':
                afp_prey90 = pre90_afp_prior_to_tare
            else:
                afp_prey90 = "NA"
          
   
        # Inputs for other variables
            dayy90_sodium = st.number_input("DAYY90_sodium (mmol/L)")
            dayy90_creatinine = st.number_input("DAYY90_creatinine (mg/dl)")
            dayy90_inr = st.number_input("DAYY90_inr")
            dayy90_albumin = st.number_input("DAYY90_albumin (g/dl)")
            dayy90_bilirubin = st.number_input("DAYY90_bilirubin (mg/dl)", value=0)
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


            
           # dayy90_child_pugh_points_emr = st.number_input(
            #     "DAYY90_Child-Pugh points EMR", min_value=5, max_value=15
            #)

            
    
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
            # Formula Calculation
            dayy90_meld_calc = (3.78*(int(dayy90_bilirubin)))+(11.2*(int(dayy90_inr)))+(9.57*(int(dayy90_creatinine)))+6.43
            dayy90_meld_na_calc = dayy90_meld_calc + 1.32*(137-int(dayy90_sodium)) - (0.033*dayy90_meld_calc*(137-int(dayy90_sodium)))
            #dayy90_albi_calc = ((math.log(int(dayy90_bilirubin)))*(0.66))+(dayy90_albumin*(-0.085))
            dayy90_bilirubin = float(dayy90_bilirubin)
            dayy90_albumin = float(dayy90_albumin)
            #dayy90_albi_calc = (math.log(dayy90_bilirubin) * 0.66) + (dayy90_albumin * -0.085)


            dayy90_child_pugh_class_calc = st.text_input("DAYY90_Child-Pugh class Calc (formula)")
            dayy90_child_pugh_points_calc = st.text_input("DAYY90_Child-Pugh points Calc (formula)")
            dayy90_bclc_calc = st.text_input("DAYY90_BCLC Calc (formula)")
            #dayy90_meld_calc = st.text_input("DAYY90_MELD Calc (formula)")
            #dayy90_meld_na_calc = st.text_input("DAYY90_MELD Na Calc (formula)")
            #dayy90_albi_calc = st.text_input("DAYY90_Albi Calc (formula)")

            dayy90_type_of_sphere = st.selectbox(
                "DAYY90_Type of Sphere", options=["Therasphere-1", "SIR-2"]
            )

            dayy90_lt_notes_ftx = st.text_area("DAYY90_LT Notes (Free Text)")

            ken_childpughscore = st.number_input("ken_ChildPughscore")
            ken_meldpretare = st.number_input("ken_MELDpreTARE")


        # Submit button
            submit_tab7 = st.form_submit_button("Submit")
            if submit_tab7:
                if 'tab1_data' not in st.session_state:
                    st.error("Please fill out Patient Info tab first!")
            else:
                dayy90_data = {
                      "DAYY90_AFP" : dayy90_afp,
                      "DAYY90_AFP Prior to TARE " : dayy90_afp_prior_to_tare,
                      "AFP_PreY90 or DAYY90" : afp_prey90,
                      "DAYY90_sodium" : dayy90_sodium,
                      "DAYY90_creatinine" : dayy90_creatinine,
                      "DAYY90_inr" : dayy90_inr,
                      "DAYY90_albumin" : dayy90_albumin,
                      "DAYY90_bilirubin" : dayy90_bilirubin,
                      "DAYY90_AST" : dayy90_ast,
                      "DAYY90_ALT" : dayy90_alt,
                      "DAYY90_Alkaline Phosphatase" : dayy90_alkaline_phosphatase,
                      "DAYY90_leukocytes" : dayy90_leukocytes,
                      "DAYY90_platelets" : dayy90_platelets,
                      "DAYY90_ascities" : dayy90_ascites,
                      "DAYY90_Hepatic Encephalopathy" : dayy90_hepatic_encephalopathy,
                      "DAYY90_Child-Pugh class EMR" : dayy90_child_pugh_class_emr,
                      "DAYY90_Child-Pugh points EMR" : dayy90_child_pugh_points_emr,
                      "DAYY90_BCLC EMR" : dayy90_bclc_emr,
                      "DAYY90_MELD EMR" : dayy90_meld_emr,
                      "DAYY90_MELD Na EMR" : dayy90_meld_na_emr,
                      "DAYY90_Albi EMR" : dayy90_albi_emr,
                      "PREY90_ECOG" : prey90_ecog,
                      "DAYY90_Child-Pugh class Calc" : dayy90_child_pugh_class_calc,
                      "DAYY90_Child-Pugh points calc" : dayy90_child_pugh_points_calc,
                      "DAYY90_BCLC calc" : dayy90_bclc_calc,
                      "DAYY90_MELD calc" : dayy90_meld_calc,
                      "DAYY90_MELD Na calc" : dayy90_meld_na_calc,
                      #"DAYY90_Albi calc" : dayy90_albi_calc,
                      "DAYY90_Type of Sphere" : dayy90_type_of_sphere,
                      "DAYY90_LT_notes_ftx" : dayy90_lt_notes_ftx,
                      "ken_ChildPughscore" : ken_childpughscore,
                      "ken_MELDpreTARE" : ken_meldpretare


                    
                    
                }
                st.session_state.form_data.append(dayy90_data)
                st.success("Day Y90 saved successfully!")

    with tab9:
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

                k_ken_albipretareraw = st.number_input("K_ken_AlbiPreTARERaw (Raw ALBI Score Pre-TARE)")
                k_ken_albipretaregrade = st.text_input("K_ken_AlbiPreTAREGrade (ALBI Grade Pre-TARE)")
                k_ken_albiposttareraw = st.number_input("K_ken_AlbiPostTARERaw (Raw ALBI Score After TARE)")
                k_ken_albiposttaregrade = st.text_input("K_ken_AlbiPostTAREGrade (ALBI Grade Post-TARE)")

                submit_tab9 = st.form_submit_button("Submit Other_Post_Tare")

                if submit_tab9:
                    if 'tab1_data' not in st.session_state:
                        st.error("Please fill out Patient Info tab first!")
                    else:
                        k_other_data = {
                            "OC_Liver_transplant" : oc_liver_transplant,
                            "OC_Liver_transplant_date" : oc_liver_transplant_date,
                            "K_ken_ToxgtG3" : k_ken_toxgtg3,
                            "K_ken_ToxgtG2" : k_ken_toxgtg2,
                            "K_ken_AlbiPreTARERaw" : k_ken_albipretareraw,
                            "K_ken_AlbiPreTAREGrade" : k_ken_albipretaregrade,
                            "K_ken_AlbiPostTARERaw" : k_ken_albiposttareraw,
                            "K_ken_AliPostTAREGrade" : k_ken_albiposttaregrade
                        }
                        st.session_state.form_data.append(k_other_data)
                        st.success("Information saved successfully!")

    # Display submitted data in a table
    if st.session_state.form_data:
        st.subheader("Submitted Patient Records")
        df = pd.DataFrame(st.session_state.form_data)
        st.dataframe(df)

        # Export option
        if st.button("Export Data"):
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"patient_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )

if __name__ == "__main__":
    main()