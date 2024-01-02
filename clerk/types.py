from typing import Any, List, Optional

from pydantic import BaseModel


class Session(BaseModel):
    object: str
    id: str
    client_id: str
    user_id: str
    status: str
    last_active_at: int
    last_active_organization_id: str
    expire_at: int
    abandon_at: int


class Client(BaseModel):
    object: str
    id: str
    last_active_session_id: Optional[str] = None
    sign_in_attempt_id: Optional[str] = None
    sign_up_attempt_id: Optional[str] = None
    ended: bool = False


class IdentificationLink(BaseModel):
    type: str
    id: str


class Verification(BaseModel):
    status: str
    strategy: str


class PhoneNumber(BaseModel):
    object: str
    id: str
    phone_number: str
    reserved_for_second_factor: bool
    verification: Verification
    linked_to: List[IdentificationLink]


class EmailAddress(BaseModel):
    object: str
    id: str
    email_address: str
    verification: Verification
    linked_to: List[IdentificationLink]


class User(BaseModel):
    object: str
    id: str
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    gender: Optional[str] = None
    birthday: Optional[str] = None
    profile_image_url: str
    primary_email_address_id: Optional[str] = None
    primary_phone_number_id: Optional[str] = None
    password_enabled: bool
    two_factor_enabled: bool
    email_addresses: List[EmailAddress]
    phone_numbers: List[PhoneNumber]
    external_accounts: List[Any]
    public_metadata: Any
    private_metadata: Any
    created_at: int
    updated_at: int
    last_sign_in_at: int
    last_active_at: int


class Error(BaseModel):
    message: str
    long_message: str
    code: str
    meta: Optional[Any] = None


class VerifyRequest(BaseModel):
    token: str


class DeleteResponse(BaseModel):
    object: str
    id: str
    deleted: bool


class DeleteUserResponse(DeleteResponse):
    pass


class UpdateUserRequest(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    primary_email_address_id: Optional[str] = None
    primary_phone_number_id: Optional[str] = None
    profile_image: Optional[str] = None
    password: Optional[str] = None


class Organization(BaseModel):
    object: str
    id: str
    name: str
    slug: str
    max_allowed_memberships: int
    admin_delete_enabled: bool | None = None
    public_metadata: dict
    private_metadata: dict
    created_by: str | None = None
    image_url: str | None = None


class DeleteOrganizationResponse(DeleteResponse):
    pass


class UpdateOrganizationRequest(BaseModel):
    name: str | None = None
    slug: str | None = None
    max_allowed_memberships: int | None = None
    admin_delete_enabled: bool | None = None


class OrganizationMembership(BaseModel):
    id: str
    object: str
    role: str
    permissions: List[str]
    public_metadata: dict
    private_metadata: dict
    organization: Organization
    public_user_data: Any
    created_at: int
    updated_at: int
