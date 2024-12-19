import os
import json
import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

# Path to YouTube timed text JSONs
youtube_dir = '../data/raw/transcripts/youtube_timedtext'
processed_dir = '../data/processed/youtube_timedtext'

# Ensure the processed directory exists
if not os.path.exists(processed_dir):
    os.makedirs(processed_dir)

# URLs for CBS episode metadata about recent seasons
cbs_urls = {
    46: "https://www.cbs.com/shows/survivor/episodes/46/",
    47: "https://www.cbs.com/shows/survivor/episodes/47/"
}

# Function to scrape CBS episode metadata (titles, air dates)
def scrape_cbs_metadata(season):
    url = cbs_urls.get(season)
    if not url:
        print(f"No URL available for season {season}")
        return []

    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        episodes = []
        for ep in soup.find_all('div', class_='episode'):
            title = ep.find('div', class_='epTitle').get_text(strip=True)
            episode_number = int(ep.find('abbr', class_='epNum').get_text(strip=True).replace("E", ""))
            episodes.append({
                'season': season,
                'episode': episode_number,
                'title': title,
            })
        return episodes
    except Exception as e:
        print(f"Error scraping metadata for season {season}: {e}")
        return []

# Function to convert timedtext JSON into a transcript
def convert_timedtext_to_transcript(timedtext_data):
    events = timedtext_data.get('events', [])
    transcript_lines = []
    for event in events:
        segments = event.get('segs', [])
        for segment in segments:
            text = segment.get('utf8', '').strip()
            if text:
                transcript_lines.append(text)
    return ' '.join(transcript_lines)

# Process YouTube timed-text JSONs and append metadata
def process_youtube_timedtext(season_metadata):
    processed_transcripts = []
    
    # Iterate through the files in youtube_timedtext directory
    for filename in os.listdir(youtube_dir):
        if filename.endswith('.json'):
            print(f"Processing file: {filename}")  # Debug

            input_path = os.path.join(youtube_dir, filename)

            # Load the YouTube JSON
            with open(input_path, 'r') as f:
                timedtext_data = json.load(f)

            # Extract the season and episode from the filename
            try:
                season_episode = filename.replace('.json', '').split('us')[1]
                season = int(season_episode[:2])
                episode = int(season_episode[2:])
            except (IndexError, ValueError):
                print(f"Skipping malformed filename: {filename}")
                continue

            # Get the transcript from the YouTube JSON
            if 'events' not in timedtext_data:
                print(f"No events found in: {filename}")
                continue
            transcript = convert_timedtext_to_transcript(timedtext_data)

            # Find the corresponding metadata (title)
            metadata = next((item for item in season_metadata if item['season'] == season and item['episode'] == episode), None)

            if metadata:
                title = metadata['title']
            else:
                title = f"Episode {episode}"
                print(f"No metadata found for Season {season}, Episode {episode}")

            # Append transcript and metadata
            processed_transcripts.append({
                'season': season,
                'episode': episode,
                'title': title,
                'transcript': transcript
            })

            # Save the processed transcript to a new file
            output_path = os.path.join(processed_dir, f'us{season}{episode}_transcript.json')
            with open(output_path, 'w') as f_out:
                json.dump({
                    'season': season,
                    'episode': episode,
                    'title': title,
                    'transcript': transcript
                }, f_out, indent=4)
                print(f"Saved processed file: {output_path}")

    return pd.DataFrame(processed_transcripts)

# Fetch and process metadata for seasons 46 and 47
season_46_metadata = scrape_cbs_metadata(46)
season_47_metadata = scrape_cbs_metadata(47)

# Combine metadata for both seasons
combined_metadata = season_46_metadata + season_47_metadata

# Process YouTube timed-text transcripts
youtube_df = process_youtube_timedtext(combined_metadata)

# Save combined YouTube transcripts to JSON and CSV
youtube_df.to_csv('../data/raw/transcripts/youtube_transcripts.csv', index=False)
youtube_df.to_json('../data/raw/transcripts/youtube_transcripts.json', indent=4, orient='records')

print("Processed YouTube transcripts with metadata successfully!")