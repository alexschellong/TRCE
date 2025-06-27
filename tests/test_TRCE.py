from fastapi.testclient import TestClient
from ..App.main import app
from ..App.TRCE_endpoint.TRCEFunctions import estimate_transportation_cost
import pytest

client = TestClient(app)

# location slug input tests
def test_location_slug_correct():
    location_slug = "helsinki"
    response = client.get("/api/v1/transportation-request-cost/", 
                         params={"location_slug": location_slug, 
                                "cart_value": 20, 
                                "user_lat": 60.170, 
                                "user_lon": 24.92})
    assert response.status_code == 200

def test_location_slug_empty():
    location_slug = ""
    response = client.get("/api/v1/transportation-request-cost/", 
                         params={"location_slug": location_slug, 
                                "cart_value": 20, 
                                "user_lat": 60.170, 
                                "user_lon": 24.92})
    assert response.status_code == 422

def test_location_slug_too_long():
    location_slug = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
    response = client.get("/api/v1/transportation-request-cost/", 
                         params={"location_slug": location_slug, 
                                "cart_value": 20, 
                                "user_lat": 60.170, 
                                "user_lon": 24.92})
    assert response.status_code == 422


@pytest.mark.parametrize("input_val, expected_output",[("adad@!@!@!@", 422), ("", 422)])
def test_cart_value_wrong_type(input_val,expected_output):
    cart_value = input_val
    response = client.get("/api/v1/transportation-request-cost/", 
                         params={"location_slug": "helsinki", 
                                "cart_value": cart_value, 
                                "user_lat": 60.170, 
                                "user_lon": 24.92})
    assert response.status_code == expected_output

# cart value input tests
def test_cart_value_zero():
    cart_value = 0
    response = client.get("/api/v1/transportation-request-cost/", 
                         params={"location_slug": "helsinki", 
                                "cart_value": cart_value, 
                                "user_lat": 60.170, 
                                "user_lon": 24.92})
    assert response.status_code == 422

# user latitude input tests
@pytest.mark.parametrize("input_val, expected_output",[("adad@!@!@!@", 422), ("", 422)])
def test_user_lat_wrong_type(input_val,expected_output):
    user_lat = input_val
    response = client.get("/api/v1/transportation-request-cost/", 
                         params={"location_slug": "helsinki", 
                                "cart_value": 20, 
                                "user_lat": user_lat, 
                                "user_lon": 24.92})
    assert response.status_code == expected_output

@pytest.mark.parametrize("input_val, expected_output",[(-91, 422), (91, 422)])
def test_user_lat_outside_range(input_val,expected_output):
    user_lat = input_val
    response = client.get("/api/v1/transportation-request-cost/", 
                         params={"location_slug": "helsinki", 
                                "cart_value": 20, 
                                "user_lat": user_lat, 
                                "user_lon": 24.92})
    assert response.status_code == expected_output


# user longtitude input tests
@pytest.mark.parametrize("input_val, expected_output",[("adad@!@!@!@", 422), ("", 422)])
def test_user_lon_wrong_type(input_val,expected_output):
    user_lon = input_val
    response = client.get("/api/v1/transportation-request-cost/", 
                         params={"location_slug": "helsinki", 
                                "cart_value": 20, 
                                "user_lat": 60.170, 
                                "user_lon": user_lon})
    assert response.status_code == expected_output

@pytest.mark.parametrize("input_val, expected_output",[(-181, 422), (181, 422)])
def test_user_lon_outside_range(input_val,expected_output):
    user_lon = input_val
    response = client.get("/api/v1/transportation-request-cost/", 
                         params={"location_slug": "helsinki", 
                                "cart_value": 20, 
                                "user_lat": 60.170, 
                                "user_lon": user_lon})
    assert response.status_code == expected_output

# users distance from the location test
def test_user_too_distant():
    user_lat = 60
    user_lon = 24
    response = client.get("/api/v1/transportation-request-cost/", 
                         params={"location_slug": "helsinki", 
                                "cart_value": 20, 
                                "user_lat": user_lat, 
                                "user_lon": user_lon})
    assert response.status_code == 400 

# test for highest transportation cost
def test_high_transportation_cost():
    distance_ranges =  [{ "min": 0, "max": 500, "a": 0, "b": 0.0, "flag": None},
                        { "min": 500, "max": 1000, "a": 100, "b": 0.0, "flag": None},
                        { "min": 1000, "max": 1500, "a": 200, "b": 0.0, "flag": None},
                        { "min": 1500, "max": 2000, "a": 200, "b": 1.0, "flag": None},
                        { "min": 2000, "max": 0, "a": 0, "b": 0.0, "flag": None}]           
    assert estimate_transportation_cost(distance_ranges, 1999, 0) == 400

# test for lowest transportation cost
def test_low_transportation_cost():
    distance_ranges =  [{ "min": 0, "max": 500, "a": 0, "b": 0.0, "flag": None},
                        { "min": 500, "max": 1000, "a": 100, "b": 0.0, "flag": None},
                        { "min": 1000, "max": 1500, "a": 200, "b": 0.0, "flag": None},
                        { "min": 1500, "max": 2000, "a": 200, "b": 1.0, "flag": None},
                        { "min": 2000, "max": 0, "a": 0, "b": 0.0, "flag": None}]           
    assert estimate_transportation_cost(distance_ranges, 0, 0) == 0
