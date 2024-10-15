# Survivor transcripts

## About

This repository has scripts for downloading and parsing show transcripts and counting castaways' keywords and phrases — by season and the series overall. 

*More documentation to come.* 

## Sources

Most transcripts sourced from [subslikescript](https://subslikescript.com/series/Survivor-239195) with a few missing seasons pulled from the closed-captioning XML files embedded in the CBS/Paramount video player or from YouTube TV's timedtext API. 

*Still need to find transcripts for season 45*

## Processes

- `scripts/fetch_transcripts.py`: This script collects episode transcript URLs for seasons 1-44, converts the URLs to metadata (episode number, season, episode title, URL, etc.) and then fetches the full transcript for each episode. The results are stored as `transcripts` in CSV and JSON formats in the `data/raw/transcripts` directory.

- `scripts/process_youtube_transcripts.py`: This script reads a series of episode transcripts from YouTube TV for seasons 46 and 47. The results are stored as `youtube_transcripts` in CSV and JSON formats in the `data/raw/transcripts` directory. *Still searching for a season 45 source*.

- `scripts/fetch_words.py`: This script reads a list of dozens of subjectively selected words and associated categories from an evolving [Google Sheets doc](https://docs.google.com/spreadsheets/d/1owUkwauJE24EkMUmVyDl7CbnumOygGfC6BufG7Vspd8/edit?gid=0#gid=0) so they can be used for text analysis of episode transcripts.

- `notebooks/01-transcript-analysis.ipynb`: A Jupyter Lab notebook that counts how often these [jargon words](https://docs.google.com/spreadsheets/d/1owUkwauJE24EkMUmVyDl7CbnumOygGfC6BufG7Vspd8/edit?gid=0#gid=0) ("tribe", "vote", "idol", "reward", etc.) have been used by season and episode, according to the transcripts. 

## Related
- [survivor-voteoffs](https://github.com/stiles/survivor-voteoffs): *How did each castaway react to his or her torch getting snuffed? There's data for that.*
- [survivoR2py](https://github.com/stiles/survivoR2py): *Converting the authoritative [survivoR](https://github.com/doehm/survivoR) repo's R data files into comma-delimitted formats for use with other tools.*

## Questions? Corrections? 

[Please let me know](mailto:mattstiles@gmail.com).