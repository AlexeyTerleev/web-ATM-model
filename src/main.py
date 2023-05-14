from fastapi import FastAPI

from src.auth.router import router as router_auth
from src.card.router import router as card_router

app = FastAPI()

app.include_router(router_auth)
app.include_router(card_router)
