from fastapi import FastAPI, HTTPException, Request, Response, Depends
from pydantic import BaseModel, EmailStr
from datetime import date, datetime, time, timedelta
from supabase import create_client, Client
from dotenv import load_dotenv
from database import engine,SessionLocal
import models 
import uuid
from typing import List,Annotated
from sqlalchemy.orm import Session
import os

load_dotenv()
app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency=Annotated[Session,Depends(get_db)]

#################################################################################################
#   MODELS
#################################################################################################

class PrimaryUserBase(BaseModel):
    email: EmailStr
    name: str
    dob: datetime
    profession: str = None
    hobby: str = None

class PrimaryUserUpdateBase(BaseModel):
    id : uuid.UUID
    # email: EmailStr = None
    name: str = None
    dob: datetime = None
    profession: str = None
    hobby: str = None

class SecondaryUserBase(BaseModel):
    name: str
    email: EmailStr

class SecondaryUserUpdateBase(BaseModel):
    id: uuid.UUID
    name: str = None

class RelationshipBase(BaseModel):
    primary_id: uuid.UUID
    secondary_id: uuid.UUID
    relationship: str

class RelationshipUpdateBase(BaseModel):
    id: uuid.UUID
    relationship: str = None


class PeriodEntryBase(BaseModel):
    primary_id: uuid.UUID
    start_date: datetime = None
    
class PeriodEntryUpdateBase(BaseModel):
    id: uuid.UUID
    start_date: datetime = None
    end_date: datetime = None
    duration: int = None

#################################################################################################
#   PRIMARY USER ENDPOINTS
#################################################################################################

@app.post("/primary_users")
async def createPrimaryUser(primaryUser: PrimaryUserBase, db:db_dependency):
    newPrimaryUser = models.PrimaryUser(
        email = primaryUser.email,
        name = primaryUser.name,
        dob = primaryUser.dob,
        profession = primaryUser.profession,
        hobby = primaryUser.hobby
    )
    
    try:
        db.add(newPrimaryUser)
        db.commit()
        db.refresh(newPrimaryUser)
    except:
        raise HTTPException(status_code=500,detail="Primary user creation failed")
    return newPrimaryUser

@app.get("/primary_users/{primary_user_id}")
async def getPrimaryUser(primary_user_id:uuid.UUID,db:db_dependency):
    result = db.query(models.PrimaryUser).filter(models.PrimaryUser.id == primary_user_id).first()
    if not result:
        raise HTTPException(status_code=404,detail="Primary user not found") 

@app.put("/primary_users")
async def updatePrimaryUser(newPrimaryUser: PrimaryUserUpdateBase, db:db_dependency):
    oldPrimaryUser = db.query(models.PrimaryUser).filter(models.PrimaryUser.id==newPrimaryUser.id).first()
    
    if oldPrimaryUser:
        
        if newPrimaryUser.name:
            oldPrimaryUser.name = newPrimaryUser.name
            
        if newPrimaryUser.dob:
            oldPrimaryUser.dob = newPrimaryUser.dob
            
        if newPrimaryUser.profession:
            oldPrimaryUser.profession = newPrimaryUser.profession
        
        if newPrimaryUser.hobby:
            oldPrimaryUser.hobby = newPrimaryUser.hobby
        
        db.commit()
        db.refresh(oldPrimaryUser)
        
    if not oldPrimaryUser:
        raise HTTPException(status_code=404,detail="Primary user not found")
    return oldPrimaryUser

#################################################################################################
#   SECONDARY USER ENDPOINTS
#################################################################################################

@app.post("/secondary_users")
async def createSecondaryUser(secondaryUser: SecondaryUserBase, db:db_dependency):
    newSecondaryUser = models.SecondaryUser(
        name = secondaryUser.name,
        email = secondaryUser.email
    )
    
    try:
        db.add(newSecondaryUser)
        db.commit()
        db.refresh(newSecondaryUser)
    except:
        raise HTTPException(status_code=500,detail="Secondary user creation failed")
    return newSecondaryUser

@app.get("/secondary_users/{secondary_user_id}")
async def getSecondaryUser(secondary_user_id:uuid.UUID,db:db_dependency):
    result = db.query(models.SecondaryUser).filter(models.SecondaryUser.id == secondary_user_id).first()
    if not result:
        raise HTTPException(status_code=404,detail="Secondary user not found") 

@app.put("/secondary_users")
async def updateSecondaryUser(newSecondaryUser: SecondaryUserUpdateBase, db:db_dependency):
    oldSecondaryUser = db.query(models.SecondaryUser).filter(models.SecondaryUser.id==newSecondaryUser.id).first()
    
    if oldSecondaryUser:
        if newSecondaryUser.name:
            oldSecondaryUser.name = newSecondaryUser.name
        
        db.commit()
        db.refresh(oldSecondaryUser)
        
    if not oldSecondaryUser:
        raise HTTPException(status_code=404,detail="Secondary user not found")
    return oldSecondaryUser

#################################################################################################
#   RELATIONSHIP ENDPOINTS
#################################################################################################

@app.post('/relationships')
async def createRelationship(relationship: RelationshipBase, db:db_dependency):
    newRelationship = models.Relationship(
        primary_id = relationship.primary_id,
        secondary_id = relationship.secondary_id,
        relationship = relationship.relationship
    )
    
    try:
        db.add(newRelationship)
        db.commit()
        db.refresh(newRelationship)
    except:
        raise HTTPException(status_code=500,detail="Relationship creation failed")
    return newRelationship

@app.get('/relationships/primary_users/{primary_user_id}')
async def getBasedOnPrimaryUserId(primary_user_id: uuid.UUID, db:db_dependency):
    allRelationships = db.query(models.Relationship).filter(models.Relationship.primary_id==primary_user_id).all()
    return allRelationships

@app.get('/relationships/secondary_users/{secondary_user_id}')
async def getBasedOnSecondaryUserId(secondary_user_id: uuid.UUID, db:db_dependency):
    allRelationships = db.query(models.Relationship).filter(models.Relationship.secondary_id==secondary_user_id).all()
    return allRelationships

@app.put('/relationships')
async def updateRelationship(newRelationship: RelationshipUpdateBase, db:db_dependency):
    oldRelationshop = db.query(models.Relationship).filter(models.Relationship.id == newRelationship.id).first()
    
    if oldRelationshop:
        
        if newRelationship.relationship:
            oldRelationshop.relationship = newRelationship.relationship
        
        db.commit()
        db.refresh(oldRelationshop)
        
    if not oldRelationshop:
        raise HTTPException(status_code=404,detail="Secondary user not found")
    return oldRelationshop

#################################################################################################
#   PERIOD ENDPOINTS
#################################################################################################

@app.post('period_entries')
async def createPeriodEntry(periodEntry: PeriodEntryBase, db:db_dependency):
    newPeriodEntries = models.PeriodEntry(
        primary_id = periodEntry.primary_id,
        start_date = periodEntry.start_date
    )
    
    try:
        db.add(newPeriodEntries)
        db.commit()
        db.refresh(newPeriodEntries)
    except:
        raise HTTPException(status_code=500,detail="Period entry creation failed")
    return newPeriodEntries

@app.get('period_entries/{primary_id}')
async def getPeriodEntry(primary_id: uuid.UUID, db:db_dependency):
    allEntries = db.query(models.PeriodEntry).filter(models.PeriodEntry.primary_id == primary_id).all()
    return allEntries

@app.put('period_entries')
async def updatePeriodEntry(newPeriodEntry: PeriodEntryUpdateBase, db:db_dependency):
    oldPeriodEntry = db.query(models.PeriodEntry).filter(models.PeriodEntry.id == newPeriodEntry.id).first()
    
    if oldPeriodEntry:
        if newPeriodEntry.end_date:
            oldPeriodEntry.end_date = newPeriodEntry.end_date
        if newPeriodEntry.duration:
            oldPeriodEntry.duration = newPeriodEntry.duration
            
    if not oldPeriodEntry:
        raise HTTPException(status_code=500,detail="Period entry not found")
    return oldPeriodEntry


#################################################################################################
#   PERIOD ENDPOINTS
#################################################################################################




#################################################################################################
#   AUTHENTICATION/AUTHORIZATION ENDPOINTS
#################################################################################################

# SUPABASE_URL = os.getenv("SUPABASE_URL")
# SUPABASE_API_KEY = os.getenv("SUPABASE_API_KEY")

# supabase: Client = create_client(SUPABASE_URL, SUPABASE_API_KEY)

# class UserAuth(BaseModel):
#     email: str
#     password: str

# @app.post("/signup")
# async def sign_up(user: UserAuth):
#     try:
#         response = supabase.auth.sign_up({
#             'email': user.email,
#             'password': user.password
#         })
#         if not response.user:
#             raise HTTPException(status_code=400, detail="Sign-up failed")
#         return {"message": "User signed up successfully"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @app.post("/signin")
# async def sign_in(user: UserAuth):
#     try:
#         response = supabase.auth.sign_in_with_password({
#             'email': user.email,
#             'password': user.password
#         })
#         if not response.user:
#             raise HTTPException(status_code=400, detail="Sign-in failed")
#         return {"message": "User signed in successfully", "session": response.session}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @app.middleware("http")
# async def authenticate_request(request: Request, call_next):
#     # Make some routes unprotected
#     if request.method == "OPTIONS" or request.url.path in ["/", "/docs", "/openapi.json", "/signup", "/signin"]:
#         return await call_next(request)

#     token = request.headers.get("authorization", "").replace("Bearer ", "")
#     print(f"Token: {token}")  # Log the token for debugging

#     if not token:
#         return Response("Unauthorized", status_code=401)

#     try:
#         # auth = supabase.auth.get_user(token)
#         # print(auth)
#         # request.state.user_id = auth.user.id
#         # print(request.state.user_id)
#         # await supabase.auth.set_auth(token)
#         # supabase.auth.set_auth(token)
#         auth_response = supabase.auth.get_user(token)
#         print(auth_response)
#         if not auth_response.user:
#             raise HTTPException(status_code=401, detail="Invalid user token")

#         request.state.user_id = auth_response.user.id
#         print(request.state.user_id)
#     except Exception as e:
#         print(f"Auth Error: {e}")  # Log the error for debugging
#         return Response("Invalid user token", status_code=401)

#     response = await call_next(request)
#     return response

# @app.get("/")
# async def root():
#     return {"message": "This is an unprotected route"}

# @app.get("/protected")
# async def protected_route(request: Request):
#     user_id = request.state.user_id
#     if not user_id:
#         raise HTTPException(status_code=401, detail="Unauthorized")
#     return {"message": f"Hello, user {user_id}"}

# @app.post("/protected/data")
# async def protected_data(request: Request):
#     user_id = request.state.user_id
#     if not user_id:
#         raise HTTPException(status_code=401, detail="Unauthorized")
#     return {"message": f"Data saved for user {user_id}"}

# @app.post("/logout")
# async def log_out(request: Request):
#     user_id = request.state.user_id
#     if not user_id:
#         raise HTTPException(status_code=401, detail="Unauthorized")
    
#     try:
#         supabase.auth.sign_out()
#         return {"message": "User logged out successfully"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
