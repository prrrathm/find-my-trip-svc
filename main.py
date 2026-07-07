from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from internal.router.router import router

app = FastAPI(title="Find My Trip")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST", "GET", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/health")
def health():
    return {"status": "ok"}
