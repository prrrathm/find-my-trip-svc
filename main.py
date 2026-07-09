from fastapi import FastAPI

from internal.middleware.session import SessionValidationMiddleware
from internal.router.router import router

app = FastAPI(title="Find My Trip")

app.add_middleware(SessionValidationMiddleware)
app.include_router(router)


@app.get("/health")
def health():
    return {"status": "ok"}
