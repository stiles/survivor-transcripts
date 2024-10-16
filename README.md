# Survivor transcripts

## About

This repository has scripts for downloading and parsing show transcripts and counting castaways' keywords and phrases — by season and the series overall. 

*More documentation to come.* 

## Sources

Most transcripts sourced from [subslikescript](https://subslikescript.com/series/Survivor-239195) with a few missing seasons pulled from the closed-captioning XML files embedded in the CBS/Paramount video player or from YouTube TV's timedtext API. 

*Still need to find transcripts for season 45*

## Processes

- `scripts/fetch_transcripts.py`: This script collects episode transcript URLs for seasons 1-44, converts the URLs to metadata (episode number, season, episode title, URL, etc.) and then fetches the full transcript for each episode. The results are stored as `transcripts` in CSV and JSON formats in the `data/raw/transcripts` directory.

- `scripts/fetch_youtube_transcripts.py`: This script reads a series of episode transcripts from YouTube TV for seasons 46 and 47. The results are stored as `youtube_transcripts` in CSV and JSON formats in the `data/raw/transcripts` directory. *Still searching for a season 45 source*.

- `scripts/process_all_transcripts.py`: This script reads all the assembled transcripts and outputs them in a single clean file with episode details in CSV and JSON formats in the `data/processed/transcripts` directory. The latest version is also stored on S3: [CSV](https://stilesdata.com/survivor/transcripts/transcripts.csv), [JSON](https://stilesdata.com/survivor/transcripts/transcripts.json). This script also loops through each transcript in the dataframe, creates a directory for each season and saves each episode transcript as a .txt file. *See below.*

- `scripts/fetch_words.py`: This script reads a list of dozens of subjectively selected words and associated categories from an evolving [Google Sheets doc](https://docs.google.com/spreadsheets/d/1owUkwauJE24EkMUmVyDl7CbnumOygGfC6BufG7Vspd8/edit?gid=0#gid=0) so they can be used for text analysis of episode transcripts.

- `notebooks/01-transcript-analysis.ipynb`: A Jupyter Lab notebook that counts how often these [jargon words](https://docs.google.com/spreadsheets/d/1owUkwauJE24EkMUmVyDl7CbnumOygGfC6BufG7Vspd8/edit?gid=0#gid=0) ("tribe", "vote", "idol", "reward", etc.) have been used by season and episode, according to the transcripts.

## Outputs

The individual Survivor episode transcripts are organized by season and episode number. You can access the files directly from S3 storage or via the provided URLs.

### File structure

Each transcript is stored in the following format:

- **Season Directories**: Files are organized by season, with each season having its own directory.
- **File Naming Convention**: Within each season directory, files are named based on the episode number, formatted as `episode_XX.txt` (where `XX` is the episode number).

### Directory structure

```
data/processed/transcripts/files/
├── season_1/
│   ├── episode_01.txt
│   ├── episode_02.txt
│   └── ...
├── season_2/
│   ├── episode_01.txt
│   ├── episode_02.txt
│   └── ...
└── season_44/
    ├── episode_01.txt
    ├── episode_02.txt
    └── ...
```

### File access

You can access each transcript by navigating to the corresponding URL. For example, to view the transcript for Season 1, Episode 1, visit the following link:

[Season 1, Episode 1 Transcript](https://stilesdata.com/survivor/transcripts/files/season_1/episode_01.txt)

To access a different episode, simply change the `season_1` and `episode_01.txt` parts of the URL to the appropriate season and episode number. For instance:

- [Season 1, Episode 2 Transcript](https://stilesdata.com/survivor/transcripts/files/season_1/episode_02.txt)
- [Season 2, Episode 1 Transcript](https://stilesdata.com/survivor/transcripts/files/season_2/episode_01.txt)

## Related work
- [survivor-voteoffs](https://github.com/stiles/survivor-voteoffs): *How did each castaway react to his or her torch getting snuffed? There's data for that.*
- [survivoR2py](https://github.com/stiles/survivoR2py): *Converting the authoritative [survivoR](https://github.com/doehm/survivoR) repo's R data files into comma-delimitted formats for use with other tools.*

## Questions? Corrections? 

[Please let me know](mailto:mattstiles@gmail.com).