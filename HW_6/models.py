from datetime import date
from pydantic import BaseModel, Field

class InputUser(BaseModel):
    first_name: str = Field(title='first_name', max_length=32)
    last_name: str = Field(title='last_name', max_length=48)
    email: str = Field(title='email', max_length=48)
    password: str = Field(title='password', min_length=6)

class User(InputUser):
    id: int

class InputProduct(BaseModel):
    model: str = Field(title='model', min_length=3)
    description: str = Field(title='description', max_length=1000)
    price: float = Field(title='price')

class Product(InputProduct):
    id: int

class InputOrder(BaseModel):
    user_id: int
    product_id: int
    date_order: date = Field(title='date_order')
    status_order: bool = Field(title='status_order')

class Order(BaseModel):
    id: int
    user: User
    product: Product
    order: bool
