# Luminara Bot

Телеграм-бот и API для персональных нумерологических прогнозов по системе Luminara.

## Стек

- FastAPI + Uvicorn  
- Supabase (PostgreSQL + Auth)  
- OpenAI (Chat Completions, кастомный ассистент)  
- Python 3.10+, venv  
- .env для хранения токенов и ключей

## Установка

1. Клонировать:
   ```bash
   git clone git@github.com:AndersonGans/Luminara_bot.git
   cd Luminara_bot

---

## 3. `app/calculator.py`

```python
# app/calculator.py

from datetime import date

def _reduce_to_1_9(n: int) -> int:
    """Приводит n к диапазону 1–9: (n−1) % 9 + 1."""
    return (n - 1) % 9 + 1

def calc_personal_numbers(datum_rozdeniya: str) -> dict:
    """
    Формулы Luminara:
    1) Личный год       = DD + MM + YYYY (текущий) → 1–9
    2) Личный месяц     = Личный год + MM (текущий) → 1–9
    3) Личный день      = Личный месяц + DD (текущий) → 1–9
    4) Число личности   = сумма цифр DD рождения → 1–9
    5) Число восприятия = сумма цифр DDMMYYYY рождения → 1–9
    """
    d, m, y = datum_rozdeniya.split('.')
    bd = [int(c) for c in d]      # [d1, d2]
    bm = [int(c) for c in m]      # [m1, m2]
    by = [int(c) for c in y]      # [y1,y2,y3,y4]

    today = date.today()
    td = [int(c) for c in f"{today.day:02d}"]
    tm = [int(c) for c in f"{today.month:02d}"]
    ty = [int(c) for c in str(today.year)]

    личный_год        = _reduce_to_1_9(sum(bd + bm + ty))
    личный_месяц     = _reduce_to_1_9(личный_год + sum(tm))
    личный_день      = _reduce_to_1_9(личный_месяц + sum(td))
    число_личности   = _reduce_to_1_9(sum(bd))
    число_восприятия = _reduce_to_1_9(sum(bd + bm + by))

    return {
        "личный_год":       личный_год,
        "личный_месяц":     личный_месяц,
        "личный_день":      личный_день,
        "число_личности":   число_личности,
        "число_восприятия": число_восприятия
    }
