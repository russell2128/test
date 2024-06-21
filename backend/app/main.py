import fastapi
import fastapi.routing

app = fastapi.FastAPI()

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, port=10400, reload=True)
