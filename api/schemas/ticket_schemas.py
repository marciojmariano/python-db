
from datetime import datetime
from typing import List, Optional
import uuid
from pydantic import BaseModel, ConfigDict, Field
from infraestrutura.banco_dados.modelos import TicketPrioridadeEnum, TicketStatusEnum
from api.schemas.ticket_historico_schemas import TicketHistoricoResponse


class TicketCreateRequest(BaseModel):
    titulo: str = Field(..., min_length=5, max_length=150)
    descricao: str = Field(..., min_length=10)
    id_usuario: uuid.UUID = Field(..., description="ID do usuário que está abrindo o ticket")
    id_categoria: uuid.UUID = Field(..., description="ID da categoria do ticket")
    prioridade: TicketPrioridadeEnum = Field(..., description="Prioridades: baixa, importante e urgente")
    model_config = {"use_enum_values": True}

# PUT /tickets/{id}/start
class TicketStartRequest(BaseModel):
    responsavel_id: uuid.UUID
    tempo_estimado: int = Field(..., ge=1, le=7) # Min 1 dia, Max 7 dias
    observacoes_iniciais: str = Field(..., min_length=30)

# PUT /tickets/{id}/done
class TicketDoneRequest(BaseModel):
    solucao_aplicada: str = Field(..., min_length=100)
    observacoes_internas: Optional[str] = None

# PUT /tickets/{id}/reopen
class TicketReopenRequest(BaseModel):
    motivo_reabertura: str = Field(..., min_length=1)
    motivo_detalhes: str = Field(..., min_length=1)

# PUT /tickets/{id}/close
class TicketCloseRequest(BaseModel):
    avaliacao: int = Field(..., ge=1, le=5)
    comentario_avaliacao: Optional[str] = None
    comentario_confirmacao_usuario: str = Field(..., min_length=30)


class TicketResponse(BaseModel):
    id: uuid.UUID
    titulo: str
    status: TicketStatusEnum
    prioridade: TicketPrioridadeEnum
    id_usuario: uuid.UUID
    id_responsavel: Optional[uuid.UUID] = None
    created_at: datetime
    historicos: List[TicketHistoricoResponse] = []
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)