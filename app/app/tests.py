from django.test import SimpleTestCase
from rest_framework.test import APIClient

from app.calc import add, subtract


class CalcTest(SimpleTestCase):

    def test_add_numbers(self):
        result = add(2, 5)

        self.assertEquals(result, 7)

    def test_substract(self):
        result = subtract(5, 3)
        self.assertEquals(result, 2)


class TestViews(SimpleTestCase):

    def test_get_greetings(self):
        client = APIClient()
        res = client.get('/greetings')

        self.assertEquals(res.status_code, 200)
        self.assertEquals(res.data, ['Hello', 'Hola'])