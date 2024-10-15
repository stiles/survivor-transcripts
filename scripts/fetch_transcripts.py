import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm

# Load the Season 18 official transcripts
season_18_df = pd.read_json('../data/raw/transcripts/closed_caption_reference.json')

def fetch_season_18_transcript(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'xml')
        p_tags = soup.find_all('p')
        
        transcript = "\n".join(p.get_text(separator=" ") for p in p_tags)
        return transcript
    except Exception as e:
        print(f"Error fetching transcript from {url}: {e}")
        return ""

# Fetch transcripts for Season 18
tqdm.pandas()
season_18_df['transcript'] = season_18_df['caption_url'].progress_apply(fetch_season_18_transcript)

# Function to get filtered URLs from subslikescript.com
def get_filtered_urls(base_url):
    try:
        response = requests.get(base_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        urls = ["https://subslikescript.com" + a.get('href') for h in soup.findAll('li') for a in h.findAll('a') if 'href' in a.attrs]
        filtered_urls = [url for url in urls if 'series' in url and 'season' in url]
        return filtered_urls
    except Exception as e:
        print(f"Error fetching URLs: {e}")
        return []

# Function to fetch transcript from subslikescript.com
def fetch_transcript(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        transcript_div = soup.find('div', class_='full-script')
        
        if transcript_div:
            transcript = transcript_div.get_text(separator="\n").strip()
            # Remove specific lines containing "foodval.com"
            filtered_lines = [line for line in transcript.split('\n') if "foodval.com" not in line]
            return "\n".join(filtered_lines)
        return ""
    except Exception as e:
        print(f"Error fetching transcript from {url}: {e}")
        return ""

# Function to extract post-voteoff lines
def extract_post_voteoff_lines(transcript, num_lines=3):
    lines = transcript.split('\n')
    for i, line in enumerate(lines):
        if "The tribe has spoken" in line:
            post_voteoff_lines = lines[i:i+num_lines+1]
            return " ".join(post_voteoff_lines).strip()
    return ""

# Get the URLs from the main page
base_url = 'https://subslikescript.com/series/Survivor-239195'
filtered_urls = get_filtered_urls(base_url)

# Debug: Print the number of filtered URLs
print(f"Number of filtered URLs: {len(filtered_urls)}")

# Create a DataFrame
df = pd.DataFrame(filtered_urls, columns=['url'])

# Extract season, episode, and title
df[['season', 'episode', 'title']] = df['url'].str.extract(r'season-(\d+)/episode-(\d+)-(.+)', expand=True)

# Clean the title by replacing underscores with spaces
df['title'] = df['title'].str.replace('_', ' ')

# Convert season and episode to integers
df['season'] = df['season'].astype(int)
df['episode'] = df['episode'].astype(int)

# Filter out Season 18
df = df[df['season'] != 18]

# Fetch transcripts with progress bar
tqdm.pandas()
df['transcript'] = df['url'].progress_apply(fetch_transcript)

# Debug: Check which seasons have empty transcripts
empty_transcripts = df[df['transcript'] == ""]
print(f"Seasons with empty transcripts:\n{empty_transcripts[['season', 'episode', 'title', 'url']]}")

# # Extract post-voteoff lines
# df['post_voteoff_lines'] = df['transcript'].apply(lambda x: extract_post_voteoff_lines(x, num_lines=3))

# # Process Season 18 transcripts
# season_18_df['post_voteoff_lines'] = season_18_df['transcript'].apply(lambda x: extract_post_voteoff_lines(x, num_lines=3))

# Merge Season 18 transcripts with others
final_df = pd.concat([df, season_18_df], ignore_index=True)

# Display the resulting DataFrame
print(final_df[['season', 'episode', 'title']])

# Optional: save to CSV and JSON
final_df.to_csv('../data/raw/transcripts/transcripts.csv', index=False)
final_df.to_json('../data/raw/transcripts/transcripts.json', indent=4, lines=False, orient='records')