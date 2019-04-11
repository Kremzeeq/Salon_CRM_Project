from django.test import TestCase
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from . import models
# from faker import Faker
import logging
import datetime

logging.basicConfig(level=logging.DEBUG)


# Create your tests here.


class CustomerTestCase(TestCase):
    """
    TestCase for Customer model
    Use following to run TestCase in command line:
    python manage.py test salon_crm_base.tests.CustomerTestCase
    """

    def setUp(self):
        self.customer_1 = models.Customer.objects.create(first_name='john',
                                                         last_name='doe',
                                                         email='john@test.com')
        self.date_today = datetime.datetime.now().strftime("%d/%m/%y")
        self.test_first_name = "test_first_name"
        self.test_second_name = "test_second_name"

    def test_save_duplicate_customer_with_same_email(self):
        with self.assertRaises(IntegrityError):
            models.Customer.objects.create(first_name='john',
                                           last_name='doe', email='john@test.com')

    def test_date_activated_updates_when_made_active(self):
        self.customer_1.save()
        self.assertEqual(self.customer_1.date_activated.strftime("%d/%m/%y"), self.date_today)

    def test_date_deactivated_updates_when_deactivated(self):
        self.customer_1.active = False
        self.customer_1.save()
        self.assertEqual(self.customer_1.date_deactivated.strftime("%d/%m/%y"), self.date_today)

    def test_activation_dates_not_equal_when_deactivated(self):
        self.customer_1.active = False
        self.customer_1.save()
        self.assertNotEqual(self.customer_1.date_activated, self.customer_1.date_deactivated)

    def test_postcode_valid(self):
        self.customer_1.postcode = "G74 4AU"
        self.assertEqual(self.customer_1.validate_postcode(), True)

    def test_postcode_not_valid(self):
        self.customer_1.postcode = "GU4 777"
        with self.assertRaises(ValidationError):
            self.customer_1.validate_postcode()

    def test_phone_valid_format_1(self):
        self.customer_1.phone_no = "01632 960343"
        self.assertEqual(self.customer_1.validate_phone_no(), True)

    def test_phone_valid_format_2(self):
        self.customer_1.phone_no = "44 1632 960343"
        self.assertEqual(self.customer_1.validate_phone_no(), True)

    def test_phone_valid_format_3(self):
        self.customer_1.phone_no = "447732960343"
        self.assertEqual(self.customer_1.validate_phone_no(), True)

    def test_phone_not_valid_format_1(self):
        self.customer_1.phone_no = "997732960343"
        with self.assertRaises(ValidationError):
            self.customer_1.validate_phone_no()

    def test_phone_not_valid_format_2(self):
        self.customer_1.phone_no = "9977329603433"
        with self.assertRaises(ValidationError):
            self.customer_1.validate_phone_no()


class GenericTestCase(TestCase):
    def setUp(self):
        self.date = datetime.date(2019, 4, 9)
        self.service_1 = models.Service.objects.create(service="hair service1",
                                                       price=40,
                                                       estimated_minutes=40)
        self.service_2 = models.Service.objects.create(service="hair service2",
                                                       price=50,
                                                       estimated_minutes=50)
        self.customer_1 = models.Customer.objects.create(first_name="test_first_name",
                                                         last_name="test_last_name",
                                                         email="test@test.com")
        self.appointment_1 = models.Appointment.objects.create(date=self.date,
                                                               start_time=datetime.time(11, 0),
                                                               customer=self.customer_1)
        self.appointment_1.services.add(self.service_1)
        self.appointment_1.save()


class AppointmentTestCase(GenericTestCase):
    """
    TestCase for Appointment model
    Use following to run TestCase in command line:
    python manage.py test salon_crm_base.tests.AppointmentTestCase
    """

    def test_validate_appointment_time_with_one_service(self):
        self.assertEqual(self.appointment_1.end_time, datetime.time(11, 40))

    def test_validate_appointment_time_with_two_services(self):
        self.appointment_1.services.add(self.service_2)
        self.appointment_1.save()
        self.assertEqual(self.appointment_1.end_time, datetime.time(12, 30))

    def test_validate_quote_updates_upon_saving(self):
        self.appointment_1.save()
        self.assertEqual(self.appointment_1.quote, 40)


class AppointmentReportMakerTestCase(GenericTestCase):
    """
    TestCase for AppointmentReportMaker Class in models.py
    This makes queries to the database
    Use following to run TestCase in command line:
    python manage.py test salon_crm_base.tests.AppointmentReportMakerTestCase
    """

    def setUp(self):
        super(AppointmentReportMakerTestCase, self).setUp()
        self.appointment_1.save()
        self.appointment_2 = models.Appointment.objects.create(date=self.date,
                                                               start_time=datetime.time(11, 40),
                                                               customer=self.customer_1)
        self.appointment_2.services.add(self.service_1)
        self.appointment_2.save()
        self.appointment_report_maker = models.AppointmentReportMaker()

    def test_get_appointment_summary_report_is_success(self):
        summary_report = self.appointment_report_maker.get_appointment_summary_report()
        self.assertEqual(summary_report['success'], True)

    def test_get_appointment_summary_report_time_slots_for_date(self):
        summary_report = self.appointment_report_maker.get_appointment_summary_report()
        logging.info(summary_report)
        time_slots_available = ''
        for day in summary_report['context_dict']['appointment_summary']:
            if day['date'] == self.date:
                time_slots_available = day['time_slots_available']
        self.assertEqual(time_slots_available, '09:00-11:00 | 12:20-17:00')

    def test_income_summary_for_date(self):
        self.appointment_1.date_paid = self.date
        self.appointment_1.save()
        daily_appointment_dict = self.appointment_report_maker.get_income_summary_for_date(self.date)
        self.assertEqual(daily_appointment_dict['forecasted_income'], 80)
        self.assertEqual(daily_appointment_dict['paid_income'], 40)

    def test_get_paid_income(self):
        appointment_dict = {'date': self.date, 'quote': 40, 'date_paid': self.date}
        paid_income = self.appointment_report_maker.get_paid_income(appointment_dict)
        self.assertEqual(paid_income, appointment_dict['quote'])

    def test_get_time_slots_available_for_date(self):
        """
        Tests functionality of TimeSlots class
        get_free_time_slots_for_date method in TimeSlot class calculates
        free time slots, based on appointments found in the DB
        """
        time_slots_available = self.appointment_report_maker.get_time_slots_available_for_date(self.date)
        self.assertEqual(time_slots_available, '09:00-11:00 | 12:20-17:00')
