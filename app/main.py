from fastapi import FastAPI
from app.web import creature, explorer

app = FastAPI()

app.include_router(explorer.router)
app.include_router(creature.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
