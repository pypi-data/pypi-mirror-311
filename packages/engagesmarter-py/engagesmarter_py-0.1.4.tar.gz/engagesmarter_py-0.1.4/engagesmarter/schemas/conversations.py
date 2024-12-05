from datetime import datetime

from pydantic import BaseModel, Field

from .tags import TagRead


class ConversationRead(BaseModel):
    id: str
    org_id: str
    data: dict
    source: str = Field(..., description="Source of the conversation.")
    cloned_from_message_id: str | None
    # api_auth: bool = Field(..., description="Was this conversation created by API key?")
    summary: str = Field(..., description="A short summary of the conversation.")
    created: datetime


class ConversationReadFull(BaseModel):
    id: str
    org_id: str
    data: dict
    source: str = Field(..., description="Source of the conversation.")
    cloned_from_message_id: str | None
    # api_auth: bool = Field(..., description="Was this conversation created by API key?")
    summary: str = Field(..., description="A short summary of the conversation.")
    created: datetime
    user_id: str
    tags: list[TagRead] = Field(
        ..., description="List of active Tags on this conversation."
    )
    is_saved: bool = Field(
        ..., description="Is this conversation saved for the calling user?"
    )


class ConversationUpdate(BaseModel):
    data: dict | None = Field(None, description="Optional metadata.")
    source: str | None = Field(None, description="Optional source of the conversation.")


class ConversationCreate(BaseModel):
    data: dict = Field({}, description="Optional metadata.")
    source: str = Field("", description="Optional source of the conversation.")
