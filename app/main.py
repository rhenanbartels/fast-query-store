from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "hello world"}


@app.get("/{slug}")
async def execute(slug: str):
    return {"slug": slug}
