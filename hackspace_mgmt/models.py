import enum
from sqlalchemy import String, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class InductionState(enum.Enum):
    valid = "valid"
    expired =  "expired"
    banned =  "banned"

    def __str__(self):
        return f'{self.name}'

class Member(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    discourse_id: Mapped[Optional[int]] = mapped_column(unique=True)
    preferred_name: Mapped[str] = mapped_column(String(200), nullable=False)
    cards: Mapped[List["Card"]] = relationship(back_populates="member")
    inductions: Mapped[List["Induction"]] = relationship(back_populates="member")

    def __str__(self):
        return self.preferred_name

class Card(db.Model):
    card_id: Mapped[int] = mapped_column(primary_key=True)
    card_serial: Mapped[int] = mapped_column(unique=True)
    member_id: Mapped[int] = mapped_column(ForeignKey("member.id"))
    member: Mapped["Member"] = relationship(back_populates="cards")

    def __str__(self):
        return f"#{self.card_id}"

class Machine(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    controllers: Mapped[List["MachineController"]] = relationship(back_populates="machine")
    inductions: Mapped[List["Induction"]] = relationship(back_populates="machine")

    def __str__(self):
        return self.name

class MachineController(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    mac: Mapped[int] = mapped_column(unique=True)
    machine_id: Mapped[int] = mapped_column(ForeignKey("machine.id"))
    machine: Mapped["Machine"] = relationship(back_populates="controllers")
    requires_update: Mapped[bool] = mapped_column()

    def __str__(self):
        return hex(self.mac)

class Induction(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    member_id: Mapped[int] = mapped_column(ForeignKey("member.id"))
    machine_id: Mapped[int] = mapped_column(ForeignKey("machine.id"))
    state: Mapped[InductionState] = mapped_column(nullable=False)
    member: Mapped["Member"] = relationship(back_populates="inductions")
    machine: Mapped["Machine"] = relationship(back_populates="inductions")
