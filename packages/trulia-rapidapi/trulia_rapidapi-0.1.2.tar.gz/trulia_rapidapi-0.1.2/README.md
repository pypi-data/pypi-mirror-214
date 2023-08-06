# Trulia API on RapidAPI

## Available on [PyPi](https://pypi.org/project/trulia_rapidapi/)
## Read more on [main project page](https://letsscrape.com/scrapers/trulia-real-estate-api/)
## See on [RapidAPI](https://rapidapi.com/letsscrape/api/trulia-real-estate-scraper)

## Install
### using pip
```
pip install trulia_rapidapi
```
### using poetry
```
poetry add trulia_rapidapi
```

### How to get RAPID API key
1. **Register** you account on RapidAPI https://rapidapi.com/auth/sign-up
2. Go to https://rapidapi.com/letsscrape/api/trulia-real-estate-scraper and **Subscribe to test**
3. After subscribing, please revisit https://rapidapi.com/letsscrape/api/trulia-real-estate-scraper to obtain your **X-RapidAPI-Key**.
4. You will find **X-RapidAPI-Key** on the right side in the Code Snippets.

```
from api import TruliaRapidAPI

import asyncio

from schemas.task_status import TaskStatus

api = TruliaAPI('____YOUR_RAPIDAPI_KEY____')

async def main():
    r = await api.get_listing_by_url("https://www.trulia.com/AZ/Scottsdale/", 1)
    print(r.status)
    print(r.data)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```

See the `tests.py` file to see how to use it.