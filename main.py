from typing import Union
from typing import Optional
# from fastapi import FastAPI


# app = FastAPI()


# @app.get("/")
# async def root():
#     return {"message": "Hello World"}


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