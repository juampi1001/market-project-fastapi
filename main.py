from fastapi import FastAPI
from api.repository.products_repository import router as product_router

app = FastAPI()

app.include_router(product_router, prefix="/api")