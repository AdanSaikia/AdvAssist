import edge_tts
import io
import os
import pygame
import time
import threading
import asyncio

# Hide Pygame support prompt
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
pygame.mixer.init()

def speak(displayPrompt: str = "", speakText: str = "Hello World!", inSync: bool = False, volume: float = 1.0, rate: int = 15, voice: int = 0, printText: bool = True):
    """
    Speaks the given text, either normally or in sync with a typewriter effect.

    Args:
        displayPrompt (str): A prefix to display before the text.
        speakText (str): The text to speak.
        inSync (bool): If True, speaks the text in sync with a typewriter effect.
        volume (float): The volume of the speech (0.0 to 1.0).
        rate (int): The speech rate in words per minute (100 to 300).
        voice (int): The voice ID for the speech (0=Male, 1=Female). Default is 0.
        printText (bool): If True, prints the text being spoken.
    """

    if voice == 0:
        voice = "en-US-AndrewMultilingualNeural"
    elif voice == 1:
        voice = "en-US-EmmaNeural"

    # Asynchronous function for speaking text using Edge TTS
    async def speak_async(text, voice: str = voice, pitch: str = "+0Hz", rate: str = "+0%", volume: str = "100%"):
        try:
            # Wait for 1 second before starting to speak
            await asyncio.sleep(1)

            # Create an in-memory buffer for the audio with custom settings
            communicate = edge_tts.Communicate(text, voice, pitch=pitch, rate=rate, volume=volume)
            stream = io.BytesIO()

            # Save TTS output directly into the in-memory buffer using async for
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    stream.write(chunk["data"])

            if stream.tell() == 0:
                raise ValueError("No audio data was received.")

            # Prepare the audio data for playback
            stream.seek(0)
            pygame.mixer.music.load(stream)
            pygame.mixer.music.play()

            # Wait for playback to finish
            while pygame.mixer.music.get_busy():
                await asyncio.sleep(0.1)  # Check every 100ms for playback status

        except Exception as e:
            print(f"Error: {e}")

    # Function for printing text with a typewriter effect
    def typewriter_effect(text):
        """Print text with a typewriter effect."""
        time.sleep(rate//7.45)
        if not text:
            return  # Do nothing if text is None or empty
        for char in text:
            print(char, end="", flush=True)
            if char == ",":
                time.sleep(0.3)
            elif char == ".":
                time.sleep(0.6)
            elif char == "\n":
                time.sleep(0.5)
            else:
                time.sleep(0.045)
        print()  # Ensure newline at the end

    # Begin the speech and typewriter effect
    if printText:
        print(displayPrompt, end="")

    # Convert volume to percentage
    volume_str = f"+{int(volume * 100)}%"  # Converts 1.0 to "100%" and so on.

    if inSync:
        # Run typewriter and speech in parallel using threading
        typewriter_thread = threading.Thread(target=typewriter_effect, args=(speakText,))
        speech_thread = threading.Thread(target=asyncio.run, args=(speak_async(speakText, voice, "+0Hz", f"+{rate}%", volume_str),))

        # Start both threads
        typewriter_thread.start()
        speech_thread.start()

        # Wait for both threads to finish
        typewriter_thread.join()
        speech_thread.join()
    else:
        # Normal TTS without typewriter effect
        asyncio.run(speak_async(speakText, voice="en-US-AndrewMultilingualNeural", pitch="+0Hz", rate=f"+{rate}%", volume=volume_str))
        if printText:
            print(speakText)

# Correct the entry point of the script
if __name__ == "__main__":
    speak(displayPrompt="Assistant says: ", speakText="Good Afternoon, how are you sir? I am glad to assist you today.",
          rate=20, volume=1.0, inSync=True)
