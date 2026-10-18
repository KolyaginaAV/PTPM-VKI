from abc import ABC, abstractmethod
#Abstract Base Class
#ABC гарантирует, что наследник реализует все абстрактные методы, иначе Python выдаст ошибку при создании объекта
#abstractmethod — это декоратор ((специальная пометка)), который делает метод «абстрактным»

class UserInterface(ABC): #ABC - этот класс нельзя создать напрямую
    @abstractmethod #метод get_user_input обязан быть переопределён в наследниках
    def get_user_input(self):
        pass #пустой оператор-заглушка

class ConsoleInterface(UserInterface):
    def get_user_input(self):
        a = input("Введите сторону A: ")
        b = input("Введите сторону B: ")
        c = input("Введите сторону C: ")
        return a, b, c