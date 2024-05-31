import google.generativeai as genai
import google.ai.generativelanguage as glm

from vars import RouteVarQuery
from stops import StopQuery
from paths import PathQuery

GOOGLE_API_KEY = 'AIzaSyDSxXpb_2TtHkAr74ctKy-sIOY8h6PLD5s'


class LLM_query:
    def __init__(self, GOOGLE_API_KEY, routevar_fp, stop_fp, path_fp):
        genai.configure(api_key=GOOGLE_API_KEY)
        self.query_tools = glm.Tool(
            function_declarations=[
                glm.FunctionDeclaration(
                    name='search_stops_by',
                    description="Returns a list of stops satisfying some given criteria.",
                    parameters=glm.Schema(
                        type=glm.Type.OBJECT,
                        properties={
                            'stop_id':glm.Schema(
                                type=glm.Type.INTEGER,
                                description='The id of the stop, e.g. 35.'),
                            'code': glm.Schema(
                                type=glm.Type.STRING,
                                description='The code of the stop, e.g. BX 01, HBC 415, QBT 280'),
                            'name': glm.Schema(
                                type=glm.Type.STRING,
                                description='The name of the stop, e.g. Bến xe buýt Sài Gòn, Bệnh viện Nhi Thành phố. \
                                Any typos, extra spaces, etc must be fixed when parsing. Example: "Bếnn  xe být Sài gòn" -> "Bến xe buýt Sài Gòn"'),
                            'stop_type':glm.Schema(
                                type=glm.Type.STRING,
                                description='The type of the stop, e.g. Bến xe, Nhà chờ, Trụ dừng, Ô sơn'),
                            'zone':glm.Schema(
                                type=glm.Type.STRING,
                                description='The zone of the stop, e.g. Quận 1, Quận Phú Nhuận'),
                            'ward':glm.Schema(
                                type=glm.Type.STRING,
                                description='The ward of the stop, e.g. Phường Bến Thành, Phường Nguyễn Thái Bình'),
                            'address_no':glm.Schema(
                                type=glm.Type.STRING,
                                description='The address number of the stop, e.g. 81-83-83B or Hàm Nghi 7'),
                            'street':glm.Schema( 
                                type=glm.Type.STRING,
                                description='The street of the stop, e.g. Hai Bà Trưng, Lê Lai'),
                            'support_disability':glm.Schema(
                                type=glm.Type.BOOLEAN,
                                description='''Whether the stop supports disability. "Có" if it does, "" if it doesn't'''),
                            'lng':glm.Schema(
                                type=glm.Type.NUMBER,
                                description='The longitude of the stop.'),
                            'lat':glm.Schema(
                                type=glm.Type.NUMBER,
                                description='The latitude of the stop.'),
                            'search':glm.Schema(
                                type=glm.Type.STRING,
                                description='The search query for the stopm e.g. BxbSG BXBSG LL, NTN 187 PNL'),
                            'routes':glm.Schema(
                                type=glm.Type.STRING,
                                description='The routes passing through the stop e.g. 03, 04, 102, 109, 140, 18, 19, 20, 28, 34, 36, 39, 46, 52, 65, 69, 72, 75, 86, 88, 93')
                        },
                    )
                ),
                glm.FunctionDeclaration(
                    name='search_routes_by',
                    description="Returns a list of routes satisfying some given criteria.",
                    parameters=glm.Schema(
                        type=glm.Type.OBJECT,
                        properties={
                            'route_id':glm.Schema(
                                type=glm.Type.NUMBER,
                                description='The id of the route, e.g. 3, 67.'),
                            'var_id':glm.Schema(
                                type=glm.Type.NUMBER,
                                description='The id of the var, e.g. 1, 2.'),
                            'var_name':glm.Schema(
                                type=glm.Type.STRING,
                                description='The name of the route, e.g. Lượt đi: Bến Thành - Thạnh Lộc, Lượt về: Tân Quy - Bến xe An Sương or \
                                Phú Mỹ Hưng (khi H) - Quận 1. \
                                Any typos, extra spaces, etc must be fixed when parsing. Example: "Sân bay tânn Sơn Nhứt" -> "Sân bay Tân Sơn Nhất"'),
                            'var_short_name':glm.Schema(
                                type=glm.Type.STRING,
                                description='The short name of the route, e.g. Quận 1, Tân Quy.'),
                            'route_no':glm.Schema(
                                type=glm.Type.STRING,
                                description='The number of the route, e.g. 03, 05, 67.'),
                            'start_stop':glm.Schema(
                                type=glm.Type.STRING,
                                description='The start stop of the route, e.g. Bến xe buýt Sài Gòn, Đại học Quốc Gia.'),
                            'end_stop':glm.Schema(
                                type=glm.Type.STRING,
                                description='The end stop of the route, e.g. Bến xe buýt Sài Gòn.'),
                            'distance':glm.Schema(
                                type=glm.Type.NUMBER,
                                description='The distance of the route, must be converted to meters when parsing.'),
                            'outbound':glm.Schema(
                                type=glm.Type.BOOLEAN,
                                description='The outbound of the route, e.g. True or False.'),
                            'running_time':glm.Schema(
                                type=glm.Type.NUMBER,
                                description='The running time of the route, must be converted to minutes when parsing.'),  
                            'route_type':glm.Schema(
                                type=glm.Type.STRING,
                                description='The type of the route.')
                        },
                    )
                ),
                glm.FunctionDeclaration(
                    name='search_paths_by',
                    description="Returns a list of paths satisfying a given criteria.",
                    parameters=glm.Schema(
                        type=glm.Type.OBJECT,
                        properties={
                            'route_id':glm.Schema(
                                type=glm.Type.NUMBER,
                                description='The id of the route, e.g. 3, 67.'),
                            'var_id':glm.Schema(
                                type=glm.Type.NUMBER,
                                description='The id of the var, e.g. 1, 2.'),
                        },
                    )
                )

            ])
        self.model = genai.GenerativeModel('gemini-1.5-pro-latest', tools=self.query_tools)
        self.routevar_query = RouteVarQuery()
        self.stop_query = StopQuery()
        self.path_query = PathQuery()
        self.routevar_query.load_data(routevar_fp)
        self.stop_query.load_data(stop_fp)
        self.path_query.load_data(path_fp)


    def start_chat(self):
        self.chat = self.model.start_chat()

        print("Chat started! Enter your query or type 'exit' to quit.")
        print() 

        while True:
            user_input = input('User: ')
            if user_input == 'exit':
                break
            response = self.chat.send_message(user_input)
            output = response.candidates[0].content.parts[0]

            if 'text' in output:
                print("Model: ", response.candidates[0].content.parts[0].text)
                print()
                continue
            
            fc = output.function_call
            print("Model: ")
            print()
            print(f"Function called: {fc.name}")
            print(f"Arguments: ")
            for key, value in fc.args.items():
                print(f"{key} = {value}")

            print()
            print("Result:")
            if fc.name == 'search_stops_by':
                query_list = getattr(self.stop_query, fc.name)(**fc.args)
                for stop in query_list:
                    print('+', stop)
                    print()
            elif fc.name == 'search_routes_by':
                query_list = getattr(self.routevar_query, fc.name)(**fc.args)
                for routevar in query_list:
                    print("+", routevar)
                    print()
            elif fc.name == 'search_paths_by':
                query_list = getattr(self.path_query, fc.name)(**fc.args)
                for path in query_list:
                    print("+", path)
                    print()
            

        print("Chat ended.")


llm = LLM_query(GOOGLE_API_KEY, './data/vars.json', './data/stops.json', './data/paths.json')
llm.start_chat()


    