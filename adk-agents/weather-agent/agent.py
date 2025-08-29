import requests
from google.adk.agents import Agent
import os
from dotenv import load_dotenv


load_dotenv()


def get_current_weather(city: str) -> dict:
   """
   Fetches the current weather data for a given city by first getting its
   coordinates using the Google Maps Geocoding API and then querying the
   Google Maps Platform Weather API.


   Args:
       city (str): The name of the city for which to retrieve weather information.


   Returns:
       dict: A dictionary containing weather information, or an error message.
   """
   google_api_key = os.getenv("MAPS_API_KEY")


   if not google_api_key:
       return {"error": "API key for Google Maps Platform is not set."}


   try:
       # Step 1: Use Geocoding API to get coordinates from the city name
       geocoding_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={city}&key={google_api_key}"
       geocoding_response = requests.get(geocoding_url)
       geocoding_response.raise_for_status()
       geocoding_data = geocoding_response.json()


       if geocoding_data['status'] != 'OK' or not geocoding_data['results']:
           return {"error": f"Could not find coordinates for '{city}'."}


       location_data = geocoding_data['results'][0]['geometry']['location']
       lat = location_data['lat']
       lon = location_data['lng']


       # Step 2: Use the Weather API with a GET request and coordinates
       weather_url = "https://weather.googleapis.com/v1/currentConditions:lookup"
      
       params = {
           "key": google_api_key,
           "location.latitude": lat,
           "location.longitude": lon,
           "unitsSystem": "METRIC"
       }


       weather_response = requests.get(weather_url, params=params)
       weather_response.raise_for_status()
       weather_data = weather_response.json()
       print(weather_data)


       return {
           "location_name": city,
           "temperature": weather_data['temperature']['degrees'],
           "feels_like": weather_data['feelsLikeTemperature']['degrees'],
           "humidity": weather_data['relativeHumidity'],
           "weather_description": weather_data['weatherCondition']['description']['text']
       }
  
   except requests.exceptions.RequestException as e:
       print(f"An error occurred while making the API request: {e}")
       return {"error": f"API request failed: {e}"}
   except Exception as e:
       print(f"An unexpected error occurred: {e}")
       return {"error": f"An unexpected error occurred: {e}"}


# Agent definition remains the same
root_agent = Agent(
   model="gemini-2.5-flash",
   name="weather_agent",
   description="A weather information agent that provides current weather data for a specified city.",
   instruction="""
   You are a specialized weather agent who can answer questions about the current weather in a given city.
   You can use the get_current_weather tool to get the most up to date information.
   The get_current_weather tool takes a city name as input and returns a dictionary with the weather details.
   """,
   tools=[get_current_weather],
)
