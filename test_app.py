import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Actor, Movie

class CastingAgencyTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "casting_test"
        self.database_path = "postgres://{}/{}".format("localhost:5432", self.database_name)
        setup_db(self.app, self.database_path)

        self.new_actor = {
            "name": "Robert DOwney Jr.",
            "age": 45,
            "gender": "male"
        }

        self.new_movie = {
            "title": "Iron Man",
            "release_date": "02/03/2004"
        }
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        pass

    def test_health(self):
        res = self.client().get('/')
        print(res)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertIn('health', data)
        self.assertEqual(data['health'], 'App is running.')

if __name__ == "__main__":
    unittest.main()