from ..constants import API_VERSION
from ..resources.base import BaseResource
from ..schemas.agents import AgentMetadata, AgentStatus


class AgentsResource(BaseResource):
    _API_PREFIX: str = f"/{API_VERSION}/agents"

    def list(self) -> list[AgentMetadata]:
        """
        Lists metadata for all agents available via the API.
        """
        response: dict = self.client.get(self._API_PREFIX)
        return [AgentMetadata(**agent_dict) for agent_dict in response.values()]

    def validate_agent(self, *, agent: str) -> AgentStatus:
        """
        Validates the name for the specified agent.
        """
        params = {"agent": agent}
        response: dict = self.client.get(f"{self._API_PREFIX}/validate", params=params)
        return AgentStatus(**response)
