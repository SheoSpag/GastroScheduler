def test_create_employee(client):
    company_data = {"name": "Test Company"}
    client.post("/company/", json=company_data)
    branch_data = {"address": "Fake Street 123", "company_id": 1}
    client.post("/branch/", json=branch_data)
    
    employee_data = {"name": "Test Employee", "hourly_wage": 10.0, "monthly_hours": 120, "branch_id": 100}
    
    result = client.post("/employee/", json=employee_data)
    
    assert result.status_code == 404
    
    employee_data = {"name": "Test Employee", "hourly_wage": 10.0, "monthly_hours": 120, "branch_id": 1}
    
    result = client.post("/employee/", json=employee_data)

    assert result.status_code == 201
    
    employee = result.json()

    assert employee["name"] == "Test Employee"

def test_delete_employee(client):
    company_data = {"name": "Test Company"}
    client.post("/company/", json=company_data)
    branch_data = {"address": "Fake Street 123", "company_id": 1}
    client.post("/branch/", json=branch_data)
    employee_data = {"name": "Test Employee", "hourly_wage": 10.0, "monthly_hours": 120, "branch_id": 1}
    client.post("/employee/", json=employee_data)
    
    result = client.delete("/employee/10")
    
    assert result.status_code == 404
    
    result = client.delete("/employee/1")
    
    assert result.status_code == 200
    
    deleted_employee = result.json()
    
    assert deleted_employee["name"] == "Test Employee"

def test_update_employee(client):
    company_data = {"name": "Test Company"}
    client.post("/company/", json=company_data)
    company_data = {"name": "Test Company2"}
    client.post("/company/", json=company_data)
    branch_data = {"address": "Fake Street 123", "company_id": 1}
    client.post("/branch/", json=branch_data)
    branch_data = {"address": "Street Fake 456", "company_id": 2}
    client.post("/branch/", json=branch_data)
    branch_data = {"address": "Street Fake 789", "company_id": 1}
    client.post("/branch/", json=branch_data)
    
    employee_data = {"name": "Test Employee", "hourly_wage": 10.0, "monthly_hours": 120, "branch_id": 1}
    
    new_employee_data = {"name": "Updated Employee", "hourly_wage": 10.0, "monthly_hours": 120, "branch_id": 2}
    
    result = client.patch("/employee/1", json=new_employee_data)
    
    assert result.status_code == 404
    
    client.post("/employee/", json=employee_data)
    
    result = client.patch("/employee/1", json=new_employee_data)
    
    assert result.status_code == 409
    
    new_employee_data = {"name": "Updated Employee", "hourly_wage": 10.0, "monthly_hours": 120, "branch_id": 3}
    
    result = client.patch("/employee/1", json=new_employee_data)
    
    assert result.status_code == 200
    
    updated_employee = result.json()
    
    assert updated_employee["name"] == "Updated Employee"
    assert updated_employee["branch_id"] == 3

def test_asign_employee_role(client):
    company_data = {"name": "Test Company"}
    client.post("/company/", json=company_data)
    branch_data = {"address": "Fake Street 123", "company_id": 1}
    client.post("/branch/", json=branch_data)
    branch_data = {"address": "Fake Street 456", "company_id": 1}
    client.post("/branch/", json=branch_data)
    area_data = {"opening_time": "00:00:00","closing_time": "00:00:00","minimum_staff": 1,"maximum_staff": 5,"name": "Bar","branch_id": 1}    
    client.post("/area/", json=area_data)
    area_data = {"opening_time": "00:00:00","closing_time": "00:00:00","minimum_staff": 1,"maximum_staff": 5,"name": "Bar 2","branch_id": 2}    
    client.post("/area/", json=area_data)
    role_data = {"name": "Bar", "area_id": 1 }
    client.post("/role/", json=role_data)
    role_data = {"name": "Bar", "area_id": 2 }
    client.post("/role/", json=role_data)
    employee_data = {"name": "Test Employee", "hourly_wage": 10.0, "monthly_hours": 120, "branch_id": 1}
    client.post("/employee/", json=employee_data)
    
    result = client.post("/employee/10/role/1")
    
    assert result.status_code == 404
    
    result = client.post("/employee/1/role/10")
    
    assert result.status_code == 404
    
    result = client.post("/employee/1/role/2")
    
    assert result.status_code == 409

    result = client.post("/employee/1/role/1")
    
    assert result.status_code == 201
    
    result = client.get("/employee/1/roles")    
    
    roles = result.json()
    
    assert len(roles) == 1
        
def test_get_employee(client):
    company_data = {"name": "Test Company"}
    client.post("/company/", json=company_data)
    branch_data = {"address": "Fake Street 123", "company_id": 1}
    client.post("/branch/", json=branch_data)
    employee_data = {"name": "Test Employee", "hourly_wage": 10.0, "monthly_hours": 120, "branch_id": 1}
    client.post("/employee/", json=employee_data)
    employee_data = {"name": "Test Employee2", "hourly_wage": 10.0, "monthly_hours": 120, "branch_id": 1}
    client.post("/employee/", json=employee_data)
    
    result = client.get("/employee/10")
    
    assert result.status_code == 404
    
    result = client.get("/employee/1")
    
    assert result.status_code == 200
    
    employee = result.json()
    
    assert employee["name"] == "Test Employee"
    
def test_get_all_employees(client):
    company_data = {"name": "Test Company"}
    client.post("/company/", json=company_data)
    branch_data = {"address": "Fake Street 123", "company_id": 1}
    client.post("/branch/", json=branch_data)
    
    result = client.get("/employee/")
    
    assert result.status_code == 204
    
    employee_data = {"name": "Test Employee", "hourly_wage": 10.0, "monthly_hours": 120, "branch_id": 1}
    client.post("/employee/", json=employee_data)
    employee_data = {"name": "Test Employee2", "hourly_wage": 10.0, "monthly_hours": 120, "branch_id": 1}
    client.post("/employee/", json=employee_data)

    result = client.get("/employee/")
    
    assert result.status_code == 200
    
    employees = result.json()
    
    assert len(employees) == 2
    
def test_get_employee_locks(client):
    company_data = {"name": "Test Company"}
    client.post("/company/", json=company_data)
    branch_data = {"address": "Fake Street 123", "company_id": 1}
    client.post("/branch/", json=branch_data)
    
    employee_data = {"name": "Test Employee", "hourly_wage": 10.0, "monthly_hours": 120, "branch_id": 1}
    employee_data2 = {"name": "Test Employee2", "hourly_wage": 10.0, "monthly_hours": 120, "branch_id": 1}
    client.post("/employee/", json=employee_data)
    client.post("/employee/", json=employee_data2)
    
    response = client.get("/employee/1/lock")
    
    assert response.status_code == 204
    
    lock_data = {"locked_date": "2025-12-15", "employee_id": 1 }
    client.post("/lock/", json=lock_data)
    lock_data = {"locked_date": "2025-12-16", "employee_id": 1 }
    client.post("/lock/", json=lock_data)
    
    response = client.get("/employee/1/lock/")
    
    assert response.status_code == 200
    
    locks = response.json()
    
    assert len(locks) == 2

def test_get_employee_role(client):
    company_data = {"name": "Test Company"}
    client.post("/company/", json=company_data)
    branch_data = {"address": "Fake Street 123", "company_id": 1}
    client.post("/branch/", json=branch_data)
    branch_data = {"address": "Fake Street 456", "company_id": 1}
    client.post("/branch/", json=branch_data)
    area_data = {"opening_time": "00:00:00","closing_time": "00:00:00","minimum_staff": 1,"maximum_staff": 5,"name": "Bar","branch_id": 1}    
    client.post("/area/", json=area_data)
    area_data = {"opening_time": "00:00:00","closing_time": "00:00:00","minimum_staff": 1,"maximum_staff": 5,"name": "Managment","branch_id": 1}    
    client.post("/area/", json=area_data)
    role_data = {"name": "Bar", "area_id": 1 }
    client.post("/role/", json=role_data)
    role_data = {"name": "Bar Managment", "area_id": 1 }
    client.post("/role/", json=role_data)
    employee_data = {"name": "Test Employee", "hourly_wage": 10.0, "monthly_hours": 120, "branch_id": 1}
    client.post("/employee/", json=employee_data)
    client.post("/employee/1/role/1")
    client.post("/employee/1/role/2")
    
    result = client.get("/employee/1/roles")    
    
    roles = result.json()
    
    assert len(roles) == 2