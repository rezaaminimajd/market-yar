from fastapi import FastAPI
from fastapi import APIRouter, Depends
import uvicorn
from apps.account import models as account_models, view as account_view, crud as account_crud
from apps.ticket import models as ticket_models, view as ticket_view
from services.sql_app.database import engine, get_db


account_models.Base.metadata.create_all(bind=engine)
ticket_models.Base.metadata.create_all(bind=engine)


app = FastAPI()

app.include_router(account_view.router)
app.include_router(ticket_view.router)

# db = Depends(get_db)

if __name__ == '__main__':
    print("Starting Application...")
   
    # account_crud.create_boss(db)
    uvicorn.run(
        app='main:app',
        host='localhost',
        port=8080,
        workers=1,
        log_level='info'
    )
    