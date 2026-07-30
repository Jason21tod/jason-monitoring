from main import app
from fastapi.testclient import TestClient


client = TestClient(app)



if __name__ == "__main__":
    def test_read_main():
        response = client.get("/")
        print(response)