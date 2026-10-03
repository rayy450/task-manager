from fastapi import FastAPI, HTTPException
from sqlmodel import SQLModel, Field, Session, create_engine, select

class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    description: str | None = None
    completed: bool = False

engine = create_engine(
    "sqlite:///database.db",
    connect_args={"check_same_thread": False}
)

def create_database():
    SQLModel.metadata.create_all(engine)
create_database()

app = FastAPI(
    title="Task Manager API",
    version="1.0.0"
)

@app.on_event("startup")
def startup():
    create_database()

@app.post("/tasks")
def create_task(task: Task):
    with Session(engine) as session:
        session.add(task)
        session.commit()
        session.refresh(task)
        return task

@app.get("/tasks")
def get_tasks():
    with Session(engine) as session:
        return session.exec(select(Task)).all()

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    with Session(engine) as session:
        task = session.get(Task, task_id)

        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        return task

@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task: Task):
    with Session(engine) as session:
        task = session.get(Task, task_id)

        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        task.title = updated_task.title
        task.description = updated_task.description
        task.completed = updated_task.completed

        session.add(task)
        session.commit()
        session.refresh(task)

        return task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    with Session(engine) as session:
        task = session.get(Task, task_id)

        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        session.delete(task)
        session.commit()

        return {"message": "Task deleted successfully"}