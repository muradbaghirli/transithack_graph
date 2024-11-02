from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta
import random

app = FastAPI()

# Define a Pydantic model for Stop
class Stop(BaseModel):
    id: int
    name: str
    location: tuple  # (latitude, longitude)

# Define a Pydantic model for Arrival times at each stop
class Arrival(BaseModel):
    stop_id: int
    time_to_arrival: int  # in minutes

# Define a Pydantic model for the Route
class Route(BaseModel):
    id: int
    stops: List[Stop]

# Define a Pydantic model for Bus
class Bus(BaseModel):
    id: int
    number: str
    route: Route

class ActiveBus(BaseModel):
    id: int
    plate_number: str
    bus: Bus
    arrivals: List[Arrival]
    location: tuple  # (latitude, longitude)
    accessible: bool


stops = [
    Stop(id=1, name="Main St", location=(40.748817, -73.985428)),
    Stop(id=2, name="Central Ave", location=(40.748441, -73.985664)),
    Stop(id=3, name="Park St", location=(40.749017, -73.986668))
]

# Mock data for route
route = Route(id=1, stops=stops)

# Mock data for buses
buses = [
    Bus(id=1, number="Bus-100", route=route),
    Bus(id=2, number="Bus-200", route=route)
]

# Mock data for exact buses (instances with plate numbers and dynamic info)
active_buses = [
    ActiveBus(
        id=1,
        plate_number="XYZ-1234",
        bus=buses[0],
        arrivals=[
            Arrival(stop_id=1, time_to_arrival=random.randint(1, 10)),
            Arrival(stop_id=2, time_to_arrival=random.randint(5, 15)),
            Arrival(stop_id=3, time_to_arrival=random.randint(10, 20))
        ],
        location=(40.748817, -73.985428),
        accessible=True
    ),
   
]

@app.get("/active_buses", response_model=List[ActiveBus])
async def get_active_buses():
    """Get all active buses with current location, plate, and arrival times."""
    return active_buses

@app.get("/active_buses/{active_bus_id}", response_model=ActiveBus)
async def get_active_bus(active_bus_id: int):
    """Get a specific active bus instance by ID."""
    for active_bus in active_buses:
        if active_bus.id == active_bus_id:
            return active_bus
    return {"error": "Active bus not found"}


# API Endpoints

@app.get("/buses", response_model=List[Bus])
async def get_buses():
    """Get all bus types with their routes."""
    return buses

@app.get("/buses/{bus_id}", response_model=Bus)
async def get_bus(bus_id: int):
    """Get specific bus type by ID."""
    for bus in buses:
        if bus.id == bus_id:
            return bus
    return {"error": "Bus not found"}


@app.get("/stops", response_model=List[Stop])
async def get_stops():
    """Get all stops."""
    return stops

@app.get("/routes", response_model=List[Route])
async def get_routes():
    """Get all routes."""
    return [route]


