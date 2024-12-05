from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class FeedbackRead(BaseModel):
    id: str
    org_id: str
    conversation_id: str
    run_id: str
    user_id: str
    thumbs: Literal["up", "down", ""] = Field(
        ..., description="Thumbs up or down feedback from user."
    )
    comment: str = Field(..., description="Optional comment from user.")
    problems: list[str] = Field(
        ..., description="List of problems identified by user in red teaming."
    )
    severity: str = Field(
        ..., description="Severity of the `problems` identified by user in red teaming."
    )
    effort: str = Field(
        ...,
        description="User's effort required to discover the `problems` in red teaming.",
    )
    description: str = Field(
        ...,
        description="Description of the `problems` identified by user in red teaming.",
    )
    correctness: str | None = Field(
        None,
        description="Correctness of the agent response in expert review.",
    )
    completeness: str | None = Field(
        None,
        description="Completeness of the agent response in expert review.",
    )
    relevance: str | None = Field(
        None,
        description="Relevance of the agent response in expert review.",
    )
    review_text: str | None = Field(
        None,
        description="Additional text comments on the agent response in expert review.",
    )
    created: datetime
    updated: datetime | None


class FeedbackUpsert(BaseModel):
    thumbs: Literal["up", "down", ""] | None = Field(
        None, description="Thumbs up or down feedback from user."
    )
    comment: str | None = Field(None, description="Optional comment from user.")
    problems: list[str] | None = Field(
        None, description="List of problems identified by user in red teaming."
    )
    severity: str | None = Field(
        None,
        description="Severity of the `problems` identified by user in red teaming.",
    )
    effort: str | None = Field(
        None,
        description="User's effort required to discover the `problems` in red teaming.",
    )
    description: str | None = Field(
        None,
        description="Description of the `problems` identified by user in red teaming.",
    )
    correctness: str | None = Field(
        None,
        description="Correctness of the agent response in expert review.",
    )
    completeness: str | None = Field(
        None,
        description="Completeness of the agent response in expert review.",
    )
    relevance: str | None = Field(
        None,
        description="Relevance of the agent response in expert review.",
    )
    review_text: str | None = Field(
        None,
        description="Additional text comments on the agent response in expert review.",
    )
