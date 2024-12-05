from enum import Enum

from pydantic import BaseModel, Field


class AgentMetadata(BaseModel):
    """Metadata about an agent on the Engage Smarter AI Platform API."""

    name: str = Field(..., description="Name and version of the agent.")
    title: str = Field(..., description="Human descriptive title for the agent.")
    description: str = Field(
        ..., description="Description providing more detail about the agent."
    )
    welcome_message: str = Field(
        "", description="Optional welcome message to be displayed to the user."
    )
    available_all_orgs: bool = Field(
        ...,
        description="Whether the agent is available to all orgs. False if available_org_ids is provided.",
    )
    available_org_ids: list[str] | None = Field(
        ...,
        description="List of org IDs this agent is available to. None if available_all_orgs is True.",
    )


class AgentStatusType(str, Enum):
    """Type of the agent status."""

    ACTIVE = "active"
    FAIL = "fail"


class AgentStatus(BaseModel):
    """Status of the agent."""

    status: AgentStatusType = Field(
        ...,
        description="Status of the agent. Can be one of 'active', 'fail'.",
    )
