from unittest import TestCase
import datetime
from Cacard.calling_card.services.calendar.utils import check_availability
from Cacard.calling_card.models import AvailableDate, DateRule


class TestDateAvailable(TestCase):
    def setUp(self):
        if len(self.initial_date) > 0:
            for data in self.initial_date:
                self.availdate = AvailableDate()
                self.availdate.save()
                self.dr = DateRule(start_date = data['start'],
                     end_date = data['end'],
                     period = 1, is_available = data['is_available'], priority = 1,
                     duration_discreteness=1, common_date_id=self.availdate.id)
                self.dr.save()

    def is_avail(self, start_date, end_date, test_result):
        self.assertEqual(check_availability(self.availdate, start_date, end_date), test_result)


class TestIsAvailable(TestDateAvailable):
    def setUp(self):
        self.initial_date = [{'start':datetime.datetime(2013, 1, 1),
                              'end':datetime.datetime(2013, 12, 12),
                              'is_available':True}]
        super(TestIsAvailable, self).setUp()

    def test(self):
        start_date = datetime.datetime(2013, 02, 22)
        end_date = datetime.datetime(2013, 02, 23)
        self.is_avail(start_date, end_date, True)


class TestIsAvailableEndBeforeStart(TestDateAvailable):
    def setUp(self):
        self.initial_date = [{'start':datetime.datetime(2013, 1, 1),
                              'end':datetime.datetime(2013, 12, 12),
                              'is_available':True}]
        super(TestIsAvailableEndBeforeStart, self).setUp()

    def test(self):
        start_date = datetime.datetime(2013, 02, 23)
        end_date = datetime.datetime(2013, 02, 22)
        self.is_avail(start_date, end_date, False)


class TestIsavailableEndAfterEndDate(TestDateAvailable):
    def setUp(self):
        self.initial_date = [{'start':datetime.datetime(2013, 1, 1),
                              'end':datetime.datetime(2013, 12, 12),
                              'is_available':True}]
        super(TestIsavailableEndAfterEndDate, self).setUp()

    def test(self):
        start_date = datetime.datetime(2013, 02, 23)
        end_date = datetime.datetime(2014, 02, 22)
        self.is_avail(start_date, end_date, False)
