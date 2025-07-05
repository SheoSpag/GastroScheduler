from datetime import time

def test_create_area(client):
    company_data = {"name": "Test Company"}
    client.post("/company/", json=company_data)
    branch_data = {"address": "Fake Street 123", "company_id": 1}
    client.post("/branch/", json=branch_data)
    
    area_data = {
        "opening_time": "00:00:00",
        "closing_time": "00:00:00",
        "minimum_staff": 1,
        "maximum_staff": 5,
        "name": "Bar",
        "branch_id": 1
    }
    
    response = client.post("/area/", json=area_data)

    assert response.status_code == 201
    
    area = response.json()
    
    assert area["branch_id"] == 1

def test_fail_create_Area(client):
    area_data = {
        "opening_time": "00:00:00",
        "closing_time": "00:00:00",
        "minimum_staff": 1,
        "maximum_staff": 5,
        "name": "Bar",
        "branch_id": 1
    }
    
    response = client.post("/area/", json=area_data)
    
    assert response.status_code == 404
    
def test_get_all_areas(client):
    company_data = {"name": "Test Company"}
    client.post("/company/", json=company_data)
    branch_data = {"address": "Fake Street 123", "company_id": 1}
    client.post("/branch/", json=branch_data)
    
    response = client.get("/area/")
    
    assert response.status_code == 204
    
    area_data = {
        "opening_time": "00:00:00",
        "closing_time": "00:00:00",
        "minimum_staff": 1,
        "maximum_staff": 5,
        "name": "Bar",
        "branch_id": 1
    }
    
    client.post("/area/", json=area_data)
    
    area_data = {
        "opening_time": "00:00:00",
        "closing_time": "00:00:00",
        "minimum_staff": 1,
        "maximum_staff": 5,
        "name": "Bar",
        "branch_id": 1
    }
    
    client.post("/area/", json=area_data)
    
    response = client.get("/area/")

    assert response.status_code == 200
    
    areas = response.json()
    
    assert len(areas) == 2
    
def test_get_areas(client):
    company_data = {"name": "Test Company"}
    client.post("/company/", json=company_data)
    branch_data = {"address": "Fake Street 123", "company_id": 1}
    client.post("/branch/", json=branch_data)
    
    response = client.get("/area/")
    
    assert response.status_code == 204
    
    area_data = {
        "opening_time": "00:00:00",
        "closing_time": "00:00:00",
        "minimum_staff": 1,
        "maximum_staff": 5,
        "name": "Bar",
        "branch_id": 1
    }
    
    client.post("/area/", json=area_data)