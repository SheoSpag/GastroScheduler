from app.models.day_settings import DaySettings

def test_create_branch(client, db):
    company_data = {"name": "Test Company"}
    client.post("/company/", json=company_data)
    branch_data = {"address": "Fake Street 123", "company_id": 1}
    
    response = client.post("/branch/", json=branch_data)

    assert response.status_code == 201
    
    branch = response.json()
    
    assert branch["address"] == "Fake Street 123"
    assert branch["company_id"] == 1
    assert branch["id"] == 1

    day_settings = db.query(DaySettings).filter(DaySettings.branch_id == 1).all()
    
    assert len(day_settings) == 7
    
def test_fail_create_branch(client, db):    
    branch_data = {"address": "Fake Street 123", "company_id": 1}
    
    response = client.post("/branch/", json=branch_data)

    assert response.status_code == 404    
    
def test_update_branch(client):
    company_data = {"name": "Test Company"}
    company_data2 = {"name": "Test Company"}
    client.post("/company/", json=company_data)
    client.post("/company/", json=company_data2)
    branch_data = {"address": "Fake Street 123", "company_id": 1}
    client.post("/branch/", json=branch_data)

    new_data = {"address": "Real Street 321", "company_id": 2}
    response = client.patch("/branch/1", json=new_data)
    
    assert response.status_code == 200
    branch = response.json()
    assert branch["company_id"] == 2
    assert branch["address"] == "Real Street 321"

def test_fail_update_branch(client): 
    company_data = {"name": "Test Company"}
    client.post("/company/", json=company_data)
    
    branch_data = {"address": "Fake Street 123", "company_id": 1}
    client.post("/branch/", json=branch_data)
    
    new_data = {"address": "Real Street 321", "company_id": 2}
    response = client.patch("/branch/1", json=new_data)
    
    assert response.status_code == 404
    
def test_get_branch(client):
    company_data = {"name": "Test Company"}
    client.post("/company/", json=company_data)
    branch_data = {"address": "Fake Street 123", "company_id": 1}
    client.post("/branch/", json=branch_data)
    
    response = client.get("/branch/1")
    
    assert response.status_code == 200
    branch = response.json()
    
    assert branch["company_id"] == 1
    assert branch["address"] == "Fake Street 123"
    
def test_fail_get_branch(client):
    response = client.get("/branch/1000")
    
    assert response.status_code == 404
    

def test_delete_branch(client):
    company_data = {"name": "Test Company"}
    client.post("/company/", json=company_data)
    branch_data = {"address": "Fake Street 123", "company_id": 1}
    client.post("/branch/", json=branch_data)

    response = client.delete("/branch/1")
    
    assert response.status_code == 200
    
    branch = response.json()
    
    assert branch["company_id"] == 1
    assert branch["address"] == "Fake Street 123"
    
    same_branch = client.get("/branch/1")
    
    assert same_branch.status_code == 404

def test_fail_delete_branch(client):
    response = client.delete("/branch/1000")
    
    assert response.status_code == 404
    
def test_get_all_branches(client):
    response = client.get("/branch/")
    
    assert response.status_code == 204
    
    company_data = {"name": "Test Company"}
    client.post("/company/", json=company_data)
    branch_data = {"address": "Fake Street 123", "company_id": 1}
    client.post("/branch/", json=branch_data)
    branch_data = {"address": "Fake Street 456", "company_id": 1}
    client.post("/branch/", json=branch_data)
    
    response = client.get("/branch/")

    assert response.status_code == 200

    branches = response.json()
    
    assert len(branches) == 2
    
    #Branch areas
    
    #Branch locks

    #Branch employees
    
    
    