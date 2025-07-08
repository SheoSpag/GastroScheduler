def test_get_one_day_setting(client):
    company_data = {"name": "Test Company"}
    client.post("/company/", json=company_data)
    branch_data = {"address": "Fake Street 123", "company_id": 1}
    
    response = client.get("/branch/1/settings/1")
    
    assert response.status_code == 404
    
    client.post("/branch/", json=branch_data)
    
    response = client.get("/branch/1/settings/1")
    
    assert response.status_code == 200
    
def  test_get_branch_all_days_settings(client):
    company_data = {"name": "Test Company"}
    client.post("/company/", json=company_data)
    branch_data = {"address": "Fake Street 123", "company_id": 1}
    client.post("/branch/", json=branch_data)
    
    response = client.get("/branch/1/settings/")
    
    assert response.status_code == 200
    
    settings = response.json()
    
    assert len(settings) == 7
    
def test_update_day_settings(client):
    company_data = {"name": "Test Company"}
    client.post("/company/", json=company_data)
    branch_data = {"address": "Fake Street 123", "company_id": 1}
    client.post("/branch/", json=branch_data)
    
    new_settings = {"closing": "18:00:00", "morning_intensity": 10}
    
    response = client.patch("/branch/10/settings/1", json=new_settings)
    
    assert response.status_code == 404
    
    response = client.patch("/branch/1/settings/1", json=new_settings)
    
    assert response.status_code == 200
    
    assert response.json()["closing"] == "18:00:00"
    
    
