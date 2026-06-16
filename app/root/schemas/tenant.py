from pydantic import BaseModel, EmailStr
from typing import Optional, List
from uuid import UUID
from datetime import datetime

class ClientBase(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    address: Optional[str] = None
    is_active: Optional[bool] = True

class ClientCreate(ClientBase):
    pass

class Client(ClientBase):
    id: UUID
    created_at: datetime
    update_at: datetime

    class Config:
        from_attributes = True

class WorkflowStepBase(BaseModel):
    step_name: str
    step_order: int

class WorkflowStepCreate(WorkflowStepBase):
    pass

class WorkflowStep(WorkflowStepBase):
    id: UUID
    workflow_id: UUID

    class Config:
        from_attributes = True

class WorkflowBase(BaseModel):
    name: str
    description: Optional[str] = None

class WorkflowCreate(WorkflowBase):
    steps: List[WorkflowStepCreate] = []

class Workflow(WorkflowBase):
    id: UUID
    steps: List[WorkflowStep] = []

    class Config:
        from_attributes = True

class CommunicationBase(BaseModel):
    event_type: str
    status: str
    external_message_id: Optional[str] = None

class CommunicationCreate(CommunicationBase):
    client_id: UUID

class Communication(CommunicationBase):
    id: UUID
    client_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True
