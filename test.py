import unittest
from app import random_result_analyzes, random_name_analyzes, records

from app import app
class AnalyzesTest(unittest.TestCase):

    def test_analyzes_res(self):
        analyzes_list = ["POS", "NEG"]
        self.assertTrue(random_result_analyzes() in analyzes_list)

    def test_analyzes_name(self):
        analyzes_list = ["анализ 0", "анализ 1", "анализ 2", "анализ 3", "анализ 4", "анализ 5", ]
        self.assertTrue(random_name_analyzes() in analyzes_list)

class PagesTest(unittest.TestCase):

    def setUp(self):
        self.app=app.test_client()

    def test_root(self):
        response=self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_records(self):
        response = self.app.get('/records')
        self.assertEqual(response.status_code, 200)

    def test_card(self):
        response = self.app.get('/card/<patient_id>')
        self.assertEqual(response.status_code, 200)

    def test_analyzes(self):
        response = self.app.get('/card/<patient_id>/analyzes')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
