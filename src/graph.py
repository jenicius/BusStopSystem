import json
from convert import Converter
import heapq
import math
from itertools import count
from heapq import heappop, heappush
from geo import geojson
from fibonacci_heap import FibonacciHeap
import sys

conv = Converter()

def build_graph(G, route_vars, paths):
    with open('data/stops.json', encoding='utf-8') as file:   
        for line in file:

            obj = json.loads(line)
            route_id = int(obj['RouteId'])
            var_id = int(obj['RouteVarId'])
            path = paths[route_id, var_id]
            x, y = conv.convert(path.get_lng(), path.get_lat())
            stop_list = json.loads(line)['Stops']
            running_time = route_vars[route_id, var_id].get_running_time()
            total_dist = route_vars[route_id, var_id].get_distance()

            match = []
            for stop in stop_list:
                stop_x, stop_y = conv.convert(stop['Lng'], stop['Lat'])
                if not match:
                    match_ind = 0
                else:
                    match_ind = match[-1]+1

                distance = conv.cartesian_distance(stop_x, stop_y, x[match_ind], y[match_ind])

                for i in range(match_ind+1, len(x)):
                    dist = conv.cartesian_distance(stop_x, stop_y, x[i], y[i])
                    if distance > dist:
                        distance = dist
                        match_ind = i
                
                match.append(match_ind)

            distance = 0
            dist = 0
            prev_stop_index = 0
            for i in range(len(x)-1):
                distance += conv.cartesian_distance(x[i], y[i], x[i+1], y[i+1])
                dist += conv.cartesian_distance(x[i], y[i], x[i+1], y[i+1])
            
                #Stop check:
                if match[prev_stop_index+1] == i+1:
                    
                    G.add_edge(stop_list[prev_stop_index]['StopId'], stop_list[prev_stop_index+1]['StopId'], 
                               key = (route_id, var_id),
                               Distance = dist, 
                               Time = running_time*dist/total_dist)
                    
                    G.nodes[stop_list[prev_stop_index]['StopId']]['x'] = x[i]
                    G.nodes[stop_list[prev_stop_index]['StopId']]['y'] = y[i]
                    G.nodes[stop_list[prev_stop_index+1]['StopId']]['x'] = x[i+1]
                    G.nodes[stop_list[prev_stop_index+1]['StopId']]['y'] = y[i+1]   
                    
                    dist = 0
                    prev_stop_index += 1
                    if prev_stop_index == len(stop_list)-1:
                        break


def dijkstra_one_dest_shortest_path(G, start_stop, end_stop):
    distances = {node: float('inf') for node in G.nodes()}
    distances[start_stop] = 0
    
    priority_queue = [(0, start_stop)]
    predecessors = {node: None for node in G.nodes()}
    
    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        
        if current_node == end_stop:
            break
        
        for neighbor in G.neighbors(current_node):
            for edge_key, edge_data in G[current_node][neighbor].items():
                weight = edge_data['Time']
                distance = current_distance + weight
                
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    predecessors[neighbor] = (current_node, edge_key)
                   
                    heapq.heappush(priority_queue, (distance, neighbor))

    # shortest_path = []
    # node = end_stop
    # while node is not None:
    #     shortest_path.append(node)
    #     node = predecessors[node][0] if predecessors[node] is not None else None

    # shortest_path.reverse()
    return predecessors, distances[end_stop]


def dijkstra_shortest_path(G, start_stop):
    distances = {node: float('inf') for node in G.nodes()}
    distances[start_stop] = 0
    
    predecessors = {}
    
    # Initialize a priority queue with the start stop
    priority_queue = [(0, start_stop)]
    
    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        
        # Iterate over all neighbors of the current node
        for neighbor in G.neighbors(current_node):
            edges = G[current_node][neighbor]
            key = min(edges, key=lambda x: edges[x]['Time'])
            weight = edges[key]['Time']
    
            distance = current_distance + weight
            
            # Update distance and predecessor if shorter path is found
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                predecessors[neighbor] = (current_node, key)
                
                heapq.heappush(priority_queue, (distance, neighbor))

    return distances, predecessors


def floyd_warshall(G):
    distances = {}
    predecessors = {}
    
    # Initialize distances and predecessors
    for u in G.nodes():
        distances[u] = {}
        predecessors[u] = {}
        for v in G.nodes():
            distances[u][v] = float('inf')
            predecessors[u][v] = None
    
    # Set initial distances and predecessors based on edge weights
    for u, v, data in G.edges(data=True):
        distances[u][v] = data['Time']
        predecessors[u][v] = u
    
    # Update distances and predecessors using Floyd-Warshall algorithm
    for k in G.nodes():
        for i in G.nodes():
            for j in G.nodes():
                if distances[i][j] > distances[i][k] + distances[k][j]:
                    distances[i][j] = distances[i][k] + distances[k][j]
                    predecessors[i][j] = predecessors[k][j]
    
    return distances, predecessors


def dijkstra_shortest_path_fibo(G, start_stop):
    distances = {node: float('inf') for node in G.nodes()}
    distances[start_stop] = 0
    
    priority_queue = FibonacciHeap()
    node_handles = {}
    predecessors = {node: None for node in G.nodes()}
    
    for node in G.nodes():
        node_handles[node] = priority_queue.insert(distances[node], node)
    
    while not priority_queue.is_empty():
        current_node = priority_queue.extract_min().value
        
        for neighbor in G.neighbors(current_node):
            edges = G[current_node][neighbor]
            edge_key = min(edges, key=lambda x: edges[x]['Time'])
            weight = edges[edge_key]['Time']
            distance = distances[current_node] + weight
            
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                predecessors[neighbor] = (current_node, neighbor, edge_key)
                
                priority_queue.decrease_key(node_handles[neighbor], distance)

    return predecessors, distances


def dijkstra_shortest_path_edge(G, start_stop, end_stop):
    distances = {node: float('inf') for node in G.nodes()}
    distances[start_stop] = 0
    
    priority_queue = [(0, start_stop)]
    predecessors = {node: None for node in G.nodes()}
    
    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        
        if current_node == end_stop:
            break
        
        for neighbor in G.neighbors(current_node):
            edges = G[current_node][neighbor]
            key = min(edges, key=lambda x: edges[x]['Time'])
            weight = edges[key]['Time']
            distance = current_distance + weight
            
            # Update distance and predecessor if shorter path is found
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                predecessors[neighbor] = (current_node, key)
                
                heapq.heappush(priority_queue, (distance, neighbor))

    shortest_edge_path = []
    node = end_stop
    while node is not None:
        if predecessors[node] is not None:
            shortest_edge_path.append(predecessors[node])
        node = predecessors[node][0] if predecessors[node] is not None else None

    shortest_edge_path.reverse()
    return shortest_edge_path, distances[end_stop]


def export_path(file_path, G, start_stop, end_stop, stops, paths):
    shortest_path_edge, _ = dijkstra_shortest_path_edge(G, start_stop, end_stop)
    full_path = []
    for edge in shortest_path_edge:
        route_id, var_id = edge[2]
        start_x, start_y = conv.convert(stops[edge[0]].get_lng(), stops[edge[0]].get_lat())
        end_x, end_y = conv.convert(stops[edge[1]].get_lng(), stops[edge[1]].get_lat())

        lat, lng = paths[route_id, var_id].get_lat(), paths[route_id, var_id].get_lng()
        x, y = conv.convert(lng, lat)
        closest_start = 0
        dist1 = conv.cartesian_distance(x[0], y[0], start_x, start_y)
        closest_end = 0
        dist2 = conv.cartesian_distance(x[0], y[0], end_x, end_y)

        for i in range(1, len(x)):
            dist = conv.cartesian_distance(x[i], y[i], start_x, start_y)
            if dist < dist1:
                dist1 = dist
                closest_start = i
            dist = conv.cartesian_distance(x[i], y[i], end_x, end_y)
            if dist < dist2:
                dist2 = dist
                closest_end = i

        for i in range(closest_start, closest_end+1):
            full_path.append((lng[i], lat[i]))
    
    obj = {
      "type": "Feature",
      "properties": {},
      "geometry": {
        "coordinates": full_path,
        "type": "LineString"
      }
    }
    geojson(file_path, [obj])


def all_pair_shortest_paths(G):
    predecessors = {}
    distances = {}

    for node in G.nodes():
        predecessors[node], distances[node] = dijkstra_shortest_path(G, node)
    
    return predecessors, distances


def all_pair_shortest_paths_fibo(G):
    predecessors = {}
    distances = {}

    for node in G.nodes():
        predecessors[node], distances[node] = dijkstra_shortest_path_fibo(G, node)
    
    return predecessors, distances


def a_star(G, start_stop, end_stop):
    distances = {node: float('inf') for node in G.nodes()}
    distances[start_stop] = 0
    
    priority_queue = [(0, start_stop)]
    predecessors = {node: None for node in G.nodes()}
    
    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        
        if current_node == end_stop:
            break
        
        for neighbor in G.neighbors(current_node):
            edges = G[current_node][neighbor]
            key = min(edges, key=lambda x: edges[x]['Time'])
            weight = edges[key]['Time']
            distance = current_distance + weight
            
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                predecessors[neighbor] = (current_node, key)
                
                heapq.heappush(priority_queue, (distance + heuristic(G, neighbor, end_stop)-heuristic(G, current_node, end_stop), neighbor))

    true_distance = 0
    node = end_stop
    while node is not None:
        if predecessors[node] is not None:
            true_distance += G[predecessors[node][0]][node][predecessors[node][1]]['Time']
        node = predecessors[node][0] if predecessors[node] is not None else None
    
    return predecessors, true_distance


def heuristic(G, node, end_stop):
    # return conv.cartesian_distance(G.nodes[node]['x'], G.nodes[node]['y'], G.nodes[end_stop]['x'], G.nodes[end_stop]['y'])
    return conv.manhattan_distance(G.nodes[node]['x'], G.nodes[node]['y'], G.nodes[end_stop]['x'], G.nodes[end_stop]['y'])

def stress_centrality(G, endpoint = False):
    stress = dict.fromkeys(G, 0.0)  
    for s in G:

        S, P, sigma, _ = stress_dijkstra(G, s)
        if endpoint:
            stress, _ = accumulate_endpoint(stress, S, P, sigma, s)
        else:
            stress, _ = accumulate(stress, S, P, sigma, s)

    return stress


def stress_centrality_fibo(G, endpoint = False):
    stress = dict.fromkeys(G, 0.0)  
    for s in G:

        S, P, sigma, _ = stress_dijkstra_fibo(G, s)
        if endpoint:
            stress, _ = accumulate_endpoint(stress, S, P, sigma, s)
        else:
            stress, _ = accumulate(stress, S, P, sigma, s)

    return stress


def stress_dijkstra(G, s):
    S = []
    P = {}
    for v in G:
        P[v] = []
    sigma = dict.fromkeys(G, 0)
    D = {}
    sigma[s] = 1
    seen = {s: 0}
    Q = []  
    heappush(Q, (0, s, s))
    while Q:
        (dist, pred, v) = heappop(Q)
        if v in D:
            continue 
        sigma[v] += sigma[pred]  
        S.append(v)
        D[v] = dist
        for w in G.neighbors(v):
            edges = G[v][w]
            key = min(edges, key=lambda x: edges[x]['Time'])
            weight = edges[key]['Time']
            vw_dist = dist + weight
            if w not in D and (w not in seen or vw_dist < seen[w]):
                seen[w] = vw_dist
                heappush(Q, (vw_dist, v, w))
                sigma[w] = 0
                P[w] = [v]
            elif vw_dist == seen[w]:
                sigma[w] += sigma[v]
                P[w].append(v)
            
    return S, P, sigma, D


def stress_dijkstra_fibo(G, s):
    S = []
    P = {}
    for v in G:
        P[v] = []
    sigma = dict.fromkeys(G, 0)
    D = {}
    sigma[s] = 1
    seen = {s: 0}
    Q = FibonacciHeap()
    node_handles = {}
    node_handles[s] = Q.insert(0, s)
    while not Q.is_empty():
        current_node = Q.extract_min().value
        if current_node in D:
            continue
        S.append(current_node)
        D[current_node] = seen[current_node]
        for neighbor in G.neighbors(current_node):
            edges = G[current_node][neighbor]
            key = min(edges, key=lambda x: edges[x]['Time'])
            weight = edges[key]['Time']
            vw_dist = seen[current_node] + weight

            if neighbor not in D and (neighbor not in seen or vw_dist < seen[neighbor]):
                seen[neighbor] = vw_dist
                node_handles[neighbor] = Q.insert(vw_dist, neighbor)
                sigma[neighbor] = 0
                P[neighbor] = [current_node]
            elif vw_dist == seen[neighbor]:
                sigma[neighbor] += sigma[current_node]
                P[neighbor].append(current_node)
    
    return S, P, sigma, D


def accumulate(stress, S, P, sigma, s):
    delta = dict.fromkeys(S, 0)
    while S:
        w = S.pop()
        for v in P[w]:
            delta[v] += 1 + delta[w]
        if w != s:
            stress[w] += sigma[w]*delta[w]
    return stress, delta


def accumulate_endpoint(stress, S, P, sigma, s):
    delta = dict.fromkeys(S, 0)
    stress[s] += len(S)-1
    while S:
        w = S.pop()
        for v in P[w]:
            delta[v] += 1 + delta[w]
        if w != s:
            stress[w] += sigma[w]*delta[w]
    return stress, delta


def top_k(file_path, G, stops, k=10, endpoint=False):

    load_centrality = stress_centrality(G, endpoint=endpoint)
    sorted_nodes = sorted(load_centrality.items(), key=lambda x: x[1], reverse=True)

    top_nodes = sorted_nodes[:k]

    with open(file_path, 'w', encoding='utf-8') as file:
        for node, _ in top_nodes:
            stop = stops[node]
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

def top_k_fibo(file_path, G, stops, k=10, endpoint=False):

    load_centrality = stress_centrality_fibo(G, endpoint=endpoint)
    sorted_nodes = sorted(load_centrality.items(), key=lambda x: x[1], reverse=True)

    top_nodes = sorted_nodes[:k]

    with open(file_path, 'w', encoding='utf-8') as file:
        for node, _ in top_nodes:
            stop = stops[node]
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
        
        
        





    


