from pydantic import BaseModel


class Agent(BaseModel):
    agent_id: str
    api_key: str
    scopes: list[str]
    spending_limit: float
