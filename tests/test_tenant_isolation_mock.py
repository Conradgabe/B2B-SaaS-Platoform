import pytest
from unittest.mock import MagicMock
from app.root.utils.tenant_context import set_tenant_schema, create_tenant_schema

def test_tenant_context_logic_mock():
    db = MagicMock()
    schema = "test_tenant"

    # Test set_tenant_schema
    set_tenant_schema(db, schema)
    # Check if execute was called with correct SQL
    args, _ = db.execute.call_args
    assert f'SET search_path TO {schema}, public' in str(args[0])

    # Test create_tenant_schema
    create_tenant_schema(db, schema)
    # Check if execute was called with correct SQL
    args, _ = db.execute.call_args_list[-1]
    assert f'CREATE SCHEMA IF NOT EXISTS {schema}' in str(args[0])
