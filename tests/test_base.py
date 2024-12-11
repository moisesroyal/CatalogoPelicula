from flask_testing import TestCase
from flask import current_app, url_for
from main import app

class MainTest(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        return app

    def test_app_exists(self):
        self.assertIsNotNone(current_app)

    def test_app_in_test_mode(self):
        self.assertTrue(current_app.config['TESTING'])

    def test_index_redirects(self):
        response = self.client.get(url_for('index'))
        self.assertEqual(response.location, url_for('hello', _external=False))

    def test_hello_get(self):
        response_login = self.client.post(url_for('auth.login'), data={'username': 'fake', 'password': 'fake-password'})
        self.assertRedirects(response_login, url_for('hello', _external=False))  

        response = self.client.get(url_for('hello'))
        self.assert200(response)


    def test_hello_post(self):
        response = self.client.post(url_for('hello'))
        self.assertEqual(response.status_code, 405)

    def test_auth_blueprint_exists(self):
        self.assertIn('auth', self.app.blueprints)

    def test_auth_login_get(self):
        response = self.client.get(url_for('auth.login'))
        self.assert200(response)

    def test_auth_login_template(self):
        self.client.get(url_for('auth.login'))
        self.assertTemplateUsed('login.html')

    def test_auth_login_post(self):
        fake_form = {
            'username': 'fake',
            'password': 'fake-password'
        }
        response = self.client.post(url_for('auth.login'), data=fake_form)
        self.assertEqual(response.location, url_for('index', _external=False))
