def fetch(songName: str):
    import requests
    from bs4 import BeautifulSoup

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }

    query = songName.replace(" ", "+")
    url = f"https://www.google.com/search?q={query}+lyrics"

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    results = soup.select('div.sATSHe')  # Update if structure changes
    finalList = []

    for result in results:
        stanzas = result.find_all('div', {'jsname': 'U8S5sf'})  # Each stanza div

        for stanza in stanzas:
            lines = stanza.find_all('span', {'jsname': 'YS01Ge'})  # Lines in the stanza

            stanza_lines = []
            for line in lines:
                text = line.text.strip()
                if text:
                    stanza_lines.append(text)

            if stanza_lines:
                finalList.append("\n".join(stanza_lines))  # Join lines in the stanza
                finalList.append("")  # Add a blank line after each stanza

    return "\n".join(finalList).strip() if finalList else "No lyrics found."

if __name__ == "__main__":
    song = input("Enter the name of the song to fetch the lyrics: ")
    lyrics = fetch(song)
    print(lyrics)
