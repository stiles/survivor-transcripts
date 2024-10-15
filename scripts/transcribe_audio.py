import os
import assemblyai as aai
import pandas as pd
import json

# Determine the current directory of the script file
script_dir = os.path.dirname(os.path.abspath(__file__))

words_path = os.path.join(script_dir, '../data/processed/transcripts/series_keyword_counts.json')
words_df = pd.read_json(words_path)
words_list = words_df['word'].head(50).to_list()
# print(words_list)


# Set AssemblyAI API Key
aai.settings.api_key = os.getenv('ASSEMBLY_AI_KEY')

# Meta data
url = 'https://www.paramountplus.com/shows/video/qlMtjCuj0Mlw02bBGu3aZDOYL_kMnosR/'
season = '46'
episode = '01'
title = 'We Can Do Hard Things'

# Path to local file
FILE_PATH = f'audio/s{season}e{episode}_full.mp3'

# Configure Assembly AI transcription
config = aai.TranscriptionConfig(
    speaker_labels=True,
    speakers_expected=5,
    word_boost=words_list
)

# Initialize Transcriber
transcriber = aai.Transcriber()

# Request transcription
transcript_data = transcriber.transcribe(FILE_PATH, config=config)

# Collect transcript text
transcript_text = "\n".join([f"Speaker {u.speaker}: {u.text}" for u in transcript_data.utterances])

# Create new transcript entry as a DataFrame row
new_entry = pd.DataFrame([{
    "url": url,
    "season": int(season),
    "episode": int(episode),
    "title": title,
    "transcript": transcript_text,
    "post_voteoff_lines": ""
}])

# Build the absolute path to the CSV and JSON files
csv_path = os.path.join(script_dir, '../data/raw/transcripts/transcripts.csv')
json_path = os.path.join(script_dir, '../data/raw/transcripts/transcripts.json')

# Ensure the directory exists
csv_dir = os.path.dirname(csv_path)
if not os.path.exists(csv_dir):
    os.makedirs(csv_dir)

# Load existing transcripts or create an empty DataFrame if not found
try:
    transcripts_df = pd.read_csv(csv_path)
except FileNotFoundError:
    transcripts_df = pd.DataFrame(columns=["url", "season", "episode", "title", "transcript", "post_voteoff_lines"])

# Concatenate new entry to the existing DataFrame
transcripts_df = pd.concat([transcripts_df, new_entry], ignore_index=True).drop_duplicates(subset=['season', 'episode'], keep='last')

# Save the updated transcripts back to CSV
transcripts_df.to_csv(csv_path, index=False)

# Save to JSON as well
transcripts_df.to_json(json_path, indent=4, orient='records')

print("Transcript saved successfully!")
