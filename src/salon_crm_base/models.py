from django.db import models
from django.contrib.auth.models import User
import datetime
from collections import defaultdict
from .utils import AppointmentUtil
import re
from django.core.exceptions import ValidationError


# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Customer(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    title = models.CharField(blank=True, null=True, max_length=35)
    first_name = models.CharField(max_length=35)
    last_name = models.CharField(max_length=35)
    phone_no = models.CharField(max_length=14, null=True, blank=True)
    email = models.EmailField(null=False, unique=True)
    active = models.BooleanField(default=True, blank=True)
    date_activated = models.DateField(auto_now_add=True, null=True)
    date_deactivated = models.DateField(null=True, blank=True)

    address_line_1 = models.CharField(max_length=35, null=True, blank=True)
    address_line_2 = models.CharField(max_length=35, null=True, blank=True)
    address_line_3 = models.CharField(max_length=35, null=True, blank=True)
    town = models.CharField(max_length=35, null=True, blank=True)
    county = models.CharField(max_length=35, null=True, blank=True)
    postcode = models.CharField(max_length=8, null=True, blank=True)

    phone_is_contactable = models.BooleanField(default=False)
    SMS_is_contactable = models.BooleanField(default=False)
    email_is_contactable = models.BooleanField(default=False)

    def __str__(self):
        return " ".join([self.first_name, self.last_name])

    class Meta:
        unique_together = (('first_name', 'last_name', 'email'))

    def save(self, *args, **kwargs):
        self.update_customer_active_status()
        super(Customer, self).save(*args, **kwargs)  # this is the real save method

    def clean(self):
        self.validate_postcode()
        self.validate_phone_no()
        self.email = self.email.lower()

    def update_customer_active_status(self):
        if self.active == False and self.date_deactivated is None:
            self.date_activated = None
            self.date_deactivated = datetime.date.today()
        elif self.active == True and len(str(self.date_deactivated)) >= 0:
            self.date_activated = datetime.date.today()
            self.date_deactivated = None
        else:
            pass

    def validate_postcode(self):
        if self.postcode != None:
            self.postcode = self.postcode.upper()
            uk_postcode_rule_1 = re.compile("[A-Z]{1,2}\d{1,2} \d[A-Z]{1,2}")
            if uk_postcode_rule_1.match(self.postcode) != None:
                return True
            raise ValidationError('Please ensure valid postcode is provided, with space included')

    def validate_phone_no(self):
        # validates uk based phone numbers
        if self.phone_no != None:
            self.phone_no = self.phone_no.lstrip("+")
            self.phone_no = self.phone_no.replace(" ", "")
            self.phone_no = int(self.phone_no)
            self.phone_no = str(self.phone_no)
            if self.phone_no[0:2] == "44":
                self.phone_no = self.phone_no[2:]
            if len(self.phone_no) == 10 and self.phone_no[0] != "0":
                self.phone_no = "0" + self.phone_no[:4] + " " + self.phone_no[4:]
                return True
            elif len(self.phone_no) == 11 and self.phone_no[0] == "0":
                self.phone_no = self.phone_no[:5] + " " + self.phone_no[5:]
                return True
            raise ValidationError('Please ensure valid UK phone number is provided')


class Service(models.Model):
    service = models.CharField(max_length=35, null=True, blank=True)
    price = models.IntegerField(blank=True, null=True)
    estimated_minutes = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return self.service


class Appointment(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False)
    date = models.DateField(null=True)
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    quote = models.FloatField(blank=True, null=True, default=0)
    date_paid = models.DateField(blank=True, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    services = models.ManyToManyField(Service, blank=True)

    class Meta:
        ordering = ['-date', 'start_time']

    def __str__(self):
        return "Appointment " + str(self.date) + ", @" + str(self.start_time)[:-2]

    def clean(self):
        self.validate_appointment_time()

    def validate_appointment_time(self):
        # As self.services cannot be consulted until model has been saved, check whether the model has been saved.
        # This is a temp fix because not evaluating services for the current change, only the previous change.
        if self.id is None:
            return False
        if self.date != None and self.start_time != None:
            appointment_util = AppointmentUtil(self.services.all(), self.start_time)
            self.end_time = appointment_util.end_time
            check_no_appointment_clashes(self.id, self.date, self.start_time, self.end_time)
            return True
        return False

    def save(self, *args, **kwargs):
        """
        First super save necessary without force insert so appointment obj
        is created first, before many to many service obj is associated.
        A quote is calculated based on services selected.
        Then this is saved under the second super save.
        Have defined the service many to many field as an
        alternative to setting up a separate model with foreign keys to
        the service and appointment objects
        This allows the functionality in the admin interface to select multiple
        services when creating or updating an appointment in the appointment detail view.
        The services field is also easy to set up in the admin.py Appointment Admin class
        """
        super(Appointment, self).save(*args, **kwargs)
        kwargs['force_insert'] = False
        appointment_util = AppointmentUtil(self.services.all(), self.start_time)
        self.end_time = appointment_util.end_time
        if self.start_time != self.end_time:
            self.quote = appointment_util.get_quote()
        super(Appointment, self).save(*args, **kwargs)


def check_no_appointment_clashes(id, date, start_time, end_time):
    overlapping_appointments = Appointment.objects.filter(date=date,
                                                          start_time__lt=end_time,
                                                          end_time__gt=start_time).exclude(id=id)
    if len(overlapping_appointments) > 0:
        raise ValidationError(
            "Please select another appointment time. Clashes with {}".format(overlapping_appointments[0]))
    return True


# noinspection SpellCheckingInspection
class AppointmentReportMaker:
    def __init__(self):
        self.dates = self.get_appointment_dates()

    def get_appointment_dates(self):
        dates = Appointment.objects.dates('date', 'day')
        return dates

    def get_appointments_dict_for_date(self, date):
        return Appointment.objects.values('date', 'quote', 'date_paid').filter(date=date)

    def get_num_of_appointments_for_date(self, date):
        return Appointment.objects.filter(date=date).count()

    def get_appointment_summary_report(self):
        context_dict = defaultdict(list)
        for date in self.dates:
            daily_appointment_summary = self.get_income_summary_for_date(date)
            daily_appointment_summary['date'] = daily_appointment_summary.get('date', date)
            daily_appointment_summary['count'] = daily_appointment_summary. \
                get('count', self.get_num_of_appointments_for_date(date))
            daily_appointment_summary['time_slots_available'] = daily_appointment_summary.get('time_slots_available',
                                                                                              self.get_time_slots_available_for_date(
                                                                                                  date))
            context_dict['appointment_summary'].append(daily_appointment_summary)
        return {'success': True, 'context_dict': dict(context_dict)}

    def get_income_summary_for_date(self, date):
        daily_appointments_dict = {}
        for appointment_dict in self.get_appointments_dict_for_date(date):
            daily_appointments_dict['forecasted_income'] = daily_appointments_dict.get('forecasted_income', 0) + \
                                                           appointment_dict['quote']
            daily_appointments_dict['paid_income'] = daily_appointments_dict.get('paid_income',
                                                                                 0) + self.get_paid_income(
                appointment_dict)
        return daily_appointments_dict

    def get_paid_income(self, appointment_dict):
        if appointment_dict['date_paid'] is not None:
            return appointment_dict['quote']
        else:
            return 0.0

    def get_time_slots_available_for_date(self, date):
        time_slots = TimeSlots(date)
        return time_slots.get_time_slots_available_for_date()


class TimeSlots:
    def __init__(self, date):
        self.date = date
        self.day_start_time = datetime.time(hour=9)
        self.day_end_time = datetime.time(hour=17)

    def get_time_slots_for_date(self):
        return Appointment.objects.values_list('start_time', 'end_time').filter(date=self.date).order_by('start_time')

    def consolidate_available_time_slots_for_date(self, time_slots):
        free_time_slots = ''
        cur_available_slot_start_time = self.day_start_time
        for time_slot in time_slots:
            time_slot = list(time_slot)
            start_time = min(time_slot)
            end_time = max(time_slot)
            if start_time <= cur_available_slot_start_time:
                # Continue looking for a free time slot after this appointment ends.
                cur_available_slot_start_time = end_time
                continue
            # If the appointment starts later than the current time look for a free slot.
            # If free time before the next appointment add this to the free time slots parameter
            free_time_slots += cur_available_slot_start_time.strftime("%H:%M") + "-" + start_time.strftime(
                "%H:%M") + " | "
            cur_available_slot_start_time = end_time
        # Check cur_available_slot_start_time against self.day_end_time
        if cur_available_slot_start_time <= self.day_end_time:
            free_time_slots += cur_available_slot_start_time.strftime("%H:%M") + "-" + self.day_end_time.strftime(
                "%H:%M")
        return free_time_slots

    def get_time_slots_available_for_date(self):
        time_slots = self.get_time_slots_for_date()
        return self.consolidate_available_time_slots_for_date(time_slots)
