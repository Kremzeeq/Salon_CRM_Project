from django.contrib import admin
from . import models


# Register your models here.

class CustomerAdmin(admin.ModelAdmin):
    list_filter = ('active',)
    search_fields = ('first_name', 'last_name', 'phone_no', 'email', 'postcode')
    list_display = ('id', 'first_name', 'last_name', 'phone_no', 'email', 'postcode')
    readonly_fields = ('date_activated', 'date_deactivated')
    fieldsets = (
        ('Name', {
            'fields': (('title', 'first_name', 'last_name'),)
        }),
        ('Contact Details', {
            'fields': (('phone_no', 'email'),)
        }),
        ('Address', {
            'fields': (('address_line_1', 'address_line_2', 'address_line_3'),
                       ('town', 'county', 'postcode'))
        }),
        ('Contact Preferences', {
            'fields': (('phone_is_contactable', 'SMS_is_contactable', 'email_is_contactable'),)
        }),
        ('Activation Information', {
            'fields': ('active', 'date_activated', 'date_deactivated')
        }))


class AppointmentAdmin(admin.ModelAdmin):
    list_filter = ('date', 'start_time')
    list_display = ('date', 'start_time', 'end_time', 'customer', 'quote')

    fieldsets = (
        ('Appointment Details', {
            'fields': ('customer', ('date', 'start_time', 'end_time'), 'services')
        }),
        ('Payment Information', {
            'fields': (('quote', 'date_paid'),)
        }),
    )

    readonly_fields = ('end_time', 'quote')

    def save_model(self, request, obj, form, change):
        super(AppointmentAdmin, self).save_model(request, obj, form, change)
        obj.services.set(form.cleaned_data['services'])
        obj.save()


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('service', 'price', 'estimated_minutes')


admin.site.register(models.Customer, CustomerAdmin)
admin.site.register(models.Appointment, AppointmentAdmin)
admin.site.register(models.Service, ServiceAdmin)
