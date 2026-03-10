from sqlalchemy.orm import Session
from sqlalchemy import and_
from . import models, schemas
from .models import StatusPedido
from typing import List, Optional

def get_pedido(db: Session, pedido_id: int):
    return db.query(models.Pedido).filter(models.Pedido.id == pedido_id).first()

def get_pedidos(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    status: Optional[str] = None,
    cliente_nome: Optional[str] = None
):
    query = db.query(models.Pedido)
    
    if status:
        query = query.filter(models.Pedido.status == status)
    if cliente_nome:
        query = query.join(models.Cliente).filter(
            models.Cliente.nome.ilike(f"%{cliente_nome}%")
        )
    
    return query.offset(skip).limit(limit).all()

def criar_cliente(db: Session, cliente: schemas.ClienteCreate) -> models.Cliente:
    db_cliente = models.Cliente(**cliente.dict())
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

def criar_pedido(db: Session, pedido: schemas.PedidoCreate) -> models.Pedido:
    # Criar ou buscar cliente
    cliente = db.query(models.Cliente).filter(
        models.Cliente.telefone == pedido.cliente_telefone
    ).first()
    
    if not cliente:
        cliente_create = schemas.ClienteCreate(
            nome=pedido.cliente_nome,
            telefone=pedido.cliente_telefone,
            whatsapp=pedido.cliente_whatsapp,
            endereco=pedido.cliente_endereco
        )
        cliente = criar_cliente(db, cliente_create)
    
    # Calcular totais
    valor_total = sum(item.preco_unitario * item.quantidade for item in pedido.itens)
    valor_entrada = valor_total * 0.5
    valor_restante = valor_total - valor_entrada
    
    # Criar pedido
    db_pedido = models.Pedido(
        cliente_id=cliente.id,
        valor_total=valor_total,
        valor_entrada=valor_entrada,
        valor_restante=valor_restante,
        status=StatusPedido.ENTRADA_PAGA,  # Assume entrada paga na criação
        observacoes_geral=pedido.observacoes_geral,
        data_entrega=pedido.data_entrega
    )
    
    db.add(db_pedido)
    db.commit()
    db.refresh(db_pedido)
    
    # Criar itens
    for item in pedido.itens:
        db_item = models.ItemPedido(
            **item.dict(),
            pedido_id=db_pedido.id
        )
        db.add(db_item)
    
    db.commit()
    db.refresh(db_pedido)
    return db_pedido

def atualizar_pedido(
    db: Session, 
    pedido_id: int, 
    pedido_update: schemas.PedidoUpdate
) -> models.Pedido:
    pedido = get_pedido(db, pedido_id)
    if not pedido:
        return None
    
    update_data = pedido_update.dict(exclude_unset=True)
    
    # Recalcular valores restantes se entrada mudou
    if "valor_entrada_pago" in update_data:
        pedido.valor_restante = pedido.valor_total - update_data["valor_entrada_pago"]
    
    for field, value in update_data.items():
        setattr(pedido, field, value)
    
    db.commit()
    db.refresh(pedido)
    return pedido

def get_totais_por_tamanho(db: Session):
    from sqlalchemy import func
    
    result = db.query(
        models.ItemPedido.tamanho,
        func.sum(models.ItemPedido.quantidade).label('total')
    ).group_by(models.ItemPedido.tamanho).all()
    
    return {item.tamanho: item.total for item in result}
