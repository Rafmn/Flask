'''
Выполнить задания 3, 4, 5, 6 презентации в виде одного приложения.

Создать API для добавления нового пользователя в базу данных. Приложение
должно иметь возможность принимать POST запросы с данными нового
пользователя и сохранять их в базу данных.
📌 Создайте модуль приложения и настройте сервер и маршрутизацию.
📌 Создайте класс User с полями id, name, email и password.
📌 Создайте список users для хранения пользователей.
📌 Создайте маршрут для добавления нового пользователя (метод POST).
📌 Реализуйте валидацию данных запроса и ответа.

Создать API для обновления информации о пользователе в базе данных.
Приложение должно иметь возможность принимать PUT запросы с данными
пользователей и обновлять их в базе данных.
📌 Создайте модуль приложения и настройте сервер и маршрутизацию.
📌 Создайте класс User с полями id, name, email и password.
📌 Создайте список users для хранения пользователей.
📌 Создайте маршрут для обновления информации о пользователе (метод PUT).
📌 Реализуйте валидацию данных запроса и ответа.

Создать API для удаления информации о пользователе из базы данных.
Приложение должно иметь возможность принимать DELETE запросы и
удалять информацию о пользователе из базы данных.
📌 Создайте модуль приложения и настройте сервер и маршрутизацию.
📌 Создайте класс User с полями id, name, email и password.
📌 Создайте список users для хранения пользователей.
📌 Создайте маршрут для удаления информации о пользователе (метод DELETE).
📌 Реализуйте проверку наличия пользователя в списке и удаление его из
списка.

Создать веб-страницу для отображения списка пользователей. Приложение
должно использовать шаблонизатор Jinja для динамического формирования HTML
страницы.
📌 Создайте модуль приложения и настройте сервер и маршрутизацию.
📌 Создайте класс User с полями id, name, email и password.
📌 Создайте список users для хранения пользователей.
📌 Создайте HTML шаблон для отображения списка пользователей. Шаблон должен
содержать заголовок страницы, таблицу со списком пользователей и кнопку для
добавления нового пользователя.
📌 Создайте маршрут для отображения списка пользователей (метод GET).
📌 Реализуйте вывод списка пользователей через шаблонизатор Jinja.
'''

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import uvicorn
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, FileResponse



app = FastAPI()
templates = Jinja2Templates(directory="templates")

class UserIn(BaseModel):
    name: str
    email: str
    password: str

class User(UserIn):
    id: int


users = []

@app.get("/", response_model=list[User])
async def read_users():
    return users

@app.get("/users_html", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("users.html", {"request": request, 'users': list(users)})

@app.post('/user', response_model=User)
async def create_user(item: UserIn):
    id = len(users) + 1
    user = User
    user.id = id
    user.name = item.name
    user.email = item.email
    user.password = item.password
    users.append(user)
    return user

@app.put('/user/{id}', response_model=User)
async def put_user(id: int, new_user: UserIn):
    for a_user in users:
        if a_user.id == id:
            a_user.name = new_user.name
            a_user.email = new_user.email
            a_user.password = new_user.password
            return a_user
    raise HTTPException(status_code=404, detail='Task not found')

@app.delete('/delete/{id}')
async def delete_user(id: int):
    for a_user in users:
        if a_user.id == id:
            users.remove(a_user)
            return users
    raise HTTPException(status_code=404, detail='Task not found')

if __name__ == '__main__':
    uvicorn.run(
        "homework:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )
    