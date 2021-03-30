from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

URL = "https://www.billboard.com/charts/hot-100/2020-08-29"

CLIENT_ID = "hello"
CLIENT_SECRET = "hello"
REDIRECT_URI = "http://example.com"

# use as YMD - 2021-01-20

date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
response = requests.get(URL)
website_html = response.text
soup = BeautifulSoup(website_html, "html.parser")

all_songs = soup.find_all("span", class_="chart-element__information__song")

song_titles = [song.getText() for song in all_songs]
print(song_titles)

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URI,
                                               scope="playlist-modify-private",
                                               show_dialog=True,
                                               cache_path="tokens.txt"))

user_id = sp.current_user()["id"]

song_URI = []
year = date.split("-")[0]
for song in song_URI:
    result = sp.search(q=f"track{song} year:{year}",type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_URI.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=user_id,public=False,name=f"Vintage year{year}")
print(playlist)
sp.playlist_add_items(playlist_id=playlist["id"], items=song_URI)

reply = response.json()
print(reply)
