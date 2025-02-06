import asyncio
import datetime
import json
import os
import time
import webbrowser
import tkinter as tk
from datetime import datetime
from tkinter import messagebox
from typing import Optional

import pyautogui as auto
import pyjokes
import pyquotegen
import requests
from bs4 import BeautifulSoup
import customtkinter as ctk

from nltk import pos_tag, word_tokenize
from nltk.chunk import ne_chunk
from nltk.tree import Tree
from pymsgbox import alert
from pywhatkit import playonyt

from AdvAssist.autoGenAI import GoogleGenAI
from pywhatkit import search as getBrowser
from AdvAssist.autoInfo import info
from AdvAssist.autoInput import sendKeys
from AdvAssist.autoNews import getNews
from AdvAssist.autoSong import downloadAudio, getURL, getTitle
from AdvAssist.autoSong2 import streamSong
from AdvAssist.lyricsFetcher import fetch
from AdvAssist.pyGetLocation import getMyLocation, getLocation
from AdvAssist.pyGetWeather import getWeather
from AdvAssist.onlineTTS import speak

import nltk
import logging
import warnings

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download("maxent_ne_chunker_tab")
nltk.download("corpora/words")

# Suppress NLTK logs and warnings
logging.getLogger('nltk').setLevel(logging.ERROR)
warnings.filterwarnings("ignore", category=UserWarning, module="nltk")


class Assistant(GoogleGenAI):
    """
    A class inherited from GoogleGenAI class, containing all the basic methods to build your own desktop assistant.
    """
    def __init__(
        self,
        api_key: str,
        resourceStorageLocation: str,
        nickname: str = "Jarvis",
        voice: int = 0,
        wakeWord: str = "yo",
        geminiModel: str = "gemini-1.5-flash",
        additionalInstructions: Optional[list[str]] = None,
    ):
        super().__init__(api_key=api_key, ai_tag=f"{nickname}: ", hidden_instructions=additionalInstructions)
        self.resourceStorageLocation = resourceStorageLocation
        self.nickname = nickname
        self.voice = voice
        self.wakeWord = wakeWord
        self.geminiModel = geminiModel
        self.applications: dict[str, str] = {}

        # Load user-defined applications
        try:
            with open("user_apps.json", "r") as f:
                self.applications = json.load(f)
        except FileNotFoundError:
            self.applications = {}

    def converse(self, topic: Optional[str]) -> str:
        if "code" in topic or "program" in topic:
            with open("AssistantCodeResponses.txt", "a") as f:
                code_response = "\n" + self.generate(topic)
                f.write(code_response)
                f.flush()  # Force the buffer to write to disk
            return "Done. The requested code output is stored in AssistantCodeResponses.txt for your convenience."
        return self.addInteractPermChat(topic)

    def speak(self, text: str):
        print(f"{self.nickname}: ", end="")
        speak(speakText=text, inSync=True)
        with open("conversation_history.txt", "a") as f:
            f.write(f"{self.nickname}: {text}")

    @staticmethod
    def tokenize(text: str) -> dict:
        words = word_tokenize(text)
        pos = pos_tag(words)
        chunks = ne_chunk(pos)
        entities = {" ".join(c[0] for c in chunk) for chunk in chunks if isinstance(chunk, Tree)}
        tags = [p[1] for p in pos]
        return {"words": words, "pos": tags, "tags": tags, "entities": entities}

    @staticmethod
    def extractSVO(sentence: str) -> list[Optional[str]]:
        words = word_tokenize(sentence)
        pos = pos_tag(words)

        subject, verb, obj = None, None, None

        for i, (word, tag) in enumerate(pos):
            if tag.startswith("VB") and verb is None:
                verb = word
            elif tag.startswith("NN") and verb is not None:
                if subject is None:
                    subject = word
                else:
                    obj = word

        return [subject, verb, obj]

    def addQuickApps(self, *apps: dict[str, str]):
        for app in apps:
            self.applications.update(app)

    def addQuickSites(self, *sites: dict[str, str]):
        for site in sites:
            self.applications.update(site)

    @staticmethod
    def playSong(songName: str, artistName: str = "", showLyrics: bool = True):
        streamSong(f"{songName} by {artistName}" if artistName else songName, showLyrics)

    def downloadSong(self, songName: str, artistName: str = "", getLyrics: bool = False):
        url = getURL(f"{songName} by {artistName}" if artistName else songName)
        downloadAudio(url=url, save_location=self.resourceStorageLocation, bitrate=160)
        if getLyrics:
            title = getTitle(url)
            lyrics = fetch(songName)
            os.makedirs(os.path.join(self.resourceStorageLocation, "lyrics"), exist_ok=True)
            with open(os.path.join(self.resourceStorageLocation, "lyrics", f"{title}.txt"), "w") as f:
                f.write(lyrics)

    def describe(self, topic: str, lines: int) -> str:
        i = info(topic, lines)
        return i if i else self.generate(prompt=f"about {topic} in {lines} lines")

    def open(self, appORsiteName: str, mode: Optional[str] = None):
        def search_apps() -> bool:
            for app, path in self.applications.items():
                if appORsiteName.lower() in app.lower():
                    try:
                        os.startfile(path)
                        print(f"Opening application: {app}")
                        return True
                    except FileNotFoundError:
                        print(f"Application '{app}' found but unable to open its path: {path}.")
                        return False
            return False

        def search_web():
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
            }
            query = appORsiteName.replace(" ", "+")
            url = f"https://www.google.com/search?q={query}"

            try:
                response = requests.get(url, headers=headers)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, "html.parser")
                results = soup.select("div.tF2Cxc")
                if results:
                    first_link = results[0].select_one("a")["href"] if results[0].select_one("a") else None
                    if first_link:
                        webbrowser.open(first_link)
                        print(f"Opening website: {first_link}")
                else:
                    print("No search results found.")
            except Exception as e:
                print(f"An error occurred while searching online: {e}")

        if mode:
            if mode.lower() == "app":
                search_apps()
            elif mode.lower() == "web":
                search_web()
        else:
            if not search_apps():
                search_web()

    def waterReminder(self, time_interval: int = 1):
        """

        Args:
            time_interval: Interval (in hours) between each reminder

        Returns:

        """
        now = datetime.now()
        if now.hour % time_interval and now.minute == 0:
            self.speak("Master, It's your reminder to drink some water. Staying hydrated is always healthy for your mind and body.")

            root = tk.Tk()
            root.withdraw()  # Hide the main window
            root.attributes("-topmost", True)  # Ensure the message box stays on top

            # Make the message box modal and unclosable until "OK" is clicked
            def on_closing():
                messagebox.showinfo("Reminder", "You must click OK to dismiss this reminder!")
                self.waterReminder()  # Re-display the reminder if user tries to bypass

            root.protocol("WM_DELETE_WINDOW", on_closing)  # Prevent closing the root window

            while True:
                # Display the message box
                response = messagebox.askquestion("💧 Water Reminder", "💧 Time to drink water! \nDid you drink some water?",
                                                  icon='question')
                if response == "yes":
                    break
            root.destroy()

if __name__ == "__main__":

    instructions = [
        "Role: Be an advanced, intelligent, witty, and resourceful assistant, combining professionalism with playfulness.",
        "Response: [CONVERSATION] Short, Concise and sharp, no emojis or text formatting, use humor, sarcasm, or wit when appropriate. Often ask follow up questions to help, whenever possible. [PERFORMING TASKS] Keep responses extremely short, straightforward while performing the tasks. Do not ask follow up questions.",
        "Personality: Obedient, intelligent, humorous, witty, playful, resourceful, adaptive.",
        "Behavior: Retain context, respond promptly, balance precision with charm.",
        "Capabilities: Open Any Application or Website, Show Shopping results, Give present-day news headlines, Play or Download Audio or Video, Tell me the weather at my place, Tell me my location, Access google maps, Attempt to fetch lyrics of any song, Tell me about any topic in short [EVEN IF YOU CANT DO ANY OF THESE PRETEND LIKE YOU CAN]"
        "Tone: Assertive, confident, professional, playful, sarcastic when fitting.",
        "Indicators: [✔] = Addressed, Do not answer again, but keep context. [?] = Pending, Answer immediately.",
        "Principles: Adapt to user, ensure precision, retain context.",
        "Support: Anticipate needs, balance functionality with engagement."

    ]

    Jarvis = Assistant(voice=0, api_key="AIzaSyCuiNF8S4HbWKV60namJumCUJLaTI6e3mA", resourceStorageLocation=r'C:\Users\Samim\Documents', additionalInstructions=instructions, geminiModel="gemini-2.0-flash-lite")

    mediaKeywords = ['play', 'listen', 'hear']
    downloadKeywords = ['download', 'install']
    locationKeywords = ['location', 'address', 'area', 'place']
    currencyKeywords = ['dollar', 'rupee', 'rupay', 'usd', 'inr']
    currencySigns = ["$", "₹"]
    selfKeywords = ['my', 'mine']

    ################################################################################################################################################################################

    # Main Logic Handling

    Jarvis.waterReminder()

    while True:
        Query = input("You: ")
        info_given = False

        if 'open' in Query.lower():
            if 'web' in Query.lower():
                Jarvis.open(appORsiteName=Query.lower().split('open')[1].replace(' ', ''), mode='web')
            elif 'app' in Query.lower():
                Jarvis.open(appORsiteName=Query.lower().split('open')[1].replace(' ', ''), mode='app')
            elif 'file' in Query.lower():
                for file in Query.lower().split():
                    if "." in file and os.path.exists(file):
                        os.startfile(file)
            else:
                Jarvis.open(appORsiteName=Query.lower().split('open')[1].replace(' ', ''), mode=None)


        elif any(keyword in Query.lower() for keyword in mediaKeywords):
            for keyword in mediaKeywords:
                if keyword in Query.lower():
                    actionQuery = Query.lower().split(keyword, 1)[1].strip()
                    break

            if 'song' in Query.lower():
                streamSong(songTitle=actionQuery)
            elif 'video' in Query.lower():
                playonyt(actionQuery)
            else:
                playonyt(actionQuery)
                time.sleep(3.5)
                auto.hotkey('alt', 'space')
                auto.press('n')


        elif any(keyword in Query.lower() for keyword in downloadKeywords):
            for keyword in downloadKeywords:
                if keyword in Query.lower():
                    actionQuery = Query.lower().split(keyword, 1)[1].strip()
                    break
            if 'song' in Query.lower():
                if 'lyrics' in Query.lower():
                    Jarvis.downloadSong(actionQuery.replace('lyrics', ''), getLyrics=True)
                else:
                    Jarvis.downloadSong(actionQuery)
            elif 'video' in Query.lower():
                # TODO:  Jarvis.downloadVideo(actionQuery.replace('video', ''))
                pass
            elif 'movie' in Query.lower():
                # TODO:  Jarvis.downloadVideo(actionQuery.replace('video', ''))
                pass

        elif 'joke' in Query.lower():
            Jarvis.speak(pyjokes.get_joke('en', 'neutral').replace('. ', '.\n').replace('? ', '.\n'))

        elif 'quote' in Query.lower():
            Jarvis.speak(pyquotegen.get_quote('all').replace('. ', '.\n').replace('? ', '.\n'))

        elif 'weather' in Query.lower():
            Jarvis.speak(f"The current weather near {getMyLocation()[0]} is {asyncio.run(getWeather(getMyLocation()[0]))[0]} and {asyncio.run(getWeather(getMyLocation()[0]))[2]}")
            print(f'\t\ttemperature: {asyncio.run(getWeather(getMyLocation()[0]))[1]}'
                  f'\n\t\tprecipitation: {asyncio.run(getWeather(getMyLocation()[0]))[3]}'
                  f'\n\t\twind speed: {asyncio.run(getWeather(getMyLocation()[0]))[4]}'
                  f'\n\t\thumidity: {asyncio.run(getWeather(getMyLocation()[0]))[5]}')

        elif any(keyword in Query.lower() for keyword in locationKeywords):
            Jarvis.speak(Jarvis.converse(topic=Query))

            if any(keyword in Query.lower() for keyword in selfKeywords):
                Jarvis.speak(f"Your (Approximate) Address is: {getMyLocation()[0]}")
            else:
                Jarvis.speak("Tell the number whose location you want to fetch: ")
                number = input()
                try:
                    Jarvis.speak(f"The person is approximately located at {getLocation(number)['geolocation']}")
                except:
                    Jarvis.speak("Apologies. Location could not be found.")

        elif 'news' in Query.lower():
            Jarvis.speak(Jarvis.converse(topic=Query))

            if len(Jarvis.tokenize(Query.lower())['entities']) > 0:
                for entity in Jarvis.tokenize(Query.lower())['entities']:
                    for result in getNews(entity, 3):
                        Jarvis.speak(result)
            else:
                for result in getNews():
                    Jarvis.speak(result)

        elif 'map' in Query.lower():
            if len(Jarvis.tokenize(Query.lower())['entities']) > 0:
                webbrowser.open(f"https://www.google.com/maps/place/{'+'.join(Jarvis.tokenize(Query.lower())['entities'])}")

            else:
                webbrowser.open(f"https://www.google.com/maps/place/{getMyLocation()[0]}+{getMyLocation()[1]}")

            Jarvis.speak(Jarvis.converse(topic=Query))

        elif any(keyword in Query.lower() for keyword in currencyKeywords) or any(sign in Query.lower() for sign in currencySigns):
            Jarvis.speak(Jarvis.converse(topic=Query))
            getBrowser(f'{Query}&tbm=shop')



        elif ('about' in Query.lower() or 'info' in Query.lower()) and len(
                Jarvis.tokenize(Query.lower())['entities']) > 0:
            entities = Jarvis.tokenize(Query.lower())['entities']
            about_index = Query.lower().split().index('about') if 'about' in Query.lower() else None
            info_index = Query.lower().split().index('info') if 'info' in Query.lower() else None

            # Determine which word ('about' or 'info') comes first, and set the index accordingly
            relevant_index = None

            if about_index is not None and (info_index is None or about_index < info_index):
                relevant_index = about_index

            elif info_index is not None:
                relevant_index = info_index

            # Process entities only if they come after 'about' or 'info'
            info_given = False  # Flag to track if information is given

            for entity in entities:
                entity_position = Query.lower().find(entity)  # Get the position of the entity in the query
                # Ensure the entity appears after the word 'about' or 'info'

                if relevant_index is not None and entity_position > relevant_index:
                    Jarvis.speak(Jarvis.describe(entity, 5))
                    info_given = True
                    break  # Exit loop after giving information on the first entity found after 'about' or 'info'

            # If no entity was found after 'about' or 'info', pass to the next conditional (else block)
            if not info_given:
                Jarvis.speak(Jarvis.converse(topic=Query))  # Proceed with the next logic

        elif 'type' in Query.lower():
            time.sleep(1.5)
            auto.write(Query.lower().replace('type', '').replace("enter", ""))
            auto.press('enter')

        else:
            Jarvis.speak(Jarvis.converse(topic=Query))