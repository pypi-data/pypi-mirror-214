from typing import List
from typing import Optional
from datetime import datetime
from pydantic.fields import Field
from .base import BaseModelORM


class Price(BaseModelORM):
    formatted_price: Optional[str]
    price: Optional[int]
    currency_code: Optional[str]
    branch_banner_price: Optional[float]


class PriceHistoryItem(BaseModelORM):
    event: Optional[str]
    formatted_data: Optional[str]
    price: Optional[Price]
    source: Optional[str]


class Price1(BaseModelORM):
    formatted_price: Optional[str]
    price: Optional[int]
    currency_code: Optional[str]
    branch_banner_price: Optional[str]


class Highlight(BaseModelORM):
    name: Optional[str]
    value: Optional[str]


class Description(BaseModelORM):
    date_last_updated_formatted: Optional[str]
    markdown: Optional[str]
    text: Optional[str]
    value: Optional[str]
    subheader: Optional[str]
    contact_phone_number: Optional[str]
    

class Location(BaseModelORM):
    state_code: Optional[str]
    full_location: Optional[str]
    city_state_zip_address: Optional[str]
    city: Optional[str]
    zip_code: Optional[str]
    neighborhood_name: Optional[str]
    street_address: Optional[str]
    formatted_location: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]


class Status(BaseModelORM):
    is_active_for_rent: bool
    is_active_for_sale: bool
    is_foreclosure: bool
    is_off_market: bool
    is_recently_rented: bool
    is_recently_sold: bool


class Attribute(BaseModelORM):
    name: Optional[str]
    value: str


class Feature(BaseModelORM):
    name: str
    attributes: List[Attribute]

class PriceChange(BaseModelORM):
    price_change_formatted: Optional[str]
    price_change: Optional[int]
    direction: Optional[str]
    change_percent_formatted: Optional[str]
    change_percent: Optional[float]
    change_date_formatted: Optional[str]
    previous_price_formatted: Optional[str]
    previous_price: Optional[int]
  
class SellingSoonInformation(BaseModelORM):
    disclaimer: Optional[str]
    description: Optional[str]

class Data(BaseModelORM):
    is_empty: bool
    price_change: Optional[PriceChange]
    price_history: List[PriceHistoryItem]
    price: Price1
    selling_soon_information: Optional[SellingSoonInformation]
    highlights: List[Highlight]
    agent_name: Optional[str]
    broker_name: Optional[str]
    date_listed: Optional[str]
    description: Optional[Description]
    url: Optional[str]
    floor_space: Optional[float]
    floor_space_formatted: Optional[str]
    tags: Optional[List[str]]
    photos: Optional[List[str]]
    property_type: Optional[str]
    location: Optional[Location]
    status: Optional[Status]
    lot_size: Optional[float]
    lot_size_formatted: Optional[str]
    bedrooms_formatted: Optional[str]
    bedrooms: Optional[int]
    bathrooms: Optional[int]
    bathrooms_formatted: Optional[str]
    features: Optional[List[Feature]]


class DetailsModel(BaseModelORM):
    description: Optional[str] = None
    status: Optional[int] = None
    data: Optional[Data] = None
