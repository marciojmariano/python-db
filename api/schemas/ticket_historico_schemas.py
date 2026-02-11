
from datetime import datetime
import uuid
from pydantic import BaseModel, ConfigDict
from infraestrutura.banco_dados.modelos import TicketStatusEnum

class TicketHistoricoCreateRequest(BaseModel):
    id_ticket: uuid.UUID
    texto: str
    status: TicketStatusEnum

class TicketHistoricoResponse(BaseModel):
    id: uuid.UUID
    status: TicketStatusEnum
    created_at: datetime
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)