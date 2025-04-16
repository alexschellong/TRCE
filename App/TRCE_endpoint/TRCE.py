from fastapi import APIRouter, HTTPException, Query
from typing import Annotated
from .TRCEFunctions import *
from .TRCESchemas import TRCERequest
from .TRCEExceptions import LargeDistanceException
import asyncio
from geopy import distance

# Root URL for the API  (mocked)
root_url = 'https://apiapi.free.beeceptor.com/api/v1/locations'
router = APIRouter()

# Uses pydantic schema for type checking and input validation 
@router.get("/api/v1/transportation-request-cost")
async def get_transportation_request_cost(
    trce_request: Annotated[TRCERequest, Query()]
):
    """
    Calculates the total price and price breakdown of a transportation request. 
    Integrates with the API to fetch location related data required to calculate the prices.

    Args:
        trce_request (TRCERequest): The request object containing:
        location slug, cart value and user's longtitude and latitude

    Returns:
        JSON containing:
        the total cost, small request surcharge, cart value, and transportation cost and distance

    Raises:
        HTTPException: If the user is too far from the location or if there's a server error.
    """

    try:

        # Asynchronously makes calls to the API and retrieves necessary data
        (location_lon, location_lat), (request_minimum_no_surcharge, base_cost, distance_ranges) = await asyncio.gather(
            API_call_static(root_url, trce_request.location_slug),
            API_call_dynamic(root_url, trce_request.location_slug)
        )

        small_request_surcharge : int = max(0, request_minimum_no_surcharge - trce_request.cart_value)

        # Gets the distance between the chosen location and the user
        distance_val : int = distance.distance((trce_request.user_lat,trce_request.user_lon),(location_lat,location_lon)).m
        
        transportation_cost : int = estimate_transportation_cost(distance_ranges,distance_val,base_cost)

        # In case the distance_val would be too high, estimate_transportation_cost returns None and API returns 400
        if transportation_cost is None:
            raise LargeDistanceException
        
        else:

            total_price : int = trce_request.cart_value + small_request_surcharge + transportation_cost

            return {
                "total_price": total_price,
                "small_request_surcharge": small_request_surcharge,
                "cart_value": trce_request.cart_value,
                "transportation": {
                    "cost": transportation_cost,
                    "distance": distance_val
                }
            }
        
    except LargeDistanceException:
        raise HTTPException(status_code=400, detail=f"user is too far away from the location: {trce_request.location_slug}")
    except:
        raise HTTPException(status_code=500) 


