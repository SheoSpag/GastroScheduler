def test_generate_weekly_shifts(client):
    #Company
    company_data = {"name": "Test Company"}
    client.post("/company/", json=company_data)
    #Branch
    branch_data = {"address": "Fake Street 123", "company_id": 1}
    client.post("/branch/", json=branch_data)

    # Pasta Area
    area_data = {"opening_time": "10:00:00","closing_time": "20:00:00","minimum_staff": 1,"maximum_staff": 2,"name": "Pasta","branch_id": 1}    
    client.post("/area/", json=area_data)

    #Pasta Roles
    role_data = {"name": "Pasta Cheff", "area_id": 1 }
    client.post("/role/", json=role_data)
    role_data = {"name": "Pasta asistant", "area_id": 1 }
    client.post("/role/", json=role_data)
    
    #Pasta Employees
    employee_data = {"name": "Gio", "hourly_wage": 10.0, "monthly_hours": 130, "branch_id": 1}
    client.post("/employee/", json=employee_data)
    employee_data = {"name": "Rodri", "hourly_wage": 10.0, "monthly_hours": 160, "branch_id": 1}
    client.post("/employee/", json=employee_data)

    #Asign role to employees    
    client.post("/employee/1/role/1")
    client.post("/employee/2/role/2")

    #Salad Area
    area_data = {"opening_time": "10:00:00","closing_time": "21:00:00","minimum_staff": 1,"maximum_staff": 2,"name": "Salad","branch_id": 1}    
    client.post("/area/", json=area_data)
    
    #Salad Roles
    role_data = {"name": "Salad Cheff", "area_id": 2 }
    client.post("/role/", json=role_data)
    role_data = {"name": "Salad asistant", "area_id": 2 }
    client.post("/role/", json=role_data)
    
    #Salad Employees
    employee_data = {"name": "Nico", "hourly_wage": 10.0, "monthly_hours": 130, "branch_id": 1}
    client.post("/employee/", json=employee_data)
    employee_data = {"name": "Esteban", "hourly_wage": 10.0, "monthly_hours": 160, "branch_id": 1}
    client.post("/employee/", json=employee_data)

    #Asign role to employees    
    client.post("/employee/3/role/3")
    client.post("/employee/4/role/4")
    
    #Pizza Area
    area_data = {"opening_time": "10:00:00","closing_time": "20:00:00","minimum_staff": 2,"maximum_staff": 3,"name": "Pizza","branch_id": 1}    
    client.post("/area/", json=area_data)
    
    #Piza Roles
    role_data = {"name": "Pizza Cheff", "area_id": 3 }
    client.post("/role/", json=role_data)
    role_data = {"name": "Pizza asistant", "area_id": 3 }
    client.post("/role/", json=role_data)
    
    #Pizza Employees
    employee_data = {"name": "Tom", "hourly_wage": 10.0, "monthly_hours": 130, "branch_id": 1}
    client.post("/employee/", json=employee_data)
    employee_data = {"name": "Jano", "hourly_wage": 10.0, "monthly_hours": 160, "branch_id": 1}
    client.post("/employee/", json=employee_data)
    employee_data = {"name": "Hassen", "hourly_wage": 10.0, "monthly_hours": 160, "branch_id": 1}
    client.post("/employee/", json=employee_data)

    #Asign role to employees    
    client.post("/employee/5/role/5")
    client.post("/employee/6/role/6")
    client.post("/employee/7/role/6")
    
    #Dishwashing Area
    area_data = {"opening_time": "11:30:00","closing_time": "21:00:00","minimum_staff": 1,"maximum_staff": 2,"name": "Dishwashing","branch_id": 1}    
    client.post("/area/", json=area_data)
    
    
    #Dishwashing Roles
    role_data = {"name": "Dishwasher", "area_id": 4}
    client.post("/role/", json=role_data)

    #Dishwasher Employees
    employee_data = {"name": "Peteer", "hourly_wage": 10.0, "monthly_hours": 130, "branch_id": 1}
    client.post("/employee/", json=employee_data)
    employee_data = {"name": "Hinger", "hourly_wage": 10.0, "monthly_hours": 160, "branch_id": 1}
    client.post("/employee/", json=employee_data)

    #Asign role to employees    
    client.post("/employee/8/role/7")
    client.post("/employee/9/role/7")
    
    #Service Area
    area_data = {"opening_time": "10:00:00","closing_time": "22:00:00","minimum_staff": 2,"maximum_staff": 3,"name": "Service","branch_id": 1}    
    client.post("/area/", json=area_data)
    
    #Service Roles
    role_data = {"name": "Servers", "area_id": 5}
    client.post("/role/", json=role_data)
    role_data = {"name": "Runners", "area_id": 5}
    client.post("/role/", json=role_data)
    
    #Service Employees
    employee_data = {"name": "Marina", "hourly_wage": 10.0, "monthly_hours": 130, "branch_id": 1}
    client.post("/employee/", json=employee_data)
    employee_data = {"name": "Sofia", "hourly_wage": 10.0, "monthly_hours": 160, "branch_id": 1}
    client.post("/employee/", json=employee_data)
    employee_data = {"name": "Alex", "hourly_wage": 10.0, "monthly_hours": 160, "branch_id": 1}
    client.post("/employee/", json=employee_data)
    
    #Asign role to employees    
    client.post("/employee/10/role/8")
    client.post("/employee/11/role/8")
    client.post("/employee/12/role/9")
    
    #Bar Area
    area_data = {"opening_time": "10:00:00","closing_time": "22:00:00","minimum_staff": 1,"maximum_staff": 3,"name": "Bar","branch_id": 1}    
    client.post("/area/", json=area_data)
    
    #Bartenders  Roles
    role_data = {"name": "Bartenders", "area_id": 6}
    client.post("/role/", json=role_data)

    #Bar Employees
    employee_data = {"name": "Erica", "hourly_wage": 10.0, "monthly_hours": 130, "branch_id": 1}
    client.post("/employee/", json=employee_data)
    employee_data = {"name": "Noah", "hourly_wage": 10.0, "monthly_hours": 160, "branch_id": 1}
    client.post("/employee/", json=employee_data)
    employee_data = {"name": "Alejandro", "hourly_wage": 10.0, "monthly_hours": 160, "branch_id": 1}
    client.post("/employee/", json=employee_data)
    
    #Asign role to employees    
    client.post("/employee/13/role/10")
    client.post("/employee/14/role/10")
    client.post("/employee/15/role/10")
    
    response = client.get("/shift/")
    
    assert response.status_code == 204
    
    response = client.post("/ia/generate-weekly-shifts/branch/1")
    assert response.status_code == 201

    response = client.get("/shift/")
    

    
    assert response.status_code == 200
    
    

    