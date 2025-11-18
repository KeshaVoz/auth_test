from enum import Enum
from typing import List, Optional
import uuid
from pydantic import BaseModel, EmailStr, Field
class SRoleEnum(str, Enum):
    SUPERUSER = "SuperUser"
    ADMIN = "Admin"
    USER = "User"

class SActionEnum(str, Enum):
    READ_ALL = "readallpermission"
    CREATE_ALL = "createallpermission"
    UPDATE_ALL = "updateallpermission"
    DELETE_ALL = "deleteallpermission"

class SResourceEnum(str, Enum):
    USERS = "users"
    ADMINS = "admins"
    SUPERUSERS = "superusers"

class SPermission(BaseModel):
    id: uuid.UUID
    resource: SResourceEnum
    action: SActionEnum

    model_config = dict(from_attributes=True)

class SRole(BaseModel):
    id: uuid.UUID
    name: SRoleEnum
    description: Optional[str]
    permissions: List[SPermission] = []

    model_config = dict(from_attributes=True)

class SUser(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr

    model_config = dict(from_attributes=True)

class SUserRegister(BaseModel):
    first_name: str = Field(..., )
    last_name: str = Field(..., )
    email: EmailStr
    password: str = Field(..., )

    model_config = dict(from_attributes=False)

class SUserLogin(BaseModel):
    email: EmailStr = Field(..., )
    password: str = Field(..., )

    model_config = dict(from_attributes=False)