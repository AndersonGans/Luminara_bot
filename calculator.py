# calculator.py
import datetime

# Нумерологическая карта планет (пример — подставьте свои символы, если нужно)
PLANET_MAP = {
    1: ("Солнце", "☀️"),
    2: ("Луна", "🌑"),
    3: ("Юпитер", "♃"),
    4: ("Раху", "☾"),
    5: ("Меркурий", "☿"),
    6: ("Венера", "♀️"),
    7: ("Кету", "☾"),
    8: ("Сатурн", "♄"),
    9: ("Марс", "♂️"),
}

def reduce_to_digit(n: int) -> int:
    """Сводит любое число к дигиту 1–9."""
    while n > 9:
        n = sum(int(d) for d in str(n))
    return n or 9

def calculate_personal_numbers(day: int, month: int, year: int) -> dict:
    """
    Вычисляет:
      • Личный год (py)
      • Личный месяц (pm)
      • Личный день (pd)
      • Число личности (per)
      • Число восприятия (pr)
    и возвращает словарь с цифрами и символами.
    """
    today = datetime.date.today()

    # 1) Личный год = день+месяц+год обращения
    py = reduce_to_digit(sum(int(d) for d in f"{day:02d}{month:02d}{today.year}"))

    # 2) Личный месяц = ЛГ + месяц обращения
    pm = reduce_to_digit(py + today.month)

    # 3) Личный день = ЛМ + день обращения
    pd = reduce_to_digit(pm + today.day)

    # 4) Число личности = сумма цифр дня рождения
    per = reduce_to_digit(sum(int(d) for d in f"{day:02d}"))

    # 5) Число восприятия = сумма всех цифр даты рождения
    pr = reduce_to_digit(sum(int(d) for d in f"{day:02d}{month:02d}{year}"))

    return {
        "year": py,              "year_symbol": PLANET_MAP[py][1],
        "month": pm,             "month_symbol": PLANET_MAP[pm][1],
        "day": pd,               "day_symbol": PLANET_MAP[pd][1],
        "personality": per,      "personality_symbol": PLANET_MAP[per][1],
        "perception": pr,        "perception_symbol": PLANET_MAP[pr][1],
    }
