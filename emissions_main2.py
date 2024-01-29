import datetime
import src.common.coefficients2 as c
import googlemaps
from datetime import datetime

transport_emission_coefficient_dict: dict = {
        'Petrol Car': c.CarPetrol.CO2_PER_km.value,
        'Diesel Car': c.CarDiesel.CO2_PER_km.value,
        'Ferry': c.Ferry.AVERAGE_CAR,
        'Flight Economy': c.AirTravelEmissionsPerPassengerKm.ECONOMY_AVERAGE.value,
        'Flight Premium Economy': c.AirTravelEmissionsPerPassengerKm.PREMIUM_ECONOMY_AVERAGE.value,
        'Flight Business': c.AirTravelEmissionsPerPassengerKm.BUSINESS_AVERAGE.value,
        'Flight First': c.AirTravelEmissionsPerPassengerKm.FIRST_AVERAGE.value,
        'Domestic Train': c.Rail.UK_DOMESTIC.value,
        'International Train': c.Rail.INTERNATIONAL.value
}

from geopy.geocoders import Nominatim
from geopy.distance import geodesic

def get_location_coordinates(location):
    geolocator = Nominatim(user_agent="my_geocoding_app", timeout=10)
    try:
        location = geolocator.geocode(location)
        if location:
            return (location.latitude, location.longitude)
        else:
            print(f"Could not find location: {location}")
            return None
    except Exception as e:
        print(f"Error occurred: {e}")
        return None

def calculate_distance(loc1, loc2):
    loc1_coords = get_location_coordinates(loc1)
    loc2_coords = get_location_coordinates(loc2)

    if loc1_coords and loc2_coords:
        distance = geodesic(loc1_coords, loc2_coords).kilometers
        return distance
    else:
        return None

def create_driving_leg(mode: str = "") -> tuple:
    query: dict = {
        "origin": "",
        "destination": "",
        "mode": mode,
        "departure_time": datetime.now()
    }

    prompts = ["Please enter the origin address or waypoint ",
               "Please enter the destination address or waypoint "]
    for (prompt, entry) in zip(prompts,
                               ["origin",
                                "destination"]):
        query[entry] = input(prompt)

    start_now = input("Do you want to start now? (yes/no) ")
    if start_now == "yes":
        query["departure_time"] = datetime.now()
    else:
        year = input("Please enter the year of your journey ")
        month = input("Please enter the month of your journey as a number (1-12) ")
        day = input("Please enter the day of your journey ")
        hour = input("Please enter the hour when you like to depart (24h-format) ")
        minute = input("Please enter the minute when you like to depart ")
        query["departure_time"] = datetime.datetime(year=int(year), month=int(month), day=int(day), hour=int(hour),
                                                   minute=int(minute))

    gmaps = googlemaps.Client(key='AIzaSyA27-jm6gjzs_sQqdiuPM8ZsWaTTItBEMw')
    directions_result = gmaps.directions(query["origin"],
                                         query["destination"],
                                         mode=query["mode"],
                                         departure_time = query["departure_time"])

    primary_query = directions_result[0]
    query_emissions = 0
    for _, leg in enumerate(primary_query['legs']):
        for step in leg["steps"]:
            if step["travel_mode"] == "DRIVING":
                query_emissions += (step["distance"]["value"] / 1000) * 0.19 # transport_emission_coefficient_dict[""]
            elif step["travel_mode"] == "TRANSIT":
                query_emissions += (step["distance"]["value"] / 1000) * 0.05 # transport_emission_coefficient_dict[]
            elif step["travel_mode"] == "CYCLING":
                query_emissions += 0
            elif step["travel_mode"] == "WALKING":
                query_emissions += 0
            else:
                query_emissions += 0


    # TODO: extract the entries of the query element and call the Google Maps API with them. Then extract all the
    # TODO: different segments from the result legs and multiply them with the corresponding emission coefficient
    # TODO: for the respective transit mode

    # # For now, grabbing approximate distance from user and multiplying by transport_emission_coefficient values
    # if query['carType'] == 'petrol':
    #     approximate_emissions = transport_emission_coefficient_dict['Petrol Car'] * float(query['approximateDist'])
    # elif query['carType'] == 'diesel':
    #     approximate_emissions = transport_emission_coefficient_dict['Diesel Car'] * float(query['approximateDist'])
    # else:
    #     raise Exception(f"{query['carType']} is not a valid car option, please re-run and enter either petrol or diesel.")
    return query["origin"], query["destination"], query_emissions


if __name__ == '__main__':
    legs = []
    got_all_entries: bool = False

    print("Emissions calculator started. Please enter the legs of your journey one at a time.")
    while not got_all_entries:
        option = input(f"Leg {len(legs) + 1}: Please choose between 'flight', 'transit', 'driving', 'walking' and "
                       f"'bicycling'. To run the calculation on all previously entered legs, type 'done' ")

        if option == "flight":
            received_valid_input: bool = False
            location1 = ""
            location2 = ""
            distance = 0

            while not received_valid_input:
                location1 = input("Please enter the starting position ")
                location2 = input("Please enter the destination ")
                distance = calculate_distance(location1, location2)

                if distance is not None:
                    print(f"The distance between {location1} and {location2} is approximately {distance:.2f} kilometers.")
                    flight_class = input("Please choose the class you fly in: Economy, Premium Economy, Business, First ")
                    received_valid_input = True
                    if flight_class == "Economy":
                        emissions = distance * transport_emission_coefficient_dict["Flight Economy"]
                    elif flight_class == "Premium":
                        pass
                    else:
                        received_valid_input = False

                else:
                    print("Could not calculate the distance due to an error.")

            legs.append((location1, location2, emissions))

        # Should we add a function for bicycling or walking here which doesn't calculate any emissions but just
        # displays info on its leg? Happy to do that :)
        elif option == "transit" or option == "driving" or option == "walking" or option == "bicycling":
            legs.append(create_driving_leg(option))

        elif option == "done":
            got_all_entries = True

        else:
            print("Unrecognised response, please choose from listed options")
            break

        print(f"Leg from {legs[-1][0]} to {legs[-1][1]} recorded")

    total_emissions: float = sum([elem[2] for elem in legs])
    print(f"Legs of Journey: {legs}")
    print(f"Total emissions: {total_emissions} kg CO2")
