from fastapi import FastAPI
from operations.router import router as operation_router

app = FastAPI(title='Roulette')

app.include_router(operation_router)
