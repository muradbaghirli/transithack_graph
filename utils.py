import osmnx as ox
import os
from logging_config import uvicorn_logger


def add_bus_routes(G, bus_nodes_file = "bus_nodes.json"):
    import json
    with open(bus_nodes_file) as f:
        bus_routes = json.load(f)

    for bus_route in bus_routes:
        bus_number = bus_route["number"]
        bus_nodes = bus_route["nodes"]
        
        for i in range(len(bus_nodes)-1):
            u = bus_nodes[i] 
            v = bus_nodes[i+1]
            edge_data = G.get_edge_data(u, v)
            try:
                edge_data[0]["bus_edge"] = True
            except:
                print(f"Edge {u} - {v} not found")
                print(edge_data)
                raise Exception(f"Edge {u} - {v} not found")


        for node in bus_nodes:
            G.nodes[node]["bus_number"] = bus_number



def add_elevations(G):
    import requests

    url_get = "http://10.33.141.3:8080/api/v1/edges"  
    response = requests.get(url_get)

    if response.status_code == 200:
        data = response.json()  
    else:
        raise Exception(f"Request failed with status code: {response.status_code}")
        
    for item in data:
        u = item["source"]["id"]
        v = item["target"]["id"]
        edge_data = G.get_edge_data(u, v)
        edge_data[0]["slope"] = item["slope"]  
            
    return G


def load_graph(city="Baku, Azerbaijan", network_type="walk"):
    """Load the graph for a specific city and network type, save it if it doesn't exist."""
    file_path = os.path.join("data", f"{city.replace(',', '_').replace(' ','')}_{network_type}.graphml")
    if os.path.exists(file_path):
        # print(f"Loading graph from {file_path}")
        G = ox.load_graphml(file_path)
        uvicorn_logger.info(f"Loaded graph from {file_path}")
    else:
        # print(f"Creating graph for {city} with network type {network_type}")
        G = ox.graph_from_place(city, network_type=network_type)
        uvicorn_logger.info(f"Created graph for {city} with network type {network_type}")
        ox.save_graphml(G, file_path)

    add_elevations(G)
    uvicorn_logger.info("Added bus routes")
    add_bus_routes(G)
    uvicorn_logger.info("Added elevations")

    
    return G





def cost_fun(u, v, d):
    """
    Cost function that calculates traversal cost based on length, slope, and bus accessibility.

    :param u: The starting node ID.
    :param v: The ending node ID.
    :param d: The edge dictionary containing attributes such as 'length', 'slope', and 'bus_access'.
    :return: The computed traversal cost, or None if the edge is impassable.
    """


    # Extract necessary attributes
    length = d[0]['length']    
    slope = d[0].get('slope', 0)        # Check if slope is available   
    bus_access = d[0].get('bus_edge', False)  # Check if bus accessibility is available
    uphill_max = 0.15                 # Maximum allowable uphill slope
    downhill_max = 0.15               # Maximum allowable downhill slope


    # If bus accessibility is available, return a very low cost to prioritize this path
    if bus_access:
        return 1e-9  # Smallest weight to favor bus-accessible routes
    
    # Check if slope is within acceptable limits for accessibility
    if slope > uphill_max or slope < -downhill_max:
        return None  # Impassable due to slope

    if slope > 0:
        time_cost = length * (1 + slope)

    else:
        time_cost = length * (1 - slope)


    return time_cost
