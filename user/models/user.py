from sqlalchemy import Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)
from datetime import datetime
from passlib.context import CryptContext
from db import Base


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class TimeStampModel(Base):
    __abstract__ = True
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )


class User(TimeStampModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)
    profile_pic: Mapped[str] = mapped_column(String(500), nullable=True)
    first_name: Mapped[str] = mapped_column(String, index=True, nullable=True)
    last_name: Mapped[str] = mapped_column(String, index=True, nullable=True)
    email: Mapped[str] = mapped_column(
        String,
        unique=True,
        index=True,
        nullable=False,
    )
    password: Mapped[str] = mapped_column(String, nullable=False)

    # One-to-One relationship
    preference: Mapped["Preference"] = relationship(
        "Preference",
        back_populates="user",
        uselist=False,
        passive_deletes=True,
    )

    # One-to-Many relationship
    addresses: Mapped[list["Address"]] = relationship(
        "Address", back_populates="user", passive_deletes=True
    )

    # Many-to-Many relationship
    roles: Mapped[list["Role"]] = relationship(
        "Role",
        secondary="user_roles",
        back_populates="users",
        passive_deletes=True,
    )
   
    # members: Mapped[list["Member"]] = relationship("Member", back_populates="user",lazy="selectin")

    def set_password(self, password: str):
        if password:
            self.password = pwd_context.hash(password)
        else:
            print("Received empty password!")

    def verify_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.password)

    def __repr__(self):
        return f"User(name={self.first_name})"


# (One-to-One with User)
class Preference(TimeStampModel):
    __tablename__ = "preferences"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    language: Mapped[str] = mapped_column(String(80), nullable=False)
    currency_code: Mapped[str] = mapped_column(String(3), nullable=False)
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )

    user: Mapped["User"] = relationship("User", back_populates="preference")


# (One-to-Many with User)
class Address(TimeStampModel):
    __tablename__ = "addresses"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    road_name: Mapped[str] = mapped_column(String(80), nullable=False)
    post_code: Mapped[str] = mapped_column(String(80), nullable=False)
    city: Mapped[str] = mapped_column(String(80), nullable=False)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    user: Mapped["User"] = relationship("User", back_populates="addresses")

    def __repr__(self):
        return f"Address(city={self.city})"


#  (Many-to-Many with User)
class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    slug: Mapped[str] = mapped_column(String(80), nullable=False, unique=True)

    users: Mapped[list["User"]] = relationship(
        "User",
        secondary="user_roles",
        back_populates="roles",
        passive_deletes=True,
    )

    def __repr__(self):
        return f"Role(name={self.name})"


#  User-Role association table (Many-to-Many)
class UserRole(Base):
    __tablename__ = "user_roles"

    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    role_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True
    )
