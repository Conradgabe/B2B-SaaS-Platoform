from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.db_handlers.session import get_db
from app.database.orms.tenant_client_schema_orm import Workflow, WorkflowStep
from app.root.schemas.tenant import WorkflowCreate, Workflow as WorkflowSchema
from app.root.utils.tenant_context import set_tenant_schema, get_tenant_schema
from app.root.utils.auth import get_current_user
from app.database.orms.public_schema_orm import User

router = APIRouter(prefix="/workflows", tags=["workflows"])

@router.post("/", response_model=WorkflowSchema)
def create_workflow(
    workflow_in: WorkflowCreate,
    schema: str = Depends(get_tenant_schema),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        set_tenant_schema(db, schema)
    except Exception:
        pass
    db_workflow = Workflow(
        name=workflow_in.name,
        description=workflow_in.description
    )
    db.add(db_workflow)
    db.flush() # Get ID

    for step_in in workflow_in.steps:
        db_step = WorkflowStep(
            workflow_id=db_workflow.id,
            **step_in.dict()
        )
        db.add(db_step)

    db.commit()
    db.refresh(db_workflow)
    return db_workflow

@router.get("/", response_model=List[WorkflowSchema])
def list_workflows(
    schema: str = Depends(get_tenant_schema),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        set_tenant_schema(db, schema)
    except Exception:
        pass
    return db.query(Workflow).all()
