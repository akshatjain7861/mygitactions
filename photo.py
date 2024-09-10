import os
import pandas as pd
import requests

# Function to download the brochure
def download_brochure(url, file_name):
    try:
        # Ensure the URL starts with http or https
        if not url.startswith('http'):
            print(f"Invalid URL '{url}' for {file_name}")
            return

        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful

        # Write the content to a file
        with open(file_name, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded: {file_name}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to download {file_name}: {e}")

# Function to clean the brochure URL (remove everything before 'https')
def clean_brochure_url(url):
    if pd.isna(url):
        return url  # If URL is NaN, return as is
    if 'https' in url:
        return url[url.index('https'):]  # Remove everything before 'https'
    return url  # Return the URL if it doesn't contain 'https'

# Main function to read Excel, clean URLs, and download brochures
def download_college_brochures(excel_file, output_folder, cleaned_excel_file):
    # Read the Excel file
    df = pd.read_excel(excel_file)

    # Check if the necessary columns exist
    if 'Name' not in df.columns or 'Brochure' not in df.columns:
        print("The Excel file must have 'Name' and 'Brochure' columns.")
        return

    # Clean the brochure URLs
    df['Brochure'] = df['Brochure'].apply(clean_brochure_url)

    # Save the cleaned DataFrame to a new Excel file
    df.to_excel(cleaned_excel_file, index=False)
    print(f"Cleaned data saved to {cleaned_excel_file}")

    # Create a directory to save brochures (if it doesn't exist)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Loop through each row in the DataFrame
    for index, row in df.iterrows():
        college_name = row['Name']
        brochure_link = row['Brochure']

        # Skip rows with missing or invalid data
        if pd.isna(college_name) or pd.isna(brochure_link):
            print(f"Skipping row {index}: Missing data")
            continue

        # Make sure college_name is a string and replace spaces
        if isinstance(college_name, str):
            file_name = f"{college_name.replace(' ', '_')}.pdf"
        else:
            print(f"Skipping row {index}: Invalid college name")
            continue

        file_path = os.path.join(output_folder, file_name)

        # Download the brochure if the URL is valid
        download_brochure(brochure_link, file_path)

# Path to your Excel file
excel_file = 'College.xls'

# Define the folder where brochures will be saved
output_folder = 'Brochures_Downloads'

# Define the name of the cleaned Excel file
cleaned_excel_file = 'Cleaned_College_Data.xls'

# Call the main function to clean the data and start downloading
download_college_brochures(excel_file, output_folder, cleaned_excel_file)
