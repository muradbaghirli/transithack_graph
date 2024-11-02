import osmnx as ox
import networkx as nx
import random
import folium

city = "Baku, Azerbaijan"
G = ox.graph_from_place(city, network_type="all_public")

# Randomly assigning slope and ramp values to edges for demonstration purposes
for u, v, data in G.edges(data=True):
    data['slope'] = random.uniform(0, 10)  
    data['ramp'] = random.choice([True, False])  

def get_weight(u, v, data):
    slope_weight = 1 + data['slope'] / 10  # Higher slope means higher weight -> [between 1 & 2]
    ramp_weight = 0 if data['ramp'] else 2  # Absence of ramp increases weight -> [either 0 or 2]
    return slope_weight + ramp_weight

# Adding weights to each edge
for u, v, data in G.edges(data=True):
    data['weight'] = get_weight(u, v, data)

# Defining start and end points
start = ox.distance.nearest_nodes(G, X=49.851199, Y=40.376313)  # UFAZ
end = ox.distance.nearest_nodes(G, X=49.8224, Y=40.3777) # Central Park

# Computing shortest ACCESIBLE route using Dijkstra's algorithm
route = nx.shortest_path(G, start, end, weight='weight')

# Extract route coordinates for plotting using Folium
route_coords = [(G.nodes[node]['y'], G.nodes[node]['x']) for node in route]

# Define the map centered on a location in Baku
map_baku = folium.Map(location=[40.4093, 49.8671], zoom_start=13)

# Ploting the route on the map
folium.PolyLine(route_coords, color="blue", weight=5).add_to(map_baku)

# Add a custom obstacle marker (for demonstration purposes), should be removed
obstacle_location = (40.3893, 49.8550)
folium.Marker(obstacle_location, popup="Obstacle: No ramp here", icon=folium.Icon(color="red")).add_to(map_baku)

map_baku.save("accessible_route_map.html")
print("Accessible route (node IDs):", route)

