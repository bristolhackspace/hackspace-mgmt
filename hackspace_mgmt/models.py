import enum
from sqlalchemy import JSON, String, ForeignKey, Enum, UniqueConstraint, types, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql import expression
from sqlalchemy.sql.functions import coalesce, concat
from sqlalchemy import cast
from typing import Optional, List
from datetime import date, datetime, timedelta, timezone

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class UTCDateTime(types.TypeDecorator):

    impl = types.DateTime
    cache_ok = True

    def process_bind_param(self, value, engine):
        if value is None:
            return
        if value.utcoffset() is None:
            raise ValueError(
                'Got naive datetime while timezone-aware is expected'
            )
        return value.astimezone(timezone.utc).replace(
            tzinfo=None
        )

    def process_result_value(self, value, engine):
        if value is not None:
            return value.replace(tzinfo=timezone.utc)


class DiscourseInvite(enum.Enum):
    no = "no"
    invited = "invited"
    emailed = "emailed"
    accepted = "accepted"
    alumni = "alumni"

    def __str__(self):
        return f'{self.name}'

class LegacyMachineAuth(enum.Enum):
    none = "none"
    password =  "password"
    padlock =  "padlock"

    def __str__(self):
        return f'{self.name}'


class Member(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(80), nullable=False)
    last_name: Mapped[str] = mapped_column(String(80), nullable=True)
    preferred_name: Mapped[str] = mapped_column(String(160), nullable=True)

    discourse: Mapped[DiscourseInvite] = mapped_column(Enum(DiscourseInvite, name="discourse_invite"), nullable=False, default=DiscourseInvite.no)
    newsletter: Mapped[bool] = mapped_column(nullable=False, default=False)
    welcome_email_sent: Mapped[bool] = mapped_column(nullable=False, default=False)
    email: Mapped[str] = mapped_column(String(300), nullable=True)
    alt_email: Mapped[str] = mapped_column(String(300), nullable=True)
    payment_ref: Mapped[str] = mapped_column(String(200), nullable=True)
    payment_active: Mapped[bool] = mapped_column(nullable=False, default=False)
    join_date: Mapped[date] = mapped_column(nullable=False, default=date.today)
    end_date: Mapped[date] = mapped_column(nullable=True)
    end_reason: Mapped[str] = mapped_column(String(500), nullable=True)
    address1: Mapped[str] = mapped_column(String(200), nullable=False, default="")
    address2: Mapped[str] = mapped_column(String(200), nullable=False, default="")
    town_city: Mapped[str] = mapped_column(String(200), nullable=False, default="")
    county: Mapped[str] = mapped_column(String(200), nullable=False, default="")
    postcode: Mapped[str] = mapped_column(String(20), nullable=False, default="")
    notes: Mapped[str] = mapped_column(String(), nullable=True)

    discourse_id: Mapped[Optional[int]] = mapped_column(unique=True)

    cards: Mapped[List["Card"]] = relationship(back_populates="member")
    inductions: Mapped[List["Induction"]] = relationship(back_populates="member", foreign_keys="Induction.member_id")
    labels: Mapped[List["Label"]] = relationship(back_populates="member")

    quiz_completions: Mapped[List["QuizCompletion"]] = relationship(back_populates="member")

    @hybrid_property
    def display_name(self):
        if self.preferred_name:
            return self.preferred_name
        else:
            last_name = self.last_name or ""
            return f"{self.first_name} {last_name}".strip()

    @display_name.expression
    def display_name(cls):
        return coalesce(cls.preferred_name, concat(cast(cls.first_name, db.String), cls.last_name))

    def __str__(self):
        return self.display_name

class Card(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    card_serial: Mapped[int] = mapped_column(unique=True, nullable=True)
    number_on_front: Mapped[int] = mapped_column(unique=True, nullable=True)
    member_id: Mapped[int] = mapped_column(ForeignKey("member.id"), nullable=True)
    lost: Mapped[bool] = mapped_column(nullable=False, default=False)
    unverified_serial: Mapped[int] = mapped_column(unique=True, nullable=True)
    door_disabled: Mapped[bool] = mapped_column(nullable=False, default=False)

    member: Mapped["Member"] = relationship(back_populates="cards")

    def __str__(self):
        return f"#{self.number_on_front}"

class Machine(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    legacy_auth: Mapped[LegacyMachineAuth] = mapped_column(Enum(LegacyMachineAuth, name="legacy_auth"), nullable=False, default=LegacyMachineAuth.none)
    legacy_password: Mapped[str] = mapped_column(String(255), nullable=False, default="")
    hide_from_home: Mapped[bool] = mapped_column(nullable=False, default=False)
    requires_in_person: Mapped[bool] = mapped_column(server_default=expression.false())
    induction_valid_for_days: Mapped[int] = mapped_column(server_default="0")

    controllers: Mapped[List["MachineController"]] = relationship(back_populates="machine")
    inductions: Mapped[List["Induction"]] = relationship(back_populates="machine")
    quizzes: Mapped[List["Quiz"]] = relationship(secondary="machine_quiz")

    def is_member_inducted(self, member: Member, check_can_induct=False):
        member_quizzes = set(completion.quiz for completion in member.quiz_completions if not completion.has_expired())
        machine_quizzes = set(self.quizzes)

        in_person_satisfied = False
        if self.requires_in_person:
            for induction in member.inductions:
                if induction.machine == self:
                    if induction.has_expired():
                        break
                    if not check_can_induct or induction.can_induct:
                        in_person_satisfied = True
                    break
        else:
            in_person_satisfied = True

        return member_quizzes >= machine_quizzes and in_person_satisfied

    def __str__(self):
        return self.name

class MachineController(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    machine_id: Mapped[int] = mapped_column(ForeignKey("machine.id"))
    machine: Mapped["Machine"] = relationship(back_populates="controllers")
    requires_update: Mapped[bool] = mapped_column()
    powered: Mapped[bool] = mapped_column()
    idle_timeout: Mapped[int] = mapped_column(nullable=False, default=-1)
    idle_power_threshold: Mapped[int] = mapped_column(nullable=False, default=50)
    invert_logout_button: Mapped[bool] = mapped_column(nullable=False, default=False)
    hostname: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)

    def __str__(self):
        return self.hostname

class Induction(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    member_id: Mapped[int] = mapped_column(ForeignKey("member.id"))
    machine_id: Mapped[int] = mapped_column(ForeignKey("machine.id"))
    inducted_by: Mapped[Optional[int]] = mapped_column(ForeignKey("member.id"))
    inducted_on: Mapped[Optional[datetime]] = mapped_column(UTCDateTime)
    can_induct: Mapped[bool] = mapped_column(nullable=False, default=False)

    member: Mapped["Member"] = relationship(back_populates="inductions", foreign_keys=[member_id])
    inductor: Mapped[Optional["Member"]] = relationship(foreign_keys=[inducted_by])
    machine: Mapped["Machine"] = relationship(back_populates="inductions")

    __table_args__ = (UniqueConstraint("member_id", "machine_id"),)

    def has_expired(self):
        valid_days = self.machine.induction_valid_for_days
        if valid_days <= 0:
            return False
        return self.inducted_on + timedelta(days=valid_days) < datetime.now(timezone.utc)

    def remaining_time(self):
        valid_days = self.machine.induction_valid_for_days
        if valid_days <= 0:
            return None
        return (self.inducted_on + timedelta(days=valid_days)) - datetime.now(timezone.utc)


class Label(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    member_id: Mapped[int] = mapped_column(ForeignKey("member.id"), nullable=True)
    expiry: Mapped[date] = mapped_column(nullable=False)
    caption: Mapped[str] = mapped_column(String(255), nullable=False)
    printed: Mapped[bool] = mapped_column(nullable=False, default=False)

    member: Mapped["Member"] = relationship(back_populates="labels")

class Quiz(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(), nullable=True)
    questions: Mapped[str] = mapped_column(String(), nullable=False)
    intro: Mapped[str] = mapped_column(String(), nullable=False, default="")
    valid_for_days: Mapped[int] = mapped_column(server_default="0")

    def __str__(self):
        return self.title

class QuizCompletion(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    quiz_id: Mapped[int] = mapped_column(ForeignKey("quiz.id"))
    member_id: Mapped[int] = mapped_column(ForeignKey("member.id"))
    completed_on: Mapped[datetime] = mapped_column(UTCDateTime)

    __table_args__ = (UniqueConstraint("quiz_id", "member_id"),)

    quiz: Mapped["Quiz"] = relationship()
    member: Mapped["Member"] = relationship()

    def has_expired(self):
        valid_days = self.quiz.valid_for_days
        if valid_days <= 0:
            return False
        return self.completed_on + timedelta(days=valid_days) < datetime.now(timezone.utc)

    def remaining_time(self):
        valid_days = self.quiz.valid_for_days
        if valid_days <= 0:
            return None
        return (self.completed_on + timedelta(days=valid_days)) - datetime.now(timezone.utc)


class MachineQuiz(db.Model):
    machine_id: Mapped[int] = mapped_column(ForeignKey("machine.id"), primary_key=True)
    quiz_id: Mapped[int] = mapped_column(ForeignKey("quiz.id"), primary_key=True)


class AuditLog(db.Model):
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    logged_at: Mapped[datetime] = mapped_column(UTCDateTime)
    category: Mapped[str] = mapped_column(String(32))
    event: Mapped[str] = mapped_column(String(32))
    member_id: Mapped[int] = mapped_column(ForeignKey("member.id"))
    data: Mapped[Optional[JSON]] = mapped_column(type_=JSON)