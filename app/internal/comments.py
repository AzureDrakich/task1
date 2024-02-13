from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
from datetime import datetime
from app.internal import article

date = "%s.%s.%s %s:%s" % (datetime.now().year, datetime.now().month, datetime.now().day, datetime.now().hour, datetime.now().minute)
app = FastAPI()
bd = article.bd
router = APIRouter(prefix="/api/v1")

class Comment(BaseModel):
    article_id: int
    comment: str

@router.get("/comments")
async def get_comments():
    cursor = bd.cursor()
    cursor.execute("SELECT * FROM comments")
    result = cursor.fetchall()
    cursor.close()
    return result

@router.get("/comments/{id}")
async def get_comment_by_id(id:int):
    cursor = bd.cursor()
    cursor.execute("SELECT * FROM comments WHERE id = %s" % id)
    result = cursor.fetchall()
    cursor.close()
    return result

@router.post("/comments")
async def post_comment(data:Comment):
    cursor = bd.cursor()
    cursor.execute("INSERT INTO comments (article_id, date, comment) VALUES (%s, %s, %s)", (data.article_id, date, data.comment))
    bd.commit()
    cursor.close()
    return "Successfully added new comment at %s" % date

@router.patch("/comments")
async def update_comments(id:int, data:Comment):
    cursor = bd.cursor()
    cursor.execute("UPDATE comments SET article_id = %s, date = %s, comment = %s  WHERE id = %s", (data.comment_id, date, data.comment, id))
    bd.commit()
    cursor.close()
    return "Successfully updated comment with id %s" % id

@router.delete("/comments/{id}")
async def delete_comment(id:int):
    cursor = bd.cursor()
    cursor.execute("DELETE FROM comments WHERE id = %s" % id)
    bd.commit()
    cursor.close()
    return "Successfully deleted comment with %s" % id

