from fastapi import FastAPI
from app.web import creature, explorer, user

app = FastAPI()

app.include_router(explorer.router)
app.include_router(creature.router)
app.include_router(user.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}
