def check_availability(common, start_date, end_date):
    import datetime
    if end_date < start_date:
        return False
    
    for date in common.daterule_set.all():
        if date.start_date.toordinal() < start_date.toordinal() and date.end_date.toordinal() > end_date.toordinal():
            return True
    return False
