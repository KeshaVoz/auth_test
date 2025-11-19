import enum
import random
import uuid
from sqlalchemy import ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base
from datetime import datetime
from typing import List


class RoleEnum(str, enum.Enum):
    SUPERUSER = "SuperUser"
    ADMIN = "Admin"
    USER = "User"


class ActionEnum(str, enum.Enum):
    READ_ALL = "readallpermission"
    CREATE_ALL = "createallpermission"
    UPDATE_ALL = "updateallpermission"
    DELETE_ALL = "deleteallpermission"


class ResourceEnum(str, enum.Enum):
    USERS = "users"
    ADMINS = "admins"
    SUPERUSERS = "superusers"


class User(Base):
    __tablename__ = 'users'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    is_deleted: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    role_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('roles.id'))
    role: Mapped["Role"] = relationship('Role', back_populates='users', lazy='selectin')

    @property
    def user_data(self) -> int:
        if not hasattr(self, '_user_data'):
            self._user_data = [random.randint(0, 100) for _ in range(5)]
        return random.choice(self._user_data)

    @user_data.setter
    def user_data(self, value):
        raise AttributeError("UPDATING THIS PROPERTY IS FORBIDDEN!!11!")
    
    @property
    def admin_data(self) -> int:
        if not hasattr(self, '_admin_data'):
            self._admin_data = 'DATA FOR ADMINS ONLY'
        return self._admin_data

    @admin_data.setter
    def admin_data(self, value):
        raise AttributeError("UPDATING THIS PROPERTY IS FORBIDDEN!!11!")


class Role(Base):
    __tablename__ = 'roles'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    description: Mapped[str] = mapped_column(nullable=True)

    users: Mapped[List[User]] = relationship('User', back_populates='role', lazy='selectin')
    permissions: Mapped[List["Permission"]] = relationship('Permission', secondary='role_permissions', back_populates='roles', lazy='selectin')

    def __str__(self):
        return f'Role {self.name}'


class Permission(Base):
    __tablename__ = 'permissions'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    resource: Mapped[str] = mapped_column(nullable=False)
    action: Mapped[str] = mapped_column(nullable=False)

    roles: Mapped[List[Role]] = relationship('Role', secondary='role_permissions', back_populates='permissions', lazy='selectin')

    def __str__(self):
        return f'Permission {self.resource} {self.action}'


class RolePermission(Base):
    __tablename__ = 'role_permissions'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    role_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('roles.id'), nullable=False)
    permission_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('permissions.id'), nullable=False)