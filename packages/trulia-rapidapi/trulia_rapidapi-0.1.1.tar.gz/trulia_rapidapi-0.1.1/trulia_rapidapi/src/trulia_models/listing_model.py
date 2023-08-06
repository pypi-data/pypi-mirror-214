from typing import List
from typing import Optional
from datetime import datetime
from pydantic.fields import Field
from .base import BaseModelORM


class Status(BaseModelORM):
    is_active_for_rent: bool
    is_active_for_sale: bool
    is_foreclosure: bool
    is_off_market: bool
    is_recently_rented: bool
    is_recently_sold: bool


class Price(BaseModelORM):
    formatted_price: str
    currency_code: Optional[str]
    price: Optional[int]


class Location(BaseModelORM):
    state_code: str
    full_location: str
    zip_code: str
    city: str
    latitude: float
    longitude: float


class Home(BaseModelORM):
    date_listed: Optional[str]
    broker_name: Optional[str]
    agent_name: Optional[str]
    lot_size: Optional[float]
    lot_size_formatted: Optional[str]
    bathrooms: Optional[int]
    bathrooms_formatted: Optional[str]
    bedrooms: Optional[int]
    bedrooms_formatted: Optional[str]
    property_type: Optional[str]
    status: Status
    price: Price
    floor_space_formatted: Optional[str]
    floor_space: Optional[int]
    photos: List[Optional[str]]
    tags: List[str]
    location: Location
    url: str


class Paging(BaseModelORM):
    current_page: int
    page_count: int
    next_page_url: Optional[str]


class Data(BaseModelORM):
    homes: List[Home]
    paging: Paging


class ListingModel(BaseModelORM):
    description: str
    status: int
    data: Optional[Data] = None
