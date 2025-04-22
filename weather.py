import sys
import urllib.request
import urllib.error
import urllib.parse
import json
import os
import argparse
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("VISUAL_CROSSING_API_KEY")

if not api_key:
    print("API key not found. Please set the VISUAL_CROSSING_API_KEY environment variable.")
    sys.exit(1)

def fetch_data(url):
    try:
        with urllib.request.urlopen(url) as response:
            data = response.read()
            return data
    except urllib.error.HTTPError as e:
        print(f"HTTP error: {e.code} - {e.reason}")


parser = argparse.ArgumentParser(description="Fetch weather information for a specific city.")
parser.add_argument("--city", type=str, help="Name of the city to fetch weather information for.")
parser.add_argument("--city_code", type=str, help="Code of the city to fetch weather information for.")
args = parser.parse_args()


if args.city:
    if ',' not in args.city:
        print("⚠️ Warning: You did not specify a country with the city name.")
        print("➡️  Example: 'Springfield,MO' or 'Orlando,US'")
        print("Proceeding anyway...\n")
    location = urllib.parse.quote(args.city)
elif args.city_code:
    location = args.city_code 
else:
    print("Please provide either a city name or a city code.")
    sys.exit(1)

url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}?unitGroup=metric&key={api_key}&contentType=json"
data = fetch_data(url)

try:
    json_data = json.loads(data)
    address = json_data.get("address", "Address not found")
    current_conditions = json_data.get("currentConditions", {})
    temperature = current_conditions.get("temp", "N/A")
    conditions = current_conditions.get("conditions", "N/A")

    print(f"Weather information for {address}:")
    print(f"Temperature: {temperature}°C")
    print(f"Conditions: {conditions}")
except json.JSONDecodeError as e:
    print(f"JSON decode error: {e.msg} - {e.doc} - {e.pos}")
    sys.exit(1)