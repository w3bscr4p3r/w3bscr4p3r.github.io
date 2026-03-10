from pydantic import BaseModel, validator
from typing import List, Optional
from datetime import datetime
from .models import StatusPedido

class ClienteBase(BaseModel):
    nome: str
    telefone: str
    whatsapp: Optional[str] = None
    endereco: Optional[str] = None

class ClienteCreate(ClienteBase):
    pass

class ClienteResponse(ClienteBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class ItemBase(BaseModel):
    tipo_item: str
    tamanho: str
    quantidade: int
    preco_unitario: float
    observacoes: Optional[str] = None

class ItemCreate(ItemBase):
    pass

class ItemResponse(ItemBase):
    id: int
    
    class Config:
        from_attributes = True

class PedidoCreate(BaseModel):
    cliente_nome: str
    cliente_telefone: str
    cliente_whatsapp: Optional[str] = None
    cliente_endereco: Optional[str] = None
    itens: List[ItemCreate]
    observacoes_geral: Optional[str] = None
    data_entrega: Optional[datetime] = None
    
    @validator('itens')
    def itens_nao_vazio(cls, v):
        if len(v) == 0:
            raise ValueError('Pedido deve ter pelo menos 1 item')
        return v

class PedidoResponse(BaseModel):
    id: int
    cliente: ClienteResponse
    valor_total: float
    valor_entrada: float
    valor_entrada_pago: float
    valor_restante: float
    status: StatusPedido
    observacoes_geral: Optional[str]
    data_pedido: datetime
    data_entrega: Optional[datetime]
    itens: List[ItemResponse] = []
    
    class Config:
        from_attributes = True

class PedidoUpdate(BaseModel):
    status: Optional[StatusPedido] = None
    valor_entrada_pago: Optional[float] = None
    observacoes_geral: Optional[str] = None
