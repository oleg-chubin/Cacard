def check_availability(common, start_date, end_date):
    if end_date < start_date:
        return False
    avail_date = []
    for avail in common:
        for date in avail.daterule_set.all():
            avail_date.append([date.priority, {'start':date.start_date,
                            'end':date.end_date, 'is_available':date.is_available}])
    avail_date.sort(reverse=True)

    to_check = [start_date, end_date]
    for item in avail_date:
        if item[1]['is_available'] == False:
            for i in range(0, len(to_check), 2):
                if ((item[1]['start'] < to_check[i] < item[1]['end']) or
                    (item[1]['start'] < to_check[i + 1] < item[1]['end'])) and to_check[i] != to_check[i + 1]:
                    return False
        else:
            for i in range(0, len(to_check), 2):
                if item[1]['start'] <= to_check[i] <= to_check[i + 1] <= item[1]['end']:
                    to_check[i] = to_check[i + 1]
                elif item[1]['start'] <= to_check[i] <= item[1]['end'] and item[1]['end'] <= to_check[i + 1]:
                    to_check[i] = item[1]['end']
                elif item[1]['start'] <= to_check[i + 1] <= item[1]['end'] and to_check[i] <= item[1]['start']:
                    to_check[i + 1] = item[1]['start']
                if to_check[i] <= item[1]['start'] <= item[1]['end'] <= to_check[i+1]:
                    to_check[i + 1:i + 1] = [item[1]['start'], item[1]['end']]
    for i in range(0, len(to_check), 2):
        if to_check[i] != to_check[i + 1]:
            return False
    return True
