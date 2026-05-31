from sqlalchemy import (
    create_engine,
    String,
    Integer,
    DateTime,
    Index,
    Text,
    func,
    ForeignKey,
)
from sqlalchemy.orm import sessionmaker, DeclarativeBase, mapped_column, Mapped
from central.common import connectionstring
from datetime import datetime, timezone

engine = create_engine(connectionstring)  # type:ignore
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Latest way of using Declarative Base Class
class Base(DeclarativeBase):
    pass


# Users model
class Users(Base):
    __tablename__ = "users"

    uid: Mapped[str] = mapped_column(
        String(36), primary_key=True
    )  # code can be used for every db whether mysql or postgres

    username: Mapped[str] = mapped_column(String(255), index=True)
    # Use Mapped[str] to tell the type checker this is a string, not a Column object
    password: Mapped[str] = mapped_column(String(255), nullable=False)


# Database Model (Our table structure)
class AppUsers(Base):
    __tablename__ = "appusers"

    serial_no: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    uid: Mapped[str] = mapped_column(String(36), ForeignKey("users.uid"))
    emp_no: Mapped[int] = mapped_column(Integer, nullable=False, index=True) # Employee ID column
    convo_id: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    request: Mapped[str] = mapped_column(Text, nullable=False)
    response: Mapped[str] = mapped_column(Text, nullable=False)
    chat_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        server_default=func.now(),
    )

    __table_args__ = (Index("index_conv_date", "convo_id", "chat_date"),)


# using get_db() as dependancy
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
