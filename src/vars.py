import json
import csv
from unidecode import unidecode

class RouteVar:
    """
    Represents a route variable with various attributes.

    Attributes:
        _route_id (int): The ID of the route.
        _var_id (int): The ID of the variable.
        _var_name (str): The name of the variable.
        _var_short_name (str): The short name of the variable.
        _route_no (str): The route number.
        _start_stop (str): The starting stop of the route.
        _end_stop (str): The ending stop of the route.
        _distance (float): The distance of the route.
        _outbound (bool or None): Indicates if the route is outbound.
        _running_time (int): The running time of the route.
    """

    def __init__(self, route_id=0, var_id=0, var_name="", var_short_name="",
                 route_no="", start_stop="", end_stop="",
                 distance=0.0, outbound=None, running_time=0):
        self._route_id = route_id
        self._var_id = var_id
        self._var_name = var_name
        self._var_short_name = var_short_name
        self._route_no = route_no
        self._start_stop = start_stop
        self._end_stop = end_stop
        self._distance = distance
        self._outbound = outbound
        self._running_time = running_time

    def __str__(self):
        """
        Returns a string representation of the RouteVar object.

        Returns:
            str: A string containing the details of the route.
        """
        return f"RouteId: {self._route_id}, VarID: {self._var_id}, VarName: {self._var_name}, VarShortName: {self._var_short_name}, RouteNo: {self._route_no}, StartStop: {self._start_stop}, EndStop: {self._end_stop}, Distance: {self._distance}, Outbound: {self._outbound}, RunningTime: {self._running_time}"
    
    def __eq__(self, other):
        """
        Checks if two RouteVar objects are equal.

        Args:
            other (RouteVar): Another RouteVar object for comparison.

        Returns:
            bool: True if the objects are equal, False otherwise.
        """
        return isinstance(other, RouteVar) and self._route_id == other._route_id and self._var_id == other._var_id
                
    def __hash__(self):
        """
        Computes the hash value of the RouteVar object.

        Returns:
            int: The hash value.
        """
        return hash((self._route_id, self._var_id))

    def get_route_id(self):
        return self._route_id

    def set_route_id(self, route_id):
        self._route_id = route_id

    def get_var_id(self):
        return self._var_id

    def set_var_id(self, var_id):
        self._var_id = var_id

    def get_var_name(self):
        return self._var_name

    def set_var_name(self, var_name):
        self._var_name = var_name

    def get_var_short_name(self):
        return self._var_short_name

    def set_var_short_name(self, var_short_name):
        self._var_short_name = var_short_name

    def get_route_no(self):
        return self._route_no

    def set_route_no(self, route_no):
        self._route_no = route_no

    def get_start_stop(self):
        return self._start_stop

    def set_start_stop(self, start_stop):
        self._start_stop = start_stop

    def get_end_stop(self):
        return self._end_stop

    def set_end_stop(self, end_stop):
        self._end_stop = end_stop

    def get_distance(self):
        return self._distance

    def set_distance(self, distance):
        self._distance = distance

    def get_outbound(self):
        return self._outbound

    def set_outbound(self, outbound):
        self._outbound = outbound

    def get_running_time(self):
        return self._running_time

    def set_running_time(self, running_time):
        self._running_time = running_time


class RouteVarQuery:
    """
    Provides methods for querying RouteVar objects based on its attributes.

    Attributes:
        route_vars (list): A list of RouteVar objects.
    """

    def __init__(self):
        self.route_vars = []

    def load_data(self, file_path):
        """
        Loads route variable data from a JSON file.

        Args:
            file_path (str): The path to the JSON file.
        """
        with open(file_path, 'r', encoding="utf-8") as file:
            for line in file:
                obj = json.loads(line)
                for rv in obj:
                    route_var = RouteVar(rv["RouteId"], rv["RouteVarId"], rv["RouteVarName"],
                                        rv["RouteVarShortName"], rv["RouteNo"], rv["StartStop"], rv["EndStop"],
                                        rv["Distance"], rv["Outbound"], rv["RunningTime"])
                    self.route_vars.append(route_var)


    def search_by_route_id(query_list, route_id):
        return [route_var for route_var in query_list if route_var.get_route_id() == route_id]

    def search_by_var_id(query_list, var_id):
        return [route_var for route_var in query_list if route_var.get_var_id() == var_id]

    def search_by_var_name(query_list, var_name):
        return [route_var for route_var in query_list if route_var.get_var_name() == var_name]

    def search_by_var_short_name(query_list, var_short_name):
        return [route_var for route_var in query_list if route_var.get_var_short_name() == var_short_name]

    def search_by_route_no(query_list, route_no):
        return [route_var for route_var in query_list if route_var.get_route_no() == route_no]

    def search_by_start_stop(query_list, start_stop):
        return [route_var for route_var in query_list if route_var.get_start_stop() == start_stop]

    def search_by_end_stop(query_list, end_stop):
        return [route_var for route_var in query_list if route_var.get_end_stop() == end_stop]

    def search_by_distance(query_list, distance):
        return [route_var for route_var in query_list if route_var.get_distance() == distance]

    def search_by_outbound(query_list, outbound):
        return [route_var for route_var in query_list if route_var.get_outbound() == outbound]

    def search_by_running_time(query_list, running_time):
        return [route_var for route_var in query_list if route_var.get_running_time() == running_time]
    

    def search_routes_by(self, *functions):
        """
        Searches for RouteVar objects using multiple search criteria.

        Args:
            *functions (tuple): A tuple of search functions and their arguments.

        Returns:
            list: A list of RouteVar objects matching all search criteria.
        """

        query_list = self.route_vars
        for function, arg in functions:
            query_list = function(query_list, arg)
        return query_list
    
    def search_routes_by(self, **kwargs):
        """
        Searches for RouteVar objects by arbitrary keyword arguments.

        This method allows searching for RouteVar objects by specifying attribute names
        and their corresponding values as keyword arguments.

        Args:
            **kwargs: Arbitrary keyword arguments where the key is the name of the attribute
                      to search for and the value is the desired value of that attribute.

        Returns:
            list: A list of RouteVar objects matching all specified attribute values.
        """

        query_list = self.route_vars

        for key, value in kwargs.items():
            if type(value) == str:
                query_list = [route_var for route_var in query_list if unidecode(getattr(route_var, f"get_{key}")()).lower() == unidecode(value).lower()]
            else:
                query_list = [route_var for route_var in query_list if getattr(route_var, f"get_{key}")() == value]

        return query_list


    def output_as_csv(self, query_list, file_path):
        """
        Outputs the query results as CSV format to a file.

        Args:
            query_list (list): The list of RouteVar objects to output.
            file_path (str): The path to the output CSV file.
        """

        with open(file_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["RouteId","RouteVarId","RouteVarName","RouteVarShortName","RouteNo","StartStop","EndStop","Distance",
                            "Outbound","RunningTime"])
            for route_var in query_list:
                writer.writerow(route_var.__dict__.values())


    def output_as_json(self, query_list, file_path):
        """
        Outputs the query results as JSON format to a file.

        Args:
            query_list (list): The list of RouteVar objects to output.
            file_path (str): The path to the output JSON file.
        """

        with open(file_path, 'w', encoding='utf-8') as file:
            for route_var in query_list:
                obj = {
                    "RouteId": route_var.get_route_id(),
                    "RouteVarId": route_var.get_var_id(),
                    "RouteVarName": route_var.get_var_name(),
                    "RouteVarShortName": route_var.get_var_short_name(),
                    "RouteNo": route_var.get_route_no(),
                    "StartStop": route_var.get_start_stop(),
                    "EndStop": route_var.get_end_stop(),
                    "Distance": route_var.get_distance(),
                    "Outbound": route_var.get_outbound(),
                    "RunningTime": route_var.get_running_time()
                }
                json.dump(obj, file, ensure_ascii=False)
                file.write('\n')


def main(route_var_path, output_csv_path, output_json_path):
    #Create an instance of RouteVarQuery and load data from route_var_path
    rv_query = RouteVarQuery()
    rv_query.load_data(route_var_path)

    #Search all (route, var) that has start_stop = 'Bến xe buýt Sài Gòn'
    query_list = rv_query.search_routes_by(end_stop = 'Bến XE Miền Tây')

    #Write the result to CSV and JSON files
    rv_query.output_as_csv(query_list, output_csv_path)
    rv_query.output_as_json(query_list, output_json_path)


if __name__ == "__main__":
    main('./data/vars.json', './output/rv_query.csv', './output/rv_query.json')