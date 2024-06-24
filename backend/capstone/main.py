import fastapi
import fastapi.routing

import capstone.universe
import capstone.routers.auth

app = fastapi.FastAPI()

app.include_router(capstone.routers.auth.router, prefix="/auth")

capstone.universe.initialize_wch()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=10400, reload=True)