from fastapi import APIRouter, Request
from models import InputOrder, Order
from db import *
from fastapi.templating import Jinja2Templates
from models import *
from fastapi.responses import HTMLResponse


templates = Jinja2Templates(directory="templates")
router = APIRouter()

@router.get('/orders', response_model=list[Order])
async def get_order():
    query = sqlalchemy.select(
        orders_db.c.id, orders_db.c.status_order,
        orders_db.c.date_order,
        users_db.c.id.label('user_id'),
        users_db.c.first_name,
        users_db.c.last_name,
        products_db.c.id.label('product_id'),
        products_db.c.model
        ).join(users_db)
    
    rows = await db.fetch_all(query)

    return [Order(id=row.id, order=row.order, user=User(id=row.user_id, first_name=row.first_name)) for row in rows]

@router.post('/orders', response_model=dict)
async def inp_order(order: InputOrder):
    query = orders_db.insert().values(
        user_id=order.user_id,
        product_id=order.product_id,
        order=order.status_order,
        )
    last_record_id = await db.execute(query)
    return {**order.dict(), 'id': last_record_id}

# Вывод товаров в HTML
@router.get('/l_ord', response_class=HTMLResponse)
async def list_orders(request: Request):
    query = orders_db.select()
    return templates.TemplateResponse('db_orders.html',
                                    {'request': request, 
                                    'products': await db.fetch_all(query)}
                                    )
