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
Current endpoints are accessible to all users, however a system for registering
an account and using these details to obtain a JSON Web Token (JWT) will be 
added in an upcoming release. 

*Note that until this admin interface is in place there are no gaurentees that
data will persist. If you are pushing data please keep backup*


Properties
^^^^^^^^^^
Available at: `/api/property`

This endpoint reads and writes :class:`api.models.Property` objects. Data should
be correctly formatted JSON. If you wish to add `Features` to a property you will
need to determine the feature ID ahead of time. The HTML interface takes care of
this using a populated combo box. We are investigating ways to make this process
easier for those posting from scripts or the command line.

First an example of getting data from the API


Features
^^^^^^^^


