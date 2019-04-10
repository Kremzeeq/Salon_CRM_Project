from django.shortcuts import render
from .models import AppointmentReportMaker
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required
def appointment_summary_report(request):
    appointment_summary_report = AppointmentReportMaker()
    appointment_summary = appointment_summary_report.get_appointment_summary_report()['context_dict']
    print("Here is the dictionary: ", appointment_summary)
    return render(request, 'admin/appointment_summary_report.html', appointment_summary)
