"""
LetsScrape, email: hello@letsscrape.com
"""
import asyncio
import time
from typing import List, Optional, Union, Dict, AnyStr
from urllib.parse import urlencode
from purl import URL
import aiohttp

from src.trulia_models.enums import *
from src.trulia_models.listing_model import ListingModel
from src.trulia_models.search_token_model import SearchTokenModel



class TruliaAPI(object):
    def __init__(self, rapid_api_key: AnyStr):
        """
        To obtain your rapid_api key, you first need to sign up on RapidAPI. You can do so by visiting this link: https://rapidapi.com/auth/sign-up.
        After registering, navigate to the Trulia Real Estate Scraper API page at https://rapidapi.com/letsscrape/api/trulia-real-estate-scraper.
        Click on "Subscribe to Test" to get access to the API.
        After subscribing, you will find your X-RapidAPI-Key. It's located on the right side of the screen, within the "Code Snippets" section.
        Remember, this key is vital for accessing the API, so keep it safe.        
        """
        self.rapidapi_host = 'trulia-real-estate-scraper.p.rapidapi.com'
        self.headers = {
            "X-RapidAPI-Key": rapid_api_key,
            "X-RapidAPI-Host": self.rapidapi_host,
        }

    async def __get_request(self, path: AnyStr, params: Optional[Dict] = None) -> Dict:
        """
        :param path: Request path
        :param params: Request query parameters
        :return: JSON Response Dictionary
        """
        if params:
            query_string = urlencode(params)
        else:
            query_string = ""

        url = URL(
            host=self.rapidapi_host,
            path=path,
            query=query_string,
            scheme="https"
        ).as_string()

        session_timeout = aiohttp.ClientTimeout(total=45.0)
        is_ok = False

        while True:
            async with aiohttp.ClientSession(headers=self.headers, timeout=session_timeout) as session:
                async with session.get(url=url) as response:
                    try:
                        json_response = await response.json()  
                        if response.status == 200:  
                            is_ok = True
                    except aiohttp.client.ContentTypeError:
                        continue
                    if is_ok:
                        break
            await asyncio.sleep(0.3)

        return json_response
    
    async def __wait(self):
        await asyncio.sleep(1)

    async def get_search_token(self, search_type: TruliaSearchType, place: str) -> SearchTokenModel:
        """
        This function generates a token (or tokens in some cases) based on the variable {place}.
        For example, if we pass a part of {place} instead of 'Scottsdale', say 'Scot', we'll receive 
        several tokens along with the matched {places}, from which we can select the token to use
        in the search_by_token function.
        """
        path = f"/search/token?search_type={search_type.name}&place={place}"
        response_data = await self.__get_request(path=path)
        response = SearchTokenModel.parse_obj(response_data)
        return response

    async def get_listing_by_url(self, url: str, page: int) -> ListingModel:
        """
        Returns homes from the listing. Just go to https://www.trulia.com/ select the listing you are interested in e.g. https://www.trulia.com/AZ/Scottsdale/ and pass that url into query.
        """
        path = f"/homes/listing_by_url?url={url}&page={page}"
        response_data = await self.__get_request(path=path)
        response = ListingModel.parse_obj(response_data)
        return response
   
    async def search_by_place(self, search_type: TruliaSearchType, place: str, page: int, 
        sort: TruliaSort=None, beds: TruliaBeds=None,
        min_price: TruliaPriceRange=None, max_price: TruliaPriceRange=None,
        house_type: TruliaHouseType=None, for_sale_by_agent: bool=None, for_sale_by_owner: bool=None,
        new_construction: bool=None) -> ListingModel:
        """
        This function automatically generates a search token based on the variable {place}. 
        If {place} returns multiple search tokens, the first element will be passed to 
        the search query. Therefore, in this function, full control is not assured since we 
        might want to use, for example, the second token that matches a different place. 
        At the same time, this function will often be sufficient for the user.

        Parameters:
        page (int): The page number you want to work with. If you want the first page, pass in 1.
        """
        token = await self.get_search_token(search_type, place)

        if len(token.data.places) == 0:
            return ListingModel(data=None, status=200, description="No places have been found!")

        return await self.search_by_token(search_type, token.data.places[0].search_token, page, sort, beds, min_price, max_price,
            house_type, for_sale_by_agent, for_sale_by_owner, new_construction)

    async def search_by_token(self, search_type:TruliaSearchType, token: str, page: int, 
        sort: TruliaSort=None, beds: TruliaBeds=None,
        min_price: TruliaPriceRange=None, max_price: TruliaPriceRange=None,
        house_type: TruliaHouseType=None, for_sale_by_agent: bool=None, 
        for_sale_by_owner: bool=None, new_construction: bool=None) -> ListingModel:
        """
        This function accepts a token, in contrast to the previous function, 
        search_by_place, where we have to manually pass the token. Hence, it's necessary 
        to first generate it with get_search_token, choose the appropriate token,
        and then pass it to the function.

        Parameters:
        page (int): The page number you want to work with. If you want the first page, pass in 1.
        """
        path = f"/search/{search_type}?search_token={token}&page={page}&sort={sort}&beds={beds}&min_price={min_price}&max_price={max_price}&house_type={house_type}&for_sale_by_agent={for_sale_by_agent}&for_sale_by_owner={for_sale_by_owner}&new_construction={new_construction}"
        path = path.replace('=None', '=')
        response_data = await self.__get_request(path=path)
        response = ListingModel.parse_obj(response_data)
        return response