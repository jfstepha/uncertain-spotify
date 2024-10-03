import re
import pandas as pd


filename = "slacklog.txt"
playlist_filename = "playlist.txt"
table_filename = "table.txt"

df = pd.DataFrame(columns=["seq", "show", "episode", "artist","track"])

i=0
show = "unknown"
episode = "unknown"
shows = ["VERY SELDOM CASUAL", "UNKNOWN FREQUENCIES", "SEEKING THE NIGHTED THRONE",
         "ENJOY THE SILENCE", "GUNS OR BUTTER", "UNCERTAIN", "THE GROOVE SCENARIO", "PLAYING AT SHADOWS" ]
bad_artists = ["Worbler", "Silent g", "Mike McKenzie"]


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
                episode = title
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


print("---------- table ---------")
print(df.to_string())
with open(table_filename, 'w', encoding='utf-8') as f:
    print(df.to_string(), file=f)


print("------- top artists ------")
print(df['artist'].value_counts().sort_values())

# print("------- playlist ---------")
# print(df[['artist','track']].to_csv(header=False,index=False, sep=' ', quoting=None) )
# df[['artist','track']].to_csv(playlist_filename, header=False,index=False, sep=',', quoting=None)

with open(playlist_filename, 'w', encoding='utf-8') as f:
    for index, row in df.iterrows():
        print(f"{row['artist']}, {row['track']}", file=f)


print("------- shows included ---------")
print(df['show'].value_counts().sort_values())

#print(df)
#print(artist_list)
#for artist in artist_list:
#    print(f"artist: {artist}")
