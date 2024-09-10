import pandas as pd

# Load the Excel file
file_path = 'C:/Users/aj481/Desktop/Projects_of_Learning/mygitactions/College.xls'
df = pd.read_excel(file_path, engine='openpyxl')

# Specify the column you want to clean
column_name = 'Broucher'

# Define a function to remove text before 'https'
def clean_text(text):
    if pd.isna(text):  # Check for NaN values
        return text
    # Find the position of 'https' and slice the string
    pos = text.find('https')
    return text[pos:] if pos != -1 else text

# Apply the cleaning function to the specified column
df[column_name] = df[column_name].apply(clean_text)

# Save the cleaned DataFrame back to Excel
df.to_excel('cleaned_file.xls', index=False, engine='openpyxl')
