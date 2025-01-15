# Подключение библиотек
import krpc   # kRPC | Соединение с Kerbal Space Program
import time   # time | Создание задержек времени
import json   # JSON | Работа с JSON файлами


# Подключение сообщений
with open("simulation/messages.json", "r", encoding="UTF-8") as file_messages:
    messages = json.load(file_messages)


#Сбор текущей информации об аппарате и её запись в файл для логирования
def log():
    ut = str(conn.space_center.ut)                                                                     # Время в игре
    altitude = vessel.flight().mean_altitude                                                           # Высота над уровнем моря
    speed = vessel.flight(vessel.orbit.body.reference_frame).speed                                     # Скорость
    vertical_speed = vessel.flight(vessel.orbit.body.reference_frame).vertical_speed                   # Вертикальная скорость
    horizontal_speed = vessel.flight(vessel.orbit.body.reference_frame).horizontal_speed               # Горизонтальная скорость
    
    with open("simulation/takeoff_logs.json", "r", encoding="UTF-8") as file_logs:
        logs = json.load(file_logs)

    with open("simulation/takeoff_logs.json", "w", encoding="UTF-8") as file_logs:
        logs[ut] = {
            "altitude": altitude,
            "vertical_speed": vertical_speed,
            "horizontal_speed": horizontal_speed,
            "speed": speed,
        }
        json.dump(logs, file_logs, ensure_ascii=True, indent=4)  


# Высоты над уровнем моря
turn_start_altitude = 250  # Начальная для маневрирования
turn_end_altitude = 70000  # Конечная для маневрирования


# Подключение к игре
conn = krpc.connect(name="Takeoff")                                          # Подключение к kRPC-серверу
print(f"Подключение к игре | Соединение: {conn.krpc.get_status().version}")  # Проверка соединения
vessel = conn.space_center.active_vessel                                     # Получение управления над кораблём
print(f"Подключение к игре | Аппарат: {vessel.name}")                        # Проверка статуса


# Настройки
stage_number = 4                                                                 # Начальная ступень
ut = conn.add_stream(getattr, conn.space_center, "ut")                           # Поток для отслеживания времени
altitude = conn.add_stream(getattr, vessel.flight(), "mean_altitude")            # Поток для отслеживания высоты
apoapsis = conn.add_stream(getattr, vessel.orbit, "apoapsis_altitude")           # Поток для отслеживания апоцентра орбиты
periapsis = conn.add_stream(getattr, vessel.orbit, "periapsis_altitude")    
stage_resources = vessel.resources_in_decouple_stage(stage=0, cumulative=False)  # Текущие ресурсы в активной ступени
stage_fuel = conn.add_stream(stage_resources.amount, "LiquidFuel")               # Поток для отслеживания уровня жидкого топлива


# Подготовка аппарата к запуску
vessel.control.sas = False     # Отключение системы автоматической стабилизации
vessel.control.rcs = False     # Отключение реактивной системы управления
vessel.control.throttle = 1.0  # Установка тяги на максимум


# Обратный отсчёт перед запуском
for i in range(3, 0, -1):
    print(messages["start_takeoff-1"] + str(i) + "...")
    time.sleep(1)
print(''.join(messages["start_takeoff-2"]))


# Запуск аппарата
vessel.auto_pilot.engage()                          # Включение автопилота
vessel.auto_pilot.target_pitch_and_heading(90, 90)  # Вертикальный взлёт
vessel.control.activate_next_stage()                # Активация 4-й ступени


# Цикл полёта
while True:
    log()
    
    # Наклон ракеты, если высота над уровнем моря находится в нужном интервале
    if turn_start_altitude < altitude() < turn_end_altitude:    # Если значение высоты над уровнем моря в нужном интервале, то
        corner = 90 * (1 - altitude() / turn_end_altitude)      # вычисление параметра наклона ракеты
        vessel.auto_pilot.target_pitch_and_heading(corner, 90)  # и его изменение 
    if altitude() >= turn_end_altitude:                         # Если значение высоты над уровнем моря больше верхней граиницы, то
        vessel.auto_pilot.target_pitch_and_heading(0, 90)       # ракета будет лететь в горизонтальном положении

    # Проверка наличия топлива в баках ступени
    if stage_fuel() < 0.01:                         # Если топливо на исходе, то
        vessel.control.activate_next_stage()        # активация следующей ступени,
        stage_number -= 1                           # изменение номера текущей ступени,
        stage_resources = vessel.resources_in_decouple_stage(stage=stage_number, cumulative=False)  # получение следую
        stage_fuel = conn.add_stream(stage_resources.amount, "LiquidFuel")
        if stage_number == 3:
            print(''.join(messages["finish_takeoff"]))  # вывод сообщений о завершении взлёта  
        elif stage_number == 2:
            break                                       # Завершение взлёта

    time.sleep(0.01) 
