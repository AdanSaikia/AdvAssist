# Dictionary to keep track of added shortcuts
defaultShortcuts = {'ctrl+y+t': "youtube",
        'ctrl+g': "google",
        'ctrl+f+b': "facebook",
        'ctrl+x': "twitter",
        'ctrl+i+g': "instagram",
        'ctrl+w+a': "whatsapp",
        'ctrl+n+p': "notepad.exe",
        'ctrl+c+m': "calc.exe",
        'ctrl+m+p': "mspaint.exe"}

def addShortcut(shortcutKey: str, appName: str) -> None:
    """
    Adds a single shortcut for an application or URL.

    Args:
        shortcutKey (str): The keyboard shortcut to trigger the app.
        appName (str): The app or URL to open.
    """

    import keyboard
    from autoOpen import openApp

    if appName not in defaultShortcuts:
        keyboard.add_hotkey(shortcutKey, lambda: openApp(appName))
        defaultShortcuts[appName] = shortcutKey  # Keep track of the shortcut
        print(f"Added shortcut '{shortcutKey}' for '{appName}'.")
    else:
        print(f"Shortcut for '{appName}' already exists.")

def removeShortcut(appName: str) -> None:
    """
    Removes a shortcut for an application or URL by app name.

    Args:
        appName (str): The app name whose shortcut should be removed.
    """

    import keyboard

    shortcutKey = defaultShortcuts.get(appName)
    if shortcutKey:
        keyboard.remove_hotkey(shortcutKey)
        del defaultShortcuts[appName]  # Remove from tracked hotkeys
        print(f"Removed shortcut for '{appName}'.")
    else:
        print(f"No shortcut found for '{appName}'.")

def setupShortcuts(hotkeysDict: dict) -> None:
    """
    Sets up multiple shortcuts from a dictionary of hotkeys and app names.

    Args:
        hotkeysDict (dict): Dictionary where keys are shortcut keys and values are app names.
    """
    for shortcutKey, appName in hotkeysDict.items():
        addShortcut(shortcutKey, appName)

def listenKeys():
    """
    Listens for shotcut keys.
    """

    import keyboard

    keyboard.wait()

    
if __name__ == "__main__":

    import os
    import webbrowser as web
    import keyboard

    setupShortcuts(defaultShortcuts)
    keyboard.wait()

