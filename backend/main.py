from datetime import datetime, timedelta
from math import exp
from typing import List, Optional

import databases
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import ormar
import sqlalchemy

WEIGHT_PRIO = 1.
WEIGHT_DEADLINE = 100.
WEIGHT_SPEND_TIME = 1.

app = FastAPI()
database = databases.Database("sqlite:///data/data.sqlite")
metadata = sqlalchemy.MetaData()
app.state.database = database

# app.mount("/ui", StaticFiles(directory="./frontend/public", html=True), name="ui")

app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:8080"],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])


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
    id: int = ormar.Integer(primary_key=True, min=0)  # type: ignore
    title: str = ormar.String(max_length=255)  # type: ignore
    text: str = ormar.String(max_length=255, default="")  # type: ignore
    priority: int = ormar.Integer(min=0, max=30, default=10)  # type: ignore
    spend_minutes: int = ormar.Integer(min=0, default=0)  # type: ignore
    deadline: Optional[datetime] = ormar.DateTime(
        nullable=True)  # type: ignore
    category: Optional[Category] = ormar.ForeignKey(Category, nullable=True)

    @ormar.property_field
    def virtual_priority(self) -> float:
        if self.deadline is not None:
            delta = (self.deadline - datetime.now())/timedelta(days=1)
        else:
            delta = float("inf")
        result: float = WEIGHT_PRIO * self.priority  \
            + WEIGHT_DEADLINE * exp(-delta) \
            + WEIGHT_SPEND_TIME * 1/(self.spend_minutes + 1)
        return result


@app.get("/")
def ui_route():
    return "Hello World from backend!"
    # return RedirectResponse("/docs")


@app.get("/create_db")
def create_db():
    engine = sqlalchemy.create_engine("sqlite:///data.sqlite")
    metadata.create_all(engine)


@app.get("/tasks/", response_model=List[Task])
async def read_tasks(category_id: Optional[int] = None):
    if category_id is not None:
        return await Task.objects.filter((Task.category is not None) &
                                         (Task.category.id ==
                                          category_id)).all()
    return await Task.objects.select_related("category").all()


@app.get("/tasks/{id}", response_model=Task)
async def read_task(id: int):
    return await Task.objects.select_related("category").get_or_none(id=id)


@app.post("/tasks/")
async def create_task(task: Task):
    return await task.save_related()


@app.delete("/tasks/{id}")
async def delete_task(id: int):
    if await Task.objects.delete(id=id) > 0:
        return "success"
    else:
        return None


@app.post("/categories/", response_model=Category)
async def create_category(category: Category):
    return await category.save()


@app.get("/categories/", response_model=List[Category])
async def get_categories():
    return await Category.objects.all()


@app.get("/categories/{id}", response_model=Category)
async def get_category(id: int):
    return await Category.objects.select_related(Category.tasks).get(id=id)

@app.delete("/categories/{id}")
async def delete_task(id: int):
    if await Category.objects.delete(id=id) > 0:
        return "success"
    else:
        return None
