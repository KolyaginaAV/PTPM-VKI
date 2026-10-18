import math

class TriangleCalculator:
    def calculate_triangle(self, a_str, b_str, c_str):
        try:
            a, b, c = float(a_str), float(b_str), float(c_str)
            if a <= 0 or b <= 0 or c <= 0:
                return "не треугольник", "Стороны должны быть положительными"
            if a + b <= c or a + c <= b or b + c <= a:
                return "не треугольник", "Неравенство треугольника не выполняется"

            if a == b == c:
                return "равносторонний", ""
            elif a == b or a == c or b == c:
                return "равнобедренный", ""
            else:
                return "разносторонний", ""
        except ValueError:
            return "", "Ошибка: введены нечисловые данные"