
def t6():
    """
from sympy import symbols, exp, pi, diff, solve, Matrix, simplify

# Объявляем переменные
x, y = symbols('x y')

# Задание плотности распределения
f = (18 * exp(-30*x**2 - 48*x*y + 8*x - 30*y**2 - 5*y - 8524)) / (24 * pi)

# Извлекаем параметры из плотности
quadratic_form = -30*x**2 - 48*x*y + 8*x - 30*y**2 - 5*y

# Найдем математические ожидания (центры)
coeff_x = diff(quadratic_form, x)
coeff_y = diff(quadratic_form, y)
mu_x, mu_y = solve([coeff_x, coeff_y], [x, y])

# Ковариационная матрица строится из коэффициентов квадратичного выражения
# Выделяем матрицу вторых производных (матрица Гессе)
hessian = Matrix([
    [diff(diff(quadratic_form, x), x), diff(diff(quadratic_form, x), y)],
    [diff(diff(quadratic_form, y), x), diff(diff(quadratic_form, y), y)]
])

# Инвертируем Гессиан, чтобы получить ковариационную матрицу
cov_matrix = -hessian.inv()

# Дисперсии и ковариация
var_x = cov_matrix[0, 0]
var_y = cov_matrix[1, 1]
cov_xy = cov_matrix[0, 1]

# Коэффициент корреляции
rho = simplify(cov_xy / (var_x**0.5 * var_y**0.5))

print("1) Математическое ожидание X =", mu_x)
print("2) Математическое ожидание Y =", mu_y)
print("3) Дисперсия X =", var_x)
print("4) Дисперсия Y =", var_y)
print("5) Ковариация =", cov_xy)
print("6) Коэффициент корреляции =", rho)
    """