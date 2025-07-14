from app.root.utils.abstract_base import AbstractBase

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, DateTime, Boolean, JSON
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, ForeignKey

from typing import List, Optional
from datetime import datetime
import uuid

class Tenant(AbstractBase):
    __tablename__ = "tenants"

    id = Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False, default=uuid.uuid4)
    company_name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    company_size: Mapped[int] = mapped_column(Integer, nullable=True)
    company_descriptio: Mapped[str] = mapped_column(String(500), nullable=True)
    address: Mapped[str] = mapped_column(String(255), nullable=True)
    schema_name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    subscription_status: Mapped[str] = mapped_column(String, default="trial", nullable=False) # trial, active, cancelled

    user_tenants: Mapped["UserTenant"] = relationship("UserTenant", back_populates="tenant", cascade="all, delete-orphan")
    tenant_audit_logs: Mapped["AuditLogs"] = relationship("AuditLogs", back_populates="tenant", cascade="all, delete-orphan")
    idempotency_key: Mapped["IdempotencyKey"] = relationship("IdempotencyKey", back_populates="tenant", cascade="all, delete-orphan")
    integration_stat: Mapped["IntegrationStatus"] = relationship("IntegrationStatus", back_populates="tenant", cascade="all, delete-orphan")


class User(AbstractBase):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    first_name: Mapped[str] = mapped_column(String(255), nullable=False)
    last_name: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    last_login: Mapped[Optional[DateTime]] = mapped_column(DateTime, default=None)

    user_tenants: Mapped["UserTenant"] = relationship("UserTenant", back_populates="user", cascade="all, delete-orphan")
    user_audit_logs: Mapped["AuditLogs"] = relationship("AuditLogs", back_populates="user", cascade="all, delete-orphan")


class UserTenant(AbstractBase):
    __tablename__ = "user_tenants"

    id = Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False, default=uuid.uuid4)
    user_id = Column(UUID, ForeignKey("users.id"), nullable=False)
    tenant_id = Column(UUID, ForeignKey("tenants.id"), nullable=False)
    role: Mapped[str] = mapped_column(String(50), nullable=False, default="staff") # admin, staff, member

    user: Mapped[User] = relationship("User", back_populates="user_tenants")
    tenant: Mapped[Tenant] = relationship("Tenant", back_populates="user_tenants")


# Tracking data changes for audit purposes
class AuditLogs(AbstractBase):
    __tablename__ = "audit_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    action: Mapped[str] = mapped_column(String(255), nullable=False) # create, update, delete
    table_name: Mapped[str] = mapped_column(String(255), nullable=False) # Name of the model that was audited
    record_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), nullable=False) # ID of record that changed
    payload: Mapped[JSON]  = mapped_column(JSON, nullable=True)  # JSON data of the record change

    tenant: Mapped[Tenant] = relationship("Tenant", back_populates="tenant_audit_logs")
    user: Mapped[User] = relationship("User", back_populates="user_audit_logs")


# Track to avoid duplicate webhook processing
class IdempotencyKey(AbstractBase):
    __tablename__ = "idempotency_keys"

    id = Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False, default=uuid.uuid4)
    key: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=True)
    tenant_id: Mapped[UUID] = mapped_column(UUID, ForeignKey('tenants.id'), nullable=False)

    tenant: Mapped[Tenant] = relationship("Tenant", back_populates="idempotency_key")


# Track the health of each third-party integration
class IntegrationStatus(AbstractBase):
    __tablename__ = "integration_status"

    id = Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False, default=uuid.uuid4)
    service_name: Mapped[str] = mapped_column(String(255), nullable=False)
    tenant_id: Mapped[UUID] = mapped_column(UUID, ForeignKey('tenants.id'), nullable=False)
    last_success: Mapped[datetime] = mapped_column(DateTime)
    last_failure: Mapped[datetime] = mapped_column(DateTime)
    failure_count: Mapped[int] = mapped_column(Integer, default=0)

    tenant: Mapped[Tenant] = relationship("Tenant", back_populates="integration_stats")