from  httpx import AsyncClient

# Makes an asynchronous API request
async def API_call(root_url: str, location_slug: str, end: str) ->  AsyncClient:
    url = f"{root_url}/{location_slug}/{end}"
    async with AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return response

# Assigns data from API call response to variables
async def API_call_static(root_url: str, location_slug: str) -> tuple[float, float]:
    
    static_response = await API_call(root_url, location_slug, "static")
    coordinates = static_response.json()["location_raw"]["location"]["coordinates"]

    location_lon = coordinates[0]
    location_lat = coordinates[1]

    return location_lon, location_lat

# Assigns data from API call response to variables
async def API_call_dynamic(root_url: str, location_slug: str)  -> tuple[int, int, list]:

    dynamic_response = await API_call(root_url, location_slug, "dynamic")
    transportation_specs = dynamic_response.json()["location_raw"]["transportation_specs"]
    
    order_minimum_no_surcharge = transportation_specs["request_minimum_no_surcharge"]
    base_cost = transportation_specs["transportation_cost"]["base_cost"]
    distance_ranges = transportation_specs["transportation_cost"]["distance_ranges"]

    return order_minimum_no_surcharge, base_cost, distance_ranges


def estimate_transportation_cost(distance_ranges: list, distance : float, base_cost: int) -> int:

    for range in distance_ranges:
        min = range["min"]
        max = range["max"]

        if distance < max:
            if distance >= min and max != 0:
                constant_fee = range["a"]
                distance_multiplier = range["b"]
                transportation_cost = round(constant_fee+(distance_multiplier * distance/10)) + base_cost
                return transportation_cost
            
    return None