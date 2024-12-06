from typing import Optional

from sqlalchemy import BOOLEAN, TIMESTAMP, VARCHAR, String, false, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database.models import Base, TableNameMixin


class User(TableNameMixin, Base):
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(
        VARCHAR(128), unique=True, index=True, nullable=False
    )
    first_name: Mapped[str] = mapped_column(VARCHAR(128), unique=True)
    last_name: Mapped[str] = mapped_column(VARCHAR(128), unique=True)
    email: Mapped[str] = mapped_column(VARCHAR(255), unique=True)
    image: Mapped[Optional[str]] = mapped_column(
        String, nullable=True, default="user.png"
    )
    password: Mapped[str] = mapped_column(String)
    is_superuser: Mapped[bool] = mapped_column(BOOLEAN, server_default=false())
    created_at: Mapped[func.now()] = mapped_column(
        TIMESTAMP, server_default=func.now(), nullable=False
    )

    def __repr__(self):
        return f"{self.username}"
