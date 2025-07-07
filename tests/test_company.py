from app.models.company import Company

def test_create_company(client):
    data = {"name": "Test Company"}
    response = client.post("/company/", json=data)
    assert response.status_code == 201

def test_get_companies(client):
    data = {"name": "Test Company"}
    client.post("/company/", json=data)
    client.post("/company/", json=data)
    
    response = client.get("/company/")
    assert response.status_code == 200

    companies = response.json()
    assert isinstance(companies, list)
    assert len(companies) == 2
    
def test_get_one_company(client):
    data = {"name": "Test Company"}
    client.post("/company/", json=data)
    
    response = client.get("/company/1")
    
    assert response.status_code == 200
    companies = response.json()
    assert companies["id"] == 1
    assert companies["name"] == "Test Company"

    
def test_update_company(client):    
    data = {"name": "Test Company"}
    client.post("/company/", json=data)
    
    new_data = {"name": "Test Company 1"}
    response = client.put("/company/1", json=new_data)
    
    assert response.status_code == 200
    company = response.json()
    assert company["id"] == 1
    assert company["name"] == "Test Company 1"
    
def test_delete_company(client, db):
    data = {"name": "Test Company"}
    client.post("/company/", json=data)
    
    response = client.delete("/company/1")
    
    assert response.status_code == 200
    company = response.json()
    
    assert company["id"] == 1
    assert company["name"] == "Test Company"
    
    response = client.delete("/company/1")
    
    assert response.status_code == 404
    
    
    
    
    
    

