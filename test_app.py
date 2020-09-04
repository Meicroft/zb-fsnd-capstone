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
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)

        setup_db(self.app, self.database_path)

        self.assistant_token = os.environ['assistant_token']
        self.direct_token = os.environ['direct_token']
        self.producer_token = os.environ['producer_token']

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

        self.VALID_NEW_ACTOR = {
            "name": "Robert Downey Jr.",
            "age": 55,
            "gender": "male"
        }

        self.INVALID_NEW_ACTOR = {
            "name": "Robert Downey Jr."
        }

        self.VALID_UPDATE_ACTOR = {
            "name": "RDJ"
        }

        self.INVALID_UPDATE_ACTOR = {}

        self.VALID_NEW_MOVIE = {
            "title": "Big Fat Liar",
            "release_date": 2/8/2003
        }

        self.INVALID_NEW_MOVIE = {
            "title": "Big Fat Liar"
        }

        self.VALID_UPDATE_MOVIE = {
            "release_date": 2/8/2004
        }

        self.INVALID_UPDATE_MOVIE = {}

    # Executed after reach test
    def tearDown(self):
        pass

    # Test for GET / (home endpoint)
    def test_health(self):
        self.client = self.app.test_client
        print(self.client())
        res = self.client().get('/actors')
        print(res)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertIn('health', data)
        self.assertEqual(data['health'], 'App is running.')

    # Failing Test trying to make a call without token
    def test_api_call_without_token(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "Authorization Header is required.")

    # def test_get_actors(self):
    # # Passing Test for GET /actors
    #     res = self.client().get('/actors', headers={
    #         'Authorization': "Bearer {}".format(self.assistant_token)
    #     })
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertTrue(len(data))
    #     self.assertTrue(data["success"])
    #     self.assertIn('actors', data)
    #     self.assertTrue(len(data["actors"]))

    # def test_get_actors_by_id(self):
    # # Passing Test for GET /actors/<actor_id>
    #     res = self.client().get('/actors/1', headers={
    #         'Authorization': "Bearer {}".format(self.assistant_token)
    #     })
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertTrue(data["success"])
    #     self.assertIn('actor', data)
    #     self.assertIn('age', data['actor'])
    #     self.assertTrue(len(data["actor"]["movies"]))

    # def test_404_get_actors_by_id(self):
    # # Failing Test for GET /actors/<actor_id>
    #     res = self.client().get('/actors/100', headers={
    #         'Authorization': "Bearer {}".format(self.assistant_token)
    #     })
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 404)
    #     self.assertFalse(data['success'])
    #     self.assertIn('message', data)

    # def test_create_actor_with_assistant_token(self):
    # # Failing Test for POST /actors
    #     res = self.client().post('/actors', headers={
    #         'Authorization': "Bearer {}".format(self.assistant_token)
    #     }, json=self.VALID_NEW_ACTOR)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 401)
    #     self.assertFalse(data["success"])
    #     self.assertIn('message', data)

    # def test_create_actor(self):
    # # Passing Test for POST /actors
    #     res = self.client().post('/actors', headers={
    #         'Authorization': "Bearer {}".format(self.direct_token)
    #     }, json=self.VALID_NEW_ACTOR)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 201)
    #     self.assertTrue(data["success"])
    #     self.assertIn('created_actor_id', data)

    # def test_422_create_actor(self):
    # # Failing Test for POST /actors
    #     res = self.client().post('/actors', headers={
    #         'Authorization': "Bearer {}".format(self.direct_token)
    #     }, json=self.INVALID_NEW_ACTOR)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 422)
    #     self.assertFalse(data['success'])
    #     self.assertIn('message', data)

    # def test_update_actor_info(self):
    # # Passing Test for PATCH /actors/<actor_id>
    #     res = self.client().patch('/actors/1', headers={
    #         'Authorization': "Bearer {}".format(self.direct_token)
    #     }, json=self.VALID_UPDATE_ACTOR)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertTrue(data["success"])
    #     self.assertIn('actor_info', data)
    #     self.assertEqual(data["actor_info"]["age"],
    #                      self.VALID_UPDATE_ACTOR["age"])

    # def test_422_update_actor_info(self):
    # # Failing Test for PATCH /actors/<actor_id>
    #     res = self.client().patch('/actors/1', headers={
    #         'Authorization': "Bearer {}".format(self.direct_token)
    #     }, json=self.INVALID_UPDATE_ACTOR)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 422)
    #     self.assertFalse(data['success'])
    #     self.assertIn('message', data)

    # def test_delete_actor_with_direct_token(self):
    # # Failing Test for DELETE /actors/<actor_id>
    #     res = self.client().delete('/actors/5', headers={
    #         'Authorization': "Bearer {}".format(self.direct_token)
    #     })
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 401)
    #     self.assertFalse(data["success"])
    #     self.assertIn('message', data)

    # def test_delete_actor(self):
    # # Passing Test for DELETE /actors/<actor_id>
    #     res = self.client().delete('/actors/5', headers={
    #         'Authorization': "Bearer {}".format(self.producer_token)
    #     })
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertTrue(data["success"])
    #     self.assertIn('deleted_actor_id', data)

    # def test_404_delete_actor(self):
    # # Passing Test for DELETE /actors/<actor_id>
    #     res = self.client().delete('/actors/100', headers={
    #         'Authorization': "Bearer {}".format(self.producer_token)
    #     })
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 404)
    #     self.assertFalse(data['success'])
    #     self.assertIn('message', data)

    # def test_get_movies(self):
    # # Passing Test for GET /movies
    #     res = self.client().get('/movies', headers={
    #         'Authorization': "Bearer {}".format(self.assistant_token)
    #     })
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertTrue(len(data))
    #     self.assertTrue(data["success"])
    #     self.assertIn('movies', data)
    #     self.assertTrue(len(data["movies"]))

    # def test_get_movie_by_id(self):
    # # Passing Test for GET /movies/<movie_id>
    #     res = self.client().get('/movies/1', headers={
    #         'Authorization': "Bearer {}".format(self.assistant_token)
    #     })
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertTrue(data["success"])
    #     self.assertIn('movie', data)
    #     self.assertIn('imdb_rating', data['movie'])
    #     self.assertIn('duration', data['movie'])
    #     self.assertIn('cast', data['movie'])
    #     self.assertTrue(len(data["movie"]["cast"]))

    # def test_404_get_movie_by_id(self):
    # # Failing Test for GET /movies/<movie_id>
    #     res = self.client().get('/movies/100', headers={
    #         'Authorization': "Bearer {}".format(self.assistant_token)
    #     })
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 404)
    #     self.assertFalse(data['success'])
    #     self.assertIn('message', data)

    # def test_create_movie_with_assistant_token(self):
    # # Failing Test for POST /movies
    #     res = self.client().post('/movies', headers={
    #         'Authorization': "Bearer {}".format(self.assistant_token)
    #     }, json=self.VALID_NEW_MOVIE)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 401)
    #     self.assertFalse(data["success"])
    #     self.assertIn('message', data)

    # def test_create_movie(self):
    # # Passing Test for POST /movies
    #     res = self.client().post('/movies', headers={
    #         'Authorization': "Bearer {}".format(self.direct_token)
    #     }, json=self.VALID_NEW_MOVIE)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 201)
    #     self.assertTrue(data["success"])
    #     self.assertIn('created_movie_id', data)

    # def test_422_create_movie(self):
    # # Failing Test for POST /movies
    #     res = self.client().post('/movies', headers={
    #         'Authorization': "Bearer {}".format(self.direct_token)
    #     }, json=self.INVALID_NEW_MOVIE)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 422)
    #     self.assertFalse(data['success'])
    #     self.assertIn('message', data)

    # def test_update_movie_info(self):
    # # Passing Test for PATCH /movies/<movie_id>
    #     res = self.client().patch('/movies/1', headers={
    #         'Authorization': "Bearer {}".format(self.direct_token)
    #     }, json=self.VALID_UPDATE_MOVIE)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertTrue(data["success"])
    #     self.assertIn('movie_info', data)
    #     self.assertEqual(data["movie_info"]["imdb_rating"],
    #                      self.VALID_UPDATE_MOVIE["imdb_rating"])

    # def test_422_update_movie_info(self):
    # # Failing Test for PATCH /movies/<movie_id>
    #     res = self.client().patch('/movies/1', headers={
    #         'Authorization': "Bearer {}".format(self.direct_token)
    #     }, json=self.INVALID_UPDATE_MOVIE)
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 422)
    #     self.assertFalse(data['success'])
    #     self.assertIn('message', data)

    # def test_delete_movie_with_direct_token(self):
    # # Failing Test for DELETE /movies/<movie_id>
    #     res = self.client().delete('/movies/3', headers={
    #         'Authorization': "Bearer {}".format(self.direct_token)
    #     })
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 401)
    #     self.assertFalse(data["success"])
    #     self.assertIn('message', data)

    # def test_delete_movie(self):
    # # Passing Test for DELETE /movies/<movie_id>
    #     res = self.client().delete('/movies/3', headers={
    #         'Authorization': "Bearer {}".format(self.producer_token)
    #     })
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertTrue(data["success"])
    #     self.assertIn('deleted_movie_id', data)

    # def test_404_delete_movie(self):
    # # Passing Test for DELETE /movies/<movie_id>
    #     res = self.client().delete('/movies/100', headers={
    #         'Authorization': "Bearer {}".format(self.producer_token)
    #     })
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 404)
    #     self.assertFalse(data['success'])
    #     self.assertIn('message', data)


if __name__ == "__main__":
    unittest.main()
