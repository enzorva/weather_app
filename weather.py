import sys
import time
import redis
import urllib.request
import urllib.error
import urllib.parse
import json
import os
import argparse
from dotenv import load_dotenv
import socket

cache = redis.Redis(host='localhost', port=6379, db=0)

load_dotenv()

api_key = os.getenv("VISUAL_CROSSING_API_KEY")

if not api_key:
    print("API key not found. Please set the VISUAL_CROSSING_API_KEY environment variable.")
    sys.exit(1)


def is_rate_limited(user_id, limit=5, period=60):
    key = f"rate_limit:{user_id}"
    now = int(time.time())

    cache.zremrangebyscore(key, 0, now - period)

    request_count = cache.zcard(key)

    if request_count >= limit:
        return True
    
    cache.zadd(key, {now: now})
    cache.expire(key, period)
    return False


def fetch_data(url):
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            data = response.read()
            return data
    except urllib.error.HTTPError as e:
        print(f"HTTP error: {e.code} - {e.reason}")
    except urllib.error.URLError as e:
        print(f"URL error: {e.reason}")
    except socket.timeout:
        print("Request time out. Please check your network connection and try again.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    
    return None


def fetch_data_with_cache(location):
    cache_key = f"weather:{location}"
    cached_data = cache.get(cache_key)

    if cached_data:
        print("✅ Using cached data.")
        return cached_data.decode('utf-8')

    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}?unitGroup=metric&key={api_key}&contentType=json"
    data = fetch_data(url)


    if data:
        cache.setex(cache_key, 3600, data)
        print("🌐 Fetched from API and cached.")
    return data


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

user_id = "default_user"

if is_rate_limited(user_id):
    print("⚠️ Rate limit exceeded. Please wait before making more requests.")
    sys.exit(1)

data = fetch_data_with_cache(location)

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