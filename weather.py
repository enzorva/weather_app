import sys
import urllib.request
import urllib.error

def fetch_data(url):
    try:
        with urllib.request.urlopen(url) as response:
            data = response.read()
            return data
    except urllib.error.HTTPError as e:
        print(f"HTTP error: {e.code} - {e.reason}")


url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/Orlando?unitGroup=us&key=YOUR_API_KEY&contentType=json"