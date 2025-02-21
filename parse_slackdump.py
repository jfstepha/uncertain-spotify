import re
import pandas as pd
from datetime import date
import datetime
import json


# https://senatorjohn.slack.com/archives/C02U38XQY
filename = "C02U38XQY.json"
schedule_filename = "schedule.txt"
playlist_filename = "playlist.txt"
table_filename = "table.txt"
show_list = []

use_schedule_file = True

df = pd.DataFrame(columns=["seq", "time", "scheduled_show", "show", "episode", "artist","track"])

i=0
show = "unknown"
episode = "unknown"
shows = ["VERY SELDOM CASUAL", "UNKNOWN FREQUENCIES", "SEEKING THE NIGHTED THRONE",
        "ENJOY THE SILENCE", "GUNS OR BUTTER", "UNCERTAIN", "THE GROOVE SCENARIO", "PLAYING AT SHADOWS",
        "ENJOY YOUR DAY", "MC & JEFF", "RADIO FREE ENTROPY", "ALLSTON PUDDING",
        "RAT FEVER", "POLICYMAKER", "GRAHAMS' COMPLETELY NORMAL RADIO PROGRAMME",
        "AMERICAN DEBAUCHERY", "YEAH RIGHT", "DUAL CASSETTE DECK", "TWO HOUR MUSIC FUN RADIO FRIEND HOUR",
        "COVER LOVER", "MAURA DOT COM SLASH UNCERTAIN" ]
bad_artists = ["Worbler", "Silent g", "Mike McKenzie", "Matt Lavallee", "DJ Senator John Blutarski", "Duane Bruce",
               "DJ Mike F", "break", "Josh L", "Jeff", "kristen", "maura dot com"]

print("--- parsing schedule ----")
with open(schedule_filename, 'r',encoding='utf-8') as f:
    for line in f:
        match = re.search("^(\\d+)([ap])\\s+(.*)", line)
        if match:
            hour = match.group(1)
            am_pm = match.group(2)
            name = match.group(3)
            print(f"Time: {hour}:00 {am_pm}: {name}")
            show_dict = {"hour":hour, "am_pm":am_pm, "name":name}
            show_list.append(show_dict)
        match = re.search("^END", line)
        if match:
            print("found end")
            break
        
def find_24_hour(hour, am):
    time_24h = 0
    if am:
        if hour == 12:
            time_24h = 0
        else:
            time_24h = hour
    else:
        if hour == 12:
            time_24h = 12
        else:
            time_24h = hour + 12
    return time_24h

def find_show_name(hour, minute, am):
    time_24h = find_24_hour(int(hour), am)
    show_name ="unknown"
    # print(f"searching for show at {hour}:{minute} {am} 24h:{time_24h}")
    for show_dict in show_list:
        show_24h = find_24_hour( int(show_dict["hour"]), show_dict["am_pm"]=="a")
        # print( f"   searching show {show_dict['name']} at {show_24h}")
        if time_24h < show_24h:
            # print(f"found show:{show_name}")
            return(show_name)
        else:
            show_name = show_dict['name']

with open(filename, 'r',encoding='utf-8') as f:
    j = json.load(f)
    msg = j['messages']
    am = True
    after_1am = False
    time="unknown"
    day = "unknown"
    scheduled_show = "unknown"
    prev_title = "none"
    for m in msg:
        if 'user' not in m.keys():
            print("no user continuing")
            continue
        if m['user'] != 'U014ASD5456':
            print("not bot user continuing")
            continue
        # print(f"bot user match. text={m['text']}")
        #match = re.search('\*_now playing\*_:\* (.*), "(.*)"', m['text'])
        match = re.search('\*_now playing_:\* (.*), "(.*)"', m['text'])
        if match:
            # print("now playing match")
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
                    episode = title[:80]
            elif title.upper() in shows:
                show = title.upper()
                episode = "unknown"
            elif title == prev_title:
                print(f"Skipping duplicate title {title}")
            else:
                df.loc[i] = [i, time, scheduled_show, show, episode, artist, title]
                prev_title = title
                i += 1
        match = re.search('UP NEXT: (.*) (#.*) with', line)
        if match:
            artist = match.group(1)
            title = match.group(2)
            if artist in shows:
                show = artist
                episode = title
        dt = datetime.datetime.fromtimestamp(int(float(m['ts'])))
        print(f"converted {m['ts']} to {dt}")
        hours24 = dt.hour
        minutes = f"{dt.minute}"
        if hours24 > 12:
            hours = hours24 - 12
            am = False
        else:
            hours = hours24
            am = True
        if am:
            time=f"{hours}:{minutes.zfill(2)} AM"
        else:
            time=f"{hours}:{minutes.zfill(2)} PM"
        if use_schedule_file:
            scheduled_show = find_show_name(hours, minutes, am)




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


# this became too complicated to parse from the web page because it's not a simple table
#### parse schedule
#days = ["MON","TUE","WED","THU","FRI","SAT","SUN"]
#today = days.index(day.upper())
#print(f"today's schedule for {day} ({today})")
#with open(schedule_filename, 'r',encoding='utf-8') as f:
#    this_line = ""
#    in_table = False
#    for line in f:
#        if in_table:
#            match = re.search('^\\d[ap]', line)
#            if match:
#                print("------------")
#                row = this_line.split("\t")
#                print(','.join(row))
#                #print (len(row))
#                #if len(row) > 1:
#                #    print( row[today])
#                
#                this_line = row[-1] + line[:-1] + " "
#                row = row[:-1]
#            else:
#                this_line += line[:-1] + " "
#        else:
#            match = re.search('MON\tTUE\tWED\tTHU\tFRI\tSAT\tSUN', line)
#            if match:
#                print("Table found")
#                in_table = True



    
