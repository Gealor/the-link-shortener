import time
from datetime import UTC
from datetime import datetime

from pydantic import BaseModel
from pydantic import Field


class Something(BaseModel):
    created_at: datetime = Field(default_factory = lambda: datetime.now(tz=UTC))

class Something2(BaseModel):
    created_at: datetime = Field(default = lambda: datetime.now(tz=UTC))

a = Something()
print(a.created_at) # нормально сгенерированная дата
a1 = Something2()
print(a1.created_at) # <function Something2.<lambda> at 0x0000028B89A42D40>

print()
time.sleep(10)
b = Something()
print(b.created_at) # нормально сгенерированная дата
b1 = Something2()
print(b1.created_at) # <function Something2.<lambda> at 0x0000028B89A42D40>