from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2
from psycopg2 import errors
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

load_dotenv()
FRONTEND_LOCALHOST = os.getenv("FRONTEND_LOCALHOST")
FRONTEND_WEBSITE_URL = os.getenv("FRONTEND_WEBSITE_URL")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

app = FastAPI()

app.add_middleware(
  CORSMiddleware,
  allow_origins=[
    FRONTEND_LOCALHOST,
    FRONTEND_WEBSITE_URL,
  ],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

class SignupData(BaseModel):
  username: str
  password: str


@app.post("/signup")
def signup(data: SignupData):

  conn = psycopg2.connect(
    host=DB_HOST,
    port=DB_PORT,
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
  )

  cursor = conn.cursor()

  try:
    cursor.execute(
      "INSERT INTO users (username, password) VALUES (%s, %s)",
      (data.username, data.password)
    )
    conn.commit()
    return {"ok": True, "message": "account created"}

  except errors.UniqueViolation:
    conn.rollback()
    return {"ok": False, "message": "username already exists"}

  finally:
    cursor.close()
    conn.close()