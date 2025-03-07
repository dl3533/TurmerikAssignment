import csv
import openai

import pandas as pd

# Ensure OpenAI API key is set
client = openai.OpenAI(api_key="YOUR-OWN-KEY")
def check_eligibility(patient, trial):
    """
    Compare a patient's data with trial requirements using OpenAI API.
    """
    prompt = f"""
    Trial Requirements:
    Trial Name: {trial['trial_name']}
    Age Range: {trial['age_range']}
    Preferred Gender: {trial['gender']}
    Inclusion Criteria: {trial['inclusion_criteria']}
    Exclusion Criteria: {trial['exclusion_criteria']}
    
    Patient Info:
    Patient ID: {patient['patient_id']}
    Name: {patient['name']}
    Gender: {patient['gender']}
    Race: {patient['race']}
    Immunizations: {patient['immunizations']}
    Medications: {patient['medications']}
    Medical Conditions: {patient['medical_conditions']}
    Other Medical Conditions: {patient['other_medical_conditions']}
    
    Does the patient meet the eligibility criteria for the trial? Respond with 'Yes' or 'No'. If 'No', explain why.
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that evaluates patient eligibility for clinical trials."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.0,
            max_tokens=200
        )
        eligibility_response = response.choices[0].message.content.strip()
        is_eligible = 'Yes' in eligibility_response
        return is_eligible, eligibility_response if is_eligible else []
    except Exception as e:
        print(f"OpenAI API Error: {e}")
        return False, []

def read_csv(file_path):
    """ Reads CSV file into a list of dictionaries. """
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        reader.fieldnames = [field.strip() for field in reader.fieldnames]
        return [row for row in reader]

def write_output_excel(output_file, patient_trials):
    """ Writes patient-trial matches to an Excel file in the requested format. """
    formatted_data = []
    
    for patient_id, trials in patient_trials.items():
        eligible_trials = []
        for trial in trials:
            if trial['eligibility_status'] == 'Eligible':
                eligible_trials.append({
                    "trialId": trial['trial_id'],
                    "trialName": trial['trial_name'],
                    "eligibilityCriteriaMet": trial['explanation']
                })
        formatted_data.append({
            "patientId": patient_id,
            "eligibleTrials": eligible_trials
        })
    
    # Convert to DataFrame and save to Excel
    df = pd.DataFrame(formatted_data)
    df.to_excel(output_file, index=False)

def main():
    trials = read_csv('clinical_trials.csv')
    patients = read_csv('patientdata.csv')
    patient_trials = {}
    
    for patient in patients:
        patient_id = patient['patient_id']
        patient_trials[patient_id] = []
        for trial in trials:
            trial_data = {
                'trial_id': trial['Trial:'],
                'trial_name': trial['Trial:'],
                'age_range': trial['Age:'],
                'gender': trial['Gender:'],
                'inclusion_criteria': trial['Inclusion Criteria:'],
                'exclusion_criteria': trial['Exclusion Criteria:'],
            }
            is_eligible, explanation = check_eligibility(patient, trial_data)
            if is_eligible:
                patient_trials[patient_id].append({
                    'trial_id': trial['Trial:'],
                    'trial_name': trial['Trial:'],
                    'eligibility_status': 'Eligible',
                    'explanation': explanation
                })
    
    write_output_excel('patient_trial_matches.xlsx', patient_trials)

if __name__ == '__main__':
    main()
