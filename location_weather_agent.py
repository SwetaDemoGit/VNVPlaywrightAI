
import requests
from langchain.tools import tool
from langchain.agents import create_agent
from langchain_ollama import ChatOllama


# Tool 1: Find approximate location using public IP
@tool
def get_my_location() -> str:
    """Find the approximate location of this computer using its public IP."""

    try:
        response = requests.get(
            "https://ipapi.co/json/",
            timeout=10
        )
        response.raise_for_status()
        data = response.json()

        city = data.get("city")
        region = data.get("region")
        country = data.get("country_name")

        if not city:
            return "Location unavailable. Please enter your city manually."

        return (
            f"Approximate location: {city}, {region}, {country}. "
            "This location is based on public IP and may be inaccurate."
        )

    except requests.RequestException:
        return (
            "The location service is temporarily unavailable. "
            "Please enter your city manually."
        )


# Tool 2: Get current weather for a city
@tool
def get_weather(city: str) -> str:
    """Get current weather for a city in India or another country."""

    try:
        # Step 1: Find the city coordinates
        geo_response = requests.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={
                "name": city,
                "count": 10,
                "language": "en"
            },
            timeout=10
        )
        geo_response.raise_for_status()

        places = geo_response.json().get("results", [])

        if not places:
            return f"Could not find a location matching '{city}'."

        # Step 2: Prefer an exact city-name match
        city_lower = city.strip().lower()

        exact_matches = [
            place for place in places
            if place.get("name", "").lower() == city_lower
        ]

        candidates = exact_matches if exact_matches else places

        # If the user names India, prefer an Indian result.
        # Otherwise, use the first exact name match returned.
        india_matches = [
            place for place in candidates
            if place.get("country_code") == "IN"
        ]

        place = india_matches[0] if india_matches else candidates[0]

        latitude = place["latitude"]
        longitude = place["longitude"]

        # Step 3: Fetch current weather
        weather_response = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": latitude,
                "longitude": longitude,
                "current": (
                    "temperature_2m,"
                    "relative_humidity_2m,"
                    "apparent_temperature,"
                    "wind_speed_10m"
                ),
                "timezone": "auto"
            },
            timeout=10
        )
        weather_response.raise_for_status()

        weather_data = weather_response.json()
        current = weather_data.get("current")

        if not current:
            return "Current weather data is unavailable."

        return (
            f"Weather for {place['name']}, "
            f"{place.get('admin1', '')}, "
            f"{place.get('country', '')}. "
            f"Temperature: {current['temperature_2m']}°C. "
            f"Feels like: {current['apparent_temperature']}°C. "
            f"Humidity: {current['relative_humidity_2m']}%. "
            f"Wind speed: {current['wind_speed_10m']} km/h. "
            f"Observation time: {current.get('time', 'not provided')}."
        )

    except requests.RequestException:
        return (
            "The weather service is temporarily unavailable. "
            "Please try again later."
        )

    except (KeyError, ValueError, TypeError):
        return "The weather service returned unexpected data."


# Step 1: Connect to the local Ollama model
llm = ChatOllama(
    model="gemma4:12b",
    temperature=0
)


# Step 2: Create the agent and provide its tools
agent = create_agent(
    model=llm,
    tools=[get_my_location, get_weather],
    system_prompt=(
        "You are a location and weather assistant. "
        "For weather questions, use get_weather and report the "
        "returned temperature accurately. Never invent weather values. "
        "When the user asks where they are, use get_my_location. "
        "When asked for weather at the user's location, call "
        "get_my_location first, then call get_weather with the city "
        "returned by the location tool. "
        "Clearly explain that IP-based location is approximate. "
        "If a tool reports that its service failed, communicate that "
        "failure honestly instead of guessing."
    )
)


# Step 3: Keep asking questions until the user types exit
while True:
    question = input("\nYou: ").strip()

    if question.lower() == "exit":
        print("Goodbye!")
        break

    if not question:
        continue

    try:
        result = agent.invoke({
            "messages": [
                {"role": "user", "content": question}
            ]
        })

        print("\nAssistant:", result["messages"][-1].content)

    except Exception as error:
        print(f"\nAgent error: {error}")
