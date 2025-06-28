from sqlalchemy import Column, Integer, String, Boolean, DateTime
from .database import Base
from pydantic import BaseModel, constr
from datetime import datetime

# SQLAlchemy Models
class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False, unique=True)
    completed = Column(Boolean, default=False)
    due = Column(DateTime, nullable=True)

class Note(Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String(1000), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

# Pydantic Models
class TaskCreate(BaseModel):
    title: constr(min_length=1, max_length=100)
    due: datetime | None = None

class TaskOut(TaskCreate):
    id: int
    completed: bool

    class Config:
        orm_mode = True

class NoteCreate(BaseModel):
    content: constr(min_length=1, max_length=1000)

class NoteOut(NoteCreate):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
