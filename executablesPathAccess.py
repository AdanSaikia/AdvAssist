import os
import platform
import subprocess
import json


def get_all_user_runnable_apps():
    """Platform-independent function to list user-runnable applications."""
    detected_apps = {}
    current_platform = platform.system()
    print(f"Detected OS: {current_platform}")

    if current_platform == "Windows":
        detected_apps = get_windows_user_apps()
    elif current_platform == "Darwin":
        detected_apps = get_macos_user_apps()
    elif current_platform == "Linux":
        detected_apps = get_linux_user_apps()
    else:
        print("Unsupported operating system.")

    return detected_apps


# Windows-specific logic
# Windows-specific logic
def get_windows_user_apps():
    """Fetch user-facing applications on Windows."""
    import winreg

    apps = {}

    # Search Start Menu shortcuts
    start_menu_dirs = [
        r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs",
        os.path.join(os.environ["APPDATA"], r"Microsoft\Windows\Start Menu\Programs")
    ]
    for directory in start_menu_dirs:
        if os.path.exists(directory):
            for root, _, files in os.walk(directory):
                for file in files:
                    if file.endswith(".lnk") or file.endswith(".exe"):
                        app_name = os.path.splitext(file)[0]
                        apps[app_name] = os.path.join(root, file)

    # Search Uninstall registry keys
    reg_paths = [
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
        r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
    ]
    for reg_path in reg_paths:
        try:
            reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path)
            for i in range(winreg.QueryInfoKey(reg_key)[0]):
                sub_key_name = winreg.EnumKey(reg_key, i)
                sub_key = winreg.OpenKey(reg_key, sub_key_name)
                try:
                    app_name = winreg.QueryValueEx(sub_key, "DisplayName")[0]
                    # Query for InstallLocation
                    try:
                        install_location = winreg.QueryValueEx(sub_key, "InstallLocation")[0]
                        if app_name and install_location:
                            apps[app_name] = install_location
                    except FileNotFoundError:
                        pass  # No InstallLocation, skip to next app
                except FileNotFoundError:
                    pass  # DisplayName not found, skip to next app
                finally:
                    winreg.CloseKey(sub_key)
        except FileNotFoundError:
            continue
        finally:
            winreg.CloseKey(reg_key)

    # Scan common directories for executables
    common_dirs = [
        r"C:\Program Files",
        r"C:\Program Files (x86)",
        os.path.expanduser(r"~\AppData\Local"),
        os.path.expanduser(r"~\AppData\Roaming")
    ]
    for directory in common_dirs:
        if os.path.exists(directory):
            for root, _, files in os.walk(directory):
                for file in files:
                    if file.endswith(".exe"):
                        app_name = os.path.splitext(file)[0]
                        apps[app_name] = os.path.join(root, file)

    return apps


# macOS-specific logic
def get_macos_user_apps():
    """Fetch user-facing applications on macOS."""
    apps = {}

    # Look in the Applications folder
    app_dirs = [
        "/Applications",
        os.path.expanduser("~/Applications")
    ]
    for directory in app_dirs:
        if os.path.exists(directory):
            for app in os.listdir(directory):
                if app.endswith(".app"):
                    app_name = os.path.splitext(app)[0]
                    apps[app_name] = os.path.join(directory, app)

    return apps


# Linux-specific logic
def get_linux_user_apps():
    """Fetch user-facing applications on Linux."""
    apps = {}

    # Look in standard application directories
    app_dirs = [
        "/usr/share/applications",
        "/usr/local/share/applications",
        os.path.expanduser("~/.local/share/applications")
    ]
    for directory in app_dirs:
        if os.path.exists(directory):
            for app in os.listdir(directory):
                if app.endswith(".desktop"):
                    app_name = os.path.splitext(app)[0]
                    apps[app_name] = os.path.join(directory, app)

    # Add executables in PATH
    for path in os.environ.get("PATH", "").split(os.pathsep):
        if os.path.exists(path):
            for file in os.listdir(path):
                file_path = os.path.join(path, file)
                if os.access(file_path, os.X_OK) and not os.path.isdir(file_path):
                    apps[file] = file_path

    return apps


def save_apps_to_json(apps):
    """Save the found apps and their paths to a JSON file."""
    with open("user_apps.json", "w") as json_file:
        json.dump(apps, json_file, indent=4)


if __name__ == "__main__":
    apps = get_all_user_runnable_apps()
    if apps:
        print("User-Facing Applications:")
        for app, path in apps.items():
            print(f"{app}: {path}")

        # Save the apps to a JSON file
        save_apps_to_json(apps)
    else:
        print("No user-facing applications found.")
