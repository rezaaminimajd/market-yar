from fastapi import FastAPI
import uvicorn
from apps.account import models as account_models, view as account_view
from apps.ticket import models as ticket_models, view as ticket_view
from services.sql_app.database import engine
from fastapi.staticfiles import StaticFiles
from starlette_validation_uploadfile import ValidateUploadFileMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

account_models.Base.metadata.create_all(bind=engine)
ticket_models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.add_middleware(
    ValidateUploadFileMiddleware,
    app_path='/account/upload',
    max_size=52428800
)

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.include_router(account_view.router)
app.include_router(ticket_view.router)


@app.get("/")
def healthy_check():
    return 'I am healthy'


if __name__ == '__main__':
    print("Starting Application...")

    uvicorn.run(
        app='main:app',
        host='localhost',
        port=8080,
        workers=1,
        log_level='info'
    )
