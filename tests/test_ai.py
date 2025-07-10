def test_ai_basic_response(client):
    message = {"message": "¿Qué opinás de los lunes?"}
    response = client.post("/ia/test", json=message)

    assert response.status_code == 200
    data = response.json()
    assert "respuesta_ia" in data
    assert isinstance(data["respuesta_ia"], str)
    print("Respuesta IA:", data["respuesta_ia"])
