from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
import databases
from pydantic import BaseModel
from typing import List
import os

DATABASE_URL = f"mysql+pymysql://{os.environ['DB_USERNAME']}:{os.environ['DB_PASSWORD']}@db:3306/fastapi"

Base = declarative_base()

class Character(Base):
    __tablename__ = "characters"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    story = Column(Text)

# SQLAlchemy
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

database = databases.Database(DATABASE_URL)

app = FastAPI()

def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic
class CharacterCreate(BaseModel):
    name: str
    story: str

class CharacterOut(BaseModel):
    id: int
    name: str
    story: str

    class Config:
        orm_mode = True

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# Exemplo de rota FastAPI
@app.get("/")
async def read_root():
    return {"Ola": "Mundo!!"}

# CRUD
def create_character(db: Session, character: CharacterCreate):
    db_character = Character(name=character.name, story=character.story)
    db.add(db_character)
    db.commit()
    db.refresh(db_character)
    return db_character

def get_characters(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Character).offset(skip).limit(limit).all()

def get_character_by_id(db: SessionLocal, character_id: int):
    return db.query(Character).filter(Character.id == character_id).first()

def update_character(db: SessionLocal, character_id: int, character_data: dict):
    db_character = db.query(Character).filter(Character.id == character_id).first()
    if not db_character:
        raise HTTPException(status_code=404, detail="Character not found")
    for key, value in character_data.items():
        setattr(db_character, key, value)
    db.commit()
    db.refresh(db_character)
    return db_character

def delete_character(db: SessionLocal, character_id: int):
    db_character = db.query(Character).filter(Character.id == character_id).first()
    if not db_character:
        raise HTTPException(status_code=404, detail="Character not found")
    db.delete(db_character)
    db.commit()

# Endpoints FastAPI
@app.post("/characters/", response_model=CharacterOut)
async def create_character_endpoint(character: CharacterCreate, db: Session = Depends(get_db_session)):
    return create_character(db=db, character=character)

@app.get("/characters/", response_model=List[CharacterOut])
async def read_characters(skip: int = 0, limit: int = 100, db: Session = Depends(get_db_session)):
    characters = get_characters(db, skip=skip, limit=limit)
    return characters

@app.get("/characters/{character_id}")
async def get_character_by_id_endpoint(character_id: int):
    db = next(get_db_session())
    character = get_character_by_id(db=db, character_id=character_id)
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")
    return character

@app.put("/characters/{character_id}", response_model=dict)
async def update_character_endpoint(character_id: int, character_data: dict):
    db = next(get_db_session())
    return update_character(db=db, character_id=character_id, character_data=character_data)

@app.delete("/characters/{character_id}")
async def delete_character_endpoint(character_id: int):
    db = next(get_db_session())
    delete_character(db=db, character_id=character_id)
    return {"detail": "Character deleted"}
