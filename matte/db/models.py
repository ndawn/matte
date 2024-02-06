from datetime import datetime
from datetime import timezone
from typing import Any

from sqlalchemy import func
from sqlalchemy import BigInteger
from sqlalchemy import ForeignKey
from sqlalchemy import UniqueConstraint
from sqlalchemy import UUID
from sqlalchemy.dialects.postgresql.json import JSON
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import MappedAsDataclass
from sqlalchemy.orm.attributes import flag_modified


class Model(MappedAsDataclass, DeclarativeBase):
    type_annotation_map = {
        dict[str, Any]: JSON,
    }


class User(Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger(), primary_key=True, autoincrement=False)
    chat_id: Mapped[int] = mapped_column(BigInteger(), nullable=False)
    is_admin: Mapped[bool] = mapped_column(init=False, default=False)
    language: Mapped[str] = mapped_column(nullable=False)
    settings: Mapped[dict[str, bool]] = mapped_column(JSON, nullable=False)
    sources: Mapped[list["Source"]] = relationship(back_populates="user", lazy="joined")

    def promote(self) -> None:
        self.is_admin = True  # type: ignore

    def demote(self) -> None:
        self.is_admin = False  # type: ignore

    def toggle_setting(self, name: str) -> bool:
        self.settings[name] = not self.settings[name]
        flag_modified(self, "settings")
        return self.settings[name]  # type: ignore


class Source(Model):
    __tablename__ = "sources"

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), init=False)
    user: Mapped["User"] = relationship(back_populates="sources", lazy="joined")
    name: Mapped[str] = mapped_column(nullable=False)
    home_link: Mapped[str] = mapped_column(nullable=False)
    link: Mapped[str] = mapped_column(nullable=False)
    last_updated: Mapped[datetime] = mapped_column(insert_default=func.now())
    is_disabled: Mapped[bool] = mapped_column(default=False, init=False)

    __table_args__ = (UniqueConstraint("user_id", "link", name="source_user_link_uc"),)

    def enable(self) -> None:
        self.is_disabled = False  # type: ignore

    def disable(self) -> None:
        self.is_disabled = True  # type: ignore

    def bump(self, timestamp: datetime | None = None) -> None:
        self.last_updated = timestamp or datetime.now(timezone.utc)  # type: ignore


class PostUrl(Model):
    __tablename__ = "urls"

    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True)
    url: Mapped[str] = mapped_column(nullable=False)
