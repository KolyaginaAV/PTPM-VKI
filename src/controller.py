from .calculator import TriangleCalculator
from .database import TriangleDatabase
from .interface import UserInterface
from .notifier import Notifier


class Controller:
    def __init__(self, calculator, db, ui, notifier):
        self.calculator = calculator
        self.db = db
        self.ui = ui
        self.notifier = notifier

    def process_user_request(self):
        a_str, b_str, c_str = self.ui.get_user_input()

        try:
            a, b, c = float(a_str), float(b_str), float(c_str)
        except ValueError:
            result = self.calculator.calculate_triangle(a_str, b_str, c_str) #oтправляем уведомление об ошибке через
            self.notifier.send_notification(f"Ошибка ввода: {result[1]}")
            return result

        db_record = self.db.get_record(a, b, c)

        if db_record:
            triangle_type, error_msg = db_record
        else:
            triangle_type, error_msg = self.calculator.calculate_triangle(a_str, b_str, c_str)
            self.db.add_record(a, b, c, triangle_type, error_msg)

        self.notifier.send_notification(f"Треугольник {a, b, c}: {triangle_type}. Ошибка: {error_msg}")
        return triangle_type, error_msg