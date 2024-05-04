# ta-dataops

Driven mainly off of the FastAPI documentation, an example (with likely many breakages in it) of a FastAPI frontend on top of a SQLite db.

in your python environment of choice run 

`pip install -r requirements.txt`

then 

`fastapi dev src/main.py`

open a browser at

`http://127.0.0.1:8000/home`

change the address to

`http://127.0.0.1:8000/load_db`

you will now be able to view 

`/users/`
`/reviews/`
and `/countries/`

reviews for each user or country can be viewed at

`/reviews/user/<user_id>`

and

`reviews/country/<country_id>`

countries can be viewed by id or name

`/countries/<name or id>/<name or id value>`

and the same can be done for users.

fuller CRUD support to come...