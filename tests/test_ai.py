import json


def test_generate_weekly_shifts(client):
    #Company
    company_data = {"name": "Test Company"}
    client.post("/company/", json=company_data)
    #Branch
    branch_data = {"address": "Fake Street 123", "company_id": 1}
    client.post("/branch/", json=branch_data)

    # Pasta Area
    area_data = {"opening_time": "11:30:00","closing_time": "20:00:00","minimum_staff": 1,"maximum_staff": 2,"name": "Pasta","branch_id": 1}    
    client.post("/area/", json=area_data)

    #Pasta Roles
    role_data = {"name": "Pasta Cheff", "area_id": 1 }
    client.post("/role/", json=role_data)
    role_data = {"name": "Pasta Cheff asistant", "area_id": 1 }
    client.post("/role/", json=role_data)
    
    #2 Employees
    employee_data = {"name": "Gio - Pasta", "hourly_wage": 10.0, "monthly_hours": 120, "branch_id": 1}
    client.post("/employee/", json=employee_data)
    employee_data = {"name": "Rodri - Cheff asistant", "hourly_wage": 10.0, "monthly_hours": 120, "branch_id": 1}
    client.post("/employee/", json=employee_data)

    #Asign role to employees    
    client.post("/employee/1/role/1")
    client.post("/employee/2/role/2")
    
    response = client.post("/ia/generate-weekly-shifts/branch/1")
    assert response.status_code == 200
    data = response.json()
    
    try:
        shifts = json.loads(data["respuesta_ia"])
    except json.JSONDecodeError:
        raise AssertionError(f"La IA devolvió una respuesta inválida: {data['respuesta_ia']}")
    
    assert isinstance(shifts, list)
    assert len(shifts) > 0
    assert all("start_date_time" in s for s in shifts)
 

    