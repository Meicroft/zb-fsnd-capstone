import os
from flask import Flask, request, abort, jsonify, render_template, \
    redirect, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import Actor, Movie, setup_db, db_drop_and_create_all, db
# from auth import AuthError, requires_auth


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    CORS(app, resources={r"/*": {"origins": "*"}})

    # db_drop_and_create_all()

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


@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('css', path)


@app.route('/')
def home():
    return render_template('home.html')


# GET
@app.route('/actors', methods=['GET'])
# @requires_auth('get:actors')
def get_actors():
    return render_template('actors.html',
                           data=Actor.query.order_by(Actor.name).all())


@app.route('/movies', methods=['GET'])
# @requires_auth('get:movies')
def get_movies():
    return render_template('movies.html',
                           data=Movie.query.order_by(Movie.title).all())


@app.route('/actors/<int:actor_id>', methods=['GET'])
def get_actor(actor_id):
    return render_template('actor.html',
                           data=Actor.query.get(actor_id))


@app.route('/movies/<int:movie_id>', methods=['GET'])
def get_movie(movie_id):
    return render_template('movie.html',
                           data=Movie.query.get(movie_id))


# DELETE
@app.route('/actors/<int:actor_id>', methods=['DELETE'])
# @requires_auth('delete:actor')
def delete_actor(actor_id):
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
# @requires_auth('delete:movie')
def delete_movie(movie_id):
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
@app.route('/actors/create', methods=['POST'])
# @requires_auth('post:actor')
def create_actor():
    actor = Actor(
        name=request.form.get('name'),
        age=request.form.get('age'),
        gender=request.form.get('gender')
        )
    actor.insert()

    return redirect(url_for('get_actors'))


@app.route('/movies/create', methods=['POST'])
# @requires_auth('post:movie')
def create_movie():
    movie = Movie(
        title=request.form.get('title'),
        release_date=request.form.get('release_date')
        )
    movie.insert()

    return redirect(url_for('get_movies'))


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
# @requires_auth('patch:movie')
def edit_movie(movie_id):
    if not movie_id:
        abort(404)

    movie = Movie.query.get(movie_id)
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
