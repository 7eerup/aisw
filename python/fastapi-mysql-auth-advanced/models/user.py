from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
    )

    password: Mapped[str] = mapped_column(
        String(255),
        nullable=True,
    )

    name: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    categories: Mapped[list["Category"]] = relationship(
        "Category",
        back_populates="user",
    )

    memos: Mapped[list["Memo"]] = relationship(
        "Memo",
        back_populates="user",
    )
