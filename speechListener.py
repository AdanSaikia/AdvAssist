def listen(text: str = "You: ", timeout: int = 3, phrase_time_limit: int = 2, ):
    """Listen for speech and recognise it."""

    import speech_recognition as sr

    print(text, end="")
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)  # Adjust to the environment noise level
        try:
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
        except sr.WaitTimeoutError:
            print("\n\nListening timed out while waiting for phrase to start.")
            return ""

    try:
        query = recognizer.recognize_google(audio)
        print(query)  
        return query.lower()
    except sr.UnknownValueError:
        print("\n\nSorry, I couldn't understand that.")
        return ""
    except sr.RequestError as e:
        print(f"\n\nError occurred during speech recognition: {e}")
        return ""
    except Exception as e:
        print(f"\n\nAn unexpected error occurred: {e}")
        return ""
    

# def listen(text: str, timeout: int = 3, phrase_time_limit: int = 2, ):
#     """Listen for speech and recognise it."""

#     import speech_recognition as sr

#     print(text, end="")
#     recognizer = sr.Recognizer()
#     with sr.Microphone() as source:
#         print("Listening...")
#         recognizer.adjust_for_ambient_noise(source, duration=1)  # Adjust to the environment noise level
#         try:
#             audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
#         except sr.WaitTimeoutError:
#             print("Listening timed out while waiting for phrase to start.")
#             return ""

#     try:
#         print("Recognizing...")
#         query = recognizer.recognize_google(audio)
#         print("You said:", query)  
#         return query.lower()
#     except sr.UnknownValueError:
#         print("Sorry, I couldn't understand that.")
#         return ""
#     except sr.RequestError as e:
#         print(f"Error occurred during speech recognition: {e}")
#         return ""
#     except Exception as e:
#         print(f"An unexpected error occurred: {e}")
#         return ""

if __name__ == "__main__":
    while True:
        print(listen())