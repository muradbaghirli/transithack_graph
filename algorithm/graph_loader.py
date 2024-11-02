import osmnx as ox
import networkx as nx
import random

def load_graph(city="Baku, Azerbaijan", network_type="walk"):
    """Load the graph for a specific city and network type."""
    G = ox.graph_from_place(city, network_type=network_type)

    # Randomly assign slope and ramp values to edges
    for u, v, data in G.edges(data=True):
        data['slope'] = random.uniform(0, 10)
        data['ramp'] = random.choice([True, False])
    
    # Add weights based on slope and ramp data
    for u, v, data in G.edges(data=True):
        data['weight'] = get_weight(u, v, data)
    
    return G

def get_weight(u, v, data):
    """Calculate the weight based on slope and ramp availability."""
    slope_weight = 1 + data['slope'] / 10
    ramp_weight = 0 if data['ramp'] else 2
    return slope_weight + ramp_weight
