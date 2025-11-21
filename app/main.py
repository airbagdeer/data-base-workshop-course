from fastapi import FastAPI
from app.routers import movies, search, analytics

app = FastAPI(
    title="Educational Movie API",
    description="API for exploring educational and documentary movies.",
    version="1.0.0"
)

app.include_router(movies.router, tags=["Movies"])
app.include_router(search.router, tags=["Search"])
app.include_router(analytics.router, tags=["Analytics"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Educational Movie API! Check /docs for documentation."}
