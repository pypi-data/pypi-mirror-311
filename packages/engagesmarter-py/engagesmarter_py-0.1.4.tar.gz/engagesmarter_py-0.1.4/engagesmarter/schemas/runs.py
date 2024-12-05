from datetime import datetime

from pydantic import BaseModel

from .tags import TagRead


class RunRead(BaseModel):
    id: str
    org_id: str
    conversation_id: str
    agent: str
    test: bool
    # api_auth: bool
    created: datetime


class RunReadFull(BaseModel):
    id: str
    org_id: str
    conversation_id: str
    agent: str
    tags: list[TagRead]
    test: bool
    # api_auth: bool
    created: datetime
