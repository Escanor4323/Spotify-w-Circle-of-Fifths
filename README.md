# README for Magical Sort Playlist Project

## Description

This advanced project sorts a given list of songs based on the Circle of Fifths and their BPM (Beats per Minute) and creates a new visually appealing playlist. Users can input the songs either manually, by reading from a file, or by providing a Spotify playlist link. The sorted songs are then added to a new playlist named "{original_playlist_name} - Magical!". Additionally, the project downloads the original playlist image, extracts the dominant color, and creates a new image with the dominant color and a logo for the new playlist.

## New Functionalities

- Downloads the original playlist image.
- Extracts the dominant color from the original playlist image.
- Creates a new image with the dominant color and a logo for the new playlist.
- Uploads the new playlist image to Spotify.

## Dependencies

- Python
- Spotipy Library
- Requests Library
- PIL (Pillow)
- ColorThief Library

## Installation

1. Ensure you have Python installed on your system.
2. Install the required libraries with the following command:
    ```bash
    pip install spotipy requests pillow colorthief
    ```

## Setting up the Application

Before running the application, replace `'YOUR CLIENT ID'`, `'YOUR CLIENT SECRET ID'`, and `'YOUR CALLBACK SERVER'` in the code with your Spotify API credentials:

```python
    CLIENT_ID = 'YOUR CLIENT ID'
    CLIENT_SECRET = 'YOUR CLIENT SECRET ID'
    SPOTIPY_REDIRECT_URI = 'YOUR CALLBACK SERVER'
```

## Usage

1. Run the script with the command:
    ```bash
    python get_song_info.py
    ```
2. You will be prompted with options to enter song data:
    - Enter `'file'` to read song data from a text file.
    - Enter `'input'` to manually input song data.
    - Enter `'link'` to provide a Spotify playlist link.
    
3. Follow the on-screen prompts to input additional data based on your chosen option.

## Examples

<!-- Previous examples remain the same, no change needed. -->

## Output

After successfully sorting the songs, creating a new playlist, and processing the playlist image, the script will output a message with the name and link of the new playlist:

```plaintext
New Playlist '{new_playlist_name}' created! Link: {new_playlist['external_urls']['spotify']}
```

## Troubleshooting

If you encounter an error related to song information retrieval or image processing, ensure that the song name and artist name are correctly formatted and the image file is accessible. If reading from a file, ensure each line is formatted as `song_name  artist_name`.

## Contribution

To contribute to this project, you can make a pull request or raise an issue on the project's repository.

## License

This project is open source and available under the [MIT License](https://opensource.org/licenses/MIT).
