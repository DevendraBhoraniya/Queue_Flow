from fastapi import FastAPI
from routes import queue, user
from database.database import engine
from database import models

models.Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(user.router)
app.include_router(queue.router)

@app.get("/")
def main():
    return {"message": "Hello World"}

