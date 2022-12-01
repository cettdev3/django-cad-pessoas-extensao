import datetime

def intervening_weekdays(start, end, inclusive=True, weekdays=[0, 1, 2, 3, 4, 5, 6]):
    if isinstance(start, datetime.datetime):
        start = start.date()               # make a date from a datetime

    if isinstance(end, datetime.datetime):
        end = end.date()                   # make a date from a datetime

    if end < start:
        # you can opt to return 0 or swap the dates around instead
        raise ValueError("start date must be before end date")

    if inclusive:
        end += datetime.timedelta(days=1)  # correct for inclusivity

    try:
        # collapse duplicate weekdays
        weekdays = {weekday % 7 for weekday in weekdays}
    except TypeError:
        weekdays = [weekdays % 7]

    ref = datetime.date.today()                    # choose a reference date
    ref -= datetime.timedelta(days=ref.weekday())  # and normalize its weekday

    # sum up all selected weekdays (max 7 iterations)
    return sum((ref_plus - start).days // 7 - (ref_plus - end).days // 7
               for ref_plus in
               (ref + datetime.timedelta(days=weekday) for weekday in weekdays))

dataInicioDate = datetime.datetime.strptime("2022-11-01", '%Y-%m-%d')
dataFimDate = datetime.datetime.strptime("2022-11-05", '%Y-%m-%d')

segunda = intervening_weekdays(dataInicioDate, dataFimDate, True, [0])
terca = intervening_weekdays(dataInicioDate, dataFimDate, True, [1])
quarta = intervening_weekdays(dataInicioDate, dataFimDate, True, [2])
quinta = intervening_weekdays(dataInicioDate, dataFimDate, True, [3])
sexta = intervening_weekdays(dataInicioDate, dataFimDate, True, [4])
sabado = intervening_weekdays(dataInicioDate, dataFimDate, True, [5])
domingo = intervening_weekdays(dataInicioDate, dataFimDate, True, [6])
print(f"segunda: {segunda}, terca: {terca}, quarta: {quarta}, quinta: {quinta}, sexta: {sexta}, sabado: {sabado}, domingo: {domingo}")