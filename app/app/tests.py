from django.test import SimpleTestCase
from app import calc

class CalcTests(SimpleTestCase):

    def test_add_numbers(self):
        res = calc.add(3,4)
        self.assertEquals(res, 7)


    def test_subtract_numbers(self):
        res = calc.subtract(10, 15)

        self.assertEquals(res,5)