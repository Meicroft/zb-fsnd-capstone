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
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)

        setup_db(self.app, self.database_path)

        self.assistant_token = os.environ['assistant_token']
        self.direct_token = os.environ['direct_token']
        self.producer_token = os.environ['producer_token']

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


    # Test for GET / (home endpoint)
    def test_health(self):
        res = self.client().get('/')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertIn('health', data)
        self.assertEqual(data['health'], 'App is running.')


    # Passing Test trying to make a call
    def test_get_actors(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

if __name__ == "__main__":
    unittest.main()
