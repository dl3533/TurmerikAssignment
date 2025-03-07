import csv

input_file = "patients.csv"  # Update with your actual file name
output_file = "patientdata.csv"   # Patient ID, Name, Race, Gender, Immunizations, Medications, Conditions, Careplans

target_value = []
rows = 10
cols = 8
array_2d = [[None for _ in range(cols)] for _ in range(rows)]
def filter_non_numeric(text):
    """Function to filter out numeric characters from a string."""
    return ''.join([char for char in text if not char.isdigit()])



with open(input_file, mode="r", newline="", encoding="utf-8") as infile:

    reader = csv.reader(infile, skipinitialspace=True)  # Ignore spaces after commas
    

    for i, row in enumerate(reader):
        if i >= 5:  # Stop after i rows
            break

        # Replace empty values with "0"
        row = [col.strip() if col.strip() else '0' for col in row]  # If value is empty, set to "0"

        if any(row):  # Ensure row is not completely empty
            if len(row) > 15:  # Ensure at least 15 columns
                 # Filter non-numeric characters from columns H and I
                 # represent names
                filtered_h = filter_non_numeric(row[7]) 
                filtered_i = filter_non_numeric(row[8])

                m = row[12] #race
                o = row[14] #gender

                # Combine filtered values from H and I columns
                combined_column = f"{filtered_h} {filtered_i}"
                array_2d[i] = [row[0], combined_column, m, o, 0, 0, 0, 0]  # Write to the output file
                target_value.append(row[0])

with open('immunizations.csv', mode="r", newline="", encoding="utf-8") as infile:

    reader = csv.reader(infile, skipinitialspace=True)  # Ignore spaces after commas
    
    for i, row in enumerate(reader):
        if i >= 5:  # Stop after i
            break

        # Replace empty values with "0"
        row = [col.strip() if col.strip() else '0' for col in row]  # If value is empty, set to "0"

        if any(row):  # Ensure row is not completely empty
            for j in range(len(target_value)):                
                array_2d[i][4] = row[4]  # Write to the output file
        

with open('medications.csv', mode="r", newline="", encoding="utf-8") as infile:

    reader = csv.reader(infile, skipinitialspace=True)  # Ignore spaces after commas
    

    for i, row in enumerate(reader):
        if i >= 5:  # Stop after i rows
            break

        # Replace empty values with "0"
        row = [col.strip() if col.strip() else '0' for col in row]  # If value is empty, set to "0"

        if any(row):  # Ensure row is not completely empty
            for j in range(len(target_value)):
                array_2d[i][5] = row[5]  # Write to the output file

with open('conditions.csv', mode="r", newline="", encoding="utf-8") as infile:

    reader = csv.reader(infile, skipinitialspace=True)  # Ignore spaces after commas
    

    for i, row in enumerate(reader):
        if i >= 5:  # Stop after i rows
            break

        # Replace empty values with "0"
        row = [col.strip() if col.strip() else '0' for col in row]  # If value is empty, set to "0"

        if any(row):  # Ensure row is not completely empty
            for j in range(len(target_value)):
                array_2d[i][6] = row[5]  # Write to the output file

with open('careplans.csv', mode="r", newline="", encoding="utf-8") as infile, \
     open(output_file, mode="w", newline="", encoding="utf-8") as outfile:

    reader = csv.reader(infile, skipinitialspace=True)  # Ignore spaces after commas
    writer = csv.writer(outfile)
    header = ['patient_id', 'name', 'race', 'gender', 'immunizations', 'medications', 'medical_conditions', 'other_medical_conditions']
    writer.writerow(header)

    for i, row in enumerate(reader):
        if i >= 5:  # Stop after i rows
            break

        # Replace empty values with "0"
        row = [col.strip() if col.strip() else '0' for col in row]  # If value is empty, set to "0"

        if any(row):  # Ensure row is not completely empty
            for j in range(len(target_value)):
                array_2d[i][7] = row[8]  # Write to the output file
        writer.writerow(array_2d[i])

print(f"Processed and saved to {output_file}")


# Data is very hard to use, some patients have no immunization records, datasets are different lengths, rather than saying no immunizations
# there are simply no entries for those without immunizations, similar to every other dataset outside of patients 