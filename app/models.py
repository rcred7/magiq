from sqlalchemy import Column, Integer, String, Boolean, DateTime
from .database import Base
from pydantic import BaseModel
from datetime import datetime

# SQLAlchemy models
class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    completed = Column(Boolean, default=False)
    due = Column(DateTime, nullable=True)

class Note(Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

# Pydantic models
class TaskCreate(BaseModel):
    title: str
    due: datetime | None = None

class TaskOut(TaskCreate):
    id: int
    completed: bool

    class Config:
        orm_mode = True

class NoteCreate(BaseModel):
    content: str

class NoteOut(NoteCreate):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
