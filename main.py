from fastapi import FastAPI

from internal.router.router import router

app = FastAPI(title="Find My Trip")
app.include_router(router)


@app.get("/health")
def health():
    return {"status": "ok"}
