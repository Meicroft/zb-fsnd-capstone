# Casting Agency - FSND Capstone

## Getting Started

### Installing Dependencies

#### Python 3.8.2

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python).

#### Virtual Enviornment

Recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/).

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages.

#### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

## Running the Server

Once you're insine the working directory, have created & source'd into your VENV, and run `pip install -r requirements.txt`, run the following:

- This will export all variables inside setup.sh, connecting your local server to the hosted database, among other things.
```
. ./setup.sh
```

- This will launch the server locally, allowing you to access it via https://127.0.0.1:5000/
```
flask run --reload
```

# API Specs
- Public Access:
    The home page (`https://{{host}}/`) is accessible by anyone, and without running the server locally you can access with the URL listed below.

- Casting Assistant:
    The casting assistant has permissions to view actor or movie specific pages (ex.:`https://{{host}}/actors/<int:actor_id>`)
- Casting Director:
    The Casting Director has permissions to add/delete an actor, edit existing actors/movies, and the permissions of the Casting Assistant.
- Executive Producer:
    The Executive Producer has permissions to add/delete a movie, and permissions of the Casting Director and Assistant.

## Endpoints
GET: main info page for actor(s) & movie(s)
- /
- /actors
- /movies
###### (requires Assistant permissions)
- /actors/<int:actor_id>
- /movies/<int:movie_id>

DELETE: delete an actor or movie
###### (requires Director permissions)
- /actors/<int:actor_id>
###### (requires Producer permissions)
- /movies/<int:movie_id>


POST: create a new actor or movie
###### (requires Director permissions)
- /actors
###### (requires Producer permissions)
- /movies

PATCH: edit info of an actor or movie
###### (requires Director permissions)
- /actors/<int:actor_id>
- /movies/<int:movie_id>

###### Postman Collection provided to test endpoints with active Beaer Tokens attached to Parents of each endpoint.
###### Access tokens also provided in setup.sh as assistant_token, direct_token, producer_token.

## Error Handling

### Errors built in to be handled:
- 400 - Bad Request
- 401 - Unauthorized
- 403 - Forbidden
- 404 - Not Found
- 405 - Method Not Allowed

Errors are returned as JSON Objects. Example below:
```
{
    "error": 401,
    "message": "The server could not verify that you are authorized to access the URL requested. You either supplied the wrong credentials (e.g. a bad password), or your browser doesn't understand how to supply the credentials required.",
    "success": false
}
```