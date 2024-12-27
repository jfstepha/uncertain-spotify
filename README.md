# uncertain-spotify

Scrape the Uncertain FM slack channel and create spotify playlists

# Instructions:
* Copy a log from the Uncertain FM #live Slack channel
* Paste into slacklog.txt
* `python parse_log.py`
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

Todo: checkout this project: https://github.com/stieterd/playlist-generator/blob/main/main.py see if I can connect directly to spotify.
