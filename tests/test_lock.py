from app.models.lock_reason import LockReason

def test_create_lock(client):
    company_data = {"name": "Test Company"}
    client.post("/company/", json=company_data)
    branch_data = {"address": "Fake Street 123", "company_id": 1}
    client.post("/branch/", json=branch_data)
    
    employee_data = {"name": "Test Employee", "hourly_wage": 10.0, "monthly_hours": 120, "branch_id": 1}
    employee_data2 = {"name": "Test Employee2", "hourly_wage": 10.0, "monthly_hours": 120, "branch_id": 1}
    client.post("/employee/", json=employee_data)
    client.post("/employee/", json=employee_data2)
    
    lock_data = {"locked_date": "2025-12-15", "employee_id": 100 }

    response = client.post("/lock/", json=lock_data)
    
    assert response.status_code == 404
    
    lock_data = {"locked_date": "2025-12-15", "employee_id": 1 }

    response = client.post("/lock/", json=lock_data)
    
    assert response.status_code == 201
    
    created_lock = response.json()
    
    assert created_lock["locked_date"] == "2025-12-15"
    assert created_lock["employee_id"] == 1
    
    response = client.post("/lock/", json=lock_data)
    
    assert response.status_code == 409


def test_delete_lock(client):
    company_data = {"name": "Test Company"}
    client.post("/company/", json=company_data)
    branch_data = {"address": "Fake Street 123", "company_id": 1}
    client.post("/branch/", json=branch_data)
    
    employee_data = {"name": "Test Employee", "hourly_wage": 10.0, "monthly_hours": 120, "branch_id": 1}
    employee_data2 = {"name": "Test Employee2", "hourly_wage": 10.0, "monthly_hours": 120, "branch_id": 1}
    client.post("/employee/", json=employee_data)
    client.post("/employee/", json=employee_data2)
    
    lock_data = {"locked_date": "2025-12-15", "employee_id": 100 }

    response = client.delete("/lock/1")

    assert response.status_code == 404
    
    lock_data = {"locked_date": "2025-12-15", "employee_id": 1 }
    
    client.post("/lock/", json=lock_data)
    
    response = client.delete("/lock/1")

    assert response.status_code == 200
    
    deleted_lock = response.json()
    
    assert deleted_lock["locked_date"] == "2025-12-15"
    
def test_update_lock(client):
    company_data = {"name": "Test Company"}
    client.post("/company/", json=company_data)
    branch_data = {"address": "Fake Street 123", "company_id": 1}
    client.post("/branch/", json=branch_data)
    
    employee_data = {"name": "Test Employee", "hourly_wage": 10.0, "monthly_hours": 120, "branch_id": 1}
    employee_data2 = {"name": "Test Employee2", "hourly_wage": 10.0, "monthly_hours": 120, "branch_id": 1}
    client.post("/employee/", json=employee_data)
    client.post("/employee/", json=employee_data2)
    
    lock_data = {"locked_date": "2025-12-15", "employee_id": 1 }
    client.post("/lock/", json=lock_data)
    
    new_lock_data = {"locked_date": "2025-12-16", "lock_reason": "wish" }

    response = client.patch("/lock/100", json=new_lock_data)
    
    assert response.status_code == 404
    
    response = client.patch("/lock/1", json=new_lock_data)
    
    assert response.status_code == 200
    
    updated_lock = response.json()
    
    assert updated_lock["lock_reason"] == "wish"
    
    assert updated_lock["locked_date"] == "2025-12-16"

def test_get_lock(client):
    company_data = {"name": "Test Company"}
    client.post("/company/", json=company_data)
    branch_data = {"address": "Fake Street 123", "company_id": 1}
    client.post("/branch/", json=branch_data)
    
    employee_data = {"name": "Test Employee", "hourly_wage": 10.0, "monthly_hours": 120, "branch_id": 1}
    employee_data2 = {"name": "Test Employee2", "hourly_wage": 10.0, "monthly_hours": 120, "branch_id": 1}
    client.post("/employee/", json=employee_data)
    client.post("/employee/", json=employee_data2)
    
    lock_data = {"locked_date": "2025-12-15", "employee_id": 1 }
    client.post("/lock/", json=lock_data)

    response = client.get("/lock/100")
    
    assert response.status_code == 404
    
    response = client.get("/lock/1")
    
    assert response.status_code == 200

def test_get_lock(client):
    company_data = {"name": "Test Company"}
    client.post("/company/", json=company_data)
    branch_data = {"address": "Fake Street 123", "company_id": 1}
    client.post("/branch/", json=branch_data)
    
    employee_data = {"name": "Test Employee", "hourly_wage": 10.0, "monthly_hours": 120, "branch_id": 1}
    employee_data2 = {"name": "Test Employee2", "hourly_wage": 10.0, "monthly_hours": 120, "branch_id": 1}
    client.post("/employee/", json=employee_data)
    client.post("/employee/", json=employee_data2)
    
    lock_data = {"locked_date": "2025-12-15", "employee_id": 1 }
    client.post("/lock/", json=lock_data)
    lock_data = {"locked_date": "2025-12-15", "employee_id": 2 }
    client.post("/lock/", json=lock_data)
    
    response = client.get("/lock/1000")
    
    assert response.status_code == 404
    
    response = client.get("/lock/1")
    
    assert response.status_code == 200
    
    lock = response.json()

    assert lock["locked_date"] == "2025-12-15"

def get_all_locks(client):
    company_data = {"name": "Test Company"}
    client.post("/company/", json=company_data)
    branch_data = {"address": "Fake Street 123", "company_id": 1}
    client.post("/branch/", json=branch_data)
    
    employee_data = {"name": "Test Employee", "hourly_wage": 10.0, "monthly_hours": 120, "branch_id": 1}
    employee_data2 = {"name": "Test Employee2", "hourly_wage": 10.0, "monthly_hours": 120, "branch_id": 1}
    client.post("/employee/", json=employee_data)
    client.post("/employee/", json=employee_data2)
    
    response = client.get("/lock/")
    
    assert response.status_code == 204
    
    lock_data = {"locked_date": "2025-12-15", "employee_id": 1 }
    client.post("/lock/", json=lock_data)
    lock_data = {"locked_date": "2025-12-15", "employee_id": 2 }
    client.post("/lock/", json=lock_data)
    
    response = client.get("/lock/")
        
    assert response.status_code == 200
    
    locks = response.json()
    
    assert len(locks) == 2
    