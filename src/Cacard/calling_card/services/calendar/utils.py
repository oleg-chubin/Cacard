def check_availability(common_date, start_date, end_date):
    if end_date < start_date:
        return False
    if common_date.start_date < start_date and common_date.end_date > end_date:
        return True
    return False
