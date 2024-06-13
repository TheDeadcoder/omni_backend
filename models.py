from sqlalchemy import Column, String, Integer, Date, ForeignKey, JSON, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid

Base = declarative_base()

class PrimaryUser(Base):
    __tablename__ = "primary_user"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False)
    dob = Column(Date, nullable=False)
    profession = Column(String, nullable=True)
    hobby = Column(String, nullable=True)

class SecondaryUser(Base):
    __tablename__ = "secondary_user"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False)

class Relationship(Base):
    __tablename__ = "relationship"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    primary_id = Column(UUID(as_uuid=True), ForeignKey('primary_user.id'), nullable=False)
    secondary_id = Column(UUID(as_uuid=True),  ForeignKey('secondary_user.id'), nullable=False)
    relationship = Column(String, nullable=False)
    accepted = Column(Boolean, nullable=False, default=False)

class HistoryOfIllness(Base):
    __tablename__ = "history_of_illness"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    primary_id = Column(UUID(as_uuid=True), ForeignKey('primary_user.id'), nullable=False)
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
    
class PeriodEntry(Base):
    __tablename__ = "period_table"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    primary_id = Column(UUID(as_uuid=True), ForeignKey('primary_user.id'), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    duration = Column(Integer, nullable=True)

class CalendarEntry(Base):
    __tablename__ = "calendar_entry"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    primary_id = Column(UUID(as_uuid=True), ForeignKey('primary_user.id'), nullable=False)
    date = Column(Date, nullable=False)
    symptom_name = Column(String, nullable="False")
    symptom_value = Column(String, nullable="False")
    symptom_unit = Column(String, nullable="True")