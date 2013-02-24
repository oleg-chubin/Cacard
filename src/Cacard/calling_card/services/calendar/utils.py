def check_availability(common, start_date, end_date):
    # TODO: rework with time.mktime(t)
    if end_date < start_date:
        return False
    # at first make testing available for month
    month = [0 for x in range(33)]
    year = []
    for x in range(14):
        year.append(month)
#    if end_date.day - start_date < common.daterule_set.all()[0].start_date.toordinal():
#        return False

    for avail in common:
        for date in avail.daterule_set.all():
            if date.duration_discreteness == 1:
                if date.start_date.month == date.end_date.month:
                    for day_av in range(date.start_date.day, date.end_date.day + 1):
                        year[date.start_date.month][day_av] = 1
                elif date.end_date.month - date.start_date.month == 1:
                    for day_av in range(date.start_date.day, 32):
                        year[date.start_date.month][day_av] = 1
                    for day_av in range(1, date.end_date.day + 1):
                        year[date.end_date.month][day_av] = 1
                else:
                    for day_av in range(date.start_date.day, 32):
                        year[date.start_date.month][day_av] = 1
                    for month_av in range(date.start_date.month + 1, date.end_date.month):
                        for day_av in range(1, 32):
                            year[month_av][day_av] = 1
                    for day_av in range(1, date.end_date.day + 1):
                        year[date.end_date.month][day_av] = 1
    if start_date.month == end_date.month:
        for x in range(start_date.day, end_date.day + 1):
            if year[start_date.month][x] == 0:
                return False
    elif end_date.month - start_date.month == 1:
        for x in range(start_date.day, 32):
            if year[start_date.month][x] == 0:
                return False
        for x in range(1, end_date.day):
            if year[end_date.month][x] == 0:
                return False
    else:
        for x in range(start_date.day, 32):
            if year[start_date.month][x] == 0:
                return False
        for month in range(start_date.month + 1, end_date.month):
            for day in range(1, 32):
                if year[month][day] == 0:
                    return False
        for x in range(1, end_date.day + 1):
            if year[end_date.month][x] == 0:
                return False
    return True
