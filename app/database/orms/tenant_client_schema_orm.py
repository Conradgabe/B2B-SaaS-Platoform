from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, ForeignKey
from app.root.utils.abstract_base import AbstractBase

import uuid


# Client and Workflow related ORM models
class Client(AbstractBase):
    __tablename__ = "clients"

    id = Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(String(50), nullable=True)
    address: Mapped[str] = mapped_column(String(255), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)  

    workflow_progress: Mapped["ClientsWorkFlowProgress"] = relationship(
        "ClientsWorkFlowProgress", back_populates="client", cascade="all, delete-orphan"
    )
    communication: Mapped["Communication"] = relationship(
        "Communication", back_populates="client", cascade="all, delete-orphan"
    )


class ClientsWorkFlowProgress(AbstractBase):
    __tablename__ = "clients_workflow_progress"

    id = Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False, default=uuid.uuid4)
    client_id = Column(UUID(as_uuid=True), ForeignKey("clients.id"), nullable=False)
    workflow_id = Column(UUID(as_uuid=True), ForeignKey("workflows.id"), nullable=False)
    current_step: Mapped[int] = mapped_column(Integer, nullable=False)
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False)

    client: Mapped[Client] = relationship("Client", back_populates="workflow_progress")
    client_workflow: Mapped["WorkFLow"] = relationship("WorkFLow", back_populates="client_workflow_progress")


class WorkFLow(AbstractBase):
    __tablename__ = "workflows"

    id = Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=True)

    workflow_step: Mapped["WorkFLowStep"] = relationship(
        "WorkFLowStep", back_populates="workflow", cascade="all, delete-orphan"
    )
    client_workflow_progress: Mapped[ClientsWorkFlowProgress] = relationship(
        "ClientsWorkFlowProgress", back_populates="client_workflow", cascade="all, delete-orphan"
    )


class WorkFLowStep(AbstractBase):
    __tablename__ = "workflow_steps"

    id = Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False, default=uuid.uuid4)
    workflow_id = Column(UUID(as_uuid=True), ForeignKey("workflows.id"), nullable=False)
    step_name: Mapped[str] = mapped_column(String(255), nullable=False)
    step_order: Mapped[int] = mapped_column(Integer, nullable=False)

    workflow: Mapped[WorkFLow] = relationship("WorkFlow", back_populates="workflow_step")


# Communication related ORM models
class Communication(AbstractBase):
    __tablename__ = "communications"

    id = Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False, default=uuid.uuid4)
    client_id = Column(UUID(as_uuid=True), ForeignKey("clients.id"), nullable=False)
    event_type: Mapped[str] = mapped_column(String(50), nullable=False)  # email, call, meeting, status_update, welcome e.t.c
    status: Mapped[str] = mapped_column(String(50), nullable=False)  # pending, sent, failed, bounced
    external_message_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    client: Mapped[Client] = relationship("Client", back_populates="communication") 