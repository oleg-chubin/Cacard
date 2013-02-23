from unittest import TestCase
import datetime
from Cacard.calling_card.services.calendar.utils import check_availability
from Cacard.calling_card.models import DateRule


class TestDateAvailable(TestCase):
    def setUp(self):
        self.s = DateRule(start_date = datetime.datetime(2013, 1, 1),
                     end_date = datetime.datetime (2013, 12, 12),
                     period = 1, is_available = True, priority = 1,
                     duration_discreteness=1)

    def test_isavailable(self):
        start_date = datetime.datetime(2013, 02, 22)
        end_date = datetime.datetime(2013, 02, 23)
        is_avail = check_availability(self.s, start_date, end_date)
        self.assertTrue(is_avail)

    def test_isavailable_end_before_start(self):
        start_date = datetime.datetime(2013, 02, 23)
        end_date = datetime.datetime(2013, 02, 22)
        is_avail = check_availability(self.s, start_date, end_date)
        self.assertFalse(is_avail)

    def test_isavailable_end_after_enddate(self):
        start_date = datetime.datetime(2013, 02, 23)
        end_date = datetime.datetime(2014, 02, 22)
        is_avail = check_availability(self.s, start_date, end_date)
        self.assertFalse(is_avail)
