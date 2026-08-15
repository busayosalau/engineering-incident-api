from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Incident(Base):
    __tablename__ = "incidents"

    incident_id: Mapped[str] = mapped_column(
        String,
        primary_key=True
    )

    description: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    production_line: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String,
        nullable=False
    )
