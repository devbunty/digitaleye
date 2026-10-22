<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> a4a6984d66345eef2f7dd334c11aef9ee67fdefd
"""SQLAlchemy models.

Table and column names are unchanged from earlier releases, so existing
databases keep working.
"""

from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

import config
from database.timeutils import as_naive_utc, to_iso, utc_now
<<<<<<< HEAD
=======
=======
from datetime import datetime, UTC

from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import Boolean

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
>>>>>>> b7a3db521b7d140ae55a4dc93167ac6b9f9b2e15
>>>>>>> a4a6984d66345eef2f7dd334c11aef9ee67fdefd


class Base(DeclarativeBase):
    pass


class Host(Base):
<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> a4a6984d66345eef2f7dd334c11aef9ee67fdefd
    __tablename__ = "hosts"

    id: Mapped[int] = mapped_column(primary_key=True)
    hostname: Mapped[str] = mapped_column(String(100), unique=True)
    ip: Mapped[str] = mapped_column(String(50))
    os: Mapped[str] = mapped_column(String(100))
    kernel: Mapped[str] = mapped_column(String(100))
    first_seen: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    last_seen: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

    # True for hosts created through the "Add Host" demo flow (no agent is
    # reporting). Lets the UI badge them and makes them safe to delete; real
    # enrolled hosts can never be deleted through the API.
    is_demo: Mapped[bool] = mapped_column(Boolean, default=False)

    @property
    def is_online(self) -> bool:
        """Demo hosts are always online; real hosts need a recent heartbeat."""
        if self.is_demo:
            return True
        if not self.last_seen:
            return False
        age = utc_now().replace(tzinfo=None) - as_naive_utc(self.last_seen)
        return age.total_seconds() <= config.ONLINE_THRESHOLD_SECONDS

    @property
    def status(self) -> str:
        return "Online" if self.is_online else "Offline"


class Incident(Base):
    __tablename__ = "incidents"

    id: Mapped[int] = mapped_column(primary_key=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    hostname: Mapped[str] = mapped_column(String(100))
    rule_id: Mapped[str] = mapped_column(String(50))
    title: Mapped[str] = mapped_column(String(200))
    severity: Mapped[str] = mapped_column(String(30))
    mitre: Mapped[str] = mapped_column(String(50))
    category: Mapped[str] = mapped_column(String(100))
    evidence: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(20), default="Open")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "timestamp": to_iso(self.timestamp),
            "hostname": self.hostname,
            "rule_id": self.rule_id,
            "title": self.title,
            "severity": self.severity,
            "mitre": self.mitre,
            "category": self.category,
            "evidence": self.evidence,
            "status": self.status,
        }


class Telemetry(Base):
    __tablename__ = "telemetry"

    id: Mapped[int] = mapped_column(primary_key=True)
    hostname: Mapped[str] = mapped_column(String(100))
    collection_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    cpu_usage: Mapped[float] = mapped_column(default=0.0)
    memory_usage: Mapped[float] = mapped_column(default=0.0)
    process_count: Mapped[int] = mapped_column(default=0)


class Process(Base):
    __tablename__ = "processes"

    id: Mapped[int] = mapped_column(primary_key=True)
    hostname: Mapped[str] = mapped_column(String(100))
    collection_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    pid: Mapped[int] = mapped_column(Integer)
    name: Mapped[str] = mapped_column(String(200))
    user: Mapped[str] = mapped_column(String(100))
    cpu_percent: Mapped[float] = mapped_column(default=0.0)
    memory_percent: Mapped[float] = mapped_column(default=0.0)
    command: Mapped[str] = mapped_column(Text)

    def to_dict(self) -> dict:
        return {
            "hostname": self.hostname,
            "time": to_iso(self.collection_time),
            "pid": self.pid,
            "name": self.name,
            "user": self.user,
            "cpu": self.cpu_percent,
            "memory": self.memory_percent,
            "command": self.command,
        }
<<<<<<< HEAD
=======
=======

    __tablename__ = "hosts"

    id: Mapped[int] = mapped_column(primary_key=True)

    hostname: Mapped[str] = mapped_column(String(100), unique=True)

    ip: Mapped[str] = mapped_column(String(50))

    os: Mapped[str] = mapped_column(String(100))

    kernel: Mapped[str] = mapped_column(String(100))

    first_seen: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC)
    )

    last_seen: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC)
    )

    # True for hosts created via the "Add Host" demo flow (no real agent
    # reporting) rather than a live collector enrollment. Lets the UI
    # badge them and allows safe deletion — real enrolled hosts can't
    # be deleted through the API.
    is_demo: Mapped[bool] = mapped_column(Boolean, default=False)


class Incident(Base):

    __tablename__ = "incidents"

    id: Mapped[int] = mapped_column(primary_key=True)

    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC)
    )

    hostname: Mapped[str] = mapped_column(String(100))

    rule_id: Mapped[str] = mapped_column(String(50))

    title: Mapped[str] = mapped_column(String(200))

    severity: Mapped[str] = mapped_column(String(30))

    mitre: Mapped[str] = mapped_column(String(50))

    category: Mapped[str] = mapped_column(String(100))

    evidence: Mapped[str] = mapped_column(Text)

    status: Mapped[str] = mapped_column(String(20), default="Open")

class Telemetry(Base):

    __tablename__ = "telemetry"

    id: Mapped[int] = mapped_column(primary_key=True)

    hostname: Mapped[str] = mapped_column(String(100))

    collection_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC)
    )

    cpu_usage: Mapped[float] = mapped_column(default=0.0)

    memory_usage: Mapped[float] = mapped_column(default=0.0)

    process_count: Mapped[int] = mapped_column(default=0)

class Process(Base):

    __tablename__ = "processes"

    id: Mapped[int] = mapped_column(primary_key=True)

    hostname: Mapped[str] = mapped_column(String(100))

    collection_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC)
    )

    pid: Mapped[int] = mapped_column(Integer)

    name: Mapped[str] = mapped_column(String(200))

    user: Mapped[str] = mapped_column(String(100))

    cpu_percent: Mapped[float] = mapped_column(default=0.0)

    memory_percent: Mapped[float] = mapped_column(default=0.0)

    command: Mapped[str] = mapped_column(Text)
>>>>>>> b7a3db521b7d140ae55a4dc93167ac6b9f9b2e15
>>>>>>> a4a6984d66345eef2f7dd334c11aef9ee67fdefd
