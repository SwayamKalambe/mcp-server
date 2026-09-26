from fastapi import FastAPI
from api.products.routes import products_router

app = FastAPI(title="mcp-api")

app.include_router(products_router)

@app.get("/")
def cover_page():
    return "mcp-api"