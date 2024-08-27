from dataclasses import dataclass
from itemadapter import ItemAdapter

@dataclass
class InventoryItem:
    name: str
    price: float
    stock: int

obj = InventoryItem(name='foo', price=20.5, stock=10)

print(ItemAdapter.is_item(obj))

adapter = ItemAdapter(obj)
print(len(adapter))

print(adapter["name"])
print(adapter.get("price"))

adapter["name"] = "bar"
adapter.update({"price": 12.7, "stock": 9})

print(adapter["name"])
print(adapter.get("price"))



@dataclass
class Price:
    value: int
    currency: str


@dataclass
class Product:
    name: str
    price: Price

item = Product("Stuff", Price(42, "UYU"))
adapter = ItemAdapter(item)
print(adapter.asdict())

'''
The following adapters are included by default:

    itemadapter.adapter.ScrapyItemAdapter: handles Scrapy items
    itemadapter.adapter.DictAdapter: handles Python dictionaries
    itemadapter.adapter.DataclassAdapter: handles dataclass objects
    itemadapter.adapter.AttrsAdapter: handles attrs objects
    itemadapter.adapter.PydanticAdapter: handles pydantic objects

'''

from itemadapter.adapter import PydanticAdapter

from datetime import datetime
from pydantic import BaseModel, PositiveInt


class User(BaseModel):
    id: int
    name: str = 'John Doe'
    signup_ts: datetime | None
    tastes: dict[str, PositiveInt]


external_data = {
    'id': 123,
    'signup_ts': '2019-06-01 12:22',
    'tastes': {
        'wine': 9,
        b'cheese': 7,
        'cabbage': '1',
    },
}

user = User(**external_data)

adapter = ItemAdapter(user)
print(adapter.item )
print(adapter.get_field_names_from_class(adapter))

