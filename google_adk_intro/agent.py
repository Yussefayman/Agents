import os
from dotenv import load_dotenv
import datetime
from zoneinfo import ZoneInfo
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

load_dotenv()

MODEL_NAME = os.getenv("MODEL_NAME")
API_BASE = os.getenv("API_BASE")
STREAM = os.getenv("STREAM", "False").lower() == "true"

def get_weather(city: str) -> dict:
    if city.lower() == "new york":
        return {
            "status": "success",
            "report": "The weather in New York is sunny with 25°C (77°F)."
        }
    else:
        return {
            "status": "error",
            "error_message": f"Weather information for '{city}' is not available."
        }

def get_current_time(city: str) -> dict:
    if city.lower() == "new york":
        tz = ZoneInfo("America/New_York")
        now = datetime.datetime.now(tz)
        return {
            "status": "success",
            "report": f"Current time in New York: {now.strftime('%Y-%m-%d %H:%M:%S %Z%z')}"
        }
    else:
        return {
            "status": "error",
            "error_message": f"Timezone information for '{city}' is unavailable."
        }

root_agent = Agent(
    name="weather_time_agent",
    model=LiteLlm(
        model=MODEL_NAME,
        api_base=API_BASE,
        stream=STREAM
    ),
    description="Agent to answer questions about the time and weather in a city.",
    instruction=(
        "Rules:\n"
        "1. For greetings (hello, hi, hey, etc.): Respond ONLY with plain text.\n"
        "2. For weather questions about a city: Call get_weather(city_name)\n"
        "3. For time questions about a city: Call get_current_time(city_name)\n"
        "4. For anything else: Respond in plain text\n"
        "5. If the user asks about weather or time without a city: Ask them for a city\n"
        "Do NOT call functions not in the tools list."
    ),
    tools=[get_weather, get_current_time],
)
