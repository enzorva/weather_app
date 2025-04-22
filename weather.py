import sys
import urllib.request
import urllib.error
import json

def fetch_data(url):
    try:
        with urllib.request.urlopen(url) as response:
            data = response.read()
            return data
    except urllib.error.HTTPError as e:
        print(f"HTTP error: {e.code} - {e.reason}")


url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/Orlando?unitGroup=metric&key=T56DMW9G2B89X7D7Y4XLU3EXT&contentType=json"
data = fetch_data(url)
print(data)