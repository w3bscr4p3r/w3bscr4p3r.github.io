from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import datetime

from .. import crud, schemas
from ..database import get_db

router = APIRouter(prefix="/pedidos", tags=["pedidos"])

@router.post("/", response_model=schemas.PedidoResponse)
def criar_pedido(pedido: schemas.PedidoCreate, db: Session = Depends(get_db)):
    return crud.criar_pedido(db, pedido)

@router.get("/", response_model=List[schemas.PedidoResponse])
def listar_pedidos(
    status: Optional[str] = Query(None),
    cliente_nome: Optional[str] = Query(None),
    skip: int = 0,
    limit: int = Query(100, le=1000),
    db: Session = Depends(get_db)
):
    pedidos = crud.get_pedidos(db, skip=skip, limit=limit, status=status, cliente_nome=cliente_nome)
    return pedidos

@router.get("/totais", response_model=dict)
def get_totais(db: Session = Depends(get_db)):
    return crud.get_totais_por_tamanho(db)

@router.get("/{pedido_id}", response_model=schemas.PedidoResponse)
def get_pedido(pedido_id: int, db: Session = Depends(get_db)):
    pedido = crud.get_pedido(db, pedido_id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return pedido

@router.put("/{pedido_id}", response_model=schemas.PedidoResponse)
def atualizar_pedido_status(
    pedido_id: int,
    pedido_update: schemas.PedidoUpdate,
    db: Session = Depends(get_db)
):
    pedido = crud.atualizar_pedido(db, pedido_id, pedido_update)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return pedido
