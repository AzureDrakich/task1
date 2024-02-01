from fastapi import FastAPI,APIRouter
from pydantic import BaseModel
import psycopg2

router = APIRouter(prefix="/api/v1")

class Article(BaseModel):
    name: str
    article: str
    date: str
    person_id: int

app=FastAPI(title="Article")
bd = psycopg2.connect(dbname="postgres", host="localhost", user="postgres", password="postgres", port="5432")
@app.get("/article")
async def get_all_articles():
    cursor = bd.cursor()
    cursor.execute("SELECT * FROM article")
    result = cursor.fetchall()
    cursor.close()
    return result
@app.get("/article/{id}")
async def get_article_by_id(person_id:int):
    cursor = bd.cursor()
    cursor.execute("SELECT * FROM article WHERE person_id = %s", (person_id,))
    result = cursor.fetchall()
    cursor.close()
    return result

@app.post("/article")
async def create_article(data:Article):
    cursor = bd.cursor()
    cursor.execute("INSERT INTO article (name, article, date, person_id) VALUES (%s, %s, %s, %s)",
                   (data.name, data.article, data.date, data.person_id))
    bd.commit()
    cursor.close()
    return "Succesfully added new article with person's id %s" % data.person_id

@app.patch("/article")
async def update_article(id: int, data:Article):
    cursor = bd.cursor()
    cursor.execute("UPDATE article SET name = %s, article = %s, date = %s, person_id = %s WHERE id = %s",
                   (data.name, data.article,data.date,data.person_id,id))
    bd.commit()
    cursor.close()
    return "Successfully updated article with id %s" % id
@app.delete("/article/{id}")
async def delete_article(id:int):
    cursor = bd.cursor()
    cursor.execute("DELETE FROM article WHERE id = %s" % id)
    bd.commit()
    cursor.close()
    return "Successfully deleted article with %s" % id


