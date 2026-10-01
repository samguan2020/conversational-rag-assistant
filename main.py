import uvicorn
from fastapi import FastAPI

from config import SETTINGS
from rag import rag_controller

app = FastAPI()
app.include_router(rag_controller.router)


@app.get("/")
async def root():
    return {'app': SETTINGS.app_name}


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8081, reload=True)
