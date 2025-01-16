# uncertain-spotify

Scrape the Uncertain FM slack channel and create spotify playlists

# New slackdump instructions
* Install slackdump (brew install slackdump)
* Run the wizard and create a new channel (I don't really remember how to do this)
* dump a day of the log: `slackdump dump -time-from=2025-01-11T11:00:00 -time-to=2025-01-12T05:00:00 -o slackdump.zip C02U38XQY`
** Time in UTC
* `unzip slackdump.zip`
* `python3 parse_slackdump.py`

# Old Instructions:
* Copy a log from the Uncertain FM #live Slack channel
* Paste into slacklog.txt
* `python3 parse_slacklog.py`
* Copy playlist.txt into https://www.spotlistr.com/search/textbox, and create a playlist.
* Open the new playlist in Spotify

A table of the songs and shows is in `table.txt`

Here's how I set it up to work on my work machine:
* Made a new ssh key pair with `ssh-keygen`, save it as id_ed25519_personal.
* Add that public key to my personal github account.
* In ~/.ssh/config:

Host github-personal
  HostName github.com
  IdentityFile ~/.ssh/id_ed25519_personal
  IdentitiesOnly yes

* Then clone git@github-personal:jfstepha/uncertain-spotify

To get python working the first time:
```
virtualenv venv
source venv/bin/activate
pip install pandas
```

To run it:
```
source venv/bin/activate
python3 parse_log.py
```





Todo: checkout this project: https://github.com/stieterd/playlist-generator/blob/main/main.py see if I can connect directly to spotify.
