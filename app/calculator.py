    personal_year      = _reduce_to_1_9(sum(bd + bm + ty))
    personal_month     = _reduce_to_1_9(personal_year + sum(tm))
    personal_day       = _reduce_to_1_9(personal_month + sum(td))
    number_personality = _reduce_to_1_9(sum(bd))
    число_восприятие   = _reduce_to_1_9(sum(bd + bm + by))

    return {
        "личный_год":       personal_year,
        "личный_месяц":     personal_month,
        "личный_день":      personal_day,
        "число_личности":   number_personality,
        "число_восприятие": число_восприятие
    }
