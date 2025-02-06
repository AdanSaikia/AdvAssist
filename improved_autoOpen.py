
def openApp(location: str) -> None:
    """
    Opens a file or URL using the default application.
    
    Args:
        location (str): The file path or web app name to open.
    """

    import os
    import webbrowser as web
    import requests

    domains = [
        ".com",
        ".org",
        ".in",
        ".co",
        ".net"
    ]
    
    if os.path.isfile(location):
        os.startfile(location)
    else:
        for domain in domains:
            print("Attempting to reach possible URLs: \n")
            try:
                url = f"https://{location}{domain}"
                requests.get(url)
                break

            except requests.exceptions.RequestException:
                print(f"Couldn't Reach: {url}")

                if domain == domains[-1]:
                    raise Exception(f"[IncorrectPathOrLocationError]: {location} may not exist")


        web.open(url=url)




if __name__ == "__main__":
    openApp(input("OPEN: "))
