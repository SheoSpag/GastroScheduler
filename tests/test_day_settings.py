def test_get_one_day_setting(client):
    company_data = {"name": "Test Company"}
    client.post("/company/", json=company_data)
    branch_data = {"address": "Fake Street 123", "company_id": 1}
    client.post("/branch/", json=branch_data)

    response = client.get("/settings/0/branch/1")
    assert response.status_code == 200
    settings = response.json()
    assert settings["week_day"] == 0
    assert settings["branch_id"] == 1

def test_get_all_branch_days_settings(client):
    company_data = {"name": "Test Company"}
    client.post("/company/", json=company_data)
    branch_data = {"address": "Fake Street 123", "company_id": 1}
    client.post("/branch/", json=branch_data)

    response = client.get("/settings/branch/1")
    assert response.status_code == 200
    settings = response.json()
    assert len(settings) == 7

def test_update_day_settings(client):
    company_data = {"name": "Test Company"}
    client.post("/company/", json=company_data)
    branch_data = {"address": "Fake Street 123", "company_id": 1}
    client.post("/branch/", json=branch_data)

    update_data = {"morning_intensity": 10}
    response = client.patch("/settings/0/branch/1", json=update_data)
    assert response.status_code == 200
    settings = response.json()
    assert settings["morning_intensity"] 