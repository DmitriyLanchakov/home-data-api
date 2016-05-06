# home-data-api
A RESTful API written in Django for user submission and lookup of home sales data

## Status

### Master
[![Build Status](https://travis-ci.org/data-skeptic/home-data-api.svg?branch=master)](https://travis-ci.org/data-skeptic/home-data-api)
[![Coverage Status](https://coveralls.io/repos/github/data-skeptic/home-data-api/badge.svg?branch=master)](https://coveralls.io/github/data-skeptic/home-data-api?branch=master)
[![Documentation Status](http://readthedocs.org/projects/data-skeptic-home-data-api/badge/?version=latest)](http://data-skeptic-home-data-api.readthedocs.org/en/latest/?badge=latest)

### Develop
[![Build Status](https://travis-ci.org/data-skeptic/home-data-api.svg?branch=develop)](https://travis-ci.org/data-skeptic/home-data-api)
[![Coverage Status](https://coveralls.io/repos/github/data-skeptic/home-data-api/badge.svg?branch=develop)](https://coveralls.io/github/data-skeptic/home-data-api?branch=develop)
[![Documentation Status](http://readthedocs.org/projects/data-skeptic-home-data-api/badge/?version=develop)](http://data-skeptic-home-data-api.readthedocs.org/en/develop/?badge=develop)


## Setting up
This project was built with python 3.4

```bash
$ python3 -m virtualenv venv
$ source ./venv/bin/activate
$ pip install -r requirements.txt
$ cd homes
$ python manage.py migrate --settings=homes.settings_local
$ python manage.py loaddata api/fixtures/groups.json --settings=homes.settings_local
$ python manage.py createsuperuser --settings=homes.settings_local
$ python manage.py runserver --settings=homes.settings_local
```

Then head to http://localhost:8000/api/ in your browser to get started.


