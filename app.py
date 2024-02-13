from fastapi import FastAPI
import uvicorn

from api.controllers import cliente_controller
from api.settings import APP_HOST, APP_PORT


app = FastAPI()
app.include_router(cliente_controller.router)

if __name__ == "__main__":
    uvicorn.run(app, host=APP_HOST, port=int(APP_PORT))
