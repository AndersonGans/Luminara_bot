import datetime

# Нумерологическая карта: номер → (название планеты, символ)
PLANET_MAP = {
    1: ("Солнце", "☀️"),
    2: ("Луна", "🌙"),
    3: ("Юпитер", "🪐"),
    4: ("Раху", "☄️"),
    5: ("Меркурий", "☿️"),
    6: ("Венера", "❤"),
    7: ("Кету", "☄️"),
    8: ("Сатурн", "♄"),
    9: ("Марс", "🔥"),
}

def reduce_to_digit(n: int) -> int:
    """
    Сводит число к одной цифре по сумме его цифр (но 9 остаётся 9, не 0).
    """
    while n > 9:
        n = sum(int(d) for d in str(n))
    return n or 9

def calculate_personal_numbers(day: int, month: int, year: int) -> dict:
    """
    Вычисляет:
      • Личный год  (py)
      • Личный месяц (pm)
      • Личный день (pd)
      • Число личности (personality)
      • Число восприятия (perception)
    и сразу возвращает их вместе с символами.
    """
    today = datetime.date.today()

    # Личный год = день + месяц + сумма цифр текущего года
    py = reduce_to_digit(day + month + sum(int(d) for d in str(today.year)))
    # Личный месяц = личный год + номер текущего месяца
    pm = reduce_to_digit(py + today.month)
    # Личный день = личный месяц + номер текущего дня
    pd = reduce_to_digit(pm + today.day)

    # Число личности = редуцированная сумма всех цифр дня + цифр года рождения
    personality = reduce_to_digit(
        sum(int(d) for d in f"{day:02d}") +
        sum(int(d) for d in str(year))
    )

    # Число восприятия = редуцированная сумма всех цифр дня + месяца + года рождения
    perception = reduce_to_digit(day + month + sum(int(d) for d in str(year)))

    return {
        "year": py,
        "year_symbol": PLANET_MAP[py][1],
        "month": pm,
        "month_symbol": PLANET_MAP[pm][1],
        "day": pd,
        "day_symbol": PLANET_MAP[pd][1],
        "personality": personality,
        "personality_symbol": PLANET_MAP[personality][1],
        "perception": perception,
        "perception_symbol": PLANET_MAP[perception][1],
    }
