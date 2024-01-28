# coefficients.py
# contains the emission coefficients for different modes of transport

from enum import Enum

# WTT emission values (well to tank): All greenhouse gas emissions from the production, transportation, transformation
# and distribution of the fuel used to power the vehicle. (these are produced in addition to the ones released by
# burning the fuel to facilitate transport)

# CO2 values are in kg if not stated otherwise


class CarDiesel(float, Enum):
    CO2_PER_TONNE = 3032.89
    WTT_CO2_PER_TONNE = 720.72857
    CO2_PER_LITER = 2.56
    WTT_CO2_PER_LITER = 0.60986
    CO2_PER_kWh = 0.26
    WTT_CO2_PER_kWh = 0.06109
    CO2_PER_km = 0.17082
    kWh_PER_km = 0.66889


class CarPetrol(float, Enum):
    CO2_PER_TONNE = 2903.08
    WTT_CO2_PER_TONNE = 824.1216
    CO2_PER_LITER = 2.16
    WTT_CO2_PER_LITER = 0.61328
    CO2_PER_kWh = 0.24
    WTT_CO2_PER_kWh = 0.06774
    CO2_PER_km = 0.17048
    kWh_PER_km = 0.71321


class MarineFuel(float, Enum):
    CO2_PER_TONNE = 3159.5
    WTT_CO2_PER_TONNE = 709.08076
    CO2_PER_LITER = 3.11
    WTT_CO2_PER_LITER = 0.69723
    CO2_PER_kWh = 0.28
    WTT_CO2_PER_kWh = 0.06264


class AviationFuel(float, Enum):
    CO2_PER_TONNE = 3181.43
    WTT_CO2_PER_TONNE = 658.57016
    CO2_PER_LITER = 2.55
    WTT_CO2_PER_LITER = 0.52686
    CO2_PER_kWh = 0.26
    WTT_CO2_PER_kWh = 0.054


class AirTravelEmissionsPerPassengerKm(float, Enum):
    DOMESTIC_UK_AVERAGE = 0.24587
    WTT_DOMESTIC_UK_AVERAGE = 0.02691
    UK_TO_EU_AVERAGE = 0.51353
    WTT_UK_TO_EU_AVERAGE = 0.01681
    UK_TO_EU_ECONOMY = 0.15102
    WTT_UK_TO_EU_ECONOMY = 0.01654
    UK_TO_EU_BUSINESS = 0.22652
    WTT_UK_TO_EU_BUSINESS = 0.0248
    UK_TO_NON_EU_AVERAGE = 0.19309
    WTT_UK_TO_NON_EU_AVERAGE = 0.02114
    UK_TO_NON_EU_ECONOMY = 0.14787
    WTT_UK_TO_NON_EU_ECONOMY = 0.01619
    UK_TO_NON_EU_PREMIUM_ECONOMY = 0.23659
    WTT_UK_TO_NON_EU_PREMIUM_ECONOMY = 0.02591
    UK_TO_NON_EU_BUSINESS = 0.42882
    WTT_UK_TO_NON_EU_BUSINESS = 0.04696
    UK_TO_NON_EU_FIRST = 0.59147
    WTT_UK_TO_NON_EU_FIRST = 0.6477
    UK_TO_NON_UK_AVERAGE = 0.18362
    WTT_UK_TO_NON_UK_AVERAGE = 0.02011
    UK_TO_NON_UK_ECONOMY = 0.140625
    WTT_UK_TO_NON_UK_ECONOMY = 0.0154
    UK_TO_NON_UK_PREMIUM_ECONOMY = 0.225
    WTT_UK_TO_NON_UK_PREMIUM_ECONOMY = 0.02464
    UK_TO_NON_UK_BUSINESS = 0.40781
    WTT_UK_TO_NON_UK_BUSINESS = 0.04466
    UK_TO_NON_UK_FIRST = 0.56251
    WTT_UK_TO_NON_UK_FIRST = 0.06159


class Ferry(float, Enum):
    FOOT_PASSENGER = 0.01874
    WTT_FOOT_PASSENGER = 0.00421
    CAR_PASSENGER = 0.012952
    WTT_CAR_PASSENGER = 0.02909
    AVERAGE_CAR = 0.11286
    WTT_AVERAGE_CAR = 0.02535


class Rail(float, Enum):
    # emissions per passenger km
    UK_DOMESTIC = 0.03549
    WTT_UK_DOMESTIC = 0.00892
    INTERNATIONAL = 0.00446
    WTT_INTERNATIONAL = 0.00116
    LIGHT_RAIL_TRAM = 0.02861
    WTT_LIGHT_RAIL_TRAM = 0.00745
    LONDON_UNDERGROUND = 0.02781
    WTT_LONDON_UNDERGROUND = 0.00724


class HotelStay(float, Enum):
    # emissions per room per night
    AUSTRALIA = 35.0
    BELGIUM = 12.2
    BRAZIL = 8.7
    CANADA = 7.4
    CHILE = 27.6
    CHINA = 53.5
    COLOMBIA = 14.7
    COSTA_RICA = 4.7
    EGYPT = 44.2
    GREECE = 6.7
    GERMANY = 13.2
    HONG_KONG = 51.5
    INDIA = 58.9
    INDONESIA = 62.7
    ITALY = 14.3
    JAPAN = 39.0
    JORDAN = 68.9
    KOREA = 55.8
    MALAYSIA = 61.5
    MALDIVES = 152.2
    MEXICO = 19.3
    NETHERLANDS = 14.8
    OMAN = 90.3
    PHILIPPINES = 54.3
    PORTUGAL = 19.0
    QATAR = 86.2
    RUSSIAN_FEDERATION = 24.2
    SAUDI_ARABIA = 106.4
    SINGAPORE = 24.5
    SOUTH_AFRICA = 51.4
    SPAIN = 7.0
    SWITZERLAND = 6.6
    THAILAND = 43.3
    TURKEY = 32.1
    UNITED_KINGDOM = 10.4
    UNITED_ARAB_EMIRATES = 63.8
    UNITED_STATES = 16.1
    VIETNAM = 38.5



