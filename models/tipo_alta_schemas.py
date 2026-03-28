from pydantic import BaseModel, Field
from typing import Optional

class TodoDelete(BaseModel):
    id: int

class TipoAlta(BaseModel):
    alta: str = Field(..., max_length=250)

class TipoAltaPatch(TipoAlta):
    alta: Optional[str] = None

class TipoAltaResponse(TipoAlta):
    id: int