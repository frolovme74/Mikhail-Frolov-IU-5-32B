import math

def input_coefficients():
    try:
        a, b, c = map(float, input("Введите коэффициенты A B C: ").split())
        return a, b, c
    except ValueError:
        print("Ошибка ввода")
        return None, None, None

def get_roots(a, b, c):
    discriminant = b * b - 4 * a * c
    if discriminant < 0:
        return []
    sqrt_d = math.sqrt(discriminant)
    root1 = (-b + sqrt_d) / (2 * a)
    root2 = (-b - sqrt_d) / (2 * a)
    return [root1, root2]

def main():
    a, b, c = input_coefficients()
    if a is None or b is None or c is None:
        return

    discriminant = b * b - 4 * a * c
    if discriminant < 0:
        print("Корней нет (дискриминант < 0)")
        return

    roots = []
    for y in get_roots(a, b, c):
        if y == 0:
            roots.append(0)
        elif y > 0:
            roots.append(math.sqrt(y))
            roots.append(-math.sqrt(y))

    if len(roots) == 0:
        print("Корней нет (отрицательные корни уравнения по x^2)")
        return

    print("Корни уравнения:")
    for root in roots:
        print(f"{root:.6f}")

if __name__ == "__main__":
    main()
