import re
import pandas as pd
from datetime import date


filename = "slacklog.txt"
playlist_filename = "playlist.txt"
table_filename = "table.txt"

df = pd.DataFrame(columns=["seq", "show", "episode", "artist","track"])

i=0
show = "unknown"
episode = "unknown"
shows = ["VERY SELDOM CASUAL", "UNKNOWN FREQUENCIES", "SEEKING THE NIGHTED THRONE",
        "ENJOY THE SILENCE", "GUNS OR BUTTER", "UNCERTAIN", "THE GROOVE SCENARIO", "PLAYING AT SHADOWS",
        "ENJOY YOUR DAY", "MC & JEFF", "RADIO FREE ENTROPY", "ALLSTON PUDDING",
        "RAT FEVER", "POLICYMAKER", "GRAHAMS' COMPLETELY NORMAL RADIO PROGRAMME",
        "AMERICAN DEBAUCHERY"  ]
bad_artists = ["Worbler", "Silent g", "Mike McKenzie", "Matt Lavallee", "DJ Senator John Blutarski", "Duane Bruce",
               "DJ Mike F"]


with open(filename, 'r',encoding='utf-8') as f:
    for line in f:
#        print(line)
        match = re.search('now playing: (.*), "(.*)"', line)
        if match:
            artist = match.group(1)
            title = match.group(2)
            if artist in bad_artists:
                print(f"ignoring bad artist {artist}")
            elif artist.upper() in shows:
                show = artist.upper()
                match = re.search('OTW: .*', title)
                if match:
                    episode = "unknown"
                else:
                    episode = title
            elif title.upper() in shows:
                show = title.upper()
                episode = "unknown"
            else:
                df.loc[i] = [i, show, episode, artist, title]
                i += 1
        match = re.search('UP NEXT: (.*) (#.*) with', line)
        if match:
            artist = match.group(1)
            title = match.group(2)
            if artist in shows:
                show = artist
                episode = title

today = date.today()
print("---------- table ---------")
print(df.to_string())
# for today
with open(table_filename, 'w', encoding='utf-8') as f:
    print(df.to_string(), file=f)
# for archive
table_filename = f"tables/table-{today}.txt"
with open(table_filename, 'w', encoding='utf-8') as f:
    print(df.to_string(), file=f)



print("------- top artists ------")
print(df['artist'].value_counts().sort_values())


# for today:
with open(playlist_filename, 'w', encoding='utf-8') as f:
    for index, row in df.iterrows():
        print(f"{row['artist']}, {row['track']}", file=f)

# for archive:
playlist_filename = f"playlists/playlist-{today}.txt"
with open(playlist_filename, 'w', encoding='utf-8') as f:
    for index, row in df.iterrows():
        print(f"{row['artist']}, {row['track']}", file=f)


print("------- shows included ---------")
print(df['show'].value_counts().sort_values())

#print(df)
#print(artist_list)
#for artist in artist_list:
#    print(f"artist: {artist}")

print(f"Date: {today}")
print(f"Paste {playlist_filename} into https://www.spotlistr.com/search/textbox")