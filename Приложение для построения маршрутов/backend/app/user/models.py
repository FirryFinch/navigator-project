from app.base.db import db
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from app.user.dataclasses import AccessClassDC, RoleDC


class UserModel(db):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    login = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)

    access = relationship(
        "RoleModel",
        back_populates="user",
        foreign_keys="RoleModel.user_id",
    )
    usermade = relationship(
        "ObjectDrawingModel", back_populates="usermade", foreign_keys="ObjectDrawingModel.creator_id"
    )
    useredit = relationship(
        "ObjectDrawingModel", back_populates="useredit", foreign_keys="ObjectDrawingModel.editor_id"
    )


class AccessClassModel(db):
    __tablename__ = "access"

    id = Column(Integer, primary_key=True, autoincrement=True)
    category_name = Column(String, unique=True, nullable=False)

    accessgiven = relationship(
        "RoleModel",
        back_populates="accessgiven",
        foreign_keys="RoleModel.access_id",
    )

    def to_dc(self) -> AccessClassDC:
        return AccessClassDC(
            id=self.id,
            category_name=self.category_name,
        )


class RoleModel(db):
    __tablename__ = "role"

    id = Column(Integer, primary_key=True, autoincrement=True)
    role_name = Column(String, unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="cascade"), nullable=False)
    access_id = Column(Integer, ForeignKey("access.id", ondelete="cascade"), nullable=False)
    assignment_role_time = Column(DateTime, nullable=True)

    __table_args__ = (UniqueConstraint("user_id", "access_id", name="_user_access_uc"),)
    user = relationship(
        "UserModel",
        back_populates="access",
        foreign_keys="RoleModel.user_id",
    )
    accessgiven = relationship(
        "AccessClassModel",
        back_populates="accessgiven",
        foreign_keys="RoleModel.access_id",
    )

    def to_dc(self) -> RoleDC:
        return RoleDC(
            id=self.id,
            role_name=self.role_name,
            access_id=self.access_id,
            assignment_role_time=self.assignment_role_time,
            user_id=self.user_id,
        )
