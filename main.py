from typing import Annotated, Literal
from fastapi import FastAPI,Query,Path,Body
from enum import Enum
from pydantic import BaseModel,Field,HttpUrl





# class ModelName(str,Enum):
#     alexnet = "alexnet"
#     resnet = "resnet"
#     lenet = "lenet"


app=FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World"}

# @app.get("/items/{item_id}")
# def root(item_id:int):
#     return {"message": f"Hello World {item_id}"}



# @app.get("/models/{model_name}")
# async def get_model(modelname:ModelName):
#     if modelname is ModelName.alexnet:
#         return {"model_name": modelname.value, "message": "Deep Learning FTW!"}
#     if modelname.value == "lenet":
#         return {"model_name": modelname, "message": "LeCNN all the images"}
#     return {"model_name": modelname, "message": "Have some residuals"}




@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}


fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: str | None = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item




# request Body 

class Item(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    tax: float | None = None


@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict





@app.get("/items/")
async def read_items(q : Annotated[str |None , Query(min_length=3, max_length=50, pattern="^fixedquery$")   ] = ...   ):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results



@app.get("/items/list")
async def read_muilt_inputs(q: Annotated[list[str] | None, Query(
            title="Query string",
            description="Query string for the items to search in the database that have a good match",
            min_length=3,
        ),] = ["foo", "bar"]):
    query_items = {"q": q}
    return query_items


#  Alias parameters¶

@app.get("/items/alias")
async def read_alias_items(q: Annotated[str | None, Query(alias="item-query",     deprecated=True,)] = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, q: str | None = None):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result

@app.get("/items/path/{item_id}")
async def read_items(
    item_id: Annotated[int, Path(title="24" , ge=10, le=100, )],
    q: Annotated[str | None, Query(alias="item-query")] = None,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results


# filter params model 

class FilterParams(BaseModel):
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: list[str] = []


@app.get("/filters/")
async def read_filters(filter_query: Annotated[FilterParams, Query()]):
    return filter_query





# custom filter  model configration 

class FilterParams(BaseModel):
    model_config = {"extra": "forbid"}

    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: list[str] = []


@app.get("/filter/custom")
async def read_items(filter_query: Annotated[FilterParams, Query()]):
    return filter_query





class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


@app.put("/items/muilt/{item_id}")
async def update_item(
    item_id: Annotated[int, Path(title="The ID of the item to get", ge=0, le=1000)],
    q: str | None = None,
    item: Item | None = None,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if item:
        results.update({"item": item})
    return results





# muiltiple path and query parameters and request body

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


class User(BaseModel):
    username: str
    full_name: str | None = None


@app.put("/items/multi_model/{item_id}")
async def update_item(item_id: int, item: Item, user: User):
    results = {"item_id": item_id, "item": item, "user": user}
    return results




# extra body params ==>  Body() 

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


class User(BaseModel):
    username: str
    full_name: str | None = None


@app.put("/items/body_extra/{item_id}")
async def update_item(
    item_id: int, item: Item, user: User, importance: Annotated[int, Body()]
):
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    return results





# do update in function 



class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


class User(BaseModel):
    username: str
    full_name: str | None = None


@app.put("/items/update_body_in/{item_id}")
async def update_item(
    *,
    item_id: int,
    item: Item,
    user: User,
    importance: Annotated[int, Body(gt=0)],
    q: str | None = None,
):
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    if q:
        results.update({"q": q})
    return results


# body one item 

class Item(BaseModel):
    name: str | None = Field(None, title="The name of the item", max_length=30)
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list[str] = []
    sets: set[int] = set()



@app.put("/items/body_one_item/{item_id}")
async def update_item(item_id: int, item: Annotated[Item, Body(embed=True)]):
    results = {"item_id": item_id, "item": item}
    return results





class Image(BaseModel):
    url: HttpUrl
    name: str


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()
    image: Image | None = None
    images: list[Image] | None = None


@app.put("/items/nested_models/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results





# dics 


@app.post("/index-weights/")
async def create_index_weights(weights: dict[int, float]):
    return weights














# from pydantic import BaseModel
# from fastapi import FastAPI
# from datetime import datetime

# from typing import Annotated




# app = FastAPI()


# @app.get("/")
# async def root():
#     return {"message": "Hello World"}


   #classes functions

"""
class Person:
    def __init__(self, name: str | None):
        self.name = name
    
    def __str__(self) -> str:
        return f"Person named {self.name if self.name else 'Anonymous'}"
    
    def __repr__(self) -> str:
        return f"Person(name='{self.name}')"
    
    def __len__(self) -> int:
        return len(self.name) if self.name else 0
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Person):
            return False
        return self.name == other.name
    
    def __getitem__(self, key):
        if key == 'name':
            return self.name
        raise KeyError(f"'{key}' is not a valid key")
    
    def __setitem__(self, key, value):
        if key == 'name':
            self.name = value
        else:
            raise KeyError(f"'{key}' is not a valid key")



# Creating instances
p1 = Person(name="John")
p2 = Person(name="John")
p3 = Person(name="Jane")

# __str__ example
print(p1)  # Output: Person named John

# __repr__ example
print(repr(p1))  # Output: Person(name='John')

# __len__ example
print(len(p1))  # Output: 4 (length of "John")

# __eq__ example
print(p1 == p2)  # Output: True
print(p1 == p3)  # Output: False

# __getitem__ example
print(p1['name'])  # Output: John

# __setitem__ example
p1['name'] = "Mike"
print(p1.name)  # Output: Mike



"""


# class User(BaseModel):
#     id:int 
#     name:str = "John Doe"
#     signup_ts: datetime | None = None
#     friends: list[int] = []


# external_data = {
#     "id": "123",
#     "signup_ts": "2017-06-01 12:22",
#     "friends": [1, "2", b"3"],
# }


# user =User(**external_data)

# print(user.signup_ts)



# def say_hello(name:Annotated[str, "The name of the person"])-> str :
#     return f"Hello {name}"



# say_hello("John")


# async def some_library():

# @app.get('/')
# async def read_results():
#     results = await some_library()
#     return results




# env variables


# import os

# # name = os.getenv("NAME", "World") World is the default value
# name = os.getenv("MY_NAME", "World")

# print(f"Hello, {name}!")



