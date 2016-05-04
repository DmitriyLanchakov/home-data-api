Using at API to push data
=========================

Disclaimer
^^^^^^^^^^
When finding data to push to the API you should take into consideration the laws
and terms of service relating to the origin of that data. We do not condone or
recommend scraping sites which forbid such practices.

By pushing data to this API you agree that it was obtained lawfully and you have
the needed permission to do so.

Tools
^^^^^
This guide displays syntax for pushing data using the command line tool `curl`,
data can also be added using the html interface found at: https://home-sales-data-api.herokuapp.com/

Endpoints
=========

Admin
^^^^^
All current endpoints are public to GET requests but require a token for any 
POST requests. This system utilises JSON Web Tokens (JWTs) for authentication.
There are three main endpoints for getting, refreshing and verifying a web token.

Tokens are valid for a period of 5 minuets (300 seconds). A token can be refreshed
any time in the 7 day period after it was issued or last refreshed. Once this
period has passed a new token must be obtained from the `/token/auth/` endpoint.

Getting a token - `/token/auth/`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
To get a new token post your username and password to the `/token/auth` endpoint.
If you are hosting a copy of this API yourself you should try and ensure you use
a https connection so the data is not sent in plain text.::
    
    $ curl -X POST -H "Content-Type: application/json" \
        -d '{"username":"<your username>", "password":"<your password>"}'
    {
        "token": "<your token>"
    }

You can now use this token with other requests by adding the header `Authorization: Bearer <your token>`.

Refreshing a token - `/token/refresh/`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Once a token has expired it can be renewed for a new token by posting to the
`/token/refresh/` endpoint.::

    $ curl -X POST -H "Content-Type: application/json" \
        -d '{"token": "<your existing token>"}'
    {
        "token": "<a new token>"
    }

Verifying a token - `/token/verify/`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
To check if a token has expired you can post to the `/token/verify/` endpoint.
If your token is still valid the server will return a `200 OK` status. If the 
token has expired a `400 BAD REQUEST` will be returned instead.::

    $ curl -X POST -H "Content-Type: application/json" \
        -d '{"token": "<your token>"}'

Properties
^^^^^^^^^^
Available at: `/api/property`

This endpoint reads and writes :class:`api.models.Property` objects. Data should
be correctly formatted JSON. If you wish to add `Features` to a property you will
need to determine the feature ID ahead of time. The HTML interface takes care of
this using a populated combo box. We are investigating ways to make this process
easier for those posting from scripts or the command line.

First an example of getting data from the API (the JSON has been formatted for
readability)::

    $ curl https://home-sales-data-api.herokuapp.com/api/property/
    [{
        "id":1,
        "upload_timestamp":"2016-04-01T04:50:26.234865Z",
        "listing_timestamp":"2016-04-01T00:30:00Z",
        "listing_type":"F",
        "price":123456.0,
        "bedrooms":1.0,
        "bathrooms":2.0,
        "car_spaces":1.0,
        "building_size":150.0,
        "land_size":150.0,
        "size_units":"M",
        "raw_address":"100 Main street new york",
        "geocoded_address":"100 Main St, Flushing, NY 11354, USA",
        "features":[1]
    }]


Features
^^^^^^^^
Available at: `/api/feature`

This endpoint reads and writes :class:`api.models.Feature` objects. These are 
simple objects you can think of like tags. Each object has two properties, a
`category` and a `tag`. The `category` is typically used to group similar features
by things like their location. For example `Outdoor` is a category which may
contain a group of outdoor features. `tag` is the actual feature within that
category for example a swimming pool may have the `category` Outdoor and the `tag`
Pool.

Currently these objects can be written by anyone but this may change in the future
in an effort to keep the number of tags under control. Features will also be given
a `value` field in a future release to allow some metric information to be paired
with the feature. The exact setup of this is undetermined at this point.


Reading the feature list is similar to the Property list above::

    $ curl https://home-sales-data-api.herokuapp.com/api/feature/
    [{
        "id":1,
        "category":"Outdoor",
        "tag":"Pool"
    }]


The `id` field returned with each object is what should be passed on the creation
of :class:`api.models.Property` objects through the `Property` endpoint.

Creating a new feature is performed with a `POST` request to the endpoint. *See
the note above about the future of this option.*::

    $ curl -X POST -H 'Content-Type: application/json' \
        -H 'Authorization: Bearer <your_token>'
        -d '{"category":"Outdoor", "tag":"Garden"}' \
        https://home-sales-data-api.herokuapp.com/api/feature/
    {
        "id":2,
        "category":"Outdoor",
        "tag":"Garden"
    }
