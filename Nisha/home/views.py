# Import necessary Django modules and Python libraries
from django.shortcuts import render  # For rendering HTML templates with context data
import requests  # For making HTTP requests to external APIs
import json  # For handling JSON data (imported but not actively used)
    """
    Home page view function that displays the main landing page with weather information.
    
    Args:
        request: HTTP request object containing user data and parameters
        
    Returns:
        Rendered HTML template with weather context data
    """
    
    # Get city parameter from URL query string, default to Osaka, Japan if not provided
    # This allows users to check weather for different cities by adding ?city=CityName to URL
    city = request.GET.get("city", "Osaka,Japan")  # Default to Osaka, Japan for user location
    
    # Initialize weather_data variable to store weather information
    
    try:
        # Attempt to fetch live weather data from wttr.in API
        # wttr.in is a free weather service that doesn't require API key registration
        # format=j1 parameter requests JSON format response
        url = f"https://wttr.in/{city}?format=j1"
        
        # Make HTTP GET request with 10 second timeout to prevent hanging
        response = requests.get(url, timeout=10)
        
        # Check if API request was successful (status code 200 = OK)
        if response.status_code == 200:
            # Parse JSON response from weather API
            data = response.json()
            
            # Extract current weather conditions from API response
            current = data['current_condition'][0]  # First (current) weather condition
            area_info = data['nearest_area'][0]     # Location information
            
            # Transform API data into format expected by our HTML template
            # This standardizes the data structure regardless of API changes
            weather_data = {
                # Format location as "City, Country" from API response
                "name": f"{area_info['areaName'][0]['value']}, {area_info['country'][0]['value']}",
                
                # Main weather measurements
                "main": {
                    "temp": float(current['temp_C']),           # Current temperature in Celsius
                    "feels_like": float(current['FeelsLikeC']), # "Feels like" temperature
                    "humidity": int(current['humidity'])         # Humidity percentage
                },
                
                # Weather condition description
                "weather": [
                    {
                        "main": current['weatherDesc'][0]['value'],        # Weather condition (e.g., "Clear")
                        "description": current['weatherDesc'][0]['value'].lower(),  # Lowercase description
                        "icon": "01d"  # Simple icon placeholder (could be enhanced with weather icons)
                    }
                ],
                
                # Wind information
                "wind": {
                    # Convert wind speed from km/h to m/s (multiply by 0.278)
                    "speed": float(current['windspeedKmph']) * 0.278
                }
            }
            # If API returns non-200 status code, raise exception to trigger fallback
            raise Exception(f"API returned status code: {response.status_code}")
            
    except Exception as e:
        # Fallback weather data if API fails (network issues, API down, etc.)
        # This ensures the page always displays something, even without internet
        weather_data = {
            "name": "Osaka, Japan",  # Default location
            
            # Realistic demo weather data for Osaka
            "main": {
                "temp": 28.5,      # Typical summer temperature in Osaka
                "feels_like": 32.1, # Higher due to humidity
                "humidity": 78      # High humidity typical of Osaka climate
            },
            
            # Typical weather condition for Osaka
            "weather": [
                {
                    "main": "Partly Cloudy",
                    "description": "partly cloudy",
                    "icon": "02d"  # Partly cloudy icon code
                }
            ],
            
            # Typical wind conditions
            "wind": {
                "speed": 2.8  # Light breeze in m/s
            },
            
            # Note explaining why demo data is being used
            "note": f"Using demo data for Osaka - Live weather unavailable: {str(e)}"
        }

    # Render the home.html template with weather data
    # The weather data will be available in the template as {{ weather }}
        "weather": weather_data,  # Pass weather data to template