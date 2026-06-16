from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.sql import quoted_name
from fastapi import Header, Depends, HTTPException
from app.database.db_handlers.session import get_db

def set_tenant_schema(db: Session, schema_name: str):
    """
    Sets the search_path to the tenant's schema.
    """
    schema = quoted_name(schema_name, quote=True)
    db.execute(text(f"SET search_path TO {schema}, public"))

def get_tenant_schema(x_tenant_id: str = Header(...)) -> str:
    """
    Dependency to extract tenant schema from header.
    In a real app, you might look up the schema name from the tenant ID in the DB.
    For this implementation, we assume x_tenant_id IS the schema_name for simplicity,
    or we can add a lookup logic.
    """
    # For now, we use it directly. In production, validate it.
    return x_tenant_id

def create_tenant_schema(db: Session, schema_name: str):
    """
    Creates a new schema for a tenant.
    """
    schema = quoted_name(schema_name, quote=True)
    db.execute(text(f"CREATE SCHEMA IF NOT EXISTS {schema}"))
    db.commit()
