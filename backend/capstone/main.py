import fastapi
import fastapi.routing

import capstone.universe.cent

app = fastapi.FastAPI()

capstone.universe.cent.initialize_wch()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, port=10400, reload=True)
