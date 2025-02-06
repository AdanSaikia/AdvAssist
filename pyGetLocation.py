import phonenumbers
from phonenumbers import timezone, carrier, geocoder
import geocoder as gc
import requests
from bs4 import BeautifulSoup


def getMyLocation():
    """
    Returns:
        list[str]: A list containing the city and state of your approximate location.
    """
    # try:
    #     # Get the current location
    #     location = gc.ip('me')
    #     if location.ok:
    #         city = location.city
    #         state = location.state
    #         return [city, state]
    #     else:
    #         print("Unable to fetch location details.")
    # except Exception as e:
    #     print(f"An error occurred: {e}"

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
        }

        # Construct the search URL to get the location
        url = "https://www.google.com/search?q=my+location"

        # Send the GET request to fetch the page content
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")

        # Find the div and span with the specified classes
        address1 = soup.find("div", class_="aiAXrc")
        address2 = soup.find("span", class_="fMYBhe")

        # Check if both address1 and address2 exist, otherwise return a default message
        if address1 and address2:
            return [address1.text.strip(), address2.text.strip()]
        else:
            return ["Unable to fetch city", "Unable to fetch state"]

    except Exception as e:
        print(f"An error occurred: {e}")
        return ["Error occurred", "Error occurred"]


def getLocation(phoneNo: str) -> dict[str, str]:
    """

    Args:
        phoneNo: Phone number of the person whose approximate location details you want.

    Returns:
        dict[str, str]: A dictionary containing Geolocation, Timezone, and the Carrier Service.

    """
    try:
        phoneNumber = phonenumbers.parse(phoneNo)
        timeZone = timezone.time_zones_for_number(phoneNumber)
        geolocation = geocoder.description_for_number(phoneNumber, "en")
        service = carrier.name_for_number(phoneNumber, "en")

        return {
            'geolocation': geolocation,
            'timezone': ', '.join(timeZone),
            'carrier': service,
        }
    except phonenumbers.NumberParseException as e:
        return {"error": f"Invalid phone number: {e}"}


if __name__ == "__main__":
    phone_number = '+918453148616'
    print("Phone Location:", getLocation(phone_number))
    print("My Location:", getMyLocation())
