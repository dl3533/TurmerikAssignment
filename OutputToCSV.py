import pandas as pd

# Load the Excel file
df = pd.read_excel("patient_trial_matches.xlsx")

# Save as CSV
df.to_csv("patient_trial_matches.csv", index=False)