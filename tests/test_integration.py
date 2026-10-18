import unittest
from unittest.mock import Mock
from src.calculator import TriangleCalculator
from src.database import TriangleDatabase
from src.controller import Controller


class TestControllerIntegration(unittest.TestCase):

    def setUp(self):
        """Подготовка перед каждым тестом"""
        self.calc = TriangleCalculator()
        self.db = TriangleDatabase()  # Чистая БД в памяти

        # Создаем заглушки (моки) для UI и Notifier (чтобы не ждать input() и не отправлять на сервер)
        self.mock_ui = Mock()
        self.mock_notifier = Mock()

        # Создаем контроллер с моками
        self.controller = Controller(self.calc, self.db, self.mock_ui, self.mock_notifier)

    def test_process_calculates_and_saves_to_db(self):
        """Интеграционный тест: расчет и сохранение в БД"""
        # Настраиваем мок (имитация ввода пользователя)
        self.mock_ui.get_user_input.return_value = ("3", "4", "5")

        # Запускаем
        result_type, result_error = self.controller.process_user_request()

        # Проверяем результат
        self.assertEqual(result_type, "разносторонний")
        self.assertEqual(result_error, "")

        # Проверяем, что запись реально появилась в БД
        db_record = self.db.get_record(3.0, 4.0, 5.0)
        self.assertIsNotNone(db_record)
        self.assertEqual(db_record[0], "разносторонний")

        # Проверяем, что уведомление было вызвано
        self.mock_notifier.send_notification.assert_called_once()

    def test_process_takes_from_db_if_exists(self):
        """Интеграционный тест: если запись есть в БД, калькулятор не вызывается"""
        # Заранее добавляем запись в БД
        self.db.add_record(3.0, 4.0, 5.0, "разносторонний", "")

        # Подменяем калькулятор на мок, чтобы проверить, что он НЕ вызывается
        self.calc.calculate_triangle = Mock()

        self.mock_ui.get_user_input.return_value = ("3", "4", "5")
        self.controller.process_user_request()

        # Проверяем, что калькулятор НЕ вызывался (взяли из БД)
        self.calc.calculate_triangle.assert_not_called()

    def test_process_handles_error_and_notifies(self):
        """Интеграционный тест: отправка уведомления при нечисловых данных"""
        self.mock_ui.get_user_input.return_value = ("abc", "4", "5")

        result_type, result_error = self.controller.process_user_request()

        self.assertEqual(result_type, "")
        self.assertIn("Ошибка", result_error) #проверяет подстроку (в сообщении об ошибке есть слово «Ошибка»)
        # Проверяем, что уведомление отправлено
        self.mock_notifier.send_notification.assert_called()

    def test_process_validates_triangle_inequality(self):
        """Интеграционный тест: проверка неравенства треугольника"""
        self.mock_ui.get_user_input.return_value = ("1", "2", "10")

        result_type, result_error = self.controller.process_user_request()

        self.assertEqual(result_type, "не треугольник")
        self.assertEqual(result_error, "Неравенство треугольника не выполняется")

    def test_notifier_receives_correct_message(self):
        """Тест на проверку, что notifier получает правильное сообщение"""
        self.mock_ui.get_user_input.return_value = ("3", "3", "3")

        self.controller.process_user_request()

        # Получаем аргументы, с которыми был вызван мок
        args, kwargs = self.mock_notifier.send_notification.call_args
        #call_args — запоминает аргументы, с которыми мок был вызван
        #args — позиционные аргументы
        #kwargs — именованные
        message = args[0]

        self.assertIn("равносторонний", message)


if __name__ == '__main__':
    unittest.main()