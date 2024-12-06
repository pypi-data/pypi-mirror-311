from pydantic import BaseModel


class GetAllSearchGalaxiesAttributes(BaseModel):
    id: int
    uuid: str
    name: str
    type: str
    description: str
    version: str
    icon: str
    namespace: str
    kill_chain_order: str | None = None
    enabled: bool
    local_only: bool
