"""
Survivor US keywords
How often were show [jargon words](https://docs.google.com/spreadsheets/d/1owUkwauJE24EkMUmVyDl7CbnumOygGfC6BufG7Vspd8/edit?gid=0#gid=0) used, by season and episode, according to the transcripts. 
"""

import re
import json
import pandas as pd
import altair as alt
from collections import defaultdict
import altair_stiles as altstiles
from google.oauth2.service_account import Credentials

alt.themes.register("stiles", altstiles.theme)
alt.themes.enable("stiles")

"""
READ
"""

# Read the defined keywords
with open('../data/processed/transcripts/survivor_transcript_words.json', 'r') as f:
    keywords = json.load(f)

keywords_df = pd.DataFrame(keywords)

# Read the transcripts
transcripts_df = pd.read_json('https://stilesdata.com/survivor/transcripts/transcripts.json')

# Function to count occurrences of a word or phrase
def count_keywords(text, word, alternates):
    text = text.lower()
    # Use re.escape to handle any special characters in words or phrases
    count = len(re.findall(r'\b' + re.escape(word.lower()) + r'\b', text))
    for alt in alternates.split(', '):
        if alt:
            count += len(re.findall(r'\b' + re.escape(alt.lower()) + r'\b', text))
    return count

# Process each transcript
keyword_counts = defaultdict(lambda: defaultdict(int))
total_word_counts = defaultdict(int)

for index, row in transcripts_df.iterrows():
    transcript = row['transcript']
    season, episode, title = row['season'], row['episode'], row['title']
    
    # Calculate total word count
    total_words = len(re.findall(r'\b\w+\b', transcript.lower()))
    total_word_counts[(season, episode, title)] = total_words
    
    for keyword in keywords:
        word = keyword['word']
        alternates = keyword['alternates']
        count = count_keywords(transcript, word, alternates)
        keyword_counts[(season, episode, title)][word] += count


# Convert the results to a list of dictionaries for JSON output
results = []
for key, counts in keyword_counts.items():
    season, episode, title = key
    counts_dict = {word: count for word, count in counts.items()}
    total_words = total_word_counts[key]
    normalized_counts = {word: (count / total_words) * 10000 for word, count in counts.items()}
    
    results.append({
        'season': season,
        'episode': episode,
        'title': title,
        'counts': counts_dict,
        'total_words': total_words,
        'normalized_counts': normalized_counts
    })

# Convert results to a DataFrame
counts_list = []
for result in results:
    season = result['season']
    episode = result['episode']
    title = result['title']
    total_words = result['total_words']
    for word, count in result['counts'].items():
        normalized_count = result['normalized_counts'][word]
        counts_list.append({
            'season': season,
            'episode': episode,
            'title': title,
            'word': word,
            'count': count,
            'total_words': total_words,
            'normalized_count': normalized_count
        })

counts_df = pd.DataFrame(counts_list)

# Aggregate by season
season_agg_src = counts_df.groupby(['season', 'word']).agg({'count': 'sum', 'total_words': 'sum'}).reset_index()
season_agg_src['normalized_count'] = round((season_agg_src['count'] / season_agg_src['total_words']) * 10000,2)

# Include word categories
season_agg_df = pd.merge(season_agg_src, keywords_df[['word', 'category']], on='word')

# Aggregate for the entire series
series_agg_df = counts_df.groupby('word').agg({'count': 'sum', 'total_words': 'sum'}).reset_index()
series_agg_df['normalized_count'] = round((series_agg_df['count'] / series_agg_df['total_words']) * 10000,2)
series_agg_df = series_agg_df.sort_values('count', ascending=False).reset_index(drop=True)

# Limit super frequent words (Jeff, tribe, etc)
most_common_keywords = series_agg_df.word.head().to_list()
least_common_keywords = series_agg_df.word.tail(10).to_list()
season_agg_simple_df = season_agg_df.query(f'~word.isin({most_common_keywords}) and ~word.isin({least_common_keywords})')

"""
CHARTS
"""
# Heatmaps to show word counts normalized to 10,000 words
chart = alt.Chart(season_agg_simple_df, padding={'left': 10}).mark_rect().encode(
    alt.X("season:O")
        .axis(
            labelAngle=0,
            labelOverlap=False,
            values=[10, 20, 30, 40]
        ).title('Season'),
    alt.Y("word:N").title(None),
    alt.Tooltip(['season', 'word', 'count', 'normalized_count']),
    # Adjust domain to better reflect the normalized counts per 10,000 words
    alt.Color("normalized_count", scale=alt.Scale(scheme='yelloworangebrown', domain=[0.001, 100])).title("Count per 10,000 words"),
).properties(width=500, height=700, title=f'Survivor: Counts of selected keywords, by season').configure_legend(orient='top', gradientLength=170).configure_axis(
    labelFontSize=10,
)

chart.save('../visuals/heatmap.png', scale_factor=2)

"""
EXPORTS
"""

# Save the aggregated results to JSON
season_agg_df.to_json('../data/processed/transcripts/season_keyword_counts.json', orient='records', indent=4)
series_agg_df.to_json('../data/processed/transcripts/series_keyword_counts.json', orient='records', indent=4)

# Save the results in a nested JSON file
output_path = '../data/processed/transcripts/transcript_keyword_counts.json'
with open(output_path, 'w') as f:
    json.dump(results, f, indent=4)