from src.calculator import TriangleCalculator
from src.database import TriangleDatabase
from src.interface import ConsoleInterface
from src.notifier import RealNotifier
from src.controller import Controller


def main():
    calculator = TriangleCalculator()
    db = TriangleDatabase()  # БД в памяти
    ui = ConsoleInterface()
    notifier = RealNotifier()

    controller = Controller(calculator, db, ui, notifier)

    print("Добро пожаловать в программу 'Треугольник'!")
    result_type, error_msg = controller.process_user_request()

    print(f"\nРезультат: {result_type}")
    if error_msg:
        print(f"Ошибка: {error_msg}")


if __name__ == "__main__":
    main()