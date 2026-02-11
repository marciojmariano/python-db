import enum

class CargoEnum(str, enum.Enum):
    n1 = "n1"
    n2 = "n2"
    n3 = "n3"
    lider = "lider"

class TicketStatusEnum(str, enum.Enum):
    aberto = "aberto"
    em_andamento = "em_andamento"
    resolvido = "resolvido"
    concluido = "concluido"
    excluido = "excluido"

class TicketPrioridadeEnum(str, enum.Enum):
    baixa = "baixa"
    importante = "importante"
    urgente = "urgente"