from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base
import enum

class StatusPedido(str, enum.Enum):
    PENDENTE = "pendente"
    ENTRADA_PAGA = "entrada_paga"
    EM_PRODUCAO = "em_producao"
    PRONTO = "pronto"
    ENTREGUE = "entregue"
    CANCELADO = "cancelado"

class Cliente(Base):
    __tablename__ = "clientes"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), index=True)
    telefone = Column(String(20))
    whatsapp = Column(String(20))
    endereco = Column(String(200))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    pedidos = relationship("Pedido", back_populates="cliente")

class ItemPedido(Base):
    __tablename__ = "itens_pedido"
    
    id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"))
    tipo_item = Column(String(50))  # ovo, casca, recheio
    tamanho = Column(String(20))    # P, M, G, GG
    quantidade = Column(Integer)
    preco_unitario = Column(Float)
    observacoes = Column(String(200))
    
    pedido = relationship("Pedido", back_populates="itens")

class Pedido(Base):
    __tablename__ = "pedidos"
    
    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"))
    valor_total = Column(Float, index=True)
    valor_entrada = Column(Float)
    valor_entrada_pago = Column(Float, default=0.0)
    valor_restante = Column(Float, default=0.0)
    status = Column(StatusPedido, default=StatusPedido.PENDENTE)
    observacoes_geral = Column(String(500))
    data_pedido = Column(DateTime(timezone=True), server_default=func.now())
    data_entrega = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    cliente = relationship("Cliente", back_populates="pedidos")
    itens = relationship("ItemPedido", back_populates="pedido", cascade="all, delete-orphan")
