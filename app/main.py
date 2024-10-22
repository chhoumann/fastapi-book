from fastapi import FastAPI
from web import creature, explorer

app = FastAPI()

app.include_router(explorer.router)
app.include_router(creature.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
