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
        
        self.assistant_auth_header = {'Authorization': 'Bearer {}'.format(self.assistant_token)}
        
        self.director_auth_header = {'AUthorization': 'Bearer {}'.format(self.direct_token)}

        self.producer_auth_header = {'AUthorization': 'Bearer {}'.format(self.producer_token)}

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
            "release_date": 2/8/2003
        }

        self.bad_new_movie = {
            "title": "Big Fat Liar"
        }

        self.update_movie = {
            "release_date": 2/8/2004
        }

        self.bad_update_movie = {}

    # Executed after reach test
    def tearDown(self):
        pass

    #####
    # Unauthorized Tests / Failing Tests
    #####

    # Test for GET / (home endpoint)
    def test_health(self):
        res = self.client().get('/')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertIn('health', data)
        self.assertEqual(data['health'], 'App is running.')

    # Passing Test to get actors page
    def test_get_actors(self):
        actor = Actor(name="Robert Downey Jr.", age="55", gender="male")
        actor.insert()

        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    #Passing Test to get movies page
    def test_get_movies(self):
        movie = Movie(title="Big Fat Liar", release_date="2/8/2003")
        movie.insert()

        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    #####
    # Assistant Tests
    #####

    # Passing Test to get specific actor with token
    def test_get_specific_actor(self):
        actor = Actor(name="Robert Downey Jr.", age="55", gender="male")
        actor.insert()

        res = self.client().get('/actors/1', headers=self.assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    #Failing Test to get a specific actor
    def test_401_get_specific_actor(self):
        actor = Actor(name="Robert Downey Jr.", age="55", gender="male")
        actor.insert()

        res = self.client().get('/actors/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unauthorized')

    #Passing Test to get specific movie with token
    def test_get_specific_movie(self):
        movie = Movie(title="Big Fat Liar", release_date="2/8/2003")
        movie.insert()

        res = self.client().get('/movies/1', headers=self.assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    #Failing Test tp get a specific movie
    def test_401_get_specific_movie(self):
        movie = Movie(title="Big Fat Liar", release_date="2/8/2003")
        movie.insert()

        res = self.client().get('/movies/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unauthorized')

    #####
    # Director Tests
    #####

    #Passing Test to create an actor
    def test_post_actor(self):
        res = self.client().post('/actors', headers=self.director_auth_header, json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

if __name__ == "__main__":
    unittest.main()
