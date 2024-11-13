import requests
import pandas as pd


# Define the API URL for ICD-11
api_url = "https://id.who.int/icd/release/11/2023-01/mms/"

headers = {
    "Authorization": "6741b7b1-5526-4309-8d92-4d017f947742_7a8d18a8-64d0-4056-869d-cc4124120650"
}
response = requests.get(api_url + "foundation", headers=headers)

# Function to fetch chapter, block, and disease data from ICD-11 API
def fetch_icd11_data():
    chapters = []
    
    # Send GET request to the ICD-11 API
    response = requests.get(api_url + "foundation")
    
    if response.status_code == 200:
        icd_data = response.json()
        
        for chapter in icd_data['child']:
            chapter_name = chapter['title']['@value']
            chapter_id = chapter['@id']
            print(f"Fetching data for chapter: {chapter_name}")

            # Extract block-level information for each chapter
            for block in chapter['child']:
                block_name = block['title']['@value']
                block_id = block['@id']

                # Extract diseases under each block
                for disease in block['child']:
                    disease_name = disease['title']['@value']
                    
                    # Add chapter, block, and disease to the list
                    chapters.append({
                        "Chapter Number": chapter_id,
                        "ICD Chapter": chapter_name,
                        "Block Level": block_name,
                        "Disease": disease_name,
                        # "Extension Code": extension_code,
                        # "Extension Title": extension_title,
                        "Extension": "None"  # Placeholder for extensions if needed
                    })
    else:
        print(f"Failed to retrieve ICD-11 data. Status Code: {response.status_code}")

    return pd.DataFrame(chapters)

# Fetch ICD-11 data
icd11_df = fetch_icd11_data()

# Save to an Excel file
output_path = "ICD11_All_Chapters.xlsx"
icd11_df.to_excel(output_path, index=False)
print(f"ICD-11 data saved to {output_path}")
