import logging
import sys
import math

#1. НАСТРОЙКА ЛОГИРОВАНИЯ
log_format = "%(asctime)s | [%(levelname)-7s] | %(message)s"
date_format = "%Y-%m-%d %H:%M:%S"

logging.basicConfig(
    level=logging.DEBUG,
    format=log_format,
    datefmt=date_format,
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("Logs/file_txt.log", encoding="utf-8")
    ]
)

# 2. ЛОГИКА РАБОТЫ С ТРЕУГОЛЬНИКОМ
def parse_side(value: str) -> float | None:
    """
    Преобразует строку в число. Возвращает None, если данные нечисловые
    или число не положительное.
    """
    try:
        num = float(value)
        if num <= 0:
            return None  # Отрицательные или нулевые стороны недопустимы
        return num
    except (ValueError, TypeError):
        return None


def get_triangle_type(a: float, b: float, c: float) -> str:
    """
    Определяет тип треугольника.
    Возвращает строку: 'равносторонний', 'равнобедренный',
    'разносторонний' или 'не треугольник'.
    """
    # Проверка неравенства треугольника
    if a + b <= c or a + c <= b or b + c <= a:
        return "не треугольник"

    # Проверка типа
    if a == b == c:
        return "равносторонний"
    elif a == b or a == c or b == c:
        return "равнобедренный"
    else:
        return "разносторонний"


def calculate_vertices(a: float, b: float, c: float) -> list[tuple[int, int]]:
    """
    Вычисляет координаты трёх вершин треугольника для отрисовки в поле 100x100.
    Возвращает список из 3 кортежей (x, y).
    """
    # Размещаем вершину A в (0, 0), вершину B в (c, 0)
    # Координаты вершины C вычисляем по теореме косинусов
    ax, ay = 0.0, 0.0
    bx, by = c, 0.0

    # Формула для x-координаты вершины C
    cx = (b ** 2 + c ** 2 - a ** 2) / (2 * c)
    # Формула для y-координаты вершины C (высота)
    cy_squared = b ** 2 - cx ** 2
    cy = math.sqrt(cy_squared) if cy_squared > 0 else 0.0

    # Нормализация координат под поле 100x100
    # Находим максимальный размах по x и по y
    max_x = max(ax, bx, cx)
    max_y = max(ay, by, cy)

    # Коэффициент масштабирования (оставляем небольшой отступ 5px)
    scale = 90.0 / max(max_x, max_y) if max(max_x, max_y) > 0 else 1.0

    # Масштабируем и сдвигаем (добавляем 5px отступа от края)
    def scale_point(x, y):
        return int(round(x * scale)) + 5, int(round(y * scale)) + 5

    return [scale_point(ax, ay), scale_point(bx, by), scale_point(cx, cy)]

# 3. ОСНОВНАЯ ФУНКЦИЯ
def main():
    logging.info("Приложение запущено")

    # Запрашиваем данные у пользователя
    input_a = input("Введите сторону A: ")
    input_b = input("Введите сторону B: ")
    input_c = input("Введите сторону C: ")

    logging.info(f"Входные данные: A={input_a}, B={input_b}, C={input_c}")

    # Парсим стороны
    a = parse_side(input_a)
    b = parse_side(input_b)
    c = parse_side(input_c)

    # Если хотя бы одно значение нечисловое
    if a is None or b is None or c is None:
        logging.error("Ошибка: входные данные нечисловые или не положительные")
        print("")  # Пустая строка для типа
        print([(-2, -2), (-2, -2), (-2, -2)])  # Координаты для нечисловых данных
        return

    # Определяем тип треугольника
    triangle_type = get_triangle_type(a, b, c)
    logging.info(f"Тип треугольника: {triangle_type}")

    # Если не треугольник — координаты сбрасываются в (-1, -1)
    if triangle_type == "не треугольник":
        logging.warning("Треугольник не существует, координаты сброшены в (-1, -1)")
        print(triangle_type)
        print([(-1, -1), (-1, -1), (-1, -1)])
        return

    # Вычисляем координаты вершин
    try:
        vertices = calculate_vertices(a, b, c)
        logging.info(f"Координаты вершин: {vertices}")
        print(triangle_type)
        print(vertices)
    except Exception as e:
        logging.exception("Ошибка при вычислении координат:")
        print(triangle_type)
        print([(-1, -1), (-1, -1), (-1, -1)])


if __name__ == "__main__":
    main()