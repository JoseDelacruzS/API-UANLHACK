from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.api.deps import get_current_db, get_pagination_params
from app.schemas.operators import (
    OperatorCreate,
    OperatorUpdate,
    OperatorResponse,
    OperatorList
)
from app.models.operators import Operator

router = APIRouter()


@router.get("/", response_model=OperatorList)
async def get_operators(
    pagination: dict = Depends(get_pagination_params),
    db: Session = Depends(get_current_db)
):
    """Obtener lista de operadores con paginación"""
    query = db.query(Operator)
    total = query.count()
    
    operators = query.offset(pagination["offset"]).limit(pagination["page_size"]).all()
    
    return OperatorList(
        operators=operators,
        total=total,
        page=pagination["page"],
        page_size=pagination["page_size"]
    )


@router.get("/{operator_id}", response_model=OperatorResponse)
async def get_operator(
    operator_id: int,
    db: Session = Depends(get_current_db)
):
    """Obtener operador por ID"""
    operator = db.query(Operator).filter(Operator.operator_id == operator_id).first()
    if not operator:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Operador no encontrado"
        )
    return operator


@router.post("/", response_model=OperatorResponse, status_code=status.HTTP_201_CREATED)
async def create_operator(
    operator_data: OperatorCreate,
    db: Session = Depends(get_current_db)
):
    """Crear nuevo operador"""
    # Verificar si ya existe un operador con ese nombre
    existing = db.query(Operator).filter(Operator.name == operator_data.name).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un operador con ese nombre"
        )
    
    operator = Operator(**operator_data.model_dump())
    db.add(operator)
    db.commit()
    db.refresh(operator)
    return operator


@router.put("/{operator_id}", response_model=OperatorResponse)
async def update_operator(
    operator_id: int,
    operator_data: OperatorUpdate,
    db: Session = Depends(get_current_db)
):
    """Actualizar operador"""
    operator = db.query(Operator).filter(Operator.operator_id == operator_id).first()
    if not operator:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Operador no encontrado"
        )
    
    # Verificar nombre único si se está actualizando
    if operator_data.name and operator_data.name != operator.name:
        existing = db.query(Operator).filter(Operator.name == operator_data.name).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe un operador con ese nombre"
            )
    
    # Actualizar campos
    for field, value in operator_data.model_dump(exclude_unset=True).items():
        setattr(operator, field, value)
    
    db.commit()
    db.refresh(operator)
    return operator


@router.delete("/{operator_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_operator(
    operator_id: int,
    db: Session = Depends(get_current_db)
):
    """Eliminar operador"""
    operator = db.query(Operator).filter(Operator.operator_id == operator_id).first()
    if not operator:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Operador no encontrado"
        )
    
    # Verificar si tiene llamadas asociadas
    if operator.calls:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se puede eliminar el operador porque tiene llamadas asociadas"
        )
    
    db.delete(operator)
    db.commit()
    return None
