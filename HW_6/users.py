from fastapi import APIRouter, Request
from models import InputUser, User
from db import *
from fastapi.templating import Jinja2Templates
from models import *
from fastapi.responses import HTMLResponse


templates = Jinja2Templates(directory="templates")
router = APIRouter()

# Создание тестовых пользователей
@router.get("/fake_users/{count}")
async def create_note(count: int):
    for i in range(1, count+1):
        query = users_db.insert().values(
            first_name=f'user_{i}',
            last_name=f'dump_{i}',
            password=f'pswwed_{i}',
            email=f'mail_{i}@email.ru')
        await db.execute(query)
    return {'message': f'{count} fake users created'}

# Создание нового пользователя
@router.post("/users/new/", response_model=User)
async def create_user(user: InputUser):
    query = users_db.insert().values(
        first_name=user.first_name,
        last_name=user.last_name,
        password=user.password,
        email=user.email)
    last_record_id = await db.execute(query)
    return {**user.dict(), "id": last_record_id}

# Список пользователей
@router.get("/users/", response_model=list[User])
async def read_users():
    query = users_db.select()
    return await db.fetch_all(query)

# Вывод пользователей в HTML
@router.get("/l_us/", response_class=HTMLResponse)
async def list_users(request: Request):
    query = users_db.select()
    return templates.TemplateResponse("db_users.html",
                                      {"request": request,
                                       'users': await db.fetch_all(query)})
