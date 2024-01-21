# main.py
# starting point of the program

import datetime


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
               "Please enter the year you want to fly in ",
               "Please enter the month you want to fly in as a number (1-12) ",
               "Please enter the day you want to fly on "]

    for (prompt, entry) in zip(prompts[:4],
                               ["origin",
                                "destination",
                                "operatingCarrierCode",
                                "flightNumber"]):
        query[entry] = input(prompt)

    for (prompt, entry) in zip(prompts[4:],
                               ["year",
                                "month",
                                "day"]):
        query["departureDate"][entry] = input(prompt)

    print(query)

    # TODO: wrap this into another dict as required by the API, then call the API and extract the result
    # TODO: from the result get the emissions value and return it here
    return query["origin"], query["destination"], 0.4  # placeholder for the actual result


def create_driving_leg(mode: str = "") -> tuple:
    query: dict = {
        "origin": "",
        "destination": "",
        "mode": mode,
        "departure_time": datetime.datetime.now()
    }

    prompts = ["Please enter the origin address or waypoint ",
               "Please enter the destination address or waypoint "]

    for (prompt, entry) in zip(prompts,
                               ["origin",
                                "destination"]):
        query[entry] = input(prompt)

    start_now = input("Do you want to start now? (yes/no) ")
    if start_now != "yes":
        year = input("Please enter the year of your journey ")
        month = input("Please enter the month of your journey as a number (1-12) ")
        day = input("Please enter the day of your journey ")
        hour = input("Please enter the hour when you like to depart (24h-format) ")
        minute = input("Please enter the minnute when you like to depart ")
        query["departureTime"] = datetime.datetime(year=int(year), month=int(month), day=int(day), hour=int(hour),
                                                   minute=int(minute))

    # TODO: extract the entries of the query element and call the Google Maps API with them. Then extract all the
    # TODO: different segments from the result legs and multiply them with the corresponding emission coefficient
    # TODO: for the respective transit mode

    print(query)
    return query["origin"], query["destination"], 0.4  # placeholder for the actual result


if __name__ == '__main__':
    legs = []
    got_all_entries: bool = False

    print("Emissions calculator started. Please enter the legs of your journey one at a time.")
    while not got_all_entries:
        option = input(f"Leg {len(legs) + 1}: Please choose between 'flight', 'transit', 'driving', 'walking' and "
                       f"'bicycling'. To run the calculation on all previously entered legs, type 'done' ")

        if option == "flight":
            legs.append(create_flight_leg())

        if option == "transport" or option == "driving" or option == "walking" or option == "bicycling":
            legs.append(create_driving_leg(option))

        if option == "done":
            got_all_entries = True

        print(f"Leg from {legs[-1][0]} to {legs[-1][1]} recorded")

    total_emissions: float = sum([elem[2] for elem in legs])
    print(f"Total emissions: {total_emissions}")
