from sqlalchemy import Column, String, Integer, Date, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid

Base = declarative_base()

class PrimaryUser(Base):
    __tablename__ = "primary_user"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, nullable=False, unique=True)  # Add email column
    name = Column(String, nullable=False)
    dob = Column(Date, nullable=False)
    profession = Column(String, nullable=True)
    hobby = Column(String, nullable=True)
    super_id = Column(UUID(as_uuid=True), ForeignKey('primary_user.id'), nullable=True)  # Add super_id column

class SecondaryUser(Base):
    __tablename__ = "secondary_user"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    primary_id = Column(UUID(as_uuid=True), ForeignKey('primary_user.id'), nullable=False)
    name = Column(String, nullable=False)
    relationship = Column(String, nullable=False)

class HistoryOfIllness(Base):
    __tablename__ = "history_of_illness"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('primary_user.id'), nullable=False)
    illness_name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    date = Column(Date, nullable=False)

class Hospital(Base):
    __tablename__ = "hospital"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    latitude = Column(String, nullable=True)
    longitude = Column(String, nullable=True)
    doctors = Column(JSON, nullable=True)

class CalendarEntry(Base):
    __tablename__ = "calendar_entry"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('primary_user.id'), nullable=False)
    date = Column(Date, nullable=False)

class CalendarEntryDetails(Base):
    __tablename__ = "calendar_entry_details"
    id = Column(Integer, primary_key=True, autoincrement=True)
    calendar_entry_id = Column(Integer, ForeignKey('calendar_entry.id'), nullable=False)
    details = Column(JSON, nullable=True)
