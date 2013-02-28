from unittest import TestCase
import datetime
from Cacard.calling_card.services.calendar.utils import check_availability
from Cacard.calling_card.models import AvailableDate, DateRule
from django.utils import timezone


class TestDateAvailable(TestCase):
    def setUp(self):
        if len(self.initial_date) > 0:
            for data in self.initial_date:
                self.availdate = AvailableDate()
                self.availdate.save()
                self.dr = DateRule(start_date=data['start'].replace(tzinfo=timezone.utc),
                     end_date=data['end'].replace(tzinfo=timezone.utc),
                     period=1, is_available=data['is_available'], priority=data['priority'],
                     duration_discreteness=1, common_date=self.availdate)
                self.dr.save()

    def is_avail(self, start_date, end_date, test_result):
        self.assertEqual(check_availability(AvailableDate.objects.all(),
                        start_date.replace(tzinfo=timezone.utc), 
                        end_date.replace(tzinfo=timezone.utc)), test_result)

    def tearDown(self):
        AvailableDate.objects.all().delete()


class TestIsAvailable(TestDateAvailable):
    def setUp(self):
        self.initial_date = [{'start':datetime.datetime(2013, 1, 5, 8, 0, 0),
                              'end':datetime.datetime(2013, 5, 25, 20, 0, 0),
                              'is_available':True, 'priority':1},
                            ]
        super(TestIsAvailable, self).setUp()

    def test_in_one_month(self):
        start_date = datetime.datetime(2013, 3, 15)
        end_date = datetime.datetime(2013, 3, 18)
        self.is_avail(start_date, end_date, True)

    def test_in_next_month(self):
        start_date = datetime.datetime(2013, 3, 15)
        end_date = datetime.datetime(2013, 4, 18)
        self.is_avail(start_date, end_date, True)

    def test_in_some_month(self):
        start_date = datetime.datetime(2013, 2, 15)
        end_date = datetime.datetime(2013, 4, 18)
        self.is_avail(start_date, end_date, True)

    def test_in_one_day(self):
        start_date = datetime.datetime(2013, 3, 15, 9, 0, 0)
        end_date = datetime.datetime(2013, 3, 15, 12, 0, 0)
        self.is_avail(start_date, end_date, True)

    def test_in_next_day(self):
        start_date = datetime.datetime(2013, 3, 15, 17, 0, 0)
        end_date = datetime.datetime(2013, 3, 16, 12, 0, 0)
        self.is_avail(start_date, end_date, True)

    def test_in_some_day(self):
        start_date = datetime.datetime(2013, 2, 15, 9, 0, 0)
        end_date = datetime.datetime(2013, 2, 18, 12, 0, 0)
        self.is_avail(start_date, end_date, True)


class TestIsAvailableEndBeforeStart(TestDateAvailable):
    def setUp(self):
        self.initial_date = [{'start':datetime.datetime(2013, 1, 1, 9, 0, 0),
                              'end':datetime.datetime(2013, 1, 10, 9, 0, 0),
                              'is_available':True, 'priority':1}]
        super(TestIsAvailableEndBeforeStart, self).setUp()

    def test_day(self):
        start_date = datetime.datetime(2013, 1, 10)
        end_date = datetime.datetime(2013, 1, 5)
        self.is_avail(start_date, end_date, False)

    def test_hour(self):
        start_date = datetime.datetime(2013, 1, 5, 10, 0, 0)
        end_date = datetime.datetime(2013, 1, 5, 8, 0, 0)
        self.is_avail(start_date, end_date, False)


class TestIsAvailableEndAfterEndDate(TestDateAvailable):
    def setUp(self):
        self.initial_date = [{'start':datetime.datetime(2013, 1, 1, 8, 0, 0),
                              'end':datetime.datetime(2013, 1, 20, 20, 0, 0),
                              'is_available':True, 'priority':1},
                             {'start':datetime.datetime(2013, 3, 1, 10, 0, 0),
                              'end':datetime.datetime(2013, 3, 1, 12, 0, 0),
                              'is_available':True, 'priority':1}
                             ]
        super(TestIsAvailableEndAfterEndDate, self).setUp()

    def test_year(self):
        start_date = datetime.datetime(2013, 1, 6, 8, 0, 0)
        end_date = datetime.datetime(2014, 1, 22, 8, 0, 0)
        self.is_avail(start_date, end_date, False)

    def test_month(self):
        start_date = datetime.datetime(2013, 1, 6, 8, 0, 0)
        end_date = datetime.datetime(2013, 2, 1, 8, 0, 0)
        self.is_avail(start_date, end_date, False)

    def test_day(self):
        start_date = datetime.datetime(2013, 1, 6, 8, 0, 0)
        end_date = datetime.datetime(2013, 1, 22, 8, 0, 0)
        self.is_avail(start_date, end_date, False)

    def test_hour(self):
        start_date = datetime.datetime(2013, 3, 1, 11, 0, 0)
        end_date = datetime.datetime(2013, 3, 1, 14, 0, 0)
        self.is_avail(start_date, end_date, False)


class TestIsAvailableStartBeforStartDate(TestDateAvailable):
    def setUp(self):
        self.initial_date = [{'start':datetime.datetime(2013, 1, 2, 8, 0, 0),
                              'end':datetime.datetime(2013, 1, 20, 20, 0, 0),
                              'is_available':True, 'priority':1},
                             {'start':datetime.datetime(2013, 3, 2, 10, 0, 0),
                              'end':datetime.datetime(2013, 3, 2, 12, 0, 0),
                              'is_available':True, 'priority':1}
                             ]
        super(TestIsAvailableStartBeforStartDate, self).setUp()

    def test_year(self):
        start_date = datetime.datetime(2012, 1, 1, 8, 0, 0)
        end_date = datetime.datetime(2013, 1, 19, 8, 0, 0)
        self.is_avail(start_date, end_date, False)

    def test_month(self):
        start_date = datetime.datetime(2013, 3, 1, 11, 0, 0)
        end_date = datetime.datetime(2013, 3, 2, 12, 0, 0)
        self.is_avail(start_date, end_date, False)

    def test_day(self):
        start_date = datetime.datetime(2013, 1, 1, 8, 0, 0)
        end_date = datetime.datetime(2013, 1, 19, 8, 0, 0)
        self.is_avail(start_date, end_date, False)

    def test_hour(self):
        start_date = datetime.datetime(2013, 3, 2, 9, 0, 0)
        end_date = datetime.datetime(2013, 3, 2, 11, 0, 0)
        self.is_avail(start_date, end_date, False)


class TestIsAvailableAllDateOut(TestDateAvailable):
    def setUp(self):
        self.initial_date = [{'start':datetime.datetime(2013, 1, 2, 8, 0, 0),
                              'end':datetime.datetime(2013, 1, 20, 20, 0, 0),
                              'is_available':True, 'priority':1},
                             {'start':datetime.datetime(2013, 3, 1, 10, 0, 0),
                              'end':datetime.datetime(2013, 3, 1, 12, 0, 0),
                              'is_available':True, 'priority':1}
                             ]
        super(TestIsAvailableAllDateOut, self).setUp()

    def test_day(self):
        start_date = datetime.datetime(2013, 1, 1, 8, 0, 0)
        end_date = datetime.datetime(2013, 1, 22, 8, 0, 0)
        self.is_avail(start_date, end_date, False)

    def test_day_hour(self):
        start_date = datetime.datetime(2013, 3, 1, 9, 0, 0)
        end_date = datetime.datetime(2013, 3, 1, 14, 0, 0)
        self.is_avail(start_date, end_date, False)


class TestIsAvailableWithSpace(TestDateAvailable):
    def setUp(self):
        self.initial_date = [{'start':datetime.datetime(2013, 1, 1, 8, 0, 0),
                              'end':datetime.datetime(2013, 1, 7, 20, 0, 0),
                              'is_available':True, 'priority':1},
                             {'start':datetime.datetime(2013, 1, 9, 8, 0, 0),
                              'end':datetime.datetime(2013, 1, 20, 20, 0, 0),
                              'is_available':True, 'priority':1},
                             {'start':datetime.datetime(2013, 1, 2, 8, 0, 0),
                              'end':datetime.datetime(2013, 1, 5, 20, 0, 0),
                              'is_available':False, 'priority':2},
                             {'start':datetime.datetime(2013, 2, 1, 8, 0, 0),
                              'end':datetime.datetime(2013, 2, 1, 12, 0, 0),
                              'is_available':True, 'priority':1},
                             {'start':datetime.datetime(2013, 2, 1, 14, 0, 0),
                              'end':datetime.datetime(2013, 2, 1, 22, 0, 0),
                              'is_available':True, 'priority':1},
                             {'start':datetime.datetime(2013, 2, 1, 19, 0, 0),
                              'end':datetime.datetime(2013, 2, 1, 22, 0, 0),
                              'is_available':False, 'priority':2}
                            ]

        super(TestIsAvailableWithSpace, self).setUp()

    def test_day(self):
        start_date = datetime.datetime(2013, 1, 6, 9, 0, 0)
        end_date = datetime.datetime(2013, 1, 10, 9, 0, 0)
        self.is_avail(start_date, end_date, False)

    def test_hour(self):
        start_date = datetime.datetime(2013, 2, 6, 9, 0, 0)
        end_date = datetime.datetime(2013, 2, 10, 16, 0, 0)
        self.is_avail(start_date, end_date, False)

    def test_day_with_priority(self):
        start_date = datetime.datetime(2013, 1, 3, 9, 0, 0)
        end_date = datetime.datetime(2013, 1, 4, 16, 0, 0)
        self.is_avail(start_date, end_date, False)

    def test_hour_with_priority(self):
        start_date = datetime.datetime(2013, 1, 3, 19, 0, 0)
        end_date = datetime.datetime(2013, 1, 4, 20, 0, 0)
        self.is_avail(start_date, end_date, False)


class TestPriority(TestDateAvailable):
    def setUp(self):
        self.initial_date = [{'start':datetime.datetime(2013, 1, 2, 8, 0, 0),
                              'end':datetime.datetime(2013, 1, 20, 20, 0, 0),
                              'is_available':True, 'priority':1},
                             {'start':datetime.datetime(2013, 1, 2, 8, 0, 0),
                              'end':datetime.datetime(2013, 1, 20, 20, 0, 0),
                              'is_available':False, 'priority':2},
                             {'start':datetime.datetime(2013, 1, 2, 8, 0, 0),
                              'end':datetime.datetime(2013, 1, 20, 20, 0, 0),
                              'is_available':True, 'priority':3},
                             ]
        super(TestPriority, self).setUp()

    def test_day(self):
        start_date = datetime.datetime(2013, 1, 3, 8, 0, 0)
        end_date = datetime.datetime(2013, 1, 15, 8, 0, 0)
        self.is_avail(start_date, end_date, True)


class TestPriorityStartBeforeStart(TestDateAvailable):
    def setUp(self):
        self.initial_date = [{'start':datetime.datetime(2013, 1, 2, 8, 0, 0),
                              'end':datetime.datetime(2013, 1, 20, 20, 0, 0),
                              'is_available':True, 'priority':1},
                             {'start':datetime.datetime(2013, 1, 8, 8, 0, 0),
                              'end':datetime.datetime(2013, 1, 10, 20, 0, 0),
                              'is_available':False, 'priority':2},
                             {'start':datetime.datetime(2013, 2, 2, 8, 0, 0),
                              'end':datetime.datetime(2013, 2, 2, 20, 0, 0),
                              'is_available':True, 'priority':1},
                             {'start':datetime.datetime(2013, 2, 2, 8, 0, 0),
                              'end':datetime.datetime(2013, 2, 2, 12, 0, 0),
                              'is_available':False, 'priority':2}
                             ]
        super(TestPriorityStartBeforeStart, self).setUp()

    def test_day(self):
        start_date = datetime.datetime(2013, 1, 9, 8, 0, 0)
        end_date = datetime.datetime(2013, 1, 15, 8, 0, 0)
        self.is_avail(start_date, end_date, False)

    def test_hour(self):
        start_date = datetime.datetime(2013, 2, 2, 11, 0, 0)
        end_date = datetime.datetime(2013, 2, 2, 13, 0, 0)
        self.is_avail(start_date, end_date, False)


class TestEdge(TestDateAvailable):
    def setUp(self):
        self.initial_date = [{'start':datetime.datetime(2013, 1, 2, 8, 0, 0),
                              'end':datetime.datetime(2013, 1, 20, 20, 0, 0),
                              'is_available':True, 'priority':1},
                             {'start':datetime.datetime(2013, 1, 2, 8, 0, 0),
                              'end':datetime.datetime(2013, 1, 2, 20, 0, 0),
                              'is_available':True, 'priority':1},
                             {'start':datetime.datetime(2013, 2, 2, 8, 0, 0),
                              'end':datetime.datetime(2013, 2, 20, 20, 0, 0),
                              'is_available':True, 'priority':1},
                             {'start':datetime.datetime(2013, 2, 5, 8, 0, 0),
                              'end':datetime.datetime(2013, 2, 16, 20, 0, 0),
                              'is_available':False, 'priority':2},
                             {'start':datetime.datetime(2013, 2, 21, 8, 0, 0),
                              'end':datetime.datetime(2013, 2, 21, 20, 0, 0),
                              'is_available':True, 'priority':1},
                             {'start':datetime.datetime(2013, 2, 21, 10, 0, 0),
                              'end':datetime.datetime(2013, 2, 21, 12, 0, 0),
                              'is_available':False, 'priority':2}
                             ]
        super(TestEdge, self).setUp()

    def test_day(self):
        start_date = datetime.datetime(2013, 1, 2, 8, 0, 0)
        end_date = datetime.datetime(2013, 1, 20, 8, 0, 0)
        self.is_avail(start_date, end_date, True)

    def test_day_priority_start(self):
        start_date = datetime.datetime(2013, 2, 16, 21, 0, 0)
        end_date = datetime.datetime(2013, 2, 20, 8, 0, 0)
        self.is_avail(start_date, end_date, True)

    def test_day_priority_end(self):
        start_date = datetime.datetime(2013, 2, 3, 8, 0, 0)
        end_date = datetime.datetime(2013, 2, 5, 8, 0, 0)
        self.is_avail(start_date, end_date, True)

    def test_hour(self):
        start_date = datetime.datetime(2013, 1, 2, 8, 0, 0)
        end_date = datetime.datetime(2013, 1, 2, 20, 0, 0)
        self.is_avail(start_date, end_date, True)

    def test_hour_priority_start(self):
        start_date = datetime.datetime(2013, 2, 21, 12, 0, 0)
        end_date = datetime.datetime(2013, 2, 21, 20, 0, 0)
        self.is_avail(start_date, end_date, True)

    def test_hour_priority_end(self):
        start_date = datetime.datetime(2013, 2, 21, 8, 0, 0)
        end_date = datetime.datetime(2013, 2, 21, 10, 0, 0)
        self.is_avail(start_date, end_date, True)


class TestIsAvailableWithBlock(TestDateAvailable):
    def setUp(self):
        self.initial_date = [{'start':datetime.datetime(2013, 1, 1, 9, 0, 0),
                              'end':datetime.datetime(2013, 1, 3, 9, 0, 0),
                              'is_available':True, 'priority':1},
                             {'start':datetime.datetime(2013, 1, 5, 9, 0, 0),
                              'end':datetime.datetime(2013, 1, 7, 9, 0, 0),
                              'is_available':True, 'priority':1},
                             {'start':datetime.datetime(2013, 1, 3, 9, 0, 0),
                              'end':datetime.datetime(2013, 1, 5, 9, 0, 0),
                              'is_available':True, 'priority':1}
                             ]
        super(TestIsAvailableWithBlock, self).setUp()

    def test_day(self):
        start_date = datetime.datetime(2013, 1, 2)
        end_date = datetime.datetime(2013, 1, 7)
        self.is_avail(start_date, end_date, True)

