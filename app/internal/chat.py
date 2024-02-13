from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
from app.internal.article import bd

app = FastAPI()
router = APIRouter(prefix="/api/v1")

class Message(BaseModel):
    sender_id: int
    receiver_id: int
    msg: str


@router.post("/chat")
async def post_message(message: Message):
    cursor = bd.cursor()
    cursor.execute("INSERT INTO chat (sender_id, receiver_id, msg) VALUES (%s,%s,%s)",
                   (message.sender_id, message.receiver_id, message.msg))
    bd.commit()
    cursor.close()
    return "Successfully sended message to %s" % message.receiver_id

@router.get("/chat/{sender_id}/{receiver_id}")
async def read_chat(sender: int,receiver: int):
    cursor = bd.cursor()
    cursor.execute("SELECT msg FROM chat WHERE sender_id=%s", (sender,))
    msg_from = cursor.fetchall()
    cursor.execute("SELECT msg FROM chat WHERE receiver_id=%s", (receiver,))
    msg_to = cursor.fetchall()
    cursor.close()
    return msg_from, msg_to