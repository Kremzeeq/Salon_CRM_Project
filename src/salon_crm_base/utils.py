import datetime


class AppointmentUtil:
    def __init__(self, services, start_time):
        self.services = services
        self.end_time = self.get_end_time(start_time)

    def __get_total_estimated_minutes(self):
        total_minutes = 0
        for service in self.services:
            total_minutes += service.estimated_minutes
        return total_minutes

    def __add_time_delta_to_time(self, time, timedelta):
        start = datetime.datetime(
            2000, 1, 1,
            hour=time.hour, minute=time.minute, second=time.second)
        end = start + timedelta
        return end.time()

    def get_end_time(self, start_time):
        total_minutes = self.__get_total_estimated_minutes()
        x = self.__add_time_delta_to_time(start_time, datetime.timedelta(minutes=total_minutes))
        return x

    def get_quote(self):
        total_quote = 0
        for x in self.services:
            total_quote += x.price
        return total_quote
