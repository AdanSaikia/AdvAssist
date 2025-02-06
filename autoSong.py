import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import pygame.mixer
import yt_dlp
from youtubesearchpython import VideosSearch
from AdvAssist.lyricsFetcher import fetch

def createLyricsDirectory(save_location):
    """Ensure the lyrics directory exists."""
    lyrics_dir = os.path.join(save_location, 'lyrics')
    if not os.path.exists(lyrics_dir):
        os.mkdir(lyrics_dir)

def getURL(title):
    """Search for a YouTube video by its title and return the first video URL."""
    videos_search = VideosSearch(title, limit=1)
    results = videos_search.result()
    if results["result"]:
        return results["result"][0]["link"]
    return None

def getTitle(url):
    """Search for a YouTube video by its URL and return the title."""
    videos_search = VideosSearch(url, limit=1)
    results = videos_search.result()
    if results["result"]:
        return results["result"][0]["title"].replace("|", "｜")
    return None

def downloadAudio(url:str, save_location:str, bitrate:int):
    """Download YouTube audio as MP3 using yt-dlp and return the file path."""
    options = {
        'format': 'bestaudio/best',
        'postprocessors': [
            {
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': f'{bitrate}',
            }
        ],
        'outtmpl': os.path.join(save_location, '%(title)s.%(ext)s'),
        'quiet': True,
        'no_warnings': True,
        'logtostderr': False,
    }

    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            title = info_dict["title"].replace("|", "｜")
            file_path = os.path.join(save_location, f"{title}.mp3")
            # print("Audio has been successfully downloaded as MP3.") DEBUG
            return file_path
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def playAudio(path):
    """Play the audio using pygame mixer."""
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    except pygame.error as e:
        print(f"Error playing song: {e}")
    finally:
        pygame.mixer.quit()

def playSong(songTitle:str, save_location:str):
    """Search for a song, download it if it doesn't exist, and play it."""
    createLyricsDirectory(save_location)

    url = getURL(songTitle)
    if not url:
        print("No results found for your query.")
        return

    title = getTitle(url)
    if not title:
        print("Failed to retrieve the title of the song.")
        return

    audio_file_path = os.path.join(save_location, f"{title}.mp3")

    if os.path.exists(audio_file_path):
        download_again = input(
            f"The specified audio file already exists at '{audio_file_path}'\n"
            f"Do you still wish to re-download before playing? (y/n)\n"
        ).lower()
        if download_again == "y":
            # print(f"Extracting Audio From {url}") DEBUG
            audio_file_path = downloadAudio(url, save_location, bitrate=128)
            if audio_file_path:
                with open(os.path.join(save_location, 'lyrics', f"{title}.txt"), "w") as f:
                    f.write(fetch(songTitle))
                # print(f"Downloaded file path: {audio_file_path}") DEBUG
    else:
        # print(f"Extracting Audio From {url}") DEBUG
        audio_file_path = downloadAudio(url, save_location, bitrate=128)
        if audio_file_path:
            with open(os.path.join(save_location, 'lyrics', f"{title}.txt"), "w") as f:
                f.write(fetch(songTitle))
            print(f"Downloaded file path: {audio_file_path}")

    if audio_file_path:
        # print(f"Now Playing: {title}") DEBUG
        lyrics_path = os.path.join(save_location, 'lyrics', f"{title}.txt")
        if os.path.exists(lyrics_path):
            with open(lyrics_path, "r") as f:
                print(f.read())
        playAudio(audio_file_path)

if __name__ == "__main__":
    song_title = input(
        "Hint: Unable to find your search?\n"
        "Try providing more info about the song (e.g., Artist, Album)\n\n"
        "Enter the title of the song you want to play: "
    )
    location = input(
        "Enter the save location (default is C:/Users/Samim/Music): "
    ) or r"C:\\Users\\Samim\\Music"
    playSong(song_title, location)
