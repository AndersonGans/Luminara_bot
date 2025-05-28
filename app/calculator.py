# app/calculator.py

from datetime import date

def _reduce_to_1_9(n: int) -> int:
    return (n - 1) % 9 + 1

def calc_personal_numbers(datum_rozdeniya: str) -> dict:
    d, m, y = datum_rozdeniya.split('.')
    bd = [int(c) for c in d]
    bm = [int(c) for c in m]
    by = [int(c) for c in y]

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
        "число_восприятия": число_восприятие
    }
