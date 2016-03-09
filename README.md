# home-data-api
A RESTful API written in Django for user submission and lookup of home sales data

## Setting up
This project was built with python 3.4

```bash
$ python3 -m virtualenv venv
$ source ./venv/bin/activate
$ pip install -r requirements.txt
$ cd homes
$ python manage.py migrate
$ python manage.py runserver
```

Then head to http://localhost:8000/api/ in your browser to get started.


