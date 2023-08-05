import asyncio
import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.trulia_models.enums import TruliaSearchType
from src.trulia_api import TruliaAPI

# To obtain your rapid_api key, you first need to sign up on RapidAPI. You can do so by visiting this link: https://rapidapi.com/auth/sign-up.
# After registering, navigate to the Trulia Real Estate Scraper API page at https://rapidapi.com/letsscrape/api/trulia-real-estate-scraper.
# Click on "Subscribe to Test" to get access to the API.
# After subscribing, you will find your X-RapidAPI-Key. It's located on the right side of the screen, within the "Code Snippets" section.
# Remember, this key is vital for accessing the API, so keep it safe.        
api = TruliaAPI('____YOUR_RAPIDAPI_KEY____')

async def test_get_listing_by_url():
    r = await api.get_listing_by_url("https://www.trulia.com/AZ/Scottsdale/", 1)
    assert r.status == 200
    assert len(r.data.homes) > 0

async def test_get_search_token():
    r = await api.get_search_token(TruliaSearchType.ForSale, "Scottsdale")
    assert r.status == 200
    
async def test_search_by_place():
    r = await api.search_by_place(TruliaSearchType.ForSale, "Scottsdale", 1)
    assert r.status == 200
    assert len(r.data.homes) > 0

async def test_search_by_token():
    token = await api.get_search_token(TruliaSearchType.ForSale, "Scottsdale")
    r = await api.search_by_token(TruliaSearchType.ForSale, token, 1)
    assert r.status == 200
    assert len(r.data.homes) > 0

async def main():
  await test_get_listing_by_url()
  await test_get_search_token()
  await test_search_by_place()
  await test_search_by_token()
  return None

loop = asyncio.get_event_loop()
loop.run_until_complete(main())







