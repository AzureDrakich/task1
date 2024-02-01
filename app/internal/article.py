from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
import psycopg2
from datetime import datetime

date = "%s.%s.%s" % (datetime.now().year, datetime.now().month, datetime.now().day)
app=FastAPI()
router = APIRouter(prefix="/api/v1")


class Article(BaseModel):
    name: str
    article: str
    person_id: int

bd = psycopg2.connect(dbname="postgres", host="localhost", user="postgres", password="postgres", port="5432")

@router.get("/article")
async def get_all_articles():
    cursor = bd.cursor()
    cursor.execute("SELECT * FROM article")
    result = cursor.fetchall()
    cursor.close()
    return result

@router.get("/article/{id}")
async def get_article_by_id(person_id:int):
    cursor = bd.cursor()
    cursor.execute("SELECT * FROM article WHERE person_id = %s", (person_id,))
    result = cursor.fetchall()
    cursor.close()
    return result

@router.post("/article")
async def create_article(data:Article):
    cursor = bd.cursor()
    cursor.execute("INSERT INTO article (name, article, date, person_id) VALUES (%s, %s, %s, %s)",
                   (data.name, data.article, date, data.person_id))
    bd.commit()
    cursor.close()
    return "Succesfully added new article %s from %s with person's id %s at %s " % (data.article, data.name, data.person_id, date)

@router.patch("/article")
async def update_article(id: int, data:Article):
    cursor = bd.cursor()
    cursor.execute("UPDATE article SET name = %s, article = %s, date = %s, person_id = %s WHERE id = %s",
                   (data.name, data.article, date, data.person_id,id))
    bd.commit()
    cursor.close()
    return "Successfully updated article with id %s" % id
@router.delete("/article/{id}")
async def delete_article(id:int):
    cursor = bd.cursor()
    cursor.execute("DELETE FROM article WHERE id = %s" % id)
    bd.commit()
    cursor.close()
    return "Successfully deleted article with %s" % id


