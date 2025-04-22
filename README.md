# Weather App

This is a simple command-line application that fetches weather information for a specified city or city code using the Visual Crossing Weather API.

## Features
- Fetch weather data by city name or city code.
- Display current temperature and weather conditions.

## Requirements
- Python 3.6 or higher
- An API key from [Visual Crossing Weather](https://www.visualcrossing.com/)

## Setup

1. Clone this repository:
   ```bash
   git clone https://roadmap.sh/projects/weather-api-wrapper-service
   ```

2. Navigate to the project directory:
   ```bash
   cd weather_app
   ```

3. Create a `.env` file in the project directory and add your API key:
   ```
   VISUAL_CROSSING_API_KEY=your_api_key_here
   ```

4. Install required dependencies (if any):
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the script with the following options:

- Fetch weather by city name:
  ```bash
  python weather.py --city "City Name"
  ```

- Fetch weather by city code:
  ```bash
  python weather.py --city_code "City Code"
  ```

## Example

To fetch weather information for Orlando:
```bash
python weather.py --city "Orlando"
```

To fetch weather information using a city code:
```bash
python weather.py --city_code "12345"
```

## Notes
- Ensure your `.env` file is not tracked by Git. This is already handled by the `.gitignore` file.

## Project Inspiration
This project was inspired by the idea shared on [Roadmap.sh](https://roadmap.sh/projects/weather-api-wrapper-service).

## License
This project is licensed under the MIT License.