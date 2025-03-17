import uvicorn

from src.service.server import MockServer

if __name__ == "__main__":
    test_path = "C:\\Users\\PatricHermannZEUFACK\\Documents\\projects\\dymock\\src\\templates\\petstore.json"
    server = MockServer(spec_path=test_path)
    app = server.create_app()
    uvicorn.run(app, host="127.0.0.1", port=8000)
