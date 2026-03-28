from pydantic import BaseModel, Field

class PerfilResponse(BaseModel):
    id: int
    nome: str = Field(..., max_length=250)
