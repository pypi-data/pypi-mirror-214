from typing import List
from typing import Optional
from datetime import datetime
from pydantic.fields import Field
from .base import BaseModelORM

class Place(BaseModelORM):
    type: str
    title: str
    search_token: str

class Data(BaseModelORM):
    places: List[Place]

class SearchTokenModel(BaseModelORM):
    description: str
    status: int
    data: Optional[Data] = None
    def __str__(self):
        if len(self.data.places) == 0:
            return None
        return self.data.places[0].search_token