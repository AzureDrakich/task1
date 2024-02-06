from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
from app.internal.article import bd

app = FastAPI()
router = APIRouter(prefix="/api/v1")

class Message(BaseModel):
    sender: str
    receiver: str
    msg: str

@router.post("/chat")
async def post_message(message: Message):
    cursor = bd.cursor()
    cursor.execute("INSERT INTO chat (sender, receiver, msg) VALUES (%s,%s,%s)", (message.sender,message.receiver,message.msg))
    bd.commit()
    cursor.close()
    return "Successfully sended message to %s" % message.receiver

@router.get("/chat/{name}/{receiver}")
async def read_chat(name: str,receiver: str):
    cursor = bd.cursor()
    cursor.execute("SELECT msg FROM chat WHERE sender=%s", (name,))
    msg_from = cursor.fetchall()
    cursor.execute("SELECT msg FROM chat WHERE receiver=%s", (name,))
    #msg_to = cursor.fetchall()
    cursor.execute("SELECT msg FROM chat WHERE sender=%s", (receiver,))
    msg_to_from = cursor.fetchall()
    cursor.close()
    return msg_from,msg_to_from