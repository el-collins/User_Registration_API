# from fastapi.testclient import TestClient
# from main import app

# client = TestClient(app)

# def test_user_registration():
#     response = client.post("/register/", json={
#         "username": "newuser",
#         "email": "newuser@example.com",
#         "password": "Password123!"
#     })
#     assert response.status_code == 200
#     assert response.json() == {
#         "message": "User successfully registered",
#         "username": "newuser",
#         "email": "newuser@example.com"
#     }

# def test_invalid_user_registration():
#     response = client.post("/register/", json={
#         "username": "nu",
#         "email": "newuser@example.com",
#         "password": "pass"
#     })
#     assert response.status_code == 422
#     assert "value_error" in response.text

# # Add additional tests as needed
