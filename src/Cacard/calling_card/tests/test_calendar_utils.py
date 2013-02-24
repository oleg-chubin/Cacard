from unittest import TestCase
import datetime
from Cacard.calling_card.services.calendar.utils import check_availability
from Cacard.calling_card.models import AvailableDate, DateRule


class TestDateAvailable(TestCase):
    def setUp(self):
        if len(self.initial_date) > 0:
            for base_cleaner in AvailableDate.objects.all():
                base_cleaner.delete()
            for data in self.initial_date:
                self.availdate = AvailableDate()
                self.availdate.save()
                self.dr = DateRule(start_date=data['start'],
                     end_date=data['end'],
                     period=1, is_available=data['is_available'], priority=1,
                     duration_discreteness=1, common_date_id=self.availdate.id)
                self.dr.save()

    def is_avail(self, start_date, end_date, test_result):
        self.assertEqual(check_availability(AvailableDate.objects.all(), start_date, end_date), test_result)


class TestIsAvailable(TestDateAvailable):
    def setUp(self):
        self.initial_date = [{'start':datetime.datetime(year=2013, month=1, day=5),
                              'end':datetime.datetime(year=2013, month=2, day=25),
                              'is_available':True},
                             {'start':datetime.datetime(year=2013, month=2, day=15),
                              'end':datetime.datetime(year=2013, month=5, day=20),
                              'is_available':True}
                            ]
        super(TestIsAvailable, self).setUp()

    def test_inonemonth(self):
        start_date = datetime.datetime(year=2013, month=3, day=15)
        end_date = datetime.datetime(year=2013, month=3, day=18)
        self.is_avail(start_date, end_date, True)

    def test_innextmonth(self):
        start_date = datetime.datetime(year=2013, month=3, day=15)
        end_date = datetime.datetime(year=2013, month=4, day=18)
        self.is_avail(start_date, end_date, True)

    def test_insomemonth(self):
        start_date = datetime.datetime(year=2013, month=2, day=15)
        end_date = datetime.datetime(year=2013, month=4, day=18)
        self.is_avail(start_date, end_date, True)


class TestIsAvailableEndBeforeStart(TestDateAvailable):
    def setUp(self):
        self.initial_date = [{'start':datetime.datetime(year=2013, month=1, day=1),
                              'end':datetime.datetime(year=2013, month=1, day=30),
                              'is_available':True}]
        super(TestIsAvailableEndBeforeStart, self).setUp()

    def test(self):
        start_date = datetime.datetime(year=2013, month=1, day=10)
        end_date = datetime.datetime(year=2013, month=1, day=5)
        self.is_avail(start_date, end_date, False)


class TestIsAvailableEndAfterEndDate(TestDateAvailable):
    def setUp(self):
        self.initial_date = [{'start':datetime.datetime(year=2013, month=1, day=1),
                              'end':datetime.datetime(year=2013, month=1, day=20),
                              'is_available':True}]
        super(TestIsAvailableEndAfterEndDate, self).setUp()

    def test(self):
        start_date = datetime.datetime(year=2013, month=1, day=6)
        end_date = datetime.datetime(year=2013, month=1, day=22)
        self.is_avail(start_date, end_date, False)

class TestIsAvailableWithSpace(TestDateAvailable):
    def setUp(self):
        self.initial_date = [{'start':datetime.datetime(year=2013, month=1, day=1),
                              'end':datetime.datetime(year=2013, month=1, day=7),
                              'is_available':True},
                             {'start':datetime.datetime(year=2013, month=1, day=9),
                              'end':datetime.datetime(year=2013, month=1, day=20),
                              'is_available':True}
                            ]

        super(TestIsAvailableWithSpace, self).setUp()

    def test(self):
        start_date = datetime.datetime(year=2013, month=1, day=6)
        end_date = datetime.datetime(year=2013, month=1, day=10)
        self.is_avail(start_date, end_date, False)
