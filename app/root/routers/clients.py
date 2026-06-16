from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from typing import List
from app.database.db_handlers.session import get_db
from app.database.orms.tenant_client_schema_orm import Client
from app.root.schemas.tenant import ClientCreate, Client as ClientSchema
from app.root.utils.tenant_context import set_tenant_schema, get_tenant_schema
from app.root.utils.auth import get_current_user
from app.database.orms.public_schema_orm import User

router = APIRouter(prefix="/clients", tags=["clients"])

@router.post("/", response_model=ClientSchema)
def create_client(
    client_in: ClientCreate,
    schema: str = Depends(get_tenant_schema),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        set_tenant_schema(db, schema)
    except Exception:
        pass
    db_client = Client(**client_in.dict())
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

@router.get("/", response_model=List[ClientSchema])
def list_clients(
    schema: str = Depends(get_tenant_schema),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        set_tenant_schema(db, schema)
    except Exception:
        pass
    return db.query(Client).all()
