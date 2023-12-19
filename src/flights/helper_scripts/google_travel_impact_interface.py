# google_travel_impact_interface.py
# interfaces with the Google Travel Impact Model Web API

import json
import requests

API_KEY: str = "AIzaSyAJjWa2zfoUMeEkcJ2bzEuK6A3-pPrVfLw"

json_demo_query: dict = {
    "flights": [
      {
        "origin": "ZRH",
        "destination": "CDG",
        "operatingCarrierCode": "AF",
        "flightNumber": 1115,
        "departureDate": {"year": 2024, "month": 6, "day": 1}
      },
      {
        "origin": "CDG",
        "destination": "BOS",
        "operatingCarrierCode": "AF",
        "flightNumber": 334,
        "departureDate": {"year": 2024, "month": 6, "day": 1}
      },
      {
        "origin": "ZRH",
        "destination": "BOS",
        "operatingCarrierCode": "LX",
        "flightNumber": 52,
        "departureDate": {"year": 2024, "month": 5, "day": 1}
      }
    ]
  }

url = "https://travelimpactmodel.googleapis.com/v1/flights:computeFlightEmissions"
header: dict = {"Content-Type": "application/json"}
params = {"key": API_KEY}

response = requests.request("POST", url, json=json_demo_query, headers=header, params=params)
print(response)

