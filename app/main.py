from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from . import models, database, crud, scheduler
from .models import TaskCreate, TaskOut, NoteCreate, NoteOut

models.Base.metadata.create_all(bind=database.engine)
app = FastAPI()

# ✅ CORS setup — add this immediately after app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change this to ["http://localhost:5173"] in dev or to your frontend domain in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Magiq Desk API is running"}     

@app.post("/tasks/", response_model=TaskOut)
def add_task(task: TaskCreate, db: Session = Depends(get_db)):
    return crud.create_task(db, task)

@app.get("/tasks/", response_model=list[TaskOut])
def read_tasks(db: Session = Depends(get_db)):
    return crud.get_tasks(db)

@app.get("/tasks/suggest-time/")
def suggest_time(db: Session = Depends(get_db)):
    tasks = crud.get_tasks(db)
    slot = scheduler.suggest_time_slot(tasks)
    return {"suggested_time": slot}

@app.post("/notes/", response_model=NoteOut)
def add_note(note: NoteCreate, db: Session = Depends(get_db)):
    return crud.create_note(db, note)

@app.get("/notes/", response_model=list[NoteOut])
def read_notes(db: Session = Depends(get_db)):
    return crud.get_notes(db)

@app.get("/quote/")
async def get_quote():
    import aiohttp
    async with aiohttp.ClientSession() as session:
        async with session.get("https://zenquotes.io/api/random") as resp:
            data = await resp.json()
            return {"quote": data[0]["q"], "author": data[0]["a"]}
