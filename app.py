from fastapi import FastAPI
from contextlib import asynccontextmanager
import osmnx as ox
from schemas import RouteModel
import networkx as nx


global G


@asynccontextmanager
async def lifespan(app: FastAPI):
    from utils import load_graph

    global G
    G = load_graph()

    yield


app = FastAPI(lifespan=lifespan)


# get the route
@app.post("/route")
async def get_route(route: RouteModel):
    from utils import cost_fun

    print(route)

    start = ox.distance.nearest_nodes(G, X=route.begin.long, Y=route.begin.lat)
    end = ox.distance.nearest_nodes(G, X=route.dest.long, Y=route.dest.lat)

    route = nx.shortest_path(G, source=start, target=end, weight=cost_fun)

    route = [{"coord": (G.nodes[node]['y'], G.nodes[node]['x']),
              "bus_number": G.nodes[node].get('bus_number', None)} for node in route]

    return route
