import datetime

def reduce_to_1_9(n: int) -> int:
    """
    Складывает цифры числа, пока не получится цифра от 1 до 9.
    Если в итоге получается 0, возвращаем 9.
    """
    while n > 9:
        n = sum(int(d) for d in str(n))
    return n or 9

def calculate_numbers(
    birth_day: int,
    birth_month: int,
    birth_year: int,
    ref_date: datetime.date = None
) -> dict:
    """
    Возвращает словарь с пятью числами:
      - personal_year  (Личный год)
      - personal_month (Личный месяц)
      - personal_day   (Личный день)
      - personality    (Число личности)
      - perception     (Число восприятия)
    """
    if ref_date is None:
        ref_date = datetime.date.today()

    # 1) Личный год = sumDigits(день_рождения + месяц_рождения + год_обращения)
    s_year = (
        sum(int(d) for d in f"{birth_day:02d}") +
        sum(int(d) for d in f"{birth_month:02d}") +
        sum(int(d) for d in str(ref_date.year))
    )
    personal_year = reduce_to_1_9(s_year)

    # 2) Личный месяц = личный_год + sumDigits(месяц_обращения)
    s_month = personal_year + sum(int(d) for d in f"{ref_date.month:02d}")
    personal_month = reduce_to_1_9(s_month)

    # 3) Личный день = личный_месяц + sumDigits(день_обращения)
    s_day = personal_month + sum(int(d) for d in f"{ref_date.day:02d}")
    personal_day = reduce_to_1_9(s_day)

    # 4) Число личности = sumDigits(день рождения)
    personality = reduce_to_1_9(sum(int(d) for d in f"{birth_day:02d}"))

    # 5) Число восприятия = sumDigits(дата рождения полностью)
    perception = reduce_to_1_9(
        sum(int(d) for d in f"{birth_day:02d}")
      + sum(int(d) for d in f"{birth_month:02d}")
      + sum(int(d) for d in str(birth_year))
    )

    return {
        "personal_year": personal_year,
        "personal_month": personal_month,
        "personal_day": personal_day,
        "personality": personality,
        "perception": perception,
    }

# Пример самостоятельного запуска для теста
if __name__ == "__main__":
    # Тестовый пример из твоего сообщения: 16.02.1987 и сегодня 26.05.2025
    test_date = datetime.date(2025, 5, 26)
    nums = calculate_numbers(16, 2, 1987, ref_date=test_date)
    print(f"Личный год:   {nums['personal_year']}")
    print(f"Личный месяц:{nums['personal_month']}")
    print(f"Личный день: {nums['personal_day']}")
    print(f"Число личности:  {nums['personality']}")
    print(f"Число восприятия:{nums['perception']}")
