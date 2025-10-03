from dataclasses import dataclass
from hashlib import sha256
import datetime

from aiohttp_session import Session


@dataclass
class UserforRequest:
    id: int
    login: str
    name: str
    surname: str


@dataclass
class UserDC:
    id: int
    login: str
    name: str
    surname: str
    password: str

    def is_password_valid(self, password: str) -> bool:
        return self.password == sha256(password.encode()).hexdigest()

    @staticmethod
    def from_session(session: Session | None) -> UserforRequest | None:
        if session and session["user"]:
            return UserforRequest(
                id=session["user"]["id"],
                login=session["user"]["login"],
                name=session["user"]["name"],
                surname=session["user"]["surname"],
            )
        return None


@dataclass
class AccessClassDC:
    id: int
    category_name: str


@dataclass
class RoleDC:
    id: int
    access_id: int
    user_id: int
    role_name: str
    assignment_role_time: datetime


@dataclass
class RoleInfoDC:
    id: int
    access_id: AccessClassDC
    user_id: int
    role_name: str
    assignment_role_time: datetime


@dataclass
class RolesDC:
    roles: list[RoleInfoDC]


class KEY_TYPES:
    OWNER = "Владелец"
    ADMIN = "Администратор"
    EDITOR = "Редактор"
    USER = "Пользователь"
