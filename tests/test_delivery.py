import unittest
import sys
import os

# Добавляем папку src в путь импорта
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from delivery_service import calculate_delivery_cost


class TestDeliveryCost(unittest.TestCase):
    """Тесты для функции calculate_delivery_cost"""

    # Валидация входных данных
    def test_invalid_weight_too_small(self):
        """Вес меньше 0.1 кг — ошибка"""
        cost, date = calculate_delivery_cost(0.05, 100, "обычный")
        self.assertEqual(cost, -1)
        self.assertEqual(date, "0000-00-00")

    def test_invalid_weight_too_large(self):
        """Вес больше 50 кг — ошибка"""
        cost, date = calculate_delivery_cost(55, 100, "обычный")
        self.assertEqual(cost, -1)
        self.assertEqual(date, "0000-00-00")

    def test_invalid_distance_zero(self):
        """Расстояние 0 км — ошибка"""
        cost, date = calculate_delivery_cost(5, 0, "обычный")
        self.assertEqual(cost, -1)
        self.assertEqual(date, "0000-00-00")

    def test_invalid_distance_too_large(self):
        """Расстояние больше 5000 км — ошибка"""
        cost, date = calculate_delivery_cost(5, 6000, "обычный")
        self.assertEqual(cost, -1)
        self.assertEqual(date, "0000-00-00")

    def test_invalid_package_type(self):
        """Неверный тип посылки — ошибка"""
        cost, date = calculate_delivery_cost(5, 100, "неизвестный")
        self.assertEqual(cost, -1)
        self.assertEqual(date, "0000-00-00")

    # Базовый расчёт стоимости
    def test_base_cost_simple(self):
        """Базовая стоимость: 200 + 100*5 = 700 (вес 1 кг, обычный)"""
        cost, date = calculate_delivery_cost(1, 100, "обычный")
        self.assertEqual(cost, 700)

    def test_base_cost_zero_distance_error(self):
        """Расстояние 1 км — минимальная допустимая дистанция"""
        cost, date = calculate_delivery_cost(1, 1, "обычный")
        # 200 + 1*5 = 205
        self.assertEqual(cost, 205)

    # Весовые коэффициенты
    def test_weight_above_5_kg(self):
        """Вес 10 кг — коэффициент 1.2"""
        # База: 200 + 100*5 = 700
        # С весовым коэффициентом: 700 * 1.2 = 840
        cost, date = calculate_delivery_cost(10, 100, "обычный")
        self.assertEqual(cost, 840)

    def test_weight_above_20_kg(self):
        """Вес 25 кг — коэффициент 1.5"""
        # База: 200 + 100*5 = 700
        # С весовым коэффициентом: 700 * 1.5 = 1050
        cost, date = calculate_delivery_cost(25, 100, "обычный")
        self.assertEqual(cost, 1050)

    def test_weight_exactly_5_kg(self):
        """Вес ровно 5 кг — коэффициент не должен применяться"""
        # База: 200 + 100*5 = 700
        cost, date = calculate_delivery_cost(5, 100, "обычный")
        self.assertEqual(cost, 700)  # БАГ? Может быть не 700

    def test_weight_exactly_20_kg(self):
        """Вес ровно 20 кг — коэффициент 1.5"""
        # База: 200 + 100*5 = 700
        # С весовым коэффициентом: 700 * 1.5 = 1050
        cost, date = calculate_delivery_cost(20, 100, "обычный")
        self.assertEqual(cost, 1050)

    # Типы посылок
    def test_fragile_package(self):
        """Хрупкая посылка — +300 к стоимости"""
        # База: 700 + 300 = 1000
        cost, date = calculate_delivery_cost(1, 100, "хрупкий")
        self.assertEqual(cost, 1000)

    def test_dangerous_package(self):
        """Опасная посылка — +1000 к стоимости"""
        # База: 700 + 1000 = 1700
        cost, date = calculate_delivery_cost(1, 100, "опасный")
        self.assertEqual(cost, 1700)

    # Экспресс-доставка (ТУТ БАГ!)
    def test_express_more_expensive_than_regular(self):
        """Экспресс должен быть ДОРОЖЕ обычной доставки — это баг!"""
        regular_cost, _ = calculate_delivery_cost(1, 100, "обычный", is_express=False)
        express_cost, _ = calculate_delivery_cost(1, 100, "обычный", is_express=True)
        # Обычно экспресс дороже. В коде он умножается на 0.5 — это баг.
        self.assertGreater(express_cost, regular_cost,
                           "БАГ: Экспресс должен быть дороже, а не дешевле!")

    # Дата доставки
    def test_delivery_date_format(self):
        """Дата доставки в формате YYYY-MM-DD"""
        _, date = calculate_delivery_cost(1, 100, "обычный")
        # Проверяем длину строки и наличие дефисов
        self.assertEqual(len(date), 10)
        self.assertEqual(date[4], "-")
        self.assertEqual(date[7], "-")

    def test_delivery_date_basic(self):
        """Дата доставки для 100 км — 1 день"""
        # Текущая дата 2026-09-03 + 1 день = 2026-09-04
        _, date = calculate_delivery_cost(1, 100, "обычный")
        self.assertEqual(date, "2026-09-04")

    def test_delivery_date_long_distance(self):
        """Дата доставки для 1500 км — 3 дня"""
        # 1500 // 500 = 3, дата: 2026-09-03 + 3 = 2026-09-06
        _, date = calculate_delivery_cost(1, 1500, "обычный")
        self.assertEqual(date, "2026-09-06")

    def test_express_delivery_date_faster(self):
        """Экспресс должен доставляться быстрее обычной"""
        _, regular_date = calculate_delivery_cost(1, 1500, "обычный", is_express=False)
        _, express_date = calculate_delivery_cost(1, 1500, "обычный", is_express=True)
        # Экспресс должен быть быстрее
        self.assertLess(express_date, regular_date,
                        "БАГ: Экспресс должен доставляться быстрее!")

    # Граничные случаи
    def test_max_weight_and_distance(self):
        """Максимально допустимые значения: 50 кг и 5000 км"""
        cost, date = calculate_delivery_cost(50, 5000, "обычный")
        # База: 200 + 5000*5 = 25200
        # Коэффициент 1.5: 25200 * 1.5 = 37800
        self.assertEqual(cost, 37800)

    def test_min_weight_and_distance(self):
        """Минимально допустимые значения: 0.1 кг и 1 км"""
        cost, date = calculate_delivery_cost(0.1, 1, "обычный")
        # База: 200 + 1*5 = 205
        self.assertEqual(cost, 205)


if __name__ == '__main__':
    unittest.main()