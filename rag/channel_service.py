from typing import List, Any
from pydantic import BaseModel
from typing import Annotated, Optional
from fastapi import Response

FILE_NAME = './channels.txt'


class ChannelInfo(BaseModel):
    current: str
    channels: Optional[list[str]] = None


def write_to_txt(channels: List[str]):
    channels = list(set(channels))
    with open(FILE_NAME, 'w') as file:
        for item in channels:
            file.write("%s\n" % item)
    print("channels have been written to", FILE_NAME)


def read_from_txt() -> List[str]:
    channels = []
    with open(FILE_NAME, 'r') as file:
        for line in file:
            channels.append(line.strip())
    return channels


def get_valid_channel(cur_channel: str, response: Response = None, append: bool = False) -> ChannelInfo:
    channels = read_from_txt()

    if append:
        if cur_channel not in channels:
            channels.append(cur_channel)
            write_to_txt(channels)
    else:
        if not cur_channel or cur_channel not in channels:
            cur_channel = channels[-1]

    if response:
        response.set_cookie(key="cur_channel", value=cur_channel)
    return ChannelInfo(channels=channels, current=cur_channel)
