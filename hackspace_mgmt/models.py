import enum
from sqlalchemy import String, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class InductionState(enum.Enum):
    valid = 1
    expired = 2
    banned = 3

class Member(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    discourse_id: Mapped[Optional[int]] = mapped_column(unique=True)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    cards: Mapped[List["Card"]] = relationship(back_populates="member")

class Card(db.Model):
    card_id: Mapped[int] = mapped_column(primary_key=True)
    card_serial: Mapped[int] = mapped_column(unique=True)
    member_id: Mapped[int] = mapped_column(ForeignKey("member.id"))
    member: Mapped["Member"] = relationship(back_populates="cards")

class Machine(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    controllers: Mapped[List["MachineController"]] = relationship(back_populates="machine")

class MachineController(db.Model):
    mac: Mapped[int] = mapped_column(primary_key=True)
    machine_id: Mapped[int] = mapped_column(ForeignKey("machine.id"))
    machine: Mapped["Machine"] = relationship(back_populates="controllers")
    requires_update: Mapped[bool] = mapped_column()

class Induction(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    member_id: Mapped[int] = mapped_column(ForeignKey("member.id"))
    machine_id: Mapped[int] = mapped_column(ForeignKey("machine.id"))
    state: Mapped[InductionState] = mapped_column(nullable=False)
