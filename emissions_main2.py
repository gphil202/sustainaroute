import datetime
import src.common.coefficients2 as c
import googlemaps # why is this grey
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

def create_flight_leg() -> tuple:
    # create query for the google travel impact model
    query: dict = {
        "origin": "",
        "destination": "",
        "operatingCarrierCode": "",
        "flightNumber": -1,
        "departureDate": {"year": -1, "month": -1, "day": -1}
    }

    prompts = ["Please enter the three letter code of the origin airport ",
               "Please enter the three letter code of the destination airport ",
               "Please enter the two letter carrier code for your flight ",
               "Please enter the flight number of your flight ",
               "Please enter the approximate distance in kilometers of your flight ", #TODO: Replace asking for explicit distance with API calculation
               "Please enter the year you want to fly in ",
               "Please enter the month you want to fly in as a number (1-12) ",
               "Please enter the day you want to fly on "]

    for (prompt, entry) in zip(prompts[:5],
                               ["origin",
                                "destination",
                                "operatingCarrierCode",
                                "flightNumber",
                                "approximateDist"]):
        query[entry] = input(prompt)

    for (prompt, entry) in zip(prompts[5:],
                               ["year",
                                "month",
                                "day"]):
        query["departureDate"][entry] = input(prompt)

    print(query)

    # # documentation: https://developers.google.com/maps/documentation/directions/get-directions?hl=de
    # now = datetime.now() # is this relevant for the flights?
    # directions_result = gmaps.directions(query["origin"],
    #                                      query["destination"],
    #                                      mode="flight",
    #                                      departure_time=query["departureDate"])
    # print(directions_result)
    # TODO: wrap this into another dict as required by the API, then call the API and extract the result
    # TODO: from the result get the emissions value and return it here

    # For now, grabbing approximate distance from user and multiplying by transport_emission_coefficient values
    approximate_emissions = transport_emission_coefficient_dict['Flight'] * float(query['approximateDist'])
    return query["origin"], query["destination"], approximate_emissions  # placeholder for the actual result


def create_driving_leg(mode: str = "") -> tuple:
    query: dict = {
        "origin": "",
        "destination": "",
        "mode": mode,
        "departure_time": datetime.datetime.now()
    }

    prompts = ["Please enter the origin address or waypoint ",
               "Please enter the destination address or waypoint ",
               "Please enter if the car is petrol or diesel ",
               "Please enter the approximate distance in kilometers ",] # can be deleted once we extracted vale of each leg

    for (prompt, entry) in zip(prompts,
                               ["origin",
                                "destination",
                                "carType", # has to be deleted in this position right? because of google API
                                "approximateDist"]): # has to be deleted in this position right? because of google API
        query[entry] = input(prompt)

    start_now = input("Do you want to start now? (yes/no) ")
    if start_now != "yes":
        year = input("Please enter the year of your journey ")
        month = input("Please enter the month of your journey as a number (1-12) ")
        day = input("Please enter the day of your journey ")
        hour = input("Please enter the hour when you like to depart (24h-format) ")
        minute = input("Please enter the minute when you like to depart ")
        query["departureTime"] = datetime.datetime(year=int(year), month=int(month), day=int(day), hour=int(hour),
                                                   minute=int(minute))
        #
        # now = datetime.now()
        # directions_result = gmaps.directions(query["origin"],
        #                                      query["destination"],
        #                                      mode="driving", what about transport?
        #                                      departure_time=query["departureTime"])
        # print(directions_result)
        # get value of each leg -> then sum and th
    # else:
        # now = datetime.now()
        # directions_result = gmaps.directions(query["origin"],
        #                                      query["destination"],
        #                                      mode="driving", what about transport?
        #                                      departure_time=now)

    # TODO: extract the entries of the query element and call the Google Maps API with them. Then extract all the
    # TODO: different segments from the result legs and multiply them with the corresponding emission coefficient
    # TODO: for the respective transit mode

    # For now, grabbing approximate distance from user and multiplying by transport_emission_coefficient values
    if query['carType'] == 'petrol':
        approximate_emissions = transport_emission_coefficient_dict['Petrol Car'] * float(query['approximateDist'])
    elif query['carType'] == 'diesel':
        approximate_emissions = transport_emission_coefficient_dict['Diesel Car'] * float(query['approximateDist'])
    else:
        raise Exception(f"{query['carType']} is not a valid car option, please re-run and enter either petrol or diesel.")
    return query["origin"], query["destination"], approximate_emissions  # placeholder for the actual result


if __name__ == '__main__':
    legs = []

    print("Emissions calculator started. Please enter the legs of your journey one at a time.")
    while True:
        option = input(f"Leg {len(legs) + 1}: Please choose between 'flight', 'transit', 'driving', 'walking' and "
                       f"'bicycling'. To run the calculation on all previously entered legs, type 'done' ")

        if option == "flight":
            legs.append(create_flight_leg())
        # Should we add a function for bicycling or walking here which doesn't calculate any emissions but just
        # displays info on its leg? Happy to do that :)
        elif option == "transport" or option == "driving" or option == "walking" or option == "bicycling":
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
