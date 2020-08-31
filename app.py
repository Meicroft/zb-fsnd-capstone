import os
from flask import Flask, request, abort, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import Actor, Movie, setup_db, db_drop_and_create_all


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    CORS(app, resources={r"/*": {"origins": "*"}})

    db_drop_and_create_all()

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)

# -----------
# @app.routes
# -----------


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods',
                         'GET, POST, PATCH, DELETE, OPTIONS')
    return response


@app.route('/')
def home():
    return render_template('home.html')


# GET
@app.route('/actors', methods=['GET'])
# @requires_auth('get:actors')
def get_actors():
    return render_template('actors.html', data=Actor.query.order_by(Actor.name).all())


@app.route('/movies', methods=['GET'])
# @requires_auth('get:movies')
def get_movies():
    return render_template('movies.html', data=Movie.query.order_by(Movie.title).all())
    # movies = Movie.query.order_by(Movie.id).all()

    # return jsonify({
    #     'success': True,
    #     'movies': [movie.format() for movie in movies]
    # }), 200


# DELETE
@app.route('/actors/<int:actor_id>', methods=['DELETE'])
# @requires_auth('delete:actor')
def delete_actor(actor_id):
    if not actor_id:
        abort(404)

    actor_to_remove = Actor.query.get(actor_id)
    if not actor_to_remove:
        abort(404)

    actor_to_remove.delete()

    return jsonify({
      'success': True,
      'actor_id': actor_id
    }), 200


@app.route('/movies/<int:movie_id>', methods=['DELETE'])
# @requires_auth('delete:movie')
def delete_movie(movie_id):
    if not movie_id:
        abort(404)

    movie_to_remove = Movie.query.get(movie_id)
    if not movie_to_remove:
        abort(404)

    movie_to_remove.delete()

    return jsonify({
      'success': True,
      'movie_id': movie_id
    }), 200


# POST
@app.route('/actors', methods=['POST'])
# @requires_auth('post:actor')
def create_actor():
    data = request.get_json()

    if 'name' not in data:
        abort(422)
    if 'age' not in data:
        abort(422)
    if 'gender' not in data:
        abort(422)

    actor = Actor(
        name=data['name'],
        age=data['age'],
        gender=data['gender']
        )
    actor.insert()

    return jsonify({
      'success': True,
      'actor': actor.format()
    }), 200


@app.route('/movies', methods=['POST'])
# @requires_auth('post:movie')
def create_movie():
    print(request.get_json())
    data = request.get_json()

    if 'title' not in data:
        abort(422)
    if 'release_date' not in data:
        abort(422)

    movie = Movie(title=data['title'], release_date=data['release_date'])
    movie.insert()

    return jsonify({
      'success': True,
      'movie': movie.format()
    }), 200


# PATCH
@app.route('/actors/<int:actor_id>', methods=['PATCH'])
# @requires_auth('patch:actor')
def edit_actor(actor_id):
    if not actor_id:
        abort(404)

    actor = Actor.query.get(actor_id)
    if not actor:
        abort(404)

    data = request.get_json()

    if 'name' in data and data['name']:
        actor.name = data['name']

    if 'age' in data and data['age']:
        actor.age = data['age']

    if 'gender' in data and data['gender']:
        actor.gender = data['gender']

    actor.update()

    return jsonify({
        'success': True,
        'actor': actor.format(),
    }), 200


@app.route('/movies/<int:movie_id>', methods=['PATCH'])
# @requires_auth('patch:movie')
def edit_movie(movie_id):
    if not movie_id:
        abort(404)

    movie = Movie.query.get(movie_id)
    if not movie:
        abort(404)

    data = request.get_json()

    if 'title' in data and data['title']:
        movie.title = data['title']

    if 'release_date' in data and data['release_date']:
        movie.release_date = data['release_date']

    movie.update()

    return jsonify({
        'success': True,
        'movie': movie.format(),
    }), 200
