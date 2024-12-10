from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from __init__ import this_is_funtion
# Database connection URL
DATABASE_URL = "mysql+mysqlconnector://root:Satwik62844&@localhost/testing_database"

# SQLAlchemy engine and session setup
engine = create_engine(DATABASE_URL, pool_size=10, max_overflow=20, pool_timeout=30)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define the User model
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    email = Column(String(255), unique=True, index=True)

# Create tables if not already created
Base.metadata.create_all(bind=engine)

# FastAPI app
app = FastAPI()

# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic model to validate the request body
class UserCreate(BaseModel):
    name: str
    email: str

# POST request to create a user
@app.post("/users/")
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(name=user.name, email=user.email)  # Create a new user from the Pydantic model
    db.add(db_user)  # Add to the session
    db.commit()  # Commit the transaction to the database
    db.refresh(db_user)  # Refresh to get the updated user (including the ID)
    return db_user  # Return the created user

# GET request to get all users
@app.get("/users/info")
async def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    this_is_funtion().capitalize
    return users

# GET request to get a user by ID
@app.get("/users/{user_id}")
async def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
