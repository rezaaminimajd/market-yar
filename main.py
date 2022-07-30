from fastapi import FastAPI
import uvicorn
from apps.account import models
from services.sql_app.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/test')
def test():
    return 'HI !'


if __name__ == '__main__':
    print("Starting Application...")
    uvicorn.run(
        app='main:app',
        host='0.0.0.0',
        port=8808,
        workers=1,
        log_level='info'
    )
