# SimilarWeb API on RapidAPI

## Available on [PyPi](https://pypi.org/project/similarweb_rapidapi/)
## Read more on [main project page](https://letsscrape.com/scrapers/similarweb-api/)
## See on [RapidAPI](https://rapidapi.com/letsscrape/api/similarweb-working-api)

## Install
### using pip
```
pip install similarweb_rapidapi
```
### using poetry
```
poetry add similarweb_rapidapi
```

## Build
### Windows
```
git clone https://github.com/letsscrape/python_similarweb_rapidapi.git

cd similarweb_rapidapi
py -m venv venv
cd venv/Scripts/ && activate && cd ../../
pip install -r requirements.txt
py setup.py sdist bdist_wheel install
```
### Linux
```
git clone https://github.com/letsscrape/python_similarweb_rapidapi.git

cd similarweb_rapidapi
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 setup.py sdist bdist_wheel install
```

### How to get RAPID API key
1. **Register** you account on RapidAPI https://rapidapi.com/auth/sign-up
2. Go to https://bit.ly/3z3DInS and **Subscribe to test**
3. After subscribing, please revisit https://bit.ly/3z3DInS to obtain your **X-RapidAPI-Key**.
4. You will find **X-RapidAPI-Key** on the right side in the Code Snippets.

```
from api import SimilarWebRapidAPI

import asyncio

from schemas.task_status import TaskStatus

api = SimilarWebRapidAPI('____YOUR_RAPIDAPI_KEY____')

async def main():
    r = await api.get_basic_data_from_domain("google.com")
    print(r.status)
    print(r.data.site_name)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```
See the `tests/tests.py` file to see how to use it.