import math

class QuadraticEquation:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def get_roots(self):
        discriminant = self.b * self.b - 4 * self.a * self.c
        if discriminant < 0:
            return []
        sqrt_d = math.sqrt(discriminant)
        root1 = (-self.b + sqrt_d) / (2 * self.a)
        root2 = (-self.b - sqrt_d) / (2 * self.a)
        return [root1, root2]

    def find_all_roots(self):
        roots = []
        for y in self.get_roots():
            if y == 0:
                roots.append(0)
            elif y > 0:
                roots.append(math.sqrt(y))
                roots.append(-math.sqrt(y))
        return roots

def input_coefficients():
    try:
        a, b, c = map(float, input("Введите коэффициенты A B C: ").split())
        return a, b, c
    except ValueError:
        print("Ошибка ввода")
        return None, None, None

def main():
    a, b, c = input_coefficients()
    if a is None or b is None or c is None:
        return

    equation = QuadraticEquation(a, b, c)
    discriminant = b * b - 4 * a * c
    if discriminant < 0:
        print("Корней нет (дискриминант < 0)")
        return

    roots = equation.find_all_roots()

    if len(roots) == 0:
        print("Корней нет (отрицательные корни уравнения по x^2)")
        return

    print("Корни уравнения:")
    for root in roots:
        print(f"{root:.6f}")

if __name__ == "__main__":
    main()
