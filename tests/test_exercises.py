import unittest

from app import app, db
from database import Exercise, User


class ExercisesRouteTests(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

        with app.app_context():
            db.session.remove()
            db.drop_all()
            db.create_all()

            user = User(username='tester')
            user.set_password('secret123')
            db.session.add(user)
            db.session.commit()

            exercise = Exercise(
                title='Hello, Python',
                description='Print a greeting.',
                starter_code='print("Hello")',
                solution='print("Hello")',
                test_cases=[{'name': 'prints hello', 'expected': 'Hello'}],
                difficulty='Easy',
                xp_reward=10,
                order=1
            )
            db.session.add(exercise)
            db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def login(self):
        return self.client.post('/login', data={'username': 'tester', 'password': 'secret123'}, follow_redirects=False)

    def test_exercises_page_requires_login(self):
        response = self.client.get('/exercises')
        self.assertEqual(response.status_code, 302)

    def test_exercises_page_renders_for_logged_in_user(self):
        self.login()
        response = self.client.get('/exercises')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Hello, Python', response.get_data(as_text=True))

    def test_run_exercise_returns_json(self):
        self.login()
        response = self.client.post('/run_exercise', data={'code': 'print("Hello")', 'exercise_id': 1})
        self.assertEqual(response.status_code, 200)
        self.assertIn('output', response.get_json())


if __name__ == '__main__':
    unittest.main()
