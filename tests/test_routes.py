from app import app
from flask import session
import unittest

class RoutesTestCase(unittest.TestCase):
    """Tests views rendered at routes"""
    def test_index(self):
        with app.test_client() as client:
            resp = client.get('/')
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('<title>Home</title>', html)

    def test_index_w_param(self):
        with app.test_client() as client:
            resp = client.get('/', data = {})
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('<title>Home</title>', html)

    def test_valid_session(self):
        with app.test_client() as client:
            with client.session_transaction() as temp_session:
                temp_session['test_data'] = 'test123!'
            resp = client.get('/')
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(session['test_data'],'test123!')

#    def test_redirect(self):
#        with app.test_client() as client:
#            resp = client.get('/reset', follow_redirects=True)
#            self.assertEqual(resp.status_code, 200)
