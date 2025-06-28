from sqlalchemy.orm import Session
from . import models

def create_task(db: Session, task_data):
    task = models.Task(**task_data.dict())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def get_tasks(db: Session):
    return db.query(models.Task).all()

def create_note(db: Session, note_data):
    note = models.Note(**note_data.dict())
    db.add(note)
    db.commit()
    db.refresh(note)
    return note

def get_notes(db: Session):
    return db.query(models.Note).order_by(models.Note.created_at.desc()).all()
