import requests
from azure.cosmos import CosmosClient, PartitionKey
from datetime import datetime
import json
import schedule
import time

# Configuration
COSMOS_ENDPOINT = "https://siminali.documents.azure.com:44"  # Replace with Azure Cosmos DB URI
COSMOS_KEY = "LA4AlrWbFszgX5NB0sk65lmAtjv24MHAkHhCAYMvw0CVHfApnUHG3lieW2qdaJaGjVmp6qccmutmACDb31JG8Q"           # Replace with Azure Cosmos DB Primary Key
DATABASE_NAME = "smart_city"
CONTAINER_NAME = "traffic_air_quality"

GOOGLE_MAPS_API_KEY = "AIzaSyBQasFff0qSckTI-aTuIvv5VtM6bl0hH"  # Replace with your Google Maps API Key
OPENWEATHER_API_KEY = "85b5b63a80899b62af2fd6f1e20537"  # Replace with your OpenWeatherMap API Key

# Initialize Cosmos DB
client = CosmosClient(COSMOS_ENDPOINT, COSMOS_KEY)
database = client.create_database_if_not_exists(id=DATABASE_NAME)
container = database.create_container_if_not_exists(
    id=CONTAINER_NAME,
    partition_key=PartitionKey(path="/timestamp"),
    offer_throughput=400
)

# Define routes
routes = [
    {"name": "Route 1", "origin": "51.5074,-0.1278", "destination": "51.5165,-0.2253", "coordinates": (51.5074, -0.1278)},  # Trafalgar Square to Imperial White City
    {"name": "Route 2", "origin": "51.556021,-0.279519", "destination": "51.4713,-0.4522", "coordinates": (51.556021, -0.279519)},  # Wembley to Heathrow
    {"name": "Route 3", "origin": "51.4769,-0.0005", "destination": "51.5054,-0.0235", "coordinates": (51.4769, -0.0005)}   # Greenwich to Canary Wharf
]

# Fetch traffic data from Google Maps API
def fetch_traffic_data(origin, destination):
    url = f"https://maps.googleapis.com/maps/api/directions/json"
    params = {
        "origin": origin,
        "destination": destination,
        "departure_time": "now",
        "key": GOOGLE_MAPS_API_KEY
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data.get("routes"):
            route = data['routes'][0]['summary']
            duration_in_traffic = data['routes'][0]['legs'][0]['duration_in_traffic']['value']
            return {
                "route": route,
                "duration_in_traffic": duration_in_traffic
            }
    print("Error fetching traffic data:", response.status_code, response.text)
    return None

# Fetch weather data from OpenWeatherMap API
def fetch_weather_data(lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": lat,
        "lon": lon,
        "appid": OPENWEATHER_API_KEY
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        weather_conditions = data['weather'][0]['main']
        temperature = data['main']['temp']
        rain = data.get('rain', {}).get('1h', 0)
        snow = data.get('snow', {}).get('1h', 0)
        return {
            "temperature": temperature,
            "weather_conditions": weather_conditions,
            "rain": rain,
            "snow": snow
        }
    print("Error fetching weather data:", response.status_code, response.text)
    return None

# Fetch air quality data from OpenWeatherMap API
def fetch_air_quality_data(lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/air_pollution"
    params = {
        "lat": lat,
        "lon": lon,
        "appid": OPENWEATHER_API_KEY
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        components = data['list'][0]['components']
        air_quality_index = data['list'][0]['main']['aqi']
        return {
            "air_quality_index": air_quality_index,
            "components": components  # Includes PM2.5, PM10, CO, etc.
        }
    print("Error fetching air quality data:", response.status_code, response.text)
    return None

# Store data in Cosmos DB
def store_data(data):
    try:
        json.dumps(data)  # Ensure JSON-serializable
        print("\nStoring data in Cosmos DB:", data)
        container.upsert_item(data)
        print("Data stored successfully:", data["timestamp"])
    except Exception as e:
        print("Error storing data:", str(e))

# Main function to collect and store data for all routes
def collect_and_store_data():
    for route in routes:
        origin = route["origin"]
        destination = route["destination"]
        lat, lon = route["coordinates"]

        # Fetch traffic, weather, and air quality data
        traffic_data = fetch_traffic_data(origin, destination)
        weather_data = fetch_weather_data(lat, lon)
        air_quality_data = fetch_air_quality_data(lat, lon)

        # Combine data and store
        if traffic_data and weather_data and air_quality_data:
            combined_data = {
                "id": f"data-{datetime.now().isoformat()}-{route['name']}",  # Unique ID
                "route_name": route["name"],
                "timestamp": datetime.now().isoformat(),  # Partition key
                "traffic_data": traffic_data,
                "weather_data": weather_data,
                "air_quality_data": air_quality_data
            }
            store_data(combined_data)
        else:
            print(f"Error: Unable to fetch data for {route['name']}.")

# Schedule API calls
def schedule_api_calls():
    print("Starting local testing: API calls every minute...")
    schedule.every(30).minutes.do(collect_and_store_data)  # Schedule the function

    while True:
        schedule.run_pending()
        time.sleep(1)

# Run the script
if __name__ == "__main__":
    # Uncomment to collect data once
    # collect_and_store_data()

    # Uncomment to schedule API calls every 30 minutes
    schedule_api_calls()
