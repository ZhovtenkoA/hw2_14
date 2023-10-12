from fastapi import FastAPI

from hw2_11.routes import contacts, auth

app = FastAPI()

app.include_router(auth.router, prefix="/api")
app.include_router(contacts.router, prefix="/api")


@app.get("/")
def read_root():
    return {"message": "This is REST API for contacts"}
