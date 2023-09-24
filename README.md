# README for Magical Sort Playlist Project

## Description

This project sorts a given list of songs based on the Circle of Fifths and their BPM (Beats per Minute). Users can input the songs either manually, by reading from a file, or by providing a Spotify playlist link. The sorted songs are then added to a new playlist named "{original_playlist_name} - Magical Sort!".

## Dependencies

- Python
- Spotipy Library

## Installation

1. Ensure you have Python installed on your system.
2. Install the Spotipy library with the following command:
    ```bash
    pip install spotipy
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

1. Manually enter song data:

    ```plaintext
    Enter 'file' to read from a text file, 'input' to manually input song names, or 'link' to provide a Spotify playlist link: input
    Enter song name: SongName
    Enter artist name: ArtistName
    ```

2. Enter song data via file:

    ```plaintext
    Enter 'file' to read from a text file, 'input' to manually input song names, or 'link' to provide a Spotify playlist link: file
    Enter the filename: filename.txt
    ```

3. Enter a Spotify playlist link:

    ```plaintext
    Enter 'file' to read from a text file, 'input' to manually input song names, or 'link' to provide a Spotify playlist link: link
    Enter the Spotify playlist link: playlist_link
    ```

The script will sort the songs based on their keys and BPM and create a new playlist with the sorted songs.

## Output

After successfully sorting the songs and creating a new playlist, the script will output a message with the name and link of the new playlist:

```plaintext
New Playlist '{new_playlist_name}' created! Link: {new_playlist['external_urls']['spotify']}
```

## Troubleshooting

If you encounter an error related to song information retrieval, ensure that the song name and artist name are correctly formatted. If reading from a file, ensure each line is formatted as `song_name  artist_name`.

## Contribution

To contribute to this project, you can make a pull request or raise an issue on the project's repository.

## License

This project is open source and available under the [MIT License](https://opensource.org/licenses/MIT).
