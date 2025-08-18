# Import necessary Django modules and Python libraries
from django.shortcuts import render  # For rendering HTML templates with context data
from django.http import HttpResponse
import requests  # For making HTTP requests to external APIs
import json  # For handling JSON data (imported but not actively used)
import os

def test_view(request):
    """Simple test view to check if Django is working"""
    html = """
    <!DOCTYPE html>
    <html>
    <head><title>🚨 TEST VIEW WORKING! 🚨</title></head>
    <body style="background: #00ff00; color: black; font-size: 32px; text-align: center; padding: 50px;">
        <h1>🎉 DJANGO IS WORKING! 🎉</h1>
        <div style="background: red; color: white; padding: 30px; margin: 30px; border: 10px solid black;">
            <h2>IF YOU SEE THIS, DJANGO IS WORKING!</h2>
            <p>This is a direct HttpResponse, not a template!</p>
        </div>
        <div style="font-size: 80px; margin: 50px;">🎉</div>
    </body>
    </html>
    """
    return HttpResponse(html)

def home_view(request):
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
    weather_data = {}
    
    try:
        # Attempt to fetch live weather data from wttr.in API
        # wttr.in is a free weather service that doesn't require API key registration
        # format=j1 parameter requests JSON format response
        url = f"https://wttr.in/{city}?format=j1"
        
        # Make HTTP GET request with 10 second timeout to prevent hanging
        response = requests.get(url, timeout=10)
        
        # Check if API request was successful (status code 200 = OK)
        if response.status_code == 200:
            try:
                # Parse JSON response from weather API
                data = response.json()
                
                # Check if the expected data structure exists
                if ('current_condition' in data and len(data['current_condition']) > 0 and
                    'nearest_area' in data and len(data['nearest_area']) > 0):
                    
                    # Extract current weather conditions from API response
                    current = data['current_condition'][0]  # First (current) weather condition
                    area_info = data['nearest_area'][0]     # Location information
                    
                    # Transform API data into format expected by our HTML template
                    # This standardizes the data structure regardless of API changes
                    weather_data = {
                        # Format location as "City, Country" from API response
                        "name": f"{area_info.get('areaName', [{}])[0].get('value', 'Unknown')}, {area_info.get('country', [{}])[0].get('value', 'Unknown')}",
                        
                        # Main weather measurements
                        "main": {
                            "temp": float(current.get('temp_C', 25)),           # Current temperature in Celsius
                            "feels_like": float(current.get('FeelsLikeC', 25)), # "Feels like" temperature
                            "humidity": int(current.get('humidity', 50))         # Humidity percentage
                        },
                        
                        # Weather condition description
                        "weather": [
                            {
                                "main": current.get('weatherDesc', [{}])[0].get('value', 'Clear'),
                                "description": current.get('weatherDesc', [{}])[0].get('value', 'clear').lower(),
                                "icon": "01d"  # Simple icon placeholder (could be enhanced with weather icons)
                            }
                        ],
                        
                        # Wind information
                        "wind": {
                            # Convert wind speed from km/h to m/s (multiply by 0.278)
                            "speed": float(current.get('windspeedKmph', 10)) * 0.278
                        }
                    }
                else:
                    # Invalid data structure from API
                    raise Exception("Invalid data structure from weather API")
                    
            except (KeyError, IndexError, ValueError) as e:
                # JSON parsing or data structure issues
                raise Exception(f"Invalid data format from weather API: {str(e)}")
        else:
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

    # For debugging, let's print the weather data
    print(f"Debug: Weather data = {weather_data}")

    # Render the home.html template with weather data
    # The weather data will be available in the template as {{ weather }}
    return render(request, 'home/home.html', {
        "weather": weather_data,  # Pass weather data to template
    })

def about_view(request):
    """
    About page view function that displays information about Rosan.
    
    Args:
        request: HTTP request object
        
    Returns:
        Rendered HTML template for the about page
    """
    return render(request, 'home/about.html')

def features_view(request):
    """
    Features page view function that displays detailed NISHA features.
    
    Args:
        request: HTTP request object
        
    Returns:
        Rendered HTML template for the features page
    """
    return render(request, 'home/features.html')