from database import Base, engine
# from models import PrimaryUser, SecondaryUser, HistoryOfIllness, Hospital, CalendarEntry, CalendarEntryDetails

# Create all tables
Base.metadata.create_all(bind=engine)
