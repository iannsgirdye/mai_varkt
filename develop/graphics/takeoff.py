import matplotlib.pyplot as plt  # Matplotlib | Рисование графиков
import numpy as np               # NumPy      | Работа с массивами и численными вычислениями
import json

TIME = 250

# Распаковка результатов
with open("math_model/takeoff_logs.json", "r", encoding="UTF-8") as math_file_logs:
    math_logs = json.load(math_file_logs)
    
with open("simulation/takeoff_logs.json", "r", encoding="UTF-8") as ksp_file_logs:
    ksp_logs = json.load(ksp_file_logs)
    max_time = len(ksp_logs)


ut = [x for x in range(1, TIME + 1)]                     # Генерация временной линии

# Компановка результатов математической модели
math_height = [math_logs[key]["height"] for key in math_logs.keys()][:TIME]
math_vertical_speed = [math_logs[key]["vertical_speed"] for key in math_logs.keys()][:TIME]
math_horizontal_speed = [math_logs[key]["horizontal_speed"] for key in math_logs.keys()][:TIME]
math_speed = [math_logs[key]["speed"] for key in math_logs.keys()][:TIME]

# Компановка результатов симуляции в KSP
ksp_altitude = [ksp_logs[key]["altitude"] for key in ksp_logs.keys()][:TIME]
ksp_vertical_speed = [ksp_logs[key]["vertical_speed"] for key in ksp_logs.keys()][:TIME]
ksp_horizontal_speed = [ksp_logs[key]["horizontal_speed"] for key in ksp_logs.keys()][:TIME]
ksp_speed = [ksp_logs[key]["speed"] for key in ksp_logs.keys()][:TIME]

# Компановка погрешностей
delta_height = [0] * TIME
delta_vertical_speed = [0] * TIME
delta_horizontal_speed = [0] * TIME
delta_speed = [0] * TIME
for i in range(TIME):
    delta_height[i] = abs(math_height[i] - ksp_altitude[i])
    delta_vertical_speed[i] = abs(math_vertical_speed[i] - ksp_vertical_speed[i])  
    delta_horizontal_speed[i] = abs(math_horizontal_speed[i] + ksp_horizontal_speed[i])   
    delta_speed[i] = abs(math_speed[i] + ksp_speed[i])
    

# График зависимости вертикальной скорости от времени
plt.subplot(2, 2, 1)                                                            # Определение места графика в сетке
plt.plot(ut, math_vertical_speed, label='Математическая модель', color='blue')  # Строительство 1-го графика
plt.plot(ut, ksp_vertical_speed, label='Симуляция в KSP', color='green')        # Строительство 2-го графика
plt.plot(ut, delta_vertical_speed, label='Погрешность', color='red')            # Строительство 3-го графика
plt.title('Зависимость скорости по вертикали от времени')                       # Название графика
plt.xlabel('Время (с)')                                                         # Название оси абсцисс
plt.ylabel('Скорость (м/с)')                                                    # Название оси ординат
plt.grid(True)                                                                  # Добавление сетки 
plt.legend()                                                                    # Создание графика

# График зависимости горизонтальной скорости от времени
plt.subplot(2, 2, 2)
plt.plot(ut, math_horizontal_speed, label='Математическая модель', color='blue')
plt.plot(ut, delta_horizontal_speed, label='Симуляция в KSP', color='green')
plt.plot(ut, ksp_horizontal_speed, label='Погрешность', color='red')
plt.title('Зависимость скорости по горизонтали от времени')
plt.xlabel('Время (с)')
plt.ylabel('Скорость (м/с)')
plt.grid(True)
plt.legend()

# График зависимости скорости от времени
plt.subplot(2, 2, 3)
plt.plot(ut, math_speed, label='Математическая модель', color='blue')
plt.plot(ut, delta_speed, label='Симуляция в KSP', color='green')
plt.plot(ut, ksp_speed, label='Погрешность', color='red')
plt.title('Зависимость скорости от времени')
plt.xlabel('Время (с)')
plt.ylabel('Скорость (м/с)')
plt.grid(True)
plt.legend()

# График зависимости высоты от времени
plt.subplot(2, 2, 4)
plt.plot(ut, math_height, label='Математическая модель', color='blue')
plt.plot(ut, ksp_altitude, label='Симуляция в KSP', color='green')
plt.plot(ut, delta_height, label='Погрешность', color='red')
plt.title('Зависимость высоты от времени')
plt.xlabel('Время (с)')
plt.ylabel('Высота (м)')
plt.grid(True)
plt.legend()

# Создание окна
plt.tight_layout(pad=3)  # Пространство между графиками
plt.show()               # Показ всех графиков
