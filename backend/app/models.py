from datetime import datetime, date
from sqlalchemy import String, Text, Integer, Date, DateTime, ForeignKey, Boolean, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .db import Base

class Manager(Base):
    __tablename__ = "managers"
    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(255), index=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(64), nullable=True)
    keycloak_username: Mapped[str | None] = mapped_column(String(128), unique=True, nullable=True, index=True)
    keycloak_user_id: Mapped[str | None] = mapped_column(String(128), unique=True, nullable=True)

class Direction(Base):
    __tablename__ = "directions"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, index=True)

class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    vendor: Mapped[str | None] = mapped_column(String(255), nullable=True)
    direction_id: Mapped[int | None] = mapped_column(ForeignKey("directions.id"), nullable=True)
    direction: Mapped[Direction | None] = relationship()

class Institution(Base):
    __tablename__ = "institutions"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    short_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    full_name: Mapped[str | None] = mapped_column(Text, nullable=True)
    region: Mapped[str | None] = mapped_column(String(255), index=True, nullable=True)
    city: Mapped[str | None] = mapped_column(String(255), nullable=True)
    institution_type: Mapped[str | None] = mapped_column(String(100), nullable=True)
    site: Mapped[str | None] = mapped_column(String(255), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(64), default="Планируется", index=True)
    vendor: Mapped[str | None] = mapped_column(String(255), nullable=True)
    software: Mapped[str | None] = mapped_column(String(255), nullable=True)
    contract_number: Mapped[str | None] = mapped_column(String(100), nullable=True)
    license_signed: Mapped[date | None] = mapped_column(Date, nullable=True)
    license_until: Mapped[date | None] = mapped_column(Date, nullable=True)
    transfer_status: Mapped[str | None] = mapped_column(String(100), nullable=True)
    comment: Mapped[str | None] = mapped_column(Text, nullable=True)
    manager_id: Mapped[int | None] = mapped_column(ForeignKey("managers.id"), nullable=True, index=True)
    manager: Mapped[Manager | None] = relationship()
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    contacts: Mapped[list["InstitutionContact"]] = relationship(cascade="all, delete-orphan", back_populates="institution")
    interactions: Mapped[list["Interaction"]] = relationship(cascade="all, delete-orphan", back_populates="institution")

class InstitutionContact(Base):
    __tablename__ = "institution_contacts"
    id: Mapped[int] = mapped_column(primary_key=True)
    institution_id: Mapped[int] = mapped_column(ForeignKey("institutions.id", ondelete="CASCADE"), index=True)
    full_name: Mapped[str] = mapped_column(String(255))
    position: Mapped[str | None] = mapped_column(String(255), nullable=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(64), nullable=True)
    institution: Mapped[Institution] = relationship(back_populates="contacts")

class Workflow(Base):
    __tablename__ = "workflows"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    version: Mapped[int] = mapped_column(Integer, default=1)
    stages: Mapped[list["WorkflowStage"]] = relationship(cascade="all, delete-orphan", back_populates="workflow", order_by="WorkflowStage.position")

class WorkflowStage(Base):
    __tablename__ = "workflow_stages"
    __table_args__ = (UniqueConstraint("workflow_id", "position"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    workflow_id: Mapped[int] = mapped_column(ForeignKey("workflows.id", ondelete="CASCADE"), index=True)
    name: Mapped[str] = mapped_column(String(255))
    position: Mapped[int] = mapped_column(Integer)
    workflow: Mapped[Workflow] = relationship(back_populates="stages")

class Interaction(Base):
    __tablename__ = "interactions"
    __table_args__ = (UniqueConstraint("source", "external_id", name="uq_interaction_source_external"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    institution_id: Mapped[int] = mapped_column(ForeignKey("institutions.id", ondelete="CASCADE"), index=True)
    direction_id: Mapped[int | None] = mapped_column(ForeignKey("directions.id"), nullable=True, index=True)
    product_id: Mapped[int | None] = mapped_column(ForeignKey("products.id"), nullable=True, index=True)
    workflow_id: Mapped[int] = mapped_column(ForeignKey("workflows.id"), index=True)
    current_stage_id: Mapped[int | None] = mapped_column(ForeignKey("workflow_stages.id"), nullable=True)
    status: Mapped[str] = mapped_column(String(100), default="Планируется", index=True)
    students_count: Mapped[int] = mapped_column(Integer, default=0)
    streams_count: Mapped[int] = mapped_column(Integer, default=0)
    applications_count: Mapped[int] = mapped_column(Integer, default=0)
    started_at: Mapped[date | None] = mapped_column(Date, nullable=True)
    ended_at: Mapped[date | None] = mapped_column(Date, nullable=True)
    source: Mapped[str | None] = mapped_column(String(32), nullable=True, index=True)
    external_id: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    external_updated_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    institution: Mapped[Institution] = relationship(back_populates="interactions")
    direction: Mapped[Direction | None] = relationship()
    product: Mapped[Product | None] = relationship()
    workflow: Mapped[Workflow] = relationship()
    current_stage: Mapped[WorkflowStage | None] = relationship(foreign_keys=[current_stage_id])
    events: Mapped[list["InteractionEvent"]] = relationship(cascade="all, delete-orphan", back_populates="interaction", order_by="InteractionEvent.created_at")

class InteractionEvent(Base):
    __tablename__ = "interaction_events"
    id: Mapped[int] = mapped_column(primary_key=True)
    interaction_id: Mapped[int] = mapped_column(ForeignKey("interactions.id", ondelete="CASCADE"), index=True)
    from_stage_id: Mapped[int | None] = mapped_column(ForeignKey("workflow_stages.id"), nullable=True)
    to_stage_id: Mapped[int | None] = mapped_column(ForeignKey("workflow_stages.id"), nullable=True)
    comment: Mapped[str | None] = mapped_column(Text, nullable=True)
    author: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    interaction: Mapped[Interaction] = relationship(back_populates="events")
    attachments: Mapped[list["Attachment"]] = relationship(cascade="all, delete-orphan", back_populates="event")

class Attachment(Base):
    __tablename__ = "attachments"
    id: Mapped[int] = mapped_column(primary_key=True)
    event_id: Mapped[int] = mapped_column(ForeignKey("interaction_events.id", ondelete="CASCADE"), index=True)
    original_name: Mapped[str] = mapped_column(String(255))
    stored_name: Mapped[str] = mapped_column(String(255), unique=True)
    content_type: Mapped[str | None] = mapped_column(String(255), nullable=True)
    size: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    event: Mapped[InteractionEvent] = relationship(back_populates="attachments")

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str | None] = mapped_column(String(128), nullable=True, index=True)
    action: Mapped[str] = mapped_column(String(128), index=True)
    entity_type: Mapped[str] = mapped_column(String(64), index=True)
    entity_id: Mapped[str | None] = mapped_column(String(128), nullable=True)
    details: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
