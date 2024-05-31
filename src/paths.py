import json
import csv


class Path:
    """
    A class representing a path with latitude, longitude, route ID, and variable ID.

    Attributes:
    - lat (list): A list of latitude coordinates.
    - lng (list): A list of longitude coordinates.
    - route_id (int): The ID of the route.
    - var_id (int): The ID of the variable.
    """
    
    def __init__(self, lat=[], lng=[], route_id=0, var_id=0):
        self._lat = lat
        self._lng = lng
        self._route_id = route_id
        self._var_id = var_id

    def __str__(self):
        return f"route_id={self._route_id}, var_id={self._var_id}, lat={self._lat}, lng={self._lng}"

    def get_lat(self):
        return self._lat

    def set_lat(self, value):
        self._lat = value

    def get_lng(self):
        return self._lng

    def set_lng(self, value):
        self._lng = value

    def get_route_id(self):
        return self._route_id

    def set_route_id(self, value):
        self._route_id = value

    def get_var_id(self):
        return self._var_id

    def set_var_id(self, value):
        self._var_id = value


class PathQuery:
    """
    A class for querying and manipulating Path objects.

    Attributes:
    - path_list (list): A list of Path objects.

    Methods:
    - load_data(file_path): Loads data from a JSON file into path_list.
    - search_by_path(query_list, lat, lng): Searches for paths matching given latitude and longitude.
    - search_by_route_id(query_list, route_id): Searches for paths matching given route ID.
    - search_by_var_id(query_list, var_id): Searches for paths matching given variable ID.
    - search_by(**kwargs): Searches for paths based on given attribute-value pairs.
    - output_as_csv(query_list, file_path): Writes query results to a CSV file.
    - output_as_json(query_list, file_path): Writes query results to a JSON file.
    """

    def __init__(self):
        self.path_list = []


    def load_data(self, file_path):
        """
        Loads data from a JSON file and appends it to path_list.

        Args:
            file_path (str): The path to the JSON file.
        """
        with open(file_path, 'r', encoding="utf-8") as file:
            for line in file:
                data = json.loads(line)
                path = Path(lat=data['lat'], lng=data['lng'], route_id=int(data['RouteId']), var_id=int(data['RouteVarId']))
                self.path_list.append(path)


    def search_by_path(query_list, lat, lng):
        sublist = list(zip(lat, lng))
        n = len(sublist)

        result = []
        for path in query_list:

            lst = list(zip(path.get_lat(), path.get_lng()))
            for i in range(len(lst) - n + 1):
                if lst[i:i + n] == sublist:
                    result.append(path)
                    break
        
        return result

    def search_by_route_id(query_list, route_id):
        return [path for path in query_list if path.get_route_id() == route_id]

    def search_by_var_id(query_list, var_id):
        return [path for path in query_list if path.get_var_id() == var_id]

    def search_paths_by(self, *functions):
        """
        Searches paths based on provided functions.

        Args:
            *functions: Variable length list of tuples containing function and its argument.

        Returns:
            list: List of paths based on the applied search functions.
        """
        query_list = self.path_list
        for function, arg in functions:
            query_list = function(query_list, arg)
        return query_list

    def search_paths_by(self, **kwargs):
        """
        Searches paths based on provided keyword arguments.

        Args:
            **kwargs: Keyword arguments representing attribute-value pairs for path search.

        Returns:
            list: List of paths matching the provided attribute-value pairs.
        """
        query_list = self.path_list
        for key, value in kwargs.items():
            query_list = [path for path in query_list if getattr(path, f"get_{key}")() == value]
        return query_list


    def output_as_csv(self, query_list, file_path):
        """
        Outputs paths as CSV format.

        Args:
            query_list (list): List of paths to output.
            file_path (str): The path to the CSV output file.
        """
        with open(file_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["latitudes", "longitude", "RouteId", "RouteVarId"])
            for path in query_list:
                writer.writerow(path.__dict__.values())


    def output_as_json(self, query_list, file_path):
        """
        Outputs paths as JSON format.

        Args:
            query_list (list): List of paths to output.
            file_path (str): The path to the JSON output file.
        """
        with open(file_path, 'w', encoding='utf-8') as file:
            for path in query_list:
                json_data={
                    "lat": path.get_lat(),
                    "lng": path.get_lng(),
                    "RouteId": path.get_route_id(),
                    "VarId": path.get_var_id()
                }
                json.dump(json_data, file)
                file.write('\n')

def main(file_path, output_csv_path, output_json_path):
    #Create an instance of PathQuery and load data from file_path
    path_query = PathQuery()
    path_query.load_data(file_path)

    #Search paths with route_id = 1
    query_list = path_query.search_paths_by(route_id=1)

    #Write the result to CSV and JSON files
    path_query.output_as_csv(query_list, output_csv_path)
    path_query.output_as_json(query_list, output_json_path)

if __name__ == "__main__":
    main('./data/paths.json', './output/path_query.csv', './output/path_query.json')




