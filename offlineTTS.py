def speak(displayPrompt: str = "", speakText: str = "Hello World!", inSync: bool = False, volume: float = 1.0, rate: int = 185, voice: int = 1, printText: bool = True):
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
    import pyttsx3
    import time
    import threading

    # Initialize pyttsx3 engine
    engine = pyttsx3.init()
    engine.setProperty('rate', rate)
    engine.setProperty('volume', volume)

    # Set the voice based on gender
    voices = engine.getProperty('voices')
    if voice == 0 and len(voices) > 0:
        engine.setProperty('voice', voices[0].id)  # Male voice
    elif voice == 1 and len(voices) > 1:
        engine.setProperty('voice', voices[1].id)  # Female voice

    def typewriter_effect(text):
        """Print text with a typewriter effect."""
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

    def speak_text(text):
        """Speak the text using pyttsx3."""
        engine.say(text.replace('**', '').replace('==', ''))
        engine.runAndWait()

    if inSync:
        # Display the prompt if any
        if printText:
            print(displayPrompt, end="")

        # Run typewriter and speech in parallel
        typewriter_thread = threading.Thread(target=typewriter_effect, args=(speakText,))
        typewriter_thread.start()

        speak_text(speakText)  # Speak the entire text
        typewriter_thread.join()  # Wait for typewriter to complete
    else:
        # Normal TTS without typewriter effect
        if printText:
            print(displayPrompt, speakText)
        speak_text(speakText)


if __name__ == "__main__":
    response = "Harry Potter is an orphan who discovers he's a wizard. He goes to Hogwarts School of Witchcraft and Wizardry and learns magic, makes friends, and fights the dark wizard Voldemort."
    speak(displayPrompt="AI: ", speakText=response, inSync=True, printText=True)
