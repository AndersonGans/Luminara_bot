from datetime import date

def mod9(n: int) -> int:
    """
    Возвращает n mod 9, но если результат 0 — возвращает 9.
    """
    m = n % 9
    return m if m != 0 else 9

def calc_personal_numbers(birth_date: str) -> dict:
    """
    Принимает строку birth_date формата "DD.MM.YYYY",
    возвращает словарь:
      - личный_год
      - личный_месяц
      - личный_день
      - число_личности
      - число_восприятия
    """
    # Парсим дату рождения
    try:
        d_str, m_str, y_str = birth_date.split(".")
        bd = [int(d_str[0]), int(d_str[1])]
        bm = [int(m_str[0]), int(m_str[1])]
        by = [int(c) for c in y_str]
    except Exception:
        raise ValueError("Неверный формат birth_date. Нужно DD.MM.YYYY")

    # Цифры сегодняшней даты
    today = date.today()
    td = [int(c) for c in f"{today.day:02d}"]
    tm = [int(c) for c in f"{today.month:02d}"]
    ty = [int(c) for c in f"{today.year:04d}"]

    # Расчёты по формулам Luminara
    personal_year      = mod9(sum(bd + bm + ty))
    personal_month     = mod9(personal_year + sum(tm))
    personal_day       = mod9(personal_month + sum(td))
    number_personality = mod9(sum(bd))
    number_perception  = mod9(sum(bd + bm + by))

    return {
        "личный_год":       personal_year,
        "личный_месяц":     personal_month,
        "личный_день":      personal_day,
        "число_личности":   number_personality,
        "число_восприятия": number_perception
    }
