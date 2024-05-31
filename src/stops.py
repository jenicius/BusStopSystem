import json
import csv


class Stop:
    """
    Represents a stop with various attributes.

    Attributes:
        _stop_id (int): The ID of the stop.
        _code (str): The code of the stop.
        _name (str): The name of the stop.
        _stop_type (str): The type of the stop.
        _zone (str): The zone of the stop.
        _ward (str): The ward of the stop.
        _address_no (str): The address number of the stop.
        _street (str): The street of the stop.
        _support_disability (bool): Indicates whether the stop supports disability.
        _status (str): The status of the stop.
        _lng (float): The longitude of the stop.
        _lat (float): The latitude of the stop.
        _search (str): The search term associated with the stop.
        _routes (list): The routes associated with the stop.
    """

    def __init__(self, stop_id, code, name, stop_type, zone, ward, address_no, street, support_disability, status, lng,
                 lat, search, routes):
        self._stop_id = stop_id
        self._code = code
        self._name = name
        self._stop_type = stop_type
        self._zone = zone
        self._ward = ward
        self._address_no = address_no
        self._street = street
        self._support_disability = support_disability
        self._status = status
        self._lng = lng
        self._lat = lat
        self._search = search
        self._routes = routes

    def __str__(self):
        """
        Returns a string representation of the Stop object.

        Returns:
            str: A string containing details of the stop.
        """

        return f"Stop ID: {self._stop_id}, Code: {self._code}, Name: {self._name}, Stop Type: {self._stop_type}, Zone: {self._zone}, Ward: {self._ward}, Address No: {self._address_no}, Street: {self._street}, Support Disability: {self._support_disability}, Status: {self._status}, Lng: {self._lng}, Lat: {self._lat}, Search: {self._search}, Routes: {self._routes}" 
    
    def __eq__(self, other):
        """
        Checks if two Stop objects are equal.

        Args:
            other (Stop): Another Stop object for comparison.

        Returns:
            bool: True if the objects are equal, False otherwise.
        """

        return isinstance(other, Stop) and self._stop_id == other._stop_id
              
    def __hash__(self):
        """
        Computes the hash value of the Stop object.

        Returns:
            int: The hash value.
        """
        return hash((self._stop_id, self._code))

    def get_stop_id(self):
        return self._stop_id

    def set_stop_id(self, stop_id):
        self._stop_id = stop_id

    def get_code(self):
        return self._code

    def set_code(self, code):
        self._code = code

    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    def get_stop_type(self):
        return self._stop_type

    def set_stop_type(self, stop_type):
        self._stop_type = stop_type

    def get_zone(self):
        return self._zone

    def set_zone(self, zone):
        self._zone = zone

    def get_ward(self):
        return self._ward

    def set_ward(self, ward):
        self._ward = ward

    def get_address_no(self):
        return self._address_no

    def set_address_no(self, address_no):
        self._address_no = address_no

    def get_street(self):
        return self._street

    def set_street(self, street):
        self._street = street

    def get_support_disability(self):
        return self._support_disability

    def set_support_disability(self, support_disability):
        self._support_disability = support_disability

    def get_status(self):
        return self._status

    def set_status(self, status):
        self._status = status

    def get_lng(self):
        return self._lng

    def set_lng(self, lng):
        self._lng = lng

    def get_lat(self):
        return self._lat

    def set_lat(self, lat):
        self._lat = lat

    def get_search(self):
        return self._search

    def set_search(self, search):
        self._search = search

    def get_routes(self):
        return self._routes

    def set_routes(self, routes):
        self._routes = routes


class StopQuery:
    """
    Provides methods for querying Stop objects based on its attributes.

    Attributes:
        stops (list): A list of Stop objects.
    """

    def __init__(self):
        self.stops = []

    def load_data(self, file_path):
        """
        Loads stop data from a JSON file.

        Args:
            file_path (str): The path to the JSON file.
        """

        with open(file_path, 'r', encoding='utf-8') as file:
            stops = set()
            for line in file:
                for stop_data in json.loads(line)['Stops']:
                        stop = Stop(stop_data['StopId'], stop_data['Code'], stop_data['Name'], stop_data['StopType'],
                                    stop_data['Zone'], stop_data['Ward'], stop_data['AddressNo'], stop_data['Street'],
                                    stop_data['SupportDisability'], stop_data['Status'], stop_data['Lng'], stop_data['Lat'],
                                    stop_data['Search'], stop_data['Routes'])
                        stops.add(stop)
            self.stops = list(stops)

    def search_by_stop_id(query_list, stop_id):
        return [stop for stop in query_list if stop.get_stop_id() == stop_id]

    def search_by_code(query_list, code):
        return [stop for stop in query_list if stop.get_code() == code]

    def search_by_name(query_list, name):
        return [stop for stop in query_list if stop.get_name() == name]

    def search_by_stop_type(query_list, stop_type):
        return [stop for stop in query_list if stop.get_stop_type() == stop_type]

    def search_by_zone(query_list, zone):
        return [stop for stop in query_list if stop.get_zone() == zone]

    def search_by_ward(query_list, ward):
        return [stop for stop in query_list if stop.get_ward() == ward]

    def search_by_address_no(query_list, address_no):
        return [stop for stop in query_list if stop.get_address_no() == address_no]

    def search_by_street(query_list, street):
        return [stop for stop in query_list if stop.get_street() == street]

    def search_by_support_disability(query_list, support_disability):
        return [stop for stop in query_list if stop.get_support_disability() == support_disability]

    def search_by_status(query_list, status):
        return [stop for stop in query_list if stop.get_status() == status]

    def search_by_lng(query_list, lng):
        return [stop for stop in query_list if stop.get_lng() == lng]

    def search_by_lat(query_list, lat):
        return [stop for stop in query_list if stop.get_lat() == lat]

    def search_by_search(query_list, search):
        return [stop for stop in query_list if stop.get_search() == search]

    def search_by_routes(query_list, routes):
        return [stop for stop in query_list if stop.get_routes() == routes]

    def search_stops_by(self, *functions):
        """
        Searches for RouteVar objects using multiple search criteria.

        Args:
            *functions (tuple): A tuple of search functions and their arguments.

        Returns:
            list: A list of RouteVar objects matching all search criteria.
        """

        query_list = self.stops
        for function, arg in functions:
            query_list = function(query_list, arg)
        return query_list
    
    def search_stops_by(self, **attr):
        """
        Searches for stops by arbitrary attributes.

        Args:
            **attr: Arbitrary keyword arguments representing attributes and their values.

        Returns:
            list: A list of Stop objects matching all specified attribute values.
        """

        query_list = self.stops

        for key, value in attr.items():
            query_list = [stop for stop in query_list if getattr(stop, f"get_{key}")() == value]

        return query_list
        
    def output_as_csv(self, query_list, file_path):
        """
        Outputs the query results as CSV format to a file.

        Args:
            query_list (list): The list of Stop objects to output.
            file_path (str): The path to the output CSV file.
        """

        with open(file_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['StopId', 'Code', 'Name', 'StopType', 'Zone', 'Ward', 'AddressNo', 'Street',
                             'SupportDisability', 'Status', 'Lng', 'Lat', 'Search', 'Routes'])
            for stop in query_list:
                writer.writerow(stop.__dict__.values())

    def output_as_json(self, query_list, file_path):
        """
        Outputs the query results as JSON format to a file.

        Args:
            query_list (list): The list of Stop objects to output.
            file_path (str): The path to the output JSON file.
        """

        with open(file_path, 'w', encoding='utf-8') as file:
            for stop in query_list:
                stop_dict = {
                    'StopId': stop.get_stop_id(),
                    'Code': stop.get_code(),
                    'Name': stop.get_name(),
                    'StopType': stop.get_stop_type(),
                    'Zone': stop.get_zone(),
                    'Ward': stop.get_ward(),
                    'AddressNo': stop.get_address_no(),
                    'Street': stop.get_street(),
                    'SupportDisability': stop.get_support_disability(),
                    'Status': stop.get_status(),
                    'Lng': stop.get_lng(),
                    'Lat': stop.get_lat(),
                    'Search': stop.get_search(),
                    'Routes': stop.get_routes()
                }
                json.dump(stop_dict, file, ensure_ascii=False)
                file.write('\n')

def main(stop_path, output_csv_path, output_json_path):
    #Create an instance of StopQuery
    stop_query = StopQuery()

    #Load data 
    stop_query.load_data(stop_path)

    #Search and output to CSV and JSON files
    query_list = stop_query.search_stops_by(street = 'Lê Lai')
    stop_query.output_as_csv(query_list, output_csv_path)
    stop_query.output_as_json(query_list, output_json_path)


if __name__ == "__main__":
    main('./data/stops.json', './output/stop_query.csv', './output/stop_query.json')