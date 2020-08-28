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

# Endpoints
GET: main info page for actor(s) & movie(s)
###### (requires Assistant permissions)
- /actors
- /movies

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
- /movies/<int:movie_id># zb-fsnd-capstone
