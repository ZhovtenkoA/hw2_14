import time
import redis.asyncio as redis

from sqlalchemy.orm import Session
from sqlalchemy import text

from fastapi import FastAPI, Request, Depends, HTTPException, status, BackgroundTasks
from fastapi_mail import MessageSchema, FastMail, ConnectionConfig, MessageType
from fastapi_limiter import FastAPILimiter
from fastapi.middleware.cors import CORSMiddleware
from fastapi_limiter.depends import RateLimiter

from hw2_11.routes import contacts, auth, users
from hw2_11.db.db import get_db
from hw2_11.schemas import EmailSchema
from hw2_11.services.email import conf

app = FastAPI()

origins = [ 
    "http://localhost:3000"
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api")
app.include_router(contacts.router, prefix="/api")
app.include_router(users.router, prefix="/api")

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["My-Process-Time"] = str(process_time)
    return response

@app.on_event("startup")
async def startup():
    r = await redis.Redis(host='localhost', port=6379, db=0, encoding="utf-8", decode_responses=True)
    await FastAPILimiter.init(r)

@app.get("/", name='Корень')
def read_root():
    return {"message": "Rest APIContacts v.1"}

@app.get("/api/healthchecker")
def healthchecher(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT 1")).fetchone()
        print(result)
        if result is None:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Database is not configured correctly")
        return {"message": "Welcom to FastApi"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Error connecting to the database")
