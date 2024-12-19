import os
import pandas as pd

"""
This script reads transcripts from various sources
and outputs a single, organized file with episode
details in CSV and JSON format
"""

# Read latest file about episodes from the `survivoR2py` repo
episode_src = pd.read_json('https://stilesdata.com/survivor/survivoR2py/processed/json/episodes.json')

episode_fix = pd.DataFrame([{
       "version": "US",
       "version_season": "US47",
       "season_name": "Survivor: 47",
       "season": 47,
       "episode_number_overall": '',
       "episode": 14,
       "episode_title": '',
       "episode_label": '',
       "episode_date": '',
       "episode_length": '',
       "viewers": '',
       "imdb_rating": '',
       "n_ratings": '',
       "episode_summary": ''
}])

episode_df = pd.concat([episode_src, episode_fix]).reset_index(drop=True)

episode_df['episode_date'] = pd.to_datetime(episode_df['episode_date'], unit='ms').dt.strftime('%Y-%m-%d')

# Subset episodes DataFrame to just US episodes
episode_us_df = episode_df.query('version == "US"').copy()

# Just the columns we want
episides_slim_cols = ['version', 'season_name', 'season',
       'episode_number_overall', 'episode', 'episode_title', 
       'episode_date', 'episode_length']
episode_us_slim_df = episode_us_df[episides_slim_cols].copy()

# Subslikescript transcripts (seasons 1-44)
transcripts_keep_cols = ['season', 'episode', 'title', 'transcript']
transcripts_past = pd.read_json('../data/raw/transcripts/transcripts.json')[transcripts_keep_cols]
transcripts_past['source'] = 'subslikescript'

# YouTube TV transcripts (seasons 46-47)
transcripts_recent = pd.read_json('../data/raw/transcripts/youtube_transcripts.json')[transcripts_keep_cols]
transcripts_recent['source'] = 'youtubetv'

transcripts_all = pd.concat([transcripts_past, transcripts_recent]).drop_duplicates(subset=['season', 'episode']).sort_values(['season', 'episode'])

# Merge the transcripts and the episode details
transcripts_details_df = pd.merge(transcripts_all, episode_us_slim_df, on=['season', 'episode'])

transcript_column_order = ['season', 'episode', 'title', 'source', 'version',
       'season_name', 'episode_number_overall', 'episode_title',
       'episode_date', 'episode_length', 'transcript']


# Base directory to store individual files
base_dir = '../data/processed/transcripts/files/'

# Ensure base directory exists
os.makedirs(base_dir, exist_ok=True)

# Iterate over each row in the merged transcripts dataframe
for _, row in transcripts_details_df.iterrows():
    # Create directory for the season if it doesn't exist
    season_dir = os.path.join(base_dir, f"season_{row['season']}")
    os.makedirs(season_dir, exist_ok=True)

    # Define the filename using episode number
    filename = f"episode_{row['episode']:02d}.txt"

    # Full path to the file
    file_path = os.path.join(season_dir, filename)

    # Write the transcript to a file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(row['transcript'])

print("All transcripts saved to individual files.")

# Export to processed
transcripts_details_df[transcript_column_order].to_csv('../data/processed/transcripts/transcripts.csv', index=False)
transcripts_details_df[transcript_column_order].to_json('../data/processed/transcripts/transcripts.json', indent=4, orient='records')