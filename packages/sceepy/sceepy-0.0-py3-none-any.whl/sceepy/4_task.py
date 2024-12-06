
def t4():
    """

Абсолютно непрерывная случайная величина X
 может принимать значения только в отрезке [4,9]
. На этом отрезке плотность распределения случайной величины X
 имеет вид: f(x)=C(1+7x0,5+8x0,7+4x0,9)1,3
, где C
 – положительная константа. Найдите: 1) константу C
; 2) математическое ожидание E(X)
; 3) стандартное отклонение σX
; 4) квантиль уровня 0,9
 распределения X
.


#1 прототип
import numpy as np
from scipy.integrate import quad
from scipy.optimize import fsolve

# Определим функцию плотности распределения
def f(x, C):
    return C * (1 + 7*x**0.5 + 8*x**0.7 + 4*x**0.9)**1.3

# 1. Найдем константу C
def integrand(x, C):
    return f(x, C)

def find_C():
    # Интегрируем функцию плотности на отрезке [4, 9]
    result, _ = quad(integrand, 4, 9, args=(1,))
    return 1 / result

# 2. Математическое ожидание E(X)
def expectation(C):
    integrand_with_x = lambda x: x * f(x, C)
    E_X, _ = quad(integrand_with_x, 4, 9)
    return E_X

# 3. Стандартное отклонение σ_X
def variance(C, E_X):
    integrand_with_x2 = lambda x: x**2 * f(x, C)
    E_X2, _ = quad(integrand_with_x2, 4, 9)
    return E_X2 - E_X**2

# 4. Квантиль уровня 0.9
def quantile(C):
    # Решаем уравнение P(X <= q) = 0.9
    def cumulative_prob(q):
        integrand_with_x = lambda x: f(x, C)
        result, _ = quad(integrand_with_x, 4, q)
        return result - 0.9

    q = fsolve(cumulative_prob, 6)  # Начальное приближение для квантиля
    return q[0]

# Найдем константу C
C = find_C()
print(C)

# Математическое ожидание E(X)
E_X = expectation(C)
print(E_X)

# Стандартное отклонение σ_X
var_X = variance(C, E_X)
sigma_X = np.sqrt(var_X)
print(sigma_X)

# Квантиль уровня 0.9
q_90 = quantile(C)
print(q_90)


Случайная величина X
 равномерно распределена на отрезке [4,8]
. Случайная величина Y
 выражается через X
 следующим образом: Y=(1+6X0,5+4X0,7+5X0,9)1,3
. Найдите: 1) математическое ожидание E(Y)
; 2) стандартное отклонение σY
; 3) асимметрию As(Y)
; 4) квантиль уровня 0,8
 распределения Y
.

import numpy as np
from scipy.integrate import quad
from scipy.optimize import fsolve


# Определим функцию для Y, заданную через X
def g(x):
    return (1 + 6 * x ** 0.5 + 4 * x ** 0.7 + 5 * x ** 0.9) ** 1.3


# Плотность распределения X (равномерное распределение на [4, 8])
def f_X(x):
    return 1 / 4


# Математическое ожидание E(Y)
def expectation_Y():
    integrand = lambda x: f_X(x) * g(x)
    E_Y, _ = quad(integrand, 4, 8)
    return E_Y


# Математическое ожидание E(Y^2)
def expectation_Y2():
    integrand = lambda x: f_X(x) * g(x) ** 2
    E_Y2, _ = quad(integrand, 4, 8)
    return E_Y2


# Дисперсия Var(Y)
def variance_Y(E_Y):
    E_Y2 = expectation_Y2()
    return E_Y2 - E_Y ** 2


# Стандартное отклонение σ_Y
def std_deviation_Y(E_Y):
    return np.sqrt(variance_Y(E_Y))


# Асимметрия As(Y)
def skewness_Y(E_Y):
    def integrand_skew(x):
        return f_X(x) * (g(x) - E_Y) ** 3

    E_skew, _ = quad(integrand_skew, 4, 8)
    variance = variance_Y(E_Y)
    return E_skew / (variance ** 1.5)

# Генерация случайных значений X, равномерно распределенных на отрезке [4, 8]
n_samples = 1000000000  # Увеличим количество выборок для большей точности
X_samples = np.random.uniform(4, 8, n_samples)

# Вычисление значений Y через X
Y_samples = (1 + 6 * X_samples**0.5 + 4 * X_samples**0.7 + 5 * X_samples**0.9)**1.3

# Вычисление 80-го процентиля для Y с повышенной точностью
quantile_80 = np.percentile(Y_samples, 80)


# Вычислим все необходимые характеристики
E_Y = expectation_Y()
print(E_Y)

sigma_Y = std_deviation_Y(E_Y)
print(sigma_Y)

skewness = skewness_Y(E_Y)
print(skewness)

print(quantile_80)
    """

