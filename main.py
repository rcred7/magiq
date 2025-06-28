import logging
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from . import models, database, crud, scheduler
from .models import TaskCreate, TaskOut, NoteCreate, NoteOut

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

models.Base.metadata.create_all(bind=database.engine)
app = FastAPI()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/tasks/", response_model=TaskOut)
def add_task(task: TaskCreate, db: Session = Depends(get_db)):
    try:
        result = crud.create_task(db, task)
        logger.info(f"Task created: {result.title}")
        return result
    except IntegrityError:
        db.rollback()
        logger.error(f"Duplicate task title: {task.title}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task title must be unique."
        )
    except Exception as e:
        logger.exception("Unexpected error in /tasks/")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/tasks/", response_model=list[TaskOut])
def read_tasks(db: Session = Depends(get_db)):
    try:
        return crud.get_tasks(db)
    except Exception as e:
        logger.exception("Error reading tasks")
        raise HTTPException(status_code=500, detail="Unable to fetch tasks")

@app.post("/notes/", response_model=NoteOut)
def add_note(note: NoteCreate, db: Session = Depends(get_db)):
    try:
        result = crud.create_note(db, note)
        logger.info("Note created")
        return result
    except Exception as e:
        logger.exception("Error creating note")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/notes/", response_model=list[NoteOut])
def read_notes(db: Session = Depends(get_db)):
    try:
        return crud.get_notes(db)
    except Exception as e:
        logger.exception("Error reading notes")
        raise HTTPException(status_code=500, detail="Unable to fetch notes")
