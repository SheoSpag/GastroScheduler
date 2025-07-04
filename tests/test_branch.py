from app.models.branch import Branch
from app.models.day_settings import DaySettings

def test_create_branch(client, db):
    db.query(Branch).delete()
    db.query(DaySettings).delete()
    db.commit()
    
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
    db.query(Branch).delete()
    db.query(DaySettings).delete()
    db.commit()
    
    branch_data = {"address": "Fake Street 123", "company_id": 1}
    
    response = client.post("/branch/", json=branch_data)

    assert response.status_code == 404    
    

    