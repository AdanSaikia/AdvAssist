def setAlarm(d: int, h: int, m: int, pathOfRingtone: str) -> None:
    """
    Sets an alarm that rings at the specified day, hour, and minute.

    Args:
        d (int): The day of the month (1-31).
        h (int): The hour in 24-hour format (0-23).
        m (int): The minute (0-59).
        pathOfRingtone (str): Path to the ringtone file to play.
    """
    import time
    from datetime import datetime
    import pygame  # For audio playback
    print(f"Alarm set for {d:02d}-{h:02d}:{m:02d}. Waiting...")

    while True:
        now = datetime.now()
        if now.day == d and now.hour == h and now.minute == m:
            print("Alarm ringing!")
            try:
                pygame.mixer.init()
                pygame.mixer.music.load(pathOfRingtone)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():  # Wait for the sound to finish
                    time.sleep(1)
            except Exception as e:
                print(f"Error playing ringtone: {e}")
            finally:
                pygame.mixer.quit()
            break
        time.sleep(1)  # Avoid excessive CPU usage

if __name__ == "__main__":
    # Set the alarm for 1 minute from the current time
    import time
    from datetime import datetime
    import pygame  # For audio playback
    current_time = datetime.now()
    setAlarm(
        d=current_time.day,
        h=current_time.hour,
        m=(current_time.minute + 1) % 60,  # Adjust to 1 minute later
        pathOfRingtone=r"C:\Users\Samim\Documents\Practice\pyauto\Adele - Hello (Official Music Video)(MP3_160K) - Copy.mp3"
    )
