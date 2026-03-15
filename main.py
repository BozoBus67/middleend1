from fastapi import FastAPI
from pydantic import BaseModel
import mysql.connector
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

load_dotenv()
FRONTEND_LOCALHOST = os.getenv("FRONTEND_LOCALHOST")
FRONTEND_WEBSITE_URL = os.getenv("FRONTEND_WEBSITE_URL")
MYSQL_ROOT_PASSWORD = os.getenv("MYSQL_ROOT_PASSWORD")

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
  sign_up_database_connection_object = mysql.connector.connect(
    host="localhost",
    user="root",
    password=MYSQL_ROOT_PASSWORD,
    database="sign_up_database"
  )
  cursor = sign_up_database_connection_object.cursor()

  try:
    cursor.execute(
      "INSERT INTO users (username, password) VALUES (%s, %s)",
      (data.username, data.password)
    )
    sign_up_database_connection_object.commit()

    return {"ok": True, "message": "account created"}

  except mysql.connector.errors.IntegrityError:
    return {"ok": False, "message": "username already exists"}

  finally:
    cursor.close()
    sign_up_database_connection_object.close()
