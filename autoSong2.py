import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import time
import yt_dlp
import shutil
from rich import print
from AdvAssist.lyricsFetcher import fetch
import random

def getURL(title: str):
    """Search for a YouTube video using yt_dlp and return the first video URL."""
    search_query = f"ytsearch1:{title}"  # 'ytsearch1' fetches the top result
    options = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': True,  # Do not download, just search
    }
    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            results = ydl.extract_info(search_query, download=False)
            if results and "entries" in results and len(results["entries"]) > 0:
                return results["entries"][0]["url"]
            return None
    except Exception as e:
        print(f"[red]Error while searching: {e}[/red]")
        return None


def downloadAudio(ytURL: str, outputFolder: str, bitrate: int = 96):
    """Download YouTube audio as MP3 using yt-dlp."""
    # Ensure the folder exists, and if it does, clear it
    if os.path.exists(outputFolder):
        if os.path.isdir(outputFolder):
            shutil.rmtree(outputFolder)  # Remove the folder and its contents
        else:
            os.remove(outputFolder)  # In case it's a file with the same name

    os.makedirs(outputFolder, exist_ok=True)  # Recreate the folder

    options = {
        'format': 'bestaudio/best',
        'postprocessors': [
            {
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': f'{bitrate}',
            }
        ],
        'outtmpl': os.path.join(outputFolder, '%(title)s.%(ext)s'),
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
        },
        'quiet': True,
        'no_warnings': True,
        'logtostderr': False,
    }

    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            info_dict = ydl.extract_info(ytURL, download=True)
            title = info_dict["title"].replace("|", "｜")
            file_path = os.path.join(outputFolder, f"{title}.mp3")
        return file_path
    except Exception as e:
        print(f"[red]An error occurred: {e}[/red]")
        return None

def playAudio(filePath: str):
    """Play the audio using pygame mixer."""


    try:
        pygame.mixer.init()
        pygame.mixer.music.load(filePath)
        pygame.mixer.music.play()

        # Wait until the music finishes playing
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
    except pygame.error as e:
        print(f"[red]Error playing song: {e}[/red]")
    finally:
        pygame.mixer.quit()  # Always quit the mixer properly

def streamSong(songTitle:str, withLyrics:bool = True, cacheFolder:str = 'cache'):
    if os.path.exists(cacheFolder):
        if os.path.isdir(cacheFolder):
            shutil.rmtree(cacheFolder)  # Remove the folder and its contents
        else:
            os.remove(cacheFolder)  # In case it's a file with the same name

    ytURL = getURL(songTitle)

    if ytURL:
        # print(f"Found YouTube URL: {ytURL}") DEBUG
        # print("Downloading audio (lowest quality)...") DEBUG
        audioFilePath = downloadAudio(ytURL, cacheFolder)

        if audioFilePath:
            if withLyrics:
                lyrics = fetch(songName=songTitle)
                if lyrics != "":
                    lyricsColor = random.choice(['green', 'yellow', 'blue'])
                    print("\n\n\n[white bold]LYRICS[/white bold]\n")
                    print(f"[{lyricsColor}]{lyrics}[/{lyricsColor}]")
                else:
                    print("[red]Lyrics not found[/red]")
            playAudio(audioFilePath)  # Play the downloaded audio
        else:
            print("[red]Failed to download or convert audio.[/red]")
    else:
        print("[red]No video found for the given title.[/red]")

if __name__ == "__main__":
    print("[cyan bold]STREAM: [/cyan bold]", end="")
    video_title = input()
    ytURL = getURL(video_title)

    if ytURL:
        # print(f"Found YouTube URL: {ytURL}") DEBUG
        cache_folder = "cache"
        # print("Downloading audio (lowest quality)...") DEBUG
        audio_file_path = downloadAudio(ytURL, cache_folder)

        if audio_file_path:
            lyrics_color = random.choice(['green', 'yellow', 'blue'])
            print("\n\n\n[white bold]LYRICS[/white bold]\n")
            print(f"[{lyrics_color}]{fetch(songName=video_title)}[/{lyrics_color}]")
            playAudio(audio_file_path)  # Play the downloaded audio
        else:
            print("[red]Failed to download or convert audio.[/red]")
    else:
        print("[red]No video found for the given title.[/red]")
