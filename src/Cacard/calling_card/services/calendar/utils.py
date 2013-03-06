from itertools import chain
from Cacard.calling_card.models import DateRule

def check_availability(product):
    data_set = DateRule.objects.filter(common_date__availabledate__product=product)
    desire_set = DateRule.objects.filter(common_date__desireddate__order_product__product=product)
    reserve_set = DateRule.objects.filter(common_date__reserveddate__order_product__product=product)
#    import ipdb; ipdb.set_trace()
    expected = [{'start_date':desire_set[0].start_date,
                 'end_date':desire_set[0].end_date}]
    if desire_set[0].end_date < desire_set[0].start_date:
        return False
    for data in chain(reserve_set,
                      sorted(data_set, key=lambda x:x.priority, reverse=True)):
        for i, portion in enumerate(expected):
            if (portion['start_date'] < data.end_date
                and portion['end_date'] > data.start_date):
                if not data.is_available:
                    return False
                expected[i:i + 1] = [{'start_date':portion['start_date'],
                                      'end_date':data.start_date},
                                     {'start_date':data.end_date,
                                      'end_date':portion['end_date']}]
            #portion         S___________E
            #data              S--------E
        expected = [i for i in expected if i['start_date'] < i['end_date']]
        if not expected:
            return True
    return False
