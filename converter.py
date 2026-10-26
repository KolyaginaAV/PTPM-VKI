class Converter:
    @staticmethod
    #пометка/декаратор статического метода, не привязан к объекту
    #Ему не нужен self. Его можно вызывать напрямую через класс, не создавая объект.
    def do(x):
        # x ∈ [100.7; + ∞) -> 1000
        if x >= 100.7:
            return 1000

        # x ∈ (0; 100.7) -> int(x)
        if 0 < x < 100.7:
            return int(x)

        # x == 0.0 -> ValueError
        if x == 0.0:
            raise ValueError("x не может быть равен 0.0")

        # x ∈ [-30.4; 0) -> int(x) - 5
        if -30.4 <= x < 0:
            return int(x) - 5

        # 5. x ∈ (-∞ ; -30.5] -> -2000
        if x <= -30.5:
            return -2000