import uvicorn

from src.main import app


if __name__ == '__main__':
    print("Running server... \n", app.version)
    uvicorn.run('start_server:app', host='0.0.0.0', reload=True)
