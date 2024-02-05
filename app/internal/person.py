from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
from app.internal import article

app=FastAPI()
router = APIRouter(prefix="/api/v1")


class User(BaseModel):
    name: str
    password: str


bd = article.bd

@router.get("/person")
async def get_all():
    cursor = bd.cursor()
    cursor.execute("SELECT * FROM person")
    result = cursor.fetchall()
    cursor.close()
    return result

@router.get("/person/{id}")
async def get_person(id: int):
    cursor = bd.cursor()
    cursor.execute("SELECT * FROM person WHERE id = %s", (id,))
    result = cursor.fetchall()
    cursor.close()
    return result

@router.post("/person")
async def create_person(data:User):
    cursor = bd.cursor()
    cursor.execute("INSERT INTO person (name,password) VALUES (%s,%s)", (data.name, data.password))
    bd.commit()
    cursor.close()
    return "Person %s created" % data.name

@router.patch("/person")
async def update_person(id:int, data:User):
    cursor = bd.cursor()
    cursor.execute("UPDATE person SET name = %s, password = %s WHERE id = %s", (data.name,data.password,id))
    bd.commit()
    cursor.close()
    return "Successfully updated person with id %s" % id

@router.delete("/person{id}")
async def delete_person(id:int):
    cursor = bd.cursor()
    cursor.execute("DELETE FROM person WHERE id = %s" % id)
    bd.commit()
    cursor.close()
    return "Successfully deleted person with id %s" % id











