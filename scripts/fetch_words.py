import os
import json
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# Load the client secrets file
service_account_file = os.path.expanduser("~/.google_service_account.json")

# Define the scope
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]

# Authenticate using the service account file
credentials = Credentials.from_service_account_file(service_account_file, scopes=scope)

# Authorize the gspread client
client = gspread.authorize(credentials)

"""
FETCH & SCORE
Read a list of words and associated categories.
Used for text analysis of episode transcripts.
"""

# Determine the absolute paths for input and output files
base_dir = os.path.dirname(os.path.abspath(__file__))
csv_output_path = os.path.join(base_dir, "../data/processed/transcripts/survivor_transcript_words.csv")
json_output_path = os.path.join(base_dir, "../data/processed/transcripts/survivor_transcript_words.json")

# Open the Google Spreadsheet by name
spreadsheet_name = "survivor_transcript_words"
spreadsheet = client.open(spreadsheet_name).get_worksheet(0)

# Fetch data from the worksheet
data = spreadsheet.get_all_records()

transcript_words_df = pd.DataFrame(data)

# Save to CSV
transcript_words_df.to_csv(csv_output_path, index=False)

# Save to JSON
transcript_words_df.to_json(json_output_path, orient='records', lines=False, indent=4)

print(f"Data saved to {csv_output_path} and {json_output_path}")