def check_availability(common, start_date, end_date):
    if end_date < start_date:
        return False
    data_set = common.daterule_set.values('priority', 'start_date',
                                          'end_date', 'is_available')
    expected = [{'start_date':start_date, 'end_date':end_date}]

    for data in sorted(data_set, key=lambda x:x['priority'], reverse=True):
        for i, portion in enumerate(expected):
            if (portion['start_date'] < data['end_date']
                and portion['end_date'] > data['start_date']):
                if not data['is_available']:
                    return False
                expected[i:i + 1] = [{'start_date':portion['start_date'],
                                      'end_date':data['start_date']},
                                     {'start_date':data['end_date'],
                                      'end_date':portion['end_date']}]
            #portion         S___________E
            #data              S--------E
        expected = [i for i in expected if i['start_date'] < i['end_date']]
        if not expected:
            return True
    return False
