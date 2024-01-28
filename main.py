from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
import psycopg2

class User(BaseModel):
    name: str
    password: str


bd = psycopg2.connect(dbname="postgres", host="localhost", user="postgres", password="postgres", port="5432")
app = FastAPI()



@app.get("/person")
async def get_all():
    cursor = bd.cursor()
    cursor.execute("SELECT * FROM person")
    result = cursor.fetchall()
    cursor.close()
    return result

@app.get("/person/{id}")
async def get_person(id: int):
    cursor = bd.cursor()
    cursor.execute("SELECT * FROM person WHERE id = %s", (id,))
    result = cursor.fetchall()
    cursor.close()
    return result

@app.post("/create_person")
async def create_person(data:User):
    cursor = bd.cursor()
    cursor.execute("INSERT INTO person (name,password) VALUES (%s,%s)", (data.name, data.password))
    bd.commit()
    cursor.close()
    return "Person %s created" % data.name



