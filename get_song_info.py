import base64

import spotipy
from spotipy.oauth2 import *
import requests
from PIL import Image
from colorthief import ColorThief


def sort_songs_by_custom_rules(songs):
    circle_of_fifths = [
        "C", "G", "D", "A", "E", "B/Cb", "F#/Gb", "C#/Db", "G#/Ab", "D#/Eb", "A#/Bb", "F"
    ]

    def get_key_index(key):
        normalized_key = key.replace('♯', '#').replace('♭', 'b')
        normalized_key_parts = set(normalized_key.split('/'))
        for idx, circle_key in enumerate(circle_of_fifths):
            circle_key_parts = set(circle_key.split('/'))
            if normalized_key_parts.intersection(circle_key_parts):
                return idx
        raise ValueError(f"{key} is not in the Circle of Fifths list.")

    # Normalize keys in the songs data and group songs by key.
    songs_by_key = {}
    for song in songs:
        song['key'] = song['key'].replace('♯', '#').replace('♭', 'b')
        key_index = get_key_index(song['key'])
        if key_index not in songs_by_key:
            songs_by_key[key_index] = []
        songs_by_key[key_index].append(song)

    sorted_songs = []
    bpm_switch = False

    for current_index in range(len(circle_of_fifths)):
        if current_index in songs_by_key:
            current_key_songs = songs_by_key[current_index]

            # Sort songs by BPM, alternate BPM order for each key group.
            if not bpm_switch:
                current_key_songs = sorted(current_key_songs, key=lambda x: x['bpm'])
            else:
                current_key_songs = sorted(current_key_songs, key=lambda x: x['bpm'], reverse=True)

            # Add up to 4 songs from the current key group to the sorted_songs list.
            sorted_songs.extend(current_key_songs[:4])

            bpm_switch = not bpm_switch  # Toggle the BPM order for the next key group.

    return sorted_songs


def extract_songs_from_playlist(sp, playlist_link):
    user_id = sp.current_user()['id']
    playlist_id = playlist_link.split("playlist/")[-1].split("?")[0]
    original_playlist = sp.playlist(playlist_id)
    original_playlist_name = original_playlist['name']
    original_playlist_image_url = original_playlist['images'][0]['url']

    # Downloading the original playlist image
    response = requests.get(original_playlist_image_url)
    with open("original_playlist_image.jpg", "wb") as file:
        file.write(response.content)

    # Extracting dominant color from the original playlist image
    color_thief = ColorThief("original_playlist_image.jpg")
    dominant_color = color_thief.get_color(quality=1)

    # Creating a new image with the dominant color
    new_image = Image.new('RGB', (500, 500), dominant_color)

    # Open the logo image
    logo = Image.open("logo.png")

    # Calculate the position where the logo should be pasted.
    # This example places the logo at the top left of the new image.
    # Adjust the coordinates (0, 0) to place the logo at a different position.
    position = (0, 0)

    # Paste the logo onto the new image at the specified position.
    new_image.paste(logo, position, logo)

    # Save the new image with the logo.
    new_image.save("new_playlist_image.jpg")

    results = sp.playlist_tracks(playlist_id)
    songs_list = []

    for item in results['items']:
        track = item['track']
        song_name = track['name']
        artist = track['artists'][0]['name']
        bpm, key = get_track_features(sp, song_name, artist)
        if bpm and key:
            songs_list.append({'id': track['id'], 'name': song_name, 'bpm': bpm, 'key': key})

    sorted_songs = sort_songs_by_custom_rules(songs_list)
    new_playlist_name = f"{original_playlist_name} - Magical!"
    new_playlist = sp.user_playlist_create(user_id, new_playlist_name, public=True)

    sorted_song_ids = [song['id'] for song in sorted_songs]
    sp.user_playlist_add_tracks(user_id, new_playlist['id'], sorted_song_ids)

    # Uploading the new playlist image with exception handling
    try:
        with open("new_playlist_image.jpg", "rb") as file:
            base64_img = base64.b64encode(file.read()).decode('utf-8')
            sp.playlist_upload_cover_image(new_playlist['id'], base64_img)
    except Exception as e:
        print(f"An error occurred while uploading the image: {e}")

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
    CLIENT_ID = 'fe6499ff20864d94a8d9daee54e078c1'
    CLIENT_SECRET = 'f7289cd180a1426e868076c6615dc846'
    SPOTIPY_REDIRECT_URI = 'http://127.0.0.1:8080/callback'

    auth_manager = SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI,
        scope="playlist-modify-public ugc-image-upload"
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
