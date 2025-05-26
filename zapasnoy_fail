import datetime

PLANET_MAP = {
    1: ("Солнце", "☀"), 2: ("Луна", "🌙"), 3: ("Юпитер", "📚"),
    4: ("Раху", "🌀"),   5: ("Меркурий", "💬"), 6: ("Венера", "💖"),
    7: ("Кету", "🔮"),   8: ("Сатурн", "🏛"),   9: ("Марс", "🔥"),
}

def reduce_to_digit(n: int) -> int:
    while n > 9:
        n = sum(int(d) for d in str(n))
    return n or 9

def calculate_personal_numbers(day: int, month: int, year: int) -> dict:
    today = datetime.date.today()
    py = reduce_to_digit(day + month + today.year)
    pm = reduce_to_digit(py + today.month)
    pd = reduce_to_digit(pm + today.day)
    per = reduce_to_digit(sum(int(d) for d in str(day)))
    pr = reduce_to_digit(sum(int(d) for d in str(month)))
    return {
        "year": py,   "year_symbol": PLANET_MAP[py][1],
        "month": pm,  "month_symbol": PLANET_MAP[pm][1],
        "day": pd,    "day_symbol": PLANET_MAP[pd][1],
        "personality": per,    "personality_symbol": PLANET_MAP[per][1],
        "perception": pr,      "perception_symbol": PLANET_MAP[pr][1],
    }
