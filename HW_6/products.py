from fastapi import APIRouter, Request
from models import InputProduct, Product
from db import *
from fastapi.templating import Jinja2Templates
from models import *
from fastapi.responses import HTMLResponse


templates = Jinja2Templates(directory="templates")
router = APIRouter()

# Список товаров
@router.get('/products', response_model=list[Product])
async def read_products():
    query = products_db.select()
    return await db.fetch_all(query)

# Добавление товара
@router.post('/products/new', response_model=Product)
async def create_product(product: InputProduct):
    query = products_db.insert().values(
        model=product.model,
        description=product.description,
        price=product.price 
    )
    last_record_id = await db.execute(query)
    return {**product.dict(), 'id': last_record_id}

# Вывод товаров в HTML
@router.get('/l_pr', response_class=HTMLResponse)
async def list_products(request: Request):
    query = products_db.select()
    return templates.TemplateResponse('db_prod.html',
                                    {'request': request, 
                                    'products': await db.fetch_all(query)}
                                    )
