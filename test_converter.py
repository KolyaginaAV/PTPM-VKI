import unittest
from converter import Converter

class TestConverter(unittest.TestCase):
    # Проверка x >= 100.7 -> 1000
    def test_upper_boundary(self):
        """Граница: x = 100.7 -> 1000"""
        self.assertEqual(Converter.do(100.7), 1000)

    def test_high_positive(self):
        """Больше 100.7: x = 100.8 -> 1000, x = 999.9 -> 1000"""
        self.assertEqual(Converter.do(100.8), 1000)
        self.assertEqual(Converter.do(999.9), 1000)

    # 2. Проверка 0 < x < 100.7 -> int(x)
    def test_positive_regular(self):
        """положительное: 65.7 -> 65"""
        self.assertEqual(Converter.do(65.7), 65)

    def test_positive_small(self):
        """Маленькое положительное: 0.1 -> 0"""
        self.assertEqual(Converter.do(0.1), 0)

    def test_positive_near_boundary(self):
        """Близко к верхней границе: 100.6 -> 100"""
        self.assertEqual(Converter.do(100.6), 100)

    # 3. Проверка x == 0.0 -> ValueError
    def test_zero_raises_error(self):
        """x = 0.0 -> ValueError"""
        #with - «выполни блок кода внутри, и примени к нему этот контекст»
        #Ожидает, что внутри блока with будет выброшено исключение ValueError
        with self.assertRaises(ValueError):
            Converter.do(0.0)

    # 4. Проверка -30.4 <= x < 0 -> int(x) - 5
    def test_lower_boundary(self):
        """Граница: -30.4 -> int(-30.4) - 5 = -30 - 5 = -35"""
        self.assertEqual(Converter.do(-30.4), -35)

    def test_negative_regular(self):
        """отрицательное: -10.5 -> int(-10.5) - 5 = -10 - 5 = -15"""
        self.assertEqual(Converter.do(-10.5), -15)

    def test_negative_near_zero(self):
        """Близко к нулю: -0.1 -> int(-0.1) - 5 = 0 - 5 = -5"""
        self.assertEqual(Converter.do(-0.1), -5)

    # 5. Проверка x <= -30.5 -> -2000
    def test_negative_boundary(self):
        """Верхняя граница: -30.5 -> -2000"""
        self.assertEqual(Converter.do(-30.5), -2000)

    def test_negative_far(self):
        """Далеко за границей: -94.5 -> -2000"""
        self.assertEqual(Converter.do(-94.5), -2000)

    def test_negative_min(self):
        """маленькое: -999.9 -> -2000"""
        self.assertEqual(Converter.do(-999.9), -2000)

if __name__ == '__main__':
    unittest.main()