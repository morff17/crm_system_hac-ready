from datetime import date
from pydantic import BaseModel, Field

class InstitutionIn(BaseModel):
    name: str
    short_name: str | None = None
    full_name: str | None = None
    region: str | None = None
    city: str | None = None
    institution_type: str | None = None
    site: str | None = None
    description: str | None = None
    status: str = "Планируется"
    vendor: str | None = None
    software: str | None = None
    contract_number: str | None = None
    license_signed: date | None = None
    license_until: date | None = None
    transfer_status: str | None = None
    comment: str | None = None
    manager_id: int | None = None

class InstitutionPatch(BaseModel):
    name: str | None = None
    short_name: str | None = None
    full_name: str | None = None
    region: str | None = None
    city: str | None = None
    institution_type: str | None = None
    site: str | None = None
    description: str | None = None
    status: str | None = None
    vendor: str | None = None
    software: str | None = None
    contract_number: str | None = None
    license_signed: date | None = None
    license_until: date | None = None
    transfer_status: str | None = None
    comment: str | None = None
    manager_id: int | None = None

class WorkflowIn(BaseModel):
    name: str
    stages: list[str] = Field(min_length=1)

class InteractionTransition(BaseModel):
    to_stage_id: int
    comment: str | None = None

class InteractionCreate(BaseModel):
    institution_id: int
    direction_id: int | None = None
    product_id: int | None = None
    workflow_id: int
    students_count: int = 0
    streams_count: int = 0
    applications_count: int = 0
    started_at: date | None = None

class LoginRequest(BaseModel):
    login: str
    password: str

class RefreshRequest(BaseModel):
    refresh_token: str

class ManagerPatch(BaseModel):
    keycloak_username: str | None = None
    keycloak_user_id: str | None = None
    full_name: str | None = None
    email: str | None = None
    phone: str | None = None

class RoleUpdate(BaseModel):
    roles: list[str]
