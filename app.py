import os
from flask import Flask, request, abort, jsonify, render_template, \
    redirect, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import Actor, Movie, setup_db, db_drop_and_create_all, db
from auth import AuthError, requires_auth


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={r"/*": {"origins": "*"}})

    # db_drop_and_create_all()


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
        return jsonify({
            'success': True,
            'health': 'App is running.'
        }), 200


    # GET
    @app.route('/actors', methods=['GET'])
    def get_actors():
        
        data = Actor.query.order_by(Actor.name).all()

        return_data = [item.format() for item in data]

        return jsonify({
            'success': True,
            'actors': return_data
        }), 200


    @app.route('/movies', methods=['GET'])
    def get_movies():

        data=Movie.query.order_by(Movie.title).all()

        return_data = [item.format() for item in data]

        return jsonify({
            'success': True,
            'movies': return_data
        }), 200


    @app.route('/actors/<int:actor_id>', methods=['GET'])
    @requires_auth('get:actors')
    def get_actor(payload, actor_id):

        data = Actor.query.get_or_404(actor_id)

        return jsonify({
            'success': True,
            'actors': data.format()
        }), 200


    @app.route('/movies/<int:movie_id>', methods=['GET'])
    @requires_auth('get:movies')
    def get_movie(payload, movie_id):

        data=Movie.query.get_or_404(movie_id)

        return jsonify({
            'success': True,
            'movies': data.format()
        }), 200


    # DELETE
    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actor')
    def delete_actor(payload, actor_id):
        if not actor_id:
            abort(404)

        actor_to_remove = Actor.query.filter_by(id=actor_id)
        if not actor_to_remove:
            abort(404)
            
        try:
            actor_to_remove.delete()
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()

        return jsonify({
        'success': True,
        'actor_id': actor_id
        }), 200


    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movie')
    def delete_movie(payload, movie_id):
        if not movie_id:
            abort(404)

        movie_to_remove = Movie.query.filter_by(id=movie_id)
        if not movie_to_remove:
            abort(404)

        try:
            movie_to_remove.delete()
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()

        return jsonify({
        'success': True,
        'movie_id': movie_id
        }), 200


    # POST
    @app.route('/actors', methods=['POST'])
    @requires_auth('post:new_actor')
    def create_actor(payload):
        data = request.get_json()
        actor = Actor(
            name=data['name'],
            age=data['age'],
            gender=data['gender']
            )
        actor.insert()

        return jsonify({
            'success': True,
            'actor': actor.format(),
        }), 200


    @app.route('/movies', methods=['POST'])
    @requires_auth('post:new_movie')
    def create_movie(payload):
        data = request.get_json()
        movie = Movie(
            title=data['title'],
            release_date=data['release_date']
            )
        movie.insert()

        return jsonify({
            'success': True,
            'movie': movie.format(),
        }), 200


    # PATCH
    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actor')
    def edit_actor(payload, actor_id):
        if not actor_id:
            abort(404)

        actor = Actor.query.get_or_404(actor_id)
        if not actor:
            abort(404)

        data = request.get_json()

        if 'name' in data and data['name'] != '':
            actor.name = data['name']

        if 'age' in data and data['age'] != '':
            actor.age = data['age']

        if 'gender' in data and data['gender'] != '':
            actor.gender = data['gender']

        actor.update()

        return jsonify({
            'success': True,
            'actor': actor.format(),
        }), 200


    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movie')
    def edit_movie(payload, movie_id):
        if not movie_id:
            abort(404)

        movie = Movie.query.get_or_404(movie_id)
        if not movie:
            abort(404)

        data = request.get_json()

        if 'title' in data and data['title'] != '':
            movie.title = data['title']

        if 'release_date' in data and data['release_date'] != '':
            movie.release_date = data['release_date']

        movie.update()

        return jsonify({
            'success': True,
            'movie': movie.format(),
        }), 200


    @app.errorhandler(400)
    @app.errorhandler(401)
    @app.errorhandler(403)
    @app.errorhandler(404)
    @app.errorhandler(405)
    def error_handler(error):
        return jsonify({
            'success': False,
            'error': error.code,
            'message': error.description
        }), error.code

    return app

app = create_app()