import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import statistics
import numpy as np
import pandas as pd
from scipy.stats import norm

file = pd.read_excel('data/ananas.xlsx')
mas  = file.iloc[1:, 1]
n = len(mas)
sort_mas = np.array(sorted(mas))

plt.xlabel('порядковый номер')
plt.ylabel('Цены')
plt.title('Вариационный ряд выборочных цен ананасов с 04.06.2021 по 14.03.2025')
q = list(range(1,n+1))
plt.scatter(q, sort_mas)
plt.grid()
plt.show()

print('Объем выборки: ', n)
sr = statistics.mean(mas)
print("Среднее арифметическое: ", sr)
dis = statistics.variance(mas)
print("дисперсия: ", dis)
med = statistics.median(mas)
print("медиана: ", med)
stotkl = statistics.pstdev(mas)
print("стандартное отклонение: ", stotkl)
moda = statistics.mode(mas)
print("мода: ", moda)
weighted_average = 0
uni, weight = np.unique(sort_mas, return_counts=True)
for i in range(len(uni)):
    weighted_average += (uni[i]*weight[i])
weighted_average /= sum(weight)
print('Среднее взвешенное: ', weighted_average)
print('Объем уникальных значений: ', len(uni))

Q1 = np.quantile(mas, 0.25)
print("Первый квартиль: ", Q1)
Q3 = np.quantile(mas, 0.75)
print("Третий квартиль: ", Q3)
Q2 = np.quantile(mas, 0.5)
print("Второй квартиль: ", Q2)
MKR = Q3 - Q1
print('Межквартильный диапозон: ', MKR )
maxoutlier = Q3 + 1.5 * MKR
minoutlier = Q1 - 1.5 * MKR
left = med - 1.5 * MKR
right = med + 1.5 * MKR

outliers = sort_mas[(sort_mas < minoutlier) | (sort_mas > maxoutlier)]
maxwhisker = sort_mas[sort_mas <= maxoutlier].max()
minwhisker = sort_mas[sort_mas >= minoutlier].min()
print(f"Верхний ус: {maxwhisker}")
print(f"Нижний ус: {minwhisker}")

plt.boxplot(sort_mas)
plt.axhline(Q1, color="r", label = 'Нижний квантиль')
plt.axhline(Q3, color="y", label = 'Верхний квантиль')
plt.axhline(med, color="b", label = 'Медиана')
plt.axhline(left, color="g", label = 'Нижний ус')
plt.axhline(right, color="g", label = 'Верхний ус')
plt.legend()
plt.title("Boxplot")
plt.ylabel("Цены ананасов")
plt.grid(True)
plt.show()


maxnumber = max(sort_mas)
minnumber = min(sort_mas)
print("Минимум: ", minnumber)
print("Максимум: ", maxnumber)
column = int(n / 10)
print(f"Количество интервалов: {column}")
scope = maxnumber - minnumber
print("Размах: ", scope)
step = scope / (column - 1)
print("Шаг: ", step)
border = list()
border.append(-np.inf)
border.append(minnumber + step / 2)
for i in range(column - 2):
    border.append(border[-1] + step)
border.append(np.inf)
kolv = list()
for i in range (len(border) - 1):
    kolv.append(len(sort_mas[np.logical_and(sort_mas>=border[i], sort_mas<border[i+1])]))
ver = list()
for i in range(column):
    ver.append(kolv[i]/n)

fig,ax = plt.subplots()
for k in range(len(border) - 1):
    rect = Rectangle((border[k], 0), width=step, height=kolv[k], edgecolor='r', facecolor='blue', alpha = 0.5)
    ax.add_patch(rect)
rect = Rectangle((border[1], 0), width=-step, height=kolv[0], edgecolor='r', facecolor='blue', alpha = 0.5)
ax.add_patch(rect)
plt.grid(True)
ax.set_xlim(minnumber-2*step, maxnumber+2*step)
ax.set_ylim(0, max(kolv) + 1)
plt.title("Частотная гистограмма")
plt.xlabel("Цены ананасов")
plt.ylabel("Количество")
plt.show()

fig2,ax2 = plt.subplots()
ax2.set_xlim(minnumber-2*step, maxnumber+2*step)
ax2.set_ylim(0, max(ver) + 0.01)
for k in range(len(border) - 1):
    rect = Rectangle((border[k], 0), width=step, height=ver[k], edgecolor='r', facecolor='blue', alpha = 0.5)
    ax2.add_patch(rect)
rect = Rectangle((border[1], 0), width=-step, height=ver[0], edgecolor='r', facecolor='blue', alpha = 0.5)
ax2.add_patch(rect)
plt.grid(True)
plt.title("Вероятностная гистограмма")
plt.xlabel("Цены ананасов")
plt.ylabel("вероятнось попадения в интервал")
plt.axvline(sr, color='black', label='Мат ожидание')
plt.axvline(med, color = 'g', label = 'Медиана')
x = np.linspace(sr - 4*stotkl, sr + 4*stotkl, 1000)
pdf = norm.pdf(x, sr, stotkl)
plt.plot(x, pdf, color = 'orange', label = 'Нормальное распределение')
plt.legend()
plt.show()

ecdf = 0
plt.hlines(ecdf, 0, sort_mas[0], color = 'r')
for i in range(1, n):
    ecdf += 1 / n
    plt.hlines(ecdf, sort_mas[i-1], sort_mas[i], color = 'r')
    plt.scatter(sort_mas[i-1], ecdf, color = 'white', edgecolors='r')
plt.title("Эмпирическая функция распределения")
plt.xlabel('x, цены ананасов')
plt.ylabel('F(x), эмпирическое распределение')
plt.grid(True)
plt.show()
