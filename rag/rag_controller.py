from typing import Annotated

import uuid
from fastapi import Cookie, APIRouter, UploadFile, File, Response

from rag.channel_service import ChannelInfo, get_valid_channel
from rag.chatting_service import do_chat
from rag.rag_service import do_embedding

router = APIRouter(prefix='/rags', tags=["rags"])


@router.get("/channels", description="get current repository id")
async def get_channels(response: Response, cur_channel: Annotated[str | None, Cookie()] = None):
    channelInfo = get_valid_channel(cur_channel, response)
    return channelInfo


@router.post("/channels", description="set current repository id")
async def set_channel(channelInfo: ChannelInfo, response: Response):
    channelInfo = get_valid_channel(channelInfo.current, response, append=True)
    return channelInfo


@router.post("/docs")
async def add_docs(file: UploadFile = File(...), cur_channel: Annotated[str | None, Cookie()] = None):
    channelInfo = get_valid_channel(cur_channel)

    return await do_embedding(file, channelInfo.current)


@router.post("/chatting")
async def chatting(question: str, response: Response, sessionId: Annotated[str | None, Cookie()] = None,
                   cur_channel: Annotated[str | None, Cookie()] = None):
    channelInfo = get_valid_channel(cur_channel)

    if not sessionId:
        sessionId = str(uuid.uuid4())
        response.set_cookie(key="sessionId", value=sessionId)

    return do_chat(question, channelInfo.current, sessionId)
