def test_healthEndpoint(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.content_type == "application/json"
    assert response.get_json() == {
        "application": "SecureBank",
        "status": "running"
    }
    
