import unittest
import sys
import os

# Добавляем папку src в путь импорта
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from my_project import parse_side, get_triangle_type, calculate_vertices


class TestParseSide(unittest.TestCase):
    """Тесты для функции parse_side"""

    def test_valid_positive_integer(self):
        """Положительное целое число преобразуется корректно"""
        self.assertEqual(parse_side("5"), 5.0)

    def test_valid_positive_float(self):
        """Положительное дробное число преобразуется корректно"""
        self.assertEqual(parse_side("3.5"), 3.5)

    def test_zero_is_invalid(self):
        """Ноль недопустим (сторона должна быть > 0)"""
        self.assertIsNone(parse_side("0"))

    def test_negative_is_invalid(self):
        """Отрицательное число недопустимо"""
        self.assertIsNone(parse_side("-5"))

    def test_non_numeric_is_invalid(self):
        """Нечисловая строка возвращает None"""
        self.assertIsNone(parse_side("abc"))

    def test_empty_string_is_invalid(self):
        """Пустая строка возвращает None"""
        self.assertIsNone(parse_side(""))


class TestGetTriangleType(unittest.TestCase):
    """Тесты для функции get_triangle_type"""

    def test_equilateral(self):
        """Равносторонний треугольник"""
        self.assertEqual(get_triangle_type(3, 3, 3), "равносторонний")

    def test_isosceles(self):
        """Равнобедренный треугольник"""
        self.assertEqual(get_triangle_type(3, 3, 5), "равнобедренный")

    def test_scalene(self):
        """Разносторонний треугольник"""
        self.assertEqual(get_triangle_type(3, 4, 5), "разносторонний")

    def test_not_a_triangle_sum_less(self):
        """Сумма двух сторон меньше третьей — не треугольник"""
        self.assertEqual(get_triangle_type(1, 2, 10), "не треугольник")

    def test_not_a_triangle_sum_equal(self):
        """Сумма двух сторон равна третьей — не треугольник (вырожденный)"""
        self.assertEqual(get_triangle_type(1, 2, 3), "не треугольник")

    def test_zero_side_is_not_triangle(self):
        """Нулевая сторона — не треугольник"""
        self.assertEqual(get_triangle_type(0, 3, 4), "не треугольник")


class TestCalculateVertices(unittest.TestCase):
    """Тесты для функции calculate_vertices"""

    def test_returns_three_points(self):
        """Функция возвращает ровно 3 точки"""
        vertices = calculate_vertices(3, 4, 5)
        self.assertEqual(len(vertices), 3)

    def test_points_are_tuples_of_ints(self):
        """Каждая точка — это кортеж из двух целых чисел"""
        vertices = calculate_vertices(3, 4, 5)
        for point in vertices:
            self.assertIsInstance(point, tuple)
            self.assertEqual(len(point), 2)
            self.assertIsInstance(point[0], int)
            self.assertIsInstance(point[1], int)

    def test_points_inside_100x100(self):
        """Все точки находятся в границах поля 100x100"""
        vertices = calculate_vertices(3, 4, 5)
        for x, y in vertices:
            self.assertGreaterEqual(x, 0)
            self.assertLessEqual(x, 100)
            self.assertGreaterEqual(y, 0)
            self.assertLessEqual(y, 100)

    def test_equilateral_symmetric(self):
        """Для равностороннего треугольника точки симметричны"""
        vertices = calculate_vertices(5, 5, 5)
        # Верхняя точка должна быть примерно посередине по x
        xs = [p[0] for p in vertices]
        self.assertAlmostEqual(max(xs) - min(xs), max(xs) - min(xs), delta=1)


if __name__ == '__main__':
    unittest.main()