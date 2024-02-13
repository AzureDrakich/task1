from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
from app.internal import article
from hashlib import md5

app=FastAPI()
router = APIRouter(prefix="/api/v1")


class User(BaseModel):
    name: str
    password: str


bd = article.bd

@router.get("/person")
async def get_all():
    cursor = bd.cursor()
    cursor.execute("SELECT * FROM users")
    result = cursor.fetchall()
    cursor.close()
    return result

@router.get("/person/{id}")
async def get_person(id: int):
    cursor = bd.cursor()
    cursor.execute("SELECT * FROM users WHERE id = %s", (id,))
    result = cursor.fetchall()
    cursor.close()
    return result

@router.post("/person")
async def create_person(data:User):
    cursor = bd.cursor()
    b_password = data.password.encode('utf-8')
    cursor.execute("INSERT INTO users (name,password) VALUES (%s,%s)", (data.name, md5(b_password).hexdigest()))
    bd.commit()
    cursor.close()
    return "Person %s created" % data.name

@router.patch("/person")
async def update_person(id:int, data:User):
    cursor = bd.cursor()
    b_password = data.password.encode('utf-8')
    cursor.execute("UPDATE users SET name = %s, password = %s WHERE id = %s", (data.name,md5(b_password).hexdigest(),id))
    bd.commit()
    cursor.close()
    return "Successfully updated person with id %s" % id

@router.delete("/person{id}")
async def delete_person(id:int):
    cursor = bd.cursor()
    cursor.execute("DELETE FROM users WHERE id = %s" % id)
    bd.commit()
    cursor.close()
    return "Successfully deleted person with id %s" % id











