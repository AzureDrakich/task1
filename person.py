from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2
import article

class User(BaseModel):
    name: str
    password: str


bd = psycopg2.connect(dbname="postgres", host="localhost", user="postgres", password="postgres", port="5432")
app = FastAPI(title="Person")



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

@app.post("/person")
async def create_person(data:User):
    cursor = bd.cursor()
    cursor.execute("INSERT INTO person (name,password) VALUES (%s,%s)", (data.name, data.password))
    bd.commit()
    cursor.close()
    return "Person %s created" % data.name

@app.patch("/person")
async def update_person(id:int, data:User):
    cursor = bd.cursor()
    cursor.execute("UPDATE person SET name = %s, password = %s WHERE id = %s", (data.name,data.password,id))
    bd.commit()
    cursor.close()
    return "Successfully updated person with id %s" % id

@app.delete("/person{id}")
async def delete_person(id:int):
    cursor = bd.cursor()
    cursor.execute("DELETE FROM person WHERE id = %s" % id)
    bd.commit()
    cursor.close()
    return "Successfully deleted person with id %s" % id

@app.get("/article")
async def get_article():
    return await article.get_all_articles()
@app.get("/article/{id}")
async def get_article_by_id(id:int):
    return await article.get_article_by_id(id)

@app.post("/article")
async def post_article(data:article.Article):
    await article.create_article(data)
    return "Succesfully added new article with person's id %s" % data.person_id

@app.patch("/article")
async def patch_article(id:int, data:article.Article):
    await article.update_article(id, data)
    return "Successfully updated article with id %s" % id

@app.delete("/article/{id}")
async def delete_article(id:int):
    await article.delete_article(id)
    return "Successfully deleted article with %s" % id









