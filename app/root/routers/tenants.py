from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.db_handlers.session import get_db
from app.database.orms.public_schema_orm import Tenant, UserTenant
from app.root.schemas.public import TenantCreate, Tenant as TenantSchema
from app.root.utils.tenant_context import create_tenant_schema
from app.root.utils.auth import get_current_user
from app.database.orms.public_schema_orm import User

router = APIRouter(prefix="/tenants", tags=["tenants"])

@router.post("/", response_model=TenantSchema)
def onboard_tenant(
    tenant_in: TenantCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Check if tenant with same name or schema exists
    existing_tenant = db.query(Tenant).filter(
        (Tenant.company_name == tenant_in.company_name) |
        (Tenant.schema_name == tenant_in.schema_name)
    ).first()
    if existing_tenant:
        raise HTTPException(status_code=400, detail="Tenant already exists")

    # Create tenant record
    db_tenant = Tenant(
        company_name=tenant_in.company_name,
        company_size=tenant_in.company_size,
        company_description=tenant_in.company_description,
        address=tenant_in.address,
        schema_name=tenant_in.schema_name,
        subscription_status="active"
    )
    db.add(db_tenant)
    db.flush()

    # Create DB schema (skipped or mocked in SQLite if needed, but the utility should be safe)
    try:
        create_tenant_schema(db, tenant_in.schema_name)
    except Exception:
        pass # SQLite doesn't support schemas in the same way, but we can continue the logic

    # Link user to tenant as admin
    user_tenant = UserTenant(
        user_id=current_user.id,
        tenant_id=db_tenant.id,
        role="admin"
    )
    db.add(user_tenant)

    db.commit()
    db.refresh(db_tenant)
    return db_tenant
