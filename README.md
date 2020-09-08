# Casting Agency - FSND Capstone
## This Casting Agency API supports The basic needs to vreate, view, edit, and remove actors & movies from an Agency's database.

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

## Testing
Once you're in the project directory & virtualenv, run `pytest`. Any failing tests are likely due to expired JWTs, update those in setup.sh, run `. ./setup.sh`, and rerun `pytest`.

# API Specs
- Public Access:
    The home page (`https://{{host}}/`) is accessible by anyone, and without running the server locally you can access the live hosted app at https://zb-fsnd-capstone.herokuapp.com/.

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
    - Example Request:
    https://zb-fsnd-capstone.herokuapp.com/actors
    - Example Response:
    ```
    {
    "actors": [
        {
            "age": 30,
            "gender": "male",
            "id": 4,
            "name": "Ben Cum"
        },
        {
            "age": 30,
            "gender": "male",
            "id": 1,
            "name": "Benedict Cumberbatch"
        },
        {
            "age": 30,
            "gender": "monster",
            "id": 5,
            "name": "Mike Wazowksi"
        },
        {
            "age": 30,
            "gender": "female",
            "id": 6,
            "name": "New Actor"
        },
        {
            "age": 30,
            "gender": "female",
            "id": 8,
            "name": "New Actor"
        },
        {
            "age": 30,
            "gender": "female",
            "id": 9,
            "name": "New Actress"
        },
        {
            "age": 30,
            "gender": "female",
            "id": 7,
            "name": "New Actress"
        }
        ],
        "success": true
    }
    ```
- /movies
    - Example Request:
    https://zb-fsnd-capstone.herokuapp.com/actors
    - Example Response:
    ```
    {
    "movies": [
        {
            "id": 2,
            "release_date": "Thu, 08 Feb 2001 00:00:00 GMT",
            "title": "Bad Movie"
        },
        {
            "id": 4,
            "release_date": "Sat, 08 Feb 2003 00:00:00 GMT",
            "title": "Big Fat Liar"
        },
        {
            "id": 6,
            "release_date": "Tue, 01 Dec 2020 00:00:00 GMT",
            "title": "New Movie"
        },
        {
            "id": 7,
            "release_date": "Tue, 01 Dec 2020 00:00:00 GMT",
            "title": "New Movie"
        },
        {
            "id": 5,
            "release_date": "Sun, 08 Feb 2004 00:00:00 GMT",
            "title": "Obese Liar"
        },
        {
            "id": 1,
            "release_date": "Tue, 08 Feb 2000 00:00:00 GMT",
            "title": "Skinny Liar"
        }
        ],
        "success": true
    }
    ```
###### (requires Assistant permissions)
- /actors/<int:actor_id>
    - Example Request:
    https://zb-fsnd-capstone.herokuapp.com/actors/1
    - Example Response:
    ```
    {
    "actors": {
        "age": 30,
        "gender": "male",
        "id": 1,
        "name": "Benedict Cumberbatch"
        },
        "success": true
    }
    ```
- /movies/<int:movie_id>
    - Example Request:
        https://zb-fsnd-capstone.herokuapp.com/movies/1
    - Example Response:
    ```
    {
    "movies": {
        "id": 1,
        "release_date": "Tue, 08 Feb 2000 00:00:00 GMT",
        "title": "Skinny Liar"
        },
        "success": true
    }
    ```

DELETE: delete an actor or movie
###### (requires Director permissions)
- /actors/<int:actor_id>
    - Example Request:
    https://zb-fsnd-capstone.herokuapp.com/actors/5
    - Example Response:
    ```
    {
    "actor_id": 5,
    "success": true
    }
    ```
###### (requires Producer permissions)
- /movies/<int:movie_id>
    - Example Request:
    https://zb-fsnd-capstone.herokuapp.com/movies/5
    - Example Response:
    ```
    {
    "movie_id": 5,
    "success": true
    }
    ```


POST: create a new actor or movie
###### (requires Director permissions)
- /actors
    - Example Request:
    https://zb-fsnd-capstone.herokuapp.com/actors
    - Example Body:
    ```
    {
    "age": 30,
    "gender": "female",
    "name": "New Actress"
    }
    ```
    - Example Response:
    ```
    {
    "actor": {
        "age": 30,
        "gender": "female",
        "id": 10,
        "name": "New Actress"
    },
    "success": true
    }
    ```

###### (requires Producer permissions)
- /movies
    - Example Request:
    https://zb-fsnd-capstone.herokuapp.com/movies
    - Example Body:
    ```
    {
    "title": "New Movie",
    "release_date": "12/01/4020"
    }
    ```
    - Example Response:
    ```
    {
    "movie": {
        "id": 8,
        "release_date": "Tue, 01 Dec 4020 00:00:00 GMT",
        "title": "New Movie"
    },
    "success": true
    }
    ```

PATCH: edit info of an actor or movie
###### (requires Director permissions)
- /actors/<int:actor_id>
    - Example Request:
    https://zb-fsnd-capstone.herokuapp.com/actors/10
    - Example Body:
    ```
    {
    "age": 300
    }
    ```
    - Example Response:
    ```
    {
    "actor": {
        "age": 300,
        "gender": "female",
        "id": 10,
        "name": "New Actress"
    },
    "success": true
    }
    ```
- /movies/<int:movie_id>
    - Example Request:
    https://zb-fsnd-capstone.herokuapp.com/actors/10
    - Example Body:
    ```
    {
    "title": "300"
    }
    ```
    - Example Response:
    ```
    {
    "movie": {
        "id": 5,
        "release_date": "Sun, 08 Feb 2004 00:00:00 GMT",
        "title": "300"
    },
    "success": true
    }
    ```

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