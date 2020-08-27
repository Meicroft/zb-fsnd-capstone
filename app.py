import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import Actor, Movie, setup_db


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    CORS(app)

    return app

app = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)

# -----------
# @app.routes
# -----------

    @app.route('/')
    def health():
        return jsonify({'health': 'App is running.'}), 200

    # GET
    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors():
        actors = Actor.query.order_by(Actor.id).all()

        if not actors:
            abort(404)

        return jsonify({
            'success': True,
            'actors': [actor.format() for actor in actors]
        }), 200

    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies():
        movies = Movie.query.order_by(Movie.id).all()

        if not movies:
            abort(404)

        return jsonify({
            'success': True,
            'movies': [movie.format() for movie in movies]
        }), 200

    # DELETE
    @app.route('/actors/<int:actor_id', methods=['DELETE'])
    @requires_auth('delete:actor')
    def delete_actor():
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
    @requires_auth('delete:movie')
    def delete_movie():
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
    @app.route('/new_actor', methods=['POST'])
    @requires_auth('post:actor')
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

    @app.route('/new_movie', methods=['POST'])
    @requires_auth('post:movie')
    def create_movie():
        data = request.get_json()

        if 'title' not in data:
            abort(422)
        if 'release_date' not in data:
            abort(422)

        movie = Movie(title=data['title'], release=data['release_date'])
        movie.insert()

        return jsonify({
          'success': True,
          'movie': movie.format()
        }), 200

    # PATCH
    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actor')
    def edit_actor():
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
    @requires_auth('patch:movie')
    def edit_movie():
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
