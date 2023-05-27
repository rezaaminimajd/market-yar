from fastapi import FastAPI
import uvicorn
from apps.statistics import Base, view
from services.connections import engine

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def healthy_check():
    return 'I am healthy'


app.include_router(view.router)
