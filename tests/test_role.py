def test_create_role(client):
    company_data = {"name": "Test Company"}
    client.post("/company/", json=company_data)
    branch_data = {"address": "Fake Street 123", "company_id": 1}
    client.post("/branch/", json=branch_data)
    area_data = {"opening_time": "00:00:00","closing_time": "00:00:00","minimum_staff": 1,"maximum_staff": 5,"name": "Bar","branch_id": 1}    
    client.post("/area/", json=area_data)
    
    role_data = {"name": "Bar", "area_id": 200 }
    
    response = client.post("/role/", json=role_data)
    
    assert response.status_code == 404
    
    role_data = {"name": "Bar", "area_id": 1 }
    
    response = client.post("/role/", json=role_data)
    
    assert response.status_code == 201
    
def test_delete_role(client):
    company_data = {"name": "Test Company"}
    client.post("/company/", json=company_data)
    branch_data = {"address": "Fake Street 123", "company_id": 1}
    client.post("/branch/", json=branch_data)
    area_data = {"opening_time": "00:00:00","closing_time": "00:00:00","minimum_staff": 1,"maximum_staff": 5,"name": "Bar","branch_id": 1}    
    client.post("/area/", json=area_data)
    role_data = {"name": "Bar", "area_id": 1 }    
    client.post("/role/", json=role_data)
    
    response = client.delete("/role/100")
    
    assert response.status_code == 404
    
    response = client.delete("/role/1")
    
    assert response.status_code == 200
    
def test_update_role(client):
    company_data = {"name": "Test Company"}
    client.post("/company/", json=company_data)
    branch_data = {"address": "Fake Street 123", "company_id": 1}
    client.post("/branch/", json=branch_data)
    area_data = {"opening_time": "00:00:00","closing_time": "00:00:00","minimum_staff": 1,"maximum_staff": 5,"name": "Bar","branch_id": 1}    
    client.post("/area/", json=area_data)
    role_data = {"name": "Bar", "area_id": 1 }    
    client.post("/role/", json=role_data)
    
    new_data = {"name": "Second Bar"}
    
    response = client.patch("/role/100", json=new_data)
    
    assert response.status_code == 404
    
    response = client.patch("/role/1", json=new_data)
    
    assert response.status_code == 200
    
    updated_role = response.json()
    
    assert updated_role["name"] == "Second Bar"    
    
def test_get_role(client):
    company_data = {"name": "Test Company"}
    client.post("/company/", json=company_data)
    branch_data = {"address": "Fake Street 123", "company_id": 1}
    client.post("/branch/", json=branch_data)
    area_data = {"opening_time": "00:00:00","closing_time": "00:00:00","minimum_staff": 1,"maximum_staff": 5,"name": "Bar","branch_id": 1}    
    client.post("/area/", json=area_data)
    role_data = {"name": "Bar", "area_id": 1 }    
    client.post("/role/", json=role_data)
    
    response = client.get("/role/100")
    
    assert response.status_code == 404
    
    response = client.get("/role/1")
    
    assert response.status_code == 200
    
def test_get_all_roles(client):
    company_data = {"name": "Test Company"}
    client.post("/company/", json=company_data)
    branch_data = {"address": "Fake Street 123", "company_id": 1}
    client.post("/branch/", json=branch_data)
    area_data = {"opening_time": "00:00:00","closing_time": "00:00:00","minimum_staff": 1,"maximum_staff": 5,"name": "Bar","branch_id": 1}    
    client.post("/area/", json=area_data)
    
    response = client.get("/role/")
    
    assert response.status_code == 204
    
    role_data = {"name": "Bar", "area_id": 1 }    
    client.post("/role/", json=role_data)
    client.post("/role/", json=role_data)
    
    response = client.get("/role/")
    
    assert response.status_code == 200
    
    roles = response.json()
    
    assert len(roles) == 2


#Get role employees