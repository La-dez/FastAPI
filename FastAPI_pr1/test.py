from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

response = client.get("/search")
print(response.status_code)
print(response.json())

response = client.get("/search", params={"post_id": 2})
print(response.status_code)
print(response.json())

response = client.get("/search", params={"post_id": 4})
print(response.status_code)
print(response.json())