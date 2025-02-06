from typing import Optional, List

def getNews(topic: Optional[str] = None, headlines: Optional[int] = 5) -> List[str]:
    import requests
    from bs4 import BeautifulSoup

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }

    # Construct the search URL based on the topic
    if topic:
        url = f"https://www.google.com/search?q=news+headlines+today+on+{topic}&tbm=nws"
    else:
        url = "https://www.google.com/search?q=news+headlines+today&tbm=nws"

    # Send the GET request to fetch the page content
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")

    # Find all divs with the specified class
    search_results = soup.find_all("div", class_="n0jPhd ynAwRc MBeuO nDgy9d")

    # Extract and clean text from these divs
    results = [result.text.strip().replace("\'", "'") for result in search_results]

    # Limit the number of headlines if specified
    if headlines:
        results = results[:headlines]

    return results


if __name__ == "__main__":
    print(getNews())