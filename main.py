import databases
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import ormar
import sqlalchemy
from typing import List, Optional

app = FastAPI()
database = databases.Database("sqlite:///data.sqlite")
metadata = sqlalchemy.MetaData()
app.state.database = database

app.mount("/", StaticFiles(directory="./frontend", html=True), name="ui")


@app.on_event("startup")
async def startup() -> None:
    database_ = app.state.database
    if not database_.is_connected:
        await database_.connect()


@app.on_event("shutdown")
async def shutdown() -> None:
    database_ = app.state.database
    if database_.is_connected:
        await database_.disconnect()


class Category(ormar.Model):
    class Meta:
        tablename = "categories"
        metadata = metadata
        database = database
    id = ormar.Integer(primary_key=True)
    name = ormar.String(max_length=100, unique=True)


class Task(ormar.Model):
    class Meta:
        tablename = "tasks"
        database = database
        metadata = metadata
    id = ormar.Integer(primary_key=True, min=0)
    title = ormar.String(max_length=255)
    text = ormar.String(max_length=255, default="")
    priority = ormar.Integer(min=0, max=30, default=10)
    spend_minutes = ormar.Integer(min=0, default=0)
    deadline = ormar.DateTime(nullable=True)
    category = ormar.ForeignKey(Category, nullable=True)


@app.get("/create_db")
def create_db():
    engine = sqlalchemy.create_engine("sqlite:///data.sqlite")
    metadata.create_all(engine)


@app.get("/tasks/", response_model=List[Task])
async def read_tasks(category_id: Optional[int] = None):
    if category_id is not None:
        return await Task.objects.filter((Task.category.id == category_id)).all()
    return await Task.objects.all()


@app.get("/tasks/{id}", response_model=Task)
async def read_task(id: int):
    return await Task.objects.get_or_none(id=id)


@app.post("/tasks/")
async def create_task(task: Task):
    return await task.save_related()


@app.post("/categories/", response_model=Category)
async def create_category(category: Category):
    return await category.save()


@app.get("/categories/", response_model=List[Category])
async def get_categories():
    return await Category.objects.all()


@app.get("/categories/{id}", response_model=Category)
async def get_category(id: int):
    return await Category.objects.select_related(Category.tasks).get(id=id)


@app.delete("/tasks/{id}")
async def delete_task(id: int):
    if await Task.objects.delete(id=id) > 0:
        return "success"
    else:
        return None
