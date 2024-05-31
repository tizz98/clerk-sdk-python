from typing import Any

from pydantic import BaseModel


class Session(BaseModel):
    object: str
    id: str
    client_id: str
    user_id: str
    status: str
    last_active_at: int
    expire_at: int
    abandon_at: int


class Client(BaseModel):
    object: str
    id: str
    last_active_session_id: str | None = None
    sign_in_attempt_id: str | None = None
    sign_up_attempt_id: str | None = None
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
    linked_to: list[IdentificationLink]


class EmailAddress(BaseModel):
    object: str
    id: str
    email_address: str
    verification: Verification
    linked_to: list[IdentificationLink]


class User(BaseModel):
    object: str
    id: str
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    gender: str | None = None
    birthday: str | None = None
    profile_image_url: str
    primary_email_address_id: str | None = None
    primary_phone_number_id: str | None = None
    password_enabled: bool
    two_factor_enabled: bool
    email_addresses: list[EmailAddress]
    phone_numbers: list[PhoneNumber]
    external_accounts: list[Any]
    public_metadata: Any
    unsafe_metadata: Any
    private_metadata: Any
    created_at: int
    updated_at: int


class Error(BaseModel):
    message: str
    long_message: str
    code: str
    meta: Any | None = None


class VerifyRequest(BaseModel):
    token: str


class DeleteUserResponse(BaseModel):
    object: str
    id: str
    deleted: bool


class UpdateUserRequest(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    primary_email_address_id: str | None = None
    primary_phone_number_id: str | None = None
    profile_image: str | None = None
    password: str | None = None
