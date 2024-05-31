import networkx as nx
from networkx.exception import NetworkXNoPath

from vars import RouteVar
from stops import Stop
from paths import Path
from graph import *
import json
import pickle
import time
import sys
import test

n_bytes = 2**31
max_bytes = 2**31 - 1
data = bytearray(n_bytes)

def load_routevar(route_vars, file_path):
    with open(file_path, 'r', encoding="utf-8") as file:
        for line in file:
            obj = json.loads(line)
            for rv in obj:
                route_var = RouteVar(rv["RouteId"], rv['RouteVarId'], rv['RouteVarName'],
                                rv['RouteVarShortName'], rv['RouteNo'], rv['StartStop'], rv['EndStop'],
                                rv['Distance'], rv['Outbound'], rv['RunningTime'])
                route_vars[rv['RouteId'], rv['RouteVarId']] = route_var


def load_stop(stops, file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            for stop_data in json.loads(line)['Stops']:
                stop = Stop(stop_data['StopId'], stop_data['Code'], stop_data['Name'], stop_data['StopType'],
                            stop_data['Zone'], stop_data['Ward'], stop_data['AddressNo'], stop_data['Street'],
                            stop_data['SupportDisability'], stop_data['Status'], stop_data['Lng'], stop_data['Lat'],  
                            stop_data['Search'], stop_data['Routes'])
                stops[stop_data['StopId']] = stop


def load_path(paths, file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            data = json.loads(line)
            path = Path(lat=data['lat'], lng=data['lng'], route_id=int(data['RouteId']), var_id=int(data['RouteVarId']))
            paths[int(data['RouteId']), int(data['RouteVarId'])] = path



def main(routevar_fp, stop_fp, path_fp):
    
    route_vars = {}
    stops = {}
    paths = {}
    load_routevar(route_vars, routevar_fp)
    load_stop(stops, stop_fp)
    load_path(paths, path_fp)

    start_time = time.time()
    G = nx.MultiDiGraph()
    build_graph(G, route_vars, paths)
    end_time = time.time()
    print('Took', end_time-start_time, 'seconds to build graph')

    print('Number of nodes:', len(G.nodes))

    fastest = float('inf')
    longest = 0
    average = 0
    itr = 0
    average_error = 0
    correct_ratio = 0
    for node in G.nodes:
        itr += 1
        for node2 in G.nodes:
            
            start_time = time.time()
            a_star(G, node, node2)
            end_time = time.time()
            time_taken = end_time - start_time
            average += time_taken

        if itr == 1:     
            break

    print('Took', average, 'seconds to run a_star')
        

    print('Correct ratio:', correct_ratio/(itr))
    print('Average error:', average_error/(itr**2))
    print('Fastest:', fastest)
    print('Longest:', longest)
    print('Average:', average/(itr**2))

            


    # start_time = time.time()
    # top_k('./output/top_k.json', G, stops, k=10)
    # end_time = time.time()

    # print('Took', end_time-start_time, 'seconds to calculate top k')
    
    # start_time = time.time()
    # all_pair_shortest_paths(G)
    # end_time = time.time() 
    # print('Took', end_time-start_time, 'seconds to calculate all pair shortest paths')

    

    # start_time = time.time()
    # top_k_fibo('./output/top_k_fibo.json', G, stops, k=10)
    # end_time = time.time()

    # print('Took', end_time-start_time, 'seconds to calculate top k with fibonacci heap')

    # start_time = time.time()
    # all_pair_shortest_paths_fibo(G)
    # end_time = time.time()
    # print('Took', end_time-start_time, 'seconds to calculate all pair shortest paths with fibonacci heap')

    # fastest = float('inf')
    # longest = 0
    # average = 0
    # itr = 0
    # for node in G.nodes:
    #     start_time = time.time()
    #     dijkstra_shortest_path_fibo(G, node)
    #     end_time = time.time()
    #     time_taken = end_time - start_time
    #     if time_taken < fastest:
    #         fastest = time_taken
    #     if time_taken > longest:
    #         longest = time_taken
    #     average += time_taken
    
    # print('Fastest:', fastest)
    # print('Longest:', longest)
    # print('Average:', average/len(G.nodes))


    # bytes_out = pickle.dumps(shortest_paths)
    # with open('./output/all_pair.pkl', 'wb') as file:
    #     for idx in range(0, len(bytes_out), max_bytes):
    #         file.write(bytes_out[idx:idx+max_bytes])
    
    # bytes_out = pickle.dumps(distances)
    # with open('./output/distances.pkl', 'wb') as file:
    #     for idx in range(0, len(bytes_out), max_bytes):
    #         file.write(bytes_out[idx:idx+max_bytes])

    # start_time = time.time()
    # export_path('./output/geo.json', G, 3, 67, stops, paths)
    # end_time = time.time()
    # print('Took', end_time-start_time, 'seconds to export path')

    # start_time = time.time()
    # top_k('./output/top_k.json', G, stops, k=10)
    # end_time = time.time()
    # print('Took', end_time-start_time, 'seconds to calculate top k')

    
    
if __name__ == '__main__':
    main('./data/vars.json', './data/stops.json', './data/paths.json')
            
         

        


    




