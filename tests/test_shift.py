def test_create_shift(client):
    company_data = {"name": "Test Company"}
    client.post("/company/", json=company_data)
    branch_data = {"address": "Fake Street 123", "company_id": 1}
    client.post("/branch/", json=branch_data)
    area_data = {"opening_time": "00:00:00","closing_time": "00:00:00","minimum_staff": 1,"maximum_staff": 5,"name": "Bar","branch_id": 1}    
    client.post("/area/", json=area_data)
    role_data = {"name": "Bar", "area_id": 1 }
    client.post("/role/", json=role_data)
    employee_data = {"name": "Test Employee", "hourly_wage": 10.0, "monthly_hours": 120, "branch_id": 1}
    client.post("/employee/", json=employee_data)  

    shift_data = {"start_date_time": "2025-07-09T14:00:00", "end_date_time": "2025-07-09T20:00:00", "date": "2025-07-09", "role_id": 1, "employee_id": 2}

    result = client.post("/shift/", json=shift_data)
    
    assert result.status_code == 404
    
    shift_data = {"start_date_time": "2025-07-09T14:00:00", "end_date_time": "2025-07-09T20:00:00", "date": "2025-07-09", "role_id": 2, "employee_id": 1}

    result = client.post("/shift/", json=shift_data)
    
    assert result.status_code == 404
    
    shift_data = {"start_date_time": "2025-07-09T14:00:00", "end_date_time": "2025-07-09T20:00:00", "date": "2025-07-09", "role_id": 1, "employee_id": 1}

    result = client.post("/shift/", json=shift_data)
    
    assert result.status_code == 409
    
    client.post("/employee/1/role/1")
    
    shift_data = {"start_date_time": "2025-07-09T14:00:00", "end_date_time": "2025-07-09T13:00:00", "date": "2025-07-09", "role_id": 1, "employee_id": 1}

    result = client.post("/shift/", json=shift_data)
    
    assert result.status_code == 422        
    
    shift_data = {"start_date_time": "2025-07-09T14:00:00", "end_date_time": "2025-07-09T20:00:00", "date": "2025-07-09", "role_id": 1, "employee_id": 1}

    result = client.post("/shift/", json=shift_data)

    assert result.status_code == 201

def test_update_shift(client):
    company_data = {"name": "Test Company"}
    client.post("/company/", json=company_data)
    branch_data = {"address": "Fake Street 123", "company_id": 1}
    client.post("/branch/", json=branch_data)
    area_data = {"opening_time": "00:00:00","closing_time": "00:00:00","minimum_staff": 1,"maximum_staff": 5,"name": "Bar","branch_id": 1}    
    client.post("/area/", json=area_data)
    role_data = {"name": "Bar", "area_id": 1 }
    client.post("/role/", json=role_data)
    role_data = {"name": "Management", "area_id": 1 }
    client.post("/role/", json=role_data)
    employee_data = {"name": "Test Employee", "hourly_wage": 10.0, "monthly_hours": 120, "branch_id": 1}
    client.post("/employee/", json=employee_data)
    employee_data = {"name": "Test Employee2", "hourly_wage": 10.0, "monthly_hours": 120, "branch_id": 1}
    client.post("/employee/", json=employee_data)  
    client.post("/employee/1/role/1")
    shift_data = {"start_date_time": "2025-07-09T14:00:00", "end_date_time": "2025-07-09T20:00:00", "date": "2025-07-09", "role_id": 1, "employee_id": 1}
    client.post("/shift/", json=shift_data)

    new_shift_data = {"start_date_time": "2025-07-09T14:00:00", "end_date_time": "2025-07-09T20:00:00", "date": "2025-07-09", "role_id": 1, "employee_id": 1}
    
    result = client.patch("/shift/100", json=new_shift_data)
    
    #Shift to edit not found
    assert result.status_code == 404

    new_shift_data = {"start_date_time": "2025-07-09T14:00:00", "end_date_time": "2025-07-09T20:00:00", "date": "2025-07-09", "role_id": 1, "employee_id": 100}
    
    result = client.patch("/shift/1", json=new_shift_data)
    
    #Employee not found
    assert result.status_code == 404

    new_shift_data = {"start_date_time": "2025-07-09T14:00:00", "end_date_time": "2025-07-09T20:00:00", "date": "2025-07-09", "role_id": 100, "employee_id": 1}
    
    result = client.patch("/shift/1", json=new_shift_data)
    
    #Role not found with no employee
    assert result.status_code == 404
    
    new_shift_data = {"start_date_time": "2025-07-09T14:00:00", "end_date_time": "2025-07-09T20:00:00", "date": "2025-07-09", "role_id": 2, "employee_id": 2}
    
    result = client.patch("/shift/1", json=new_shift_data)
    
    #Role not in baseemployee roles
    assert result.status_code == 409

    new_shift_data = {"start_date_time": "2025-07-09T14:00:00", "end_date_time": "2025-07-09T20:00:00", "date": "2025-07-09", "role_id": 1, "employee_id": 1}
    
    result = client.patch("/shift/1", json=new_shift_data)
    
    #All good
    assert result.status_code == 200


def test_delete_shift(client):
    company_data = {"name": "Test Company"}
    client.post("/company/", json=company_data)
    branch_data = {"address": "Fake Street 123", "company_id": 1}
    client.post("/branch/", json=branch_data)
    area_data = {"opening_time": "00:00:00","closing_time": "00:00:00","minimum_staff": 1,"maximum_staff": 5,"name": "Bar","branch_id": 1}    
    client.post("/area/", json=area_data)
    role_data = {"name": "Bar", "area_id": 1 }
    client.post("/role/", json=role_data)
    employee_data = {"name": "Test Employee", "hourly_wage": 10.0, "monthly_hours": 120, "branch_id": 1}
    client.post("/employee/", json=employee_data)
    client.post("/employee/1/role/1")
    shift_data = {"start_date_time": "2025-07-09T14:00:00", "end_date_time": "2025-07-09T20:00:00", "date": "2025-07-09", "role_id": 1, "employee_id": 1}
    client.post("/shift/", json=shift_data)
    
    response = client.delete("/shift/100")
    
    assert response.status_code == 404

    response = client.delete("/shift/1")
    
    assert response.status_code == 200
    
    shift = response.json()
    
    assert shift["date"] == "2025-07-09"
    assert shift["role_id"] == 1

def test_get_shift(client):
    company_data = {"name": "Test Company"}
    client.post("/company/", json=company_data)
    branch_data = {"address": "Fake Street 123", "company_id": 1}
    client.post("/branch/", json=branch_data)
    area_data = {"opening_time": "00:00:00","closing_time": "00:00:00","minimum_staff": 1,"maximum_staff": 5,"name": "Bar","branch_id": 1}    
    client.post("/area/", json=area_data)
    role_data = {"name": "Bar", "area_id": 1 }
    client.post("/role/", json=role_data)
    employee_data = {"name": "Test Employee", "hourly_wage": 10.0, "monthly_hours": 120, "branch_id": 1}
    client.post("/employee/", json=employee_data)
    client.post("/employee/1/role/1")
    shift_data = {"start_date_time": "2025-07-09T14:00:00", "end_date_time": "2025-07-09T20:00:00", "date": "2025-07-09", "role_id": 1, "employee_id": 1}
    client.post("/shift/", json=shift_data)
    
    response = client.get("/shift/100")
    
    assert response.status_code == 404

    response = client.get("/shift/1")
    
    assert response.status_code == 200
    
    shift = response.json()
    
    assert shift["date"] == "2025-07-09"
    assert shift["role_id"] == 1    

def test_get_all_shifts(client):
    company_data = {"name": "Test Company"}
    client.post("/company/", json=company_data)
    branch_data = {"address": "Fake Street 123", "company_id": 1}
    client.post("/branch/", json=branch_data)
    area_data = {"opening_time": "00:00:00","closing_time": "00:00:00","minimum_staff": 1,"maximum_staff": 5,"name": "Bar","branch_id": 1}    
    client.post("/area/", json=area_data)
    role_data = {"name": "Bar", "area_id": 1 }
    client.post("/role/", json=role_data)
    employee_data = {"name": "Test Employee", "hourly_wage": 10.0, "monthly_hours": 120, "branch_id": 1}
    client.post("/employee/", json=employee_data)
    client.post("/employee/1/role/1")

    response = client.get("/shift/")
    
    assert response.status_code == 204

    shift_data = {"start_date_time": "2025-07-09T14:00:00", "end_date_time": "2025-07-09T20:00:00", "date": "2025-07-09", "role_id": 1, "employee_id": 1}
    client.post("/shift/", json=shift_data)
    shift_data = {"start_date_time": "2025-07-10T14:00:00", "end_date_time": "2025-07-10T20:00:00", "date": "2025-07-10", "role_id": 1, "employee_id": 1}
    client.post("/shift/", json=shift_data)

    response = client.get("/shift/")
    
    assert response.status_code == 200
    
    shifts = response.json()
    
    assert len(shifts) == 2

    