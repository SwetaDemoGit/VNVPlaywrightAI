"""
LangChain Agent Demo for Freshers (OpenAI version)
--------------------------------------------------
Ask: "Where am I and what's the temperature?"  or  "Temperature in Bangalore?"

Tools:
  1. get_my_location            -> approximate location from your IP (ip-api.com, fallback ipapi.co)
  2. get_temperature            -> temperature for latitude/longitude (wttr.in)
  3. get_temperature_by_city    -> temperature for a city name (wttr.in)

No API key is needed for location/weather. Only OPENAI_API_KEY is needed.

Setup:
    pip install langchain langchain-openai requests
    export OPENAI_API_KEY="your-key-here"      # Windows: set OPENAI_API_KEY=your-key-here

Run:
    python location_weather_agent.py
"""

import requests
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_openai import ChatOpenAI

HEADERS = {"User-Agent": "Mozilla/5.0 (langchain-demo)"}


# ---------------------------------------------------------------
# STEP 1: Tools
# The docstring is IMPORTANT: the LLM reads it to know when to use the tool.
# Tools return an "ERROR: ..." text on failure so the agent can say so honestly.
# ---------------------------------------------------------------
@tool
def get_my_location() -> str:
    """Find the user's current approximate location (city, region, country,
    latitude, longitude) from their IP address. Use this when the user asks
    where they are."""
    # Try API 1: ip-api.com
    try:
        d = requests.get("http://ip-api.com/json", timeout=10, headers=HEADERS).json()
        if d.get("status") == "success":
            return (
                f"City: {d['city']}, Region: {d['regionName']}, Country: {d['country']}, "
                f"Latitude: {d['lat']}, Longitude: {d['lon']}"
            )
    except Exception:
        pass

    # Try API 2 (backup): ipapi.co
    try:
        d = requests.get("https://ipapi.co/json/", timeout=10, headers=HEADERS).json()
        if d.get("latitude"):
            return (
                f"City: {d['city']}, Region: {d['region']}, Country: {d['country_name']}, "
                f"Latitude: {d['latitude']}, Longitude: {d['longitude']}"
            )
    except Exception:
        pass

    return "ERROR: Could not detect location. Ask the user to tell their city."


def _wttr(query: str) -> str:
    """Helper: call wttr.in and format the current weather."""
    r = requests.get(f"https://wttr.in/{query}", params={"format": "j1"}, timeout=15, headers=HEADERS)
    r.raise_for_status()
    data = r.json()
    now = data["current_condition"][0]
    place = data["nearest_area"][0]["areaName"][0]["value"]
    return (
        f"Weather near {place}: {now['temp_C']} °C "
        f"(feels like {now['FeelsLikeC']} °C), {now['weatherDesc'][0]['value']}, "
        f"humidity {now['humidity']}%"
    )


@tool
def get_temperature(latitude: float, longitude: float) -> str:
    """Get the current temperature (Celsius) for a latitude and longitude.
    Use get_my_location first if the coordinates are unknown."""
    try:
        return _wttr(f"{latitude},{longitude}")
    except Exception as e:
        return f"ERROR: weather service failed ({e})"


@tool
def get_temperature_by_city(city: str) -> str:
    """Get the current temperature (Celsius) for a city name, e.g. 'Bangalore'."""
    try:
        return _wttr(city)
    except Exception as e:
        return f"ERROR: weather service failed ({e})"


# ---------------------------------------------------------------
# STEP 2: LLM (the brain)
# ---------------------------------------------------------------
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


# ---------------------------------------------------------------
# STEP 3: Agent = LLM + tools + instructions
# ---------------------------------------------------------------
agent = create_agent(
    model=llm,
    tools=[get_my_location, get_temperature, get_temperature_by_city],
    system_prompt=(
        "You are a helpful assistant. ALWAYS use the tools for location and "
        "temperature; never guess or use your own knowledge. If the user asks "
        "where they are, call get_my_location. If they ask for the temperature "
        "of their place, call get_my_location then get_temperature. If they "
        "name a city, call get_temperature_by_city. If a tool returns an ERROR, "
        "tell the user honestly. Answer in one friendly sentence."
    ),
)


# ---------------------------------------------------------------
# STEP 4: Run (type questions; press Enter on empty line to quit)
# ---------------------------------------------------------------
if __name__ == "__main__":
    while True:
        question = input("\nAsk something (Enter to quit): ").strip()
        if not question:
            break
        for step in agent.stream(
            {"messages": [{"role": "user", "content": question}]},
            stream_mode="values",
        ):
            step["messages"][-1].pretty_print()
