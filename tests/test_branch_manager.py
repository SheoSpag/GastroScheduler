def test_register_branch_manager(client):

    branch_manager_data = {
        "email": "email@radom.com",
        "password": "password",
        "branch_id": 1
    }
    
    response = client.post("/branch_manager/register/", json=branch_manager_data)
    
    assert response.status_code == 404
    
    company_data = {"name": "Test Company"}
    client.post("/company/", json=company_data)
    branch_data = {"address": "Fake Street 123", "company_id": 1}
    client.post("/branch/", json=branch_data)
    
    response = client.post("/branch_manager/register/", json=branch_manager_data)
    
    assert response.status_code == 201
    
    response = client.post("/branch_manager/register/", json=branch_manager_data)
    
    assert response.status_code == 400
