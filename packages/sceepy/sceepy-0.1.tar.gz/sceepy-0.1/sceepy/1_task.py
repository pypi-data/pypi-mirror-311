


def t1():
    """

В первой корзине имеется 12 шаров, при этом количество белых шаров равно либо 5, либо 10.
Оба варианта равновероятны. Во второй корзине имеется 29 шаров, а количество белых шаров равно 2, 10 или 13
Эти три варианта также равновероятны. Из обеих корзин все шары перекладываются в третью корзину.
Какова вероятность P(A), что случайно вынутый из третьей корзины шар окажется белым (событие A)?
Найдите условную вероятность P(H|A), того, что случайно вынутый из третьей корзины шар
первоначально находился в первой корзине (событие H), при условии, что он белый (событие A)?



white_first = [5,10]
white_second = [2,10,13]

p_first = 1 / len(white_first)
p_second = 1 /len(white_second)

total_first = 12
total_second = 29
total_balls = total_first + total_second

p_A = 0
for i in white_first:
    for j in white_second:
        p_combination = p_first * p_second
        total_white = i+j

        p_A += (total_white / total_balls) * p_combination

print(p_A, "1 прототип")

p_H_A = 0

for i in white_first:
    for j in white_second:
        p_combination = p_first * p_second
        total_white = i+j
        p_white = total_white / total_balls
        p_white_first = i/total_white
        p_H_A += p_combination * p_white * p_white_first

p_H_A /= p_A
print(p_H_A, "1 прототип")


Имеется две корзины с белыми и черными шарами. В первой корзине всего 13 шаров,
при этом количество белых шаров распределено по биномиальному закону с параметрами n = 5 и p = 0,3.
Во второй корзине имеется всего 12 шаров, при этом количество белых шаров распределено
по биномиальному закону с параметрами n = 11 и p = 0,1.
Из обеих корзин все шары перекладываются в третью корзину. 1) Какова вероятность P(A), что случайно вынутый из третьей
корзины шар окажется белым (событие A)?
2) Найдите условную вероятность P(H|A), того, что случайно вынутый из
третьей корзины шар первоначально находился в первой корзине (событие H), при условии, что он белый (событие A)?

from scipy.stats import binom

n1, p1 = 5, 0.3
n2, p2 = 11, 0.1

total_first = 13
total_second = 12
total_balls = total_first + total_second

p_A = 0
for i in range(0, n1+1):
    for j in range(0,n2+1):
        p_combination = binom.pmf(i,n1,p1) * binom.pmf(j,n2,p2)
        total_white = i+j
        p_white = total_white / total_balls
        p_A += p_combination * p_white

p_H_A = 0
for i in range(0, n1+1):
    for j in range(0,n2+1):
        p_combination = binom.pmf(i, n1, p1) * binom.pmf(j, n2, p2)
        total_white = i + j
        if total_white > 0:
            p_white = total_white / total_balls
            p_white_first = i/total_white
            p_H_A += p_combination * p_white * p_white_first

p_H_A /= p_A
print(p_A, "2 прототип")
print(p_H_A, "2 прототип")


1. Имеется две корзины с белыми и черными шарами.
В первой корзине количество белых – 9, количество черных – 13.
Во второй корзине количество белых – 19, количество черных – 20.
Из первой корзины случайно, без возвращения, излекаются 7 шаров, а из второй – 8 шаров.
Отобранные из обеих корзин шары перекладываются в третью корзину.
1) Какова вероятность $P(A)$, что случайно вынутый из третьей корзины шар окажется белым (событие $A$)?
2) Найдите условную вероятность $P(H|A)$, того, что случайно вынутый из третьей корзины шар
первоначально находился в первой корзине (событие $H$), при условии, что он белый (событие $A$)?<br/>


from scipy.special import comb

w_a_1, b_a_1 = 9, 13
w_a_2, b_a_2 = 19, 20

draw_f = 7
draw_s = 8
draw_total = draw_f + draw_s

def hp(interest, other, total, total_interest):
    return comb(interest, total_interest) * comb(other, total - total_interest) / comb(interest + other,total)

p_A = 0
for i in range(0, draw_f + 1):
    for j in range(0, draw_s + 1):
        p_combination = hp(w_a_1, b_a_1, draw_f, i) * hp(w_a_2, b_a_2, draw_s, j)
        total_white = i+j
        p_white = total_white/draw_total if total_white > 0 else 0
        p_A += p_combination * p_white
p_H_A = 0
for i in range(0, draw_f + 1):
    for j in range(0, draw_s + 1):
        p_combination = hp(w_a_1, b_a_1, draw_f, i) * hp(w_a_2, b_a_2, draw_s, j)
        total_white = i+j
        if total_white > 0:
            p_white = total_white/draw_total if total_white > 0 else 0
            p_white_first = i/total_white
            p_H_A += p_combination * p_white * p_white_first
p_H_A /= p_A

print(p_A, "3 прототип")
print(p_H_A, "3 прототип")


Имеется 37 монет, из которых 6 бракованные: вследствие заводского брака на этих монетах с обеих сторон отчеканен герб. Наугад выбранную монету, не разглядывая, бросают несколько раз.

Какова вероятность, что при 4 бросках она ляжет гербом вверх?
При 4 бросках монета легла гербом вверх. Какова вероятность того, что была выбрана монета с двумя гербами?



total = 37
defective = 6

p_default_coin = 1/2
p_default_coin_4_times = p_default_coin**4
p_defective_coin_4_times = 1**4

total_default = total - defective

p_default_selected = total_default / total
p_defective_selected = defective / total

p_A = p_default_selected * p_default_coin_4_times + p_defective_selected * p_defective_coin_4_times
p_B_A = p_defective_coin_4_times * p_defective_selected / p_A
print(p_A, "4 прототип")
print(p_B_A, "4 прототип")

    """
    pass



