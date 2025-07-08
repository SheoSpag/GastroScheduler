from app.models.day_settings import DaySettings

def test_create_branch(client, db):
    branch_data = {"address": "Fake Street 123", "company_id": 1}
    
    response = client.post("/branch/", json=branch_data)

    assert response.status_code == 404   
    
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
    
def test_update_branch(client):
    company_data = {"name": "Test Company"}
    company_data2 = {"name": "Test Company"}
    client.post("/company/", json=company_data)

    branch_data = {"address": "Fake Street 123", "company_id": 1}
    client.post("/branch/", json=branch_data)
    
    new_data = {"address": "Real Street 321", "company_id": 2}
    response = client.patch("/branch/1", json=new_data)
    
    assert response.status_code == 404
    
    client.post("/company/", json=company_data2)

    new_data = {"address": "Real Street 321", "company_id": 2}
    response = client.patch("/branch/1", json=new_data)
    
    assert response.status_code == 200
    branch = response.json()
    assert branch["company_id"] == 2
    assert branch["address"] == "Real Street 321"
    
def test_get_branch(client):
    response = client.get("/branch/1")

    assert response.status_code == 404

    company_data = {"name": "Test Company"}
    client.post("/company/", json=company_data)
    branch_data = {"address": "Fake Street 123", "company_id": 1}
    client.post("/branch/", json=branch_data)
    
    response = client.get("/branch/1")
    
    assert response.status_code == 200
    branch = response.json()

    assert branch["company_id"] == 1
    assert branch["address"] == "Fake Street 123"

def test_delete_branch(client):
    response = client.delete("/branch/1000")
    
    assert response.status_code == 404

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
    
def test_get_branch_areas(client):
    company_data = {"name": "Test Company"}
    client.post("/company/", json=company_data)
    branch_data = {"address": "Fake Street 123", "company_id": 1}
    response = client.post("/branch/", json=branch_data)
    
    assert response.status_code == 201
     
    response = client.get("/branch/1/areas")
    
    assert response.status_code == 204
    
    area_data = {"name": "Test Area", "branch_id": 1, "opening_time": "00:00:00", "closing_time": "00:00:00", "minimum_staff": 1, "maximum_staff": 10}
    area_data2 = {"name": "Test Area2", "branch_id": 1, "opening_time": "00:00:00", "closing_time": "00:00:00", "minimum_staff": 1, "maximum_staff": 10}
    response = client.post("/area/", json=area_data)
    response = client.post("/area/", json=area_data2)
    
    response = client.get("/branch/1/areas")
    
    assert response.status_code == 200
    
    branch_areas = response.json()
    
    assert len(branch_areas) == 2
       
    
def test_get_branch_employees(client):
    company_data = {"name": "Test Company"}
    client.post("/company/", json=company_data)
    branch_data = {"address": "Fake Street 123", "company_id": 1}
    client.post("/branch/", json=branch_data)
    
    response = client.get("/branch/1/employees")
    
    assert response.status_code == 204
    
    employee_data = {"name": "Test Employee", "hourly_wage": 10.0, "monthly_hours": 120, "branch_id": 1}
    client.post("/employee/", json=employee_data)
    client.post("/employee/", json=employee_data)
    
    response = client.get("/branch/1/employees")
    
    assert response.status_code == 200
    assert len(response.json()) == 2
    
def test_get_branch_locks(client):
    company_data = {"name": "Test Company"}
    client.post("/company/", json=company_data)
    branch_data = {"address": "Fake Street 123", "company_id": 1}
    client.post("/branch/", json=branch_data)
    
    employee_data = {"name": "Test Employee", "hourly_wage": 10.0, "monthly_hours": 120, "branch_id": 1}
    employee_data2 = {"name": "Test Employee2", "hourly_wage": 10.0, "monthly_hours": 120, "branch_id": 1}
    client.post("/employee/", json=employee_data)
    client.post("/employee/", json=employee_data2)
    
    lock_data = {"locked_date": "2025-12-15", "employee_id": 1 }
    lock_data2 = {"locked_date": "2025-12-15", "employee_id": 2 }
    
    client.post("/lock/", json=lock_data)
    client.post("/lock/", json=lock_data2)
    
    response = client.get("/branch/1/locks")
    
    assert response.status_code == 200
    
    branch_locks = response.json()
    
    assert len(branch_locks) == 2

    
    
    
    
    
    