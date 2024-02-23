from opensky_api import OpenSkyApi
import time
from datetime import datetime, timezone, timedelta
import airportsdata
from zoneinfo import ZoneInfo
from plane_data import plane_data

airports = airportsdata.load()  # key is the ICAO identifier (the default)

class Aircraft():
    def __init__(self):
        self.api = OpenSkyApi()

    def get_by_aircraft(self, icao24, start, end): 
        try: 
            self.flights = self.api.get_flights_by_aircraft(icao24, start, end)
            return self.flights
        except:
            self.flights = plane_data
            print("OpenSky Error, default FlightData set")

    def get_route(self, icao24, start, end):
        self.get_by_aircraft(icao24, start, end)
        if self.flights is not None:
            for flight in self.flights:
                departure_airport = "Departure Airport Not Found"
                arrival_airport = "Arrival Airport Not Found"
                if flight.estDepartureAirport is not None:
                    departure_airport = airports[flight.estDepartureAirport]['name']
                if flight.estArrivalAirport is not None:
                    arrival_airport = airports[flight.estArrivalAirport]['name']
                seconds_elapsed = timedelta(flight.lastSeen - flight.firstSeen)
                hours_div = timedelta(hours = 1)
                minutes_div = timedelta(minutes = 1)
                hours_elapsed, remainder = divmod(seconds_elapsed, hours_div)
                minutes_elapsed, remainder = divmod(remainder, minutes_div)

                # Calculate Departure Time and Timezone
                departure_timezone = ZoneInfo(airports[flight.estDepartureAirport]['tz'])
                departure_time = time.gmtime(flight.firstSeen)
                departure_datetime = datetime(departure_time.tm_year, departure_time.tm_mon, \
                    departure_time.tm_mday, departure_time.tm_hour, \
                        departure_time.tm_min, departure_time.tm_sec,
                    tzinfo = departure_timezone)
                # Calculate Arrival Time and Timezone
                arrival_timezone = ZoneInfo(airports[flight.estArrivalAirport]['tz'])
                arrival_time = time.gmtime(flight.lastSeen)
                arrival_datetime = datetime(arrival_time.tm_year, arrival_time.tm_mon, \
                    arrival_time.tm_mday, arrival_time.tm_hour, \
                        arrival_time.tm_min, arrival_time.tm_sec,
                    tzinfo = arrival_timezone)
                    # Need to fix this hours_elapsed business
                route = "Plane {} travelled from {} on {} to {} on {}. \
                    Duration was {} hours and {} minutes".format \
                    (flight.icao24, departure_airport, departure_datetime, \
                        arrival_airport, arrival_datetime, hours_elapsed, minutes_elapsed)
                print(route)
                return route
                        
