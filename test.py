import unittest
from app import app

class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_get_functions(self):
        response = self.app.get('/api/functions')
        self.assertEqual(response.status_code, 200)

    def test_translation_endpoint(self):
        response = self.app.post('/api/translation', json={'user-content': 'write me a poem'})
        data = response.get_json()
        self.assertIn('translated_text', data)

    def test_summarize_endpoint(self):
        response = self.app.post('/api/summarize', json={'text': 'Write a concise summary of the following text.'})
        data = response.get_json()
        self.assertIn('summarized_text', data)

if __name__ == '__main__':
    unittest.main()

