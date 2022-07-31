from fastapi import FastAPI
import uvicorn
from apps.account import models, view
from services.sql_app.database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(view.router)


if __name__ == '__main__':
    print("Starting Application...")
    uvicorn.run(
        app='main:app',
        host='0.0.0.0',
        port=8808,
        workers=1,
        log_level='info'
    )
