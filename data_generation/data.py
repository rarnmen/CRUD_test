import requests
from random import randrange
from datetime import timedelta
from datetime import datetime as dt
import random
import sys
import math
import random
import math

def random_date(start, end):
    """
    This function will return a random datetime between two datetime 
    objects.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)




def generate_random_coordinates(center_lat, center_lon, radius_km):
    # Convert radius from kilometers to degrees
    radius_in_degrees = radius_km / 111.32  # Approximately 111.32 km per degree latitude

    # Generate a random distance and angle
    distance = random.uniform(0, radius_in_degrees)
    angle = random.uniform(0, 2 * math.pi)

    # Calculate the new latitude and longitude
    delta_lat = distance * math.cos(angle)
    delta_lon = distance * math.sin(angle) / math.cos(math.radians(center_lat))

    new_lat = center_lat + delta_lat
    new_lon = center_lon + delta_lon

    return new_lat, new_lon

# Example usage
center_lat = 10.3910  # Latitude of Cartagena
center_lon = -75.4794  # Longitude of Cartagena
radius_km = 10  # Radius in kilometers

lat, lon = generate_random_coordinates(center_lat, center_lon, radius_km)
nombres = ['Pedro', 'Rafael', 'Juan', 'Andrea']
operador = ['ADHL', 'SERVIENTREGA', 'COORD']

for i in range(100):
    url = f'http://localhost:5000/orden/create'
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        "ubicacion": "{}".format(generate_random_coordinates(center_lat, center_lon, radius_km)),
        "nombre_cliente": nombres[random.randint(0,3)],
        "nombre_operador": operador[random.randint(0,2)],
        "productos": f"[{random.randint(1,56)},{random.randint(1,56)},{random.randint(1,56)}]",
        "created_at": random_date(dt(2024,1,1), dt(2024,5,31)).strftime("%Y-%m-%dT%H:%M:%SZ")
        }
    response = requests.post(url, headers=headers, json=data)
    print(response.text, response.status_code)


