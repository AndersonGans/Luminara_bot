# app/calculator.py

from datetime import date

def _mod9_or_9(n: int) -> int:
    """Возвращает n mod 9, но если результат 0 — возвращает 9."""
    m = n % 9
    return m if m != 0 else 9

def calc_personal_numbers(birth_date: str) -> dict:
    """
    Принимает строку birth_date формата "DD.MM.YYYY",
    возвращает:
      - personal_year (Личный год)
      - personal_month (Личный месяц)
      - personal_day (Личный день)
      - number_personality (Число личности)
      - number_perception (Число восприятия)
    """
    # 1) Извлечь цифры из birth_date
    try:
        d, m, y = birth_date.split('.')
        bd1, bd2 = int(d[0]), int(d[1])
        bm1, bm2 = int(m[0]), int(m[1])
        by_digits = [int(c) for c in y]  # [year1, year2, year3, year4]
    except Exception:
        raise ValueError("Неверный формат birth_date. Должен быть DD.MM.YYYY")

    # 2) Извлечь цифры из сегодняшней даты
    today = date.today()
    td = f"{today.day:02d}"
    tm = f"{today.month:02d}"
    ty = f"{today.year:04d}"
    td1, td2 = int(td[0]), int(td[1])
    tm1, tm2 = int(tm[0]), int(tm[1])
    ty_digits = [int(c) for c in ty]  # [year_msg1..4]

    # --- Личный год ---
    sum_year = td1 + td2 + tm1 + tm2 + sum(ty_digits)
    personal_year = _mod9_or_9(sum_year)

    # --- Личный месяц ---
    sum_month = personal_year + tm1 + tm2
    personal_month = _mod9_or_9(sum_month)

    # --- Личный день ---
    sum_day = personal_month + td1 + td2
    personal_day = _mod9_or_9(sum_day)

    # --- Число личности (только из digits дня рождения) ---
    sum_personality = bd1 + bd2
    number_personality = _mod9_or_9(sum_personality)

    # --- Число восприятия (из всех digits даты рождения) ---
    sum_perception = bd1 + bd2 + bm1 + bm2 + sum(by_digits)
    number_perception = _mod9_or_9(sum_perception)

    return {
        "personal_year": personal_year,
        "personal_month": personal_month,
        "personal_day": personal_day,
        "number_personality": number_personality,
        "number_perception": number_perception
    }
