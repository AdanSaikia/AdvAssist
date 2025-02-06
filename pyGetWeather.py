from typing import List

import python_weather
import asyncio
import os

from AdvAssist.pyGetLocation import getMyLocation


def summarizeWeather(temperature, description, precipitation, wind_speed, humidity):
    """
    Summarize the weather conditions into a single descriptive word.

    Args:
        temperature (int): Current temperature in Fahrenheit.
        description (str): Weather description (e.g., haze, clear sky).
        precipitation (float): Precipitation in inches.
        wind_speed (float): Wind speed in mph.
        humidity (int): Humidity percentage.

    Returns:
        str: A single word summarizing the weather.
    """
    if precipitation > 0.1:
        return "Rainy"
    elif "snow" in description.lower():
        return "Snowy"
    elif "clear" in description.lower() and temperature > 80:
        return "Sunny"
    elif "haze" in description.lower() or "fog" in description.lower():
        return "Hazy"
    elif humidity > 80:
        return "Humid"
    elif wind_speed > 15:
        return "Windy"
    elif temperature < 32:
        return "Cold"
    elif temperature > 85:
        return "Hot"
    else:
        return "Mild"


async def getWeather(city: str) -> List[str|int]:
    """
    Fetch the current weather of the specified city and return a summary.

    Args:
        city (str): The name of the city for which to fetch the weather.

    Returns:
        str: A single word summarizing the weather.
    """
    async with python_weather.Client(unit=python_weather.IMPERIAL) as client:
        # Fetch the weather data for the city
        weather = await client.get(city)

        # Summarize the weather
        return [summarizeWeather(
            temperature=weather.temperature,
            description=weather.description,
            precipitation=weather.precipitation,
            wind_speed=weather.wind_speed,
            humidity=weather.humidity),

            weather.temperature,
            weather.description,
            weather.precipitation,
            weather.wind_speed,
            weather.humidity]


if __name__ == '__main__':
    # Workaround for Windows event loop policy
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    city = getMyLocation()[0]
    weather_summary = f"{asyncio.run(getWeather(city))[0]}, {asyncio.run(getWeather(city))[2]}"
    print(type(weather_summary))
    print(f"The weather in {city} can be described as: {weather_summary}")
