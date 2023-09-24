import sys
import spotipy
from spotipy.oauth2 import *


def sort_songs_by_custom_rules(songs):
    circle_of_fifths = [
        "C", "G", "D", "A", "E", "B/Cb", "F#/Gb", "C#/Db", "G#/Ab", "D#/Eb", "A#/Bb", "F"
    ]

    # Helper function to get the index based on either sharp or flat version
    def get_key_index(key):
        normalized_key = key.replace('♯', '#').replace('♭', 'b')
        normalized_key_parts = set(normalized_key.split('/'))
        for idx, circle_key in enumerate(circle_of_fifths):
            circle_key_parts = set(circle_key.split('/'))
            if normalized_key_parts.intersection(circle_key_parts):
                return idx
        raise ValueError(f"{key} is not in the Circle of Fifths list.")

    # Normalize keys in the songs data
    for song in songs:
        song['key'] = song['key'].replace('♯', '#').replace('♭', 'b')

    sorted_songs = []
    current_index = 0
    same_key_count = 0
    bpm_switch = False

    while songs:
        current_key_songs = [song for song in songs if get_key_index(song['key']) == current_index]
        if current_key_songs:
            if not bpm_switch:
                current_key_songs_sorted = sorted(current_key_songs, key=lambda x: x['bpm'])
            else:
                current_key_songs_sorted = sorted(current_key_songs, key=lambda x: x['bpm'], reverse=True)

            for song in current_key_songs_sorted:
                sorted_songs.append(song)
                songs.remove(song)
                same_key_count += 1
                if same_key_count >= 4:
                    same_key_count = 0
                    bpm_switch = not bpm_switch
        else:
            current_index = (current_index + 1) % len(circle_of_fifths)  # Move to the next key in the circle

    return sorted_songs


def extract_songs_from_playlist(sp, playlist_link):
    user_id = sp.current_user()['id']  # Get the current user's Spotify username
    playlist_id = playlist_link.split("playlist/")[-1].split("?")[0]
    original_playlist = sp.playlist(playlist_id)  # Get the original playlist details
    original_playlist_name = original_playlist['name']  # Get the original playlist name

    results = sp.playlist_tracks(playlist_id)

    songs_list = []  # List to store song info

    for item in results['items']:
        track = item['track']
        song_name = track['name']
        artist = track['artists'][0]['name']

        bpm, key = get_track_features(sp, song_name, artist)
        if bpm and key:
            songs_list.append({'id': track['id'], 'name': song_name, 'bpm': bpm, 'key': key})

    sorted_songs = sort_songs_by_custom_rules(songs_list)
    new_playlist_name = f"{original_playlist_name} - Magical Sort!"
    new_playlist = sp.user_playlist_create(user_id, new_playlist_name, public=True)

    sorted_song_ids = [song['id'] for song in sorted_songs]
    sp.user_playlist_add_tracks(user_id, new_playlist['id'], sorted_song_ids)

    print(f"New Playlist '{new_playlist_name}' created! Link: {new_playlist['external_urls']['spotify']}")


def get_track_features(sp, song_name, artist):
    # Key map
    key_map = {
        0: "C",
        1: "C♯/D♭",
        2: "D",
        3: "D♯/E♭",
        4: "E",
        5: "F",
        6: "F♯/G♭",
        7: "G",
        8: "G♯/A♭",
        9: "A",
        10: "A♯/B♭",
        11: "B"
    }

    results = sp.search(q=f'track:{song_name} artist:{artist}', limit=1)
    if not results['tracks']['items']:
        print(f"No track found for {song_name} by {artist}")
        return None, None

    track_id = results['tracks']['items'][0]['id']
    features = sp.audio_features([track_id])[0]

    bpm = round(features['tempo'])
    key_name = key_map[features['key']]

    return bpm, key_name


def fetch_song_info_from_file(sp, filename):
    with open(filename, 'r') as file:
        for line in file:
            try:
                song_name, artist = line.strip().split('  ')
                bpm, key = get_track_features(sp, song_name.strip(), artist.strip())
                save_to_file(song_name, bpm, key)
            except ValueError:
                print(f"Error processing line: '{line.strip()}'. Please ensure it's formatted correctly.")


def fetch_song_info_from_input(sp):
    song_name = input("Enter song name: ").strip()
    artist = input("Enter artist name: ").strip()
    bpm, key = get_track_features(sp, song_name, artist)
    if bpm and key:
        save_to_file(song_name, bpm, key)


def save_to_file(song_name, bpm, key):
    with open("song_info.txt", "a", encoding="utf-8") as file:
        file.write(f"{song_name} - {bpm} BPM - Key {key}\n")
    print(f"Saved {song_name} - {bpm} BPM - Key {key} to song_info.txt")


if __name__ == "__main__":
    CLIENT_ID = 'Your CLIENT ID'
    CLIENT_SECRET = 'Your seret CLIENT ID'
    SPOTIPY_REDIRECT_URI = 'Your callback server'

    auth_manager = SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI,
        scope="playlist-modify-public"
    )
    sp = spotipy.Spotify(auth_manager=auth_manager)

    option = input(
        "Enter 'file' to read from a text file, 'input' to manually input song names, or 'link' to provide a Spotify "
        "playlist link: ").lower()

    if option == 'file':
        filename = input("Enter the filename: ").strip()
        fetch_song_info_from_file(sp, filename)
    elif option == 'input':
        fetch_song_info_from_input(sp)
    elif option == 'link':
        playlist_link = input("Enter the Spotify playlist link: ").strip()
        extract_songs_from_playlist(sp, playlist_link)
    else:
        print("Invalid option.")
