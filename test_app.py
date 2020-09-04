import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie, db_drop_and_create_all


class CastingAgencyTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()

        self.client = self.app.test_client

        self.database_name = "casting_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432',
                                                       self.database_name)

        setup_db(self.app, self.database_path)

        self.assistant_token = os.environ.get('assistant_token')
        self.direct_token = os.environ.get('direct_token')
        self.producer_token = os.environ.get('producer_token')

        # print('assistant', self.assistant_token)
        # print('director', self.direct_token)
        # print('producer', self.producer_token)
        
        self.assistant_auth_header = {'Authorization': 'Bearer {}'.format(self.assistant_token)}
        self.director_auth_header = {'Authorization': 'Bearer {}'.format(self.direct_token)}
        self.producer_auth_header = {'Authorization': 'Bearer {}'.format(self.producer_token)}

        # print('assistant', self.assistant_auth_header)
        # print('director', self.director_auth_header)
        # print('producer', self.producer_auth_header)

        with self.app.app_context():
            db_drop_and_create_all()
            # self.db = SQLAlchemy()
            # self.db.init_app(self.app)
            # self.db.create_all()

        self.new_actor = {
            "name": "Robert Downey Jr.",
            "age": 55,
            "gender": "male"
        }

        self.bad_new_actor = {
            "name": "Robert Downey Jr."
        }

        self.update_actor = {
            "name": "RDJ"
        }

        self.bad_update_actor = {}

        self.new_movie = {
            "title": "Big Fat Liar",
            "release_date": "2/8/2003"
        }

        self.bad_new_movie = {
            "title": "Big Fat Liar"
        }

        self.update_movie = {
            "release_date": "2/8/2004"
        }

        self.bad_update_movie = {}

    # Executed after reach test
    def tearDown(self):
        pass

    #####
    # Unauthorized Tests / Failing Tests
    #####

    # Test for GET / (home endpoint)
    def test_health_as_public(self):
        res = self.client().get('/')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertIn('health', data)
        self.assertEqual(data['health'], 'App is running.')

    # Passing Test to get actors page
    def test_get_actors_as_public(self):
        actor = Actor(name="Robert Downey Jr.", age="55", gender="male")
        actor.insert()

        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    #Passing Test to get movies page
    def test_get_movies_as_public(self):
        movie = Movie(title="Big Fat Liar", release_date="2/8/2003")
        movie.insert()

        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    #Failing Test to get non-existant page
    def test_404_get_fake_page(self):
        res = self.client().get('/studios')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], "The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.")

    #####
    # Assistant Tests
    #####

    # Passing Test to get specific actor with token
    def test_get_specific_actor_as_assistant(self):
        actor = Actor(name="Robert Downey Jr.", age="55", gender="male")
        actor.insert()

        res = self.client().get('/actors/1', headers=self.assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    #Failing Test to get a specific actor
    def test_401_get_specific_actor_as_assistant(self):
        actor = Actor(name="Robert Downey Jr.", age="55", gender="male")
        actor.insert()

        res = self.client().get('/actors/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "The server could not verify that you are authorized to access the URL requested. You either supplied the wrong credentials (e.g. a bad password), or your browser doesn't understand how to supply the credentials required.")
    
    #Failing Test to get a fake specific actor
    def test_404_get_specific_actor_as_assistant(self):
        res = self.client().get('/actors/30', headers=self.assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.")

    #Passing Test to get specific movie with token
    def test_get_specific_movie_as_assistant(self):
        movie = Movie(title="Big Fat Liar", release_date="2/8/2003")
        movie.insert()

        res = self.client().get('/movies/1', headers=self.assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    #Failing Test tp get a specific movie
    def test_401_get_specific_movie_as_assistant(self):
        movie = Movie(title="Big Fat Liar", release_date="2/8/2003")
        movie.insert()

        res = self.client().get('/movies/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "The server could not verify that you are authorized to access the URL requested. You either supplied the wrong credentials (e.g. a bad password), or your browser doesn't understand how to supply the credentials required.")

    #Failing Test to get a fake specific movie
    def test_404_get_specific_movie_as_assistant(self):
        res = self.client().get('/movies/30', headers=self.assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.")

    #####
    # Director Tests
    #####

    #Passing Test to create an actor
    def test_post_actor_as_director(self):
        res = self.client().post('/actors', headers=self.director_auth_header, json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    #Passing Test to patch an actor
    def test_update_actor_as_director(self):
        actor = Actor(name="Robert Downey Jr.", age="55", gender="male")
        actor.insert()

        res = self.client().patch('/actors/1', headers=self.director_auth_header, json=self.update_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    #Passing Test to delete an actor
    def test_delete_actor_as_director(self):
        actor = Actor(name="Robert Downey Jr.", age="55", gender="male")
        actor.insert()

        res = self.client().get('/actors/1', headers=self.director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    #Failing Test to create an actor
    def test_401_post_actor_as_public(self):
        res = self.client().post('/actors', json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "The server could not verify that you are authorized to access the URL requested. You either supplied the wrong credentials (e.g. a bad password), or your browser doesn't understand how to supply the credentials required.")

    #Failing Test to patch an actor
    def test_401_update_actor_as_public(self):
        actor = Actor(name="Robert Downey Jr.", age="55", gender="male")
        actor.insert()

        res = self.client().patch('/actors/1', json=self.update_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "The server could not verify that you are authorized to access the URL requested. You either supplied the wrong credentials (e.g. a bad password), or your browser doesn't understand how to supply the credentials required.")

    #Failing Test to delete an actor
    def test_401_delete_actor_as_public(self):
        actor = Actor(name="Robert Downey Jr.", age="55", gender="male")
        actor.insert()

        res = self.client().get('/actors/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "The server could not verify that you are authorized to access the URL requested. You either supplied the wrong credentials (e.g. a bad password), or your browser doesn't understand how to supply the credentials required.")

    #####
    # Producer Tests
    #####

    #Passing Test to create a movie
    def test_post_movie_as_producer(self):
        res = self.client().post('/movies', headers=self.producer_auth_header, json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    #Passing Test to delete an actor
    def test_delete_movie_as_producer(self):
        movie = Movie(title="Big Fat Liar", release_date="2/8/2003")
        movie.insert()

        res = self.client().get('/movies/1', headers=self.producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    #Failing Test to create a movie
    def test_401_post_movie_as_public(self):
        res = self.client().post('/movies', json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "The server could not verify that you are authorized to access the URL requested. You either supplied the wrong credentials (e.g. a bad password), or your browser doesn't understand how to supply the credentials required.")

    #Passing Test to delete an actor
    def test_401_delete_movie_as_public(self):
        movie = Movie(title="Big Fat Liar", release_date="2/8/2003")
        movie.insert()

        res = self.client().get('/movies/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "The server could not verify that you are authorized to access the URL requested. You either supplied the wrong credentials (e.g. a bad password), or your browser doesn't understand how to supply the credentials required.")



if __name__ == "__main__":
    unittest.main()
