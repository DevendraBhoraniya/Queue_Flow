from fastapi import FastAPI
from routes import queue, user, token
from database.database import engine
from database import models

models.Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(user.router)
app.include_router(queue.router)
app.include_router(token.router)

@app.get("/health")
def main():
    return {"message": "Healthy"}

