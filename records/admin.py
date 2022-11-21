from django.contrib import admin

from records.models import Clients, Doctors, Records, Specials


class DoctorsAdmin(admin.ModelAdmin):
    list_display = ('name', 'achiv_short', 'email', 'special')
    search_fields = ('name', 'special')
    list_filter = ('name', 'special')


class SpecialsAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)


class ClientsAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone')
    search_fields = ('name', 'phone')
    list_filter = ('name',)


class RecordsAdmin(admin.ModelAdmin):
    list_display = ('user', 'doctor', 'date', 'time', 'finish')
    search_fields = ('user', 'doctor', 'date', 'time', 'finish')
    list_filter = ('user', 'doctor', 'date', 'finish')
    ordering = ('date', 'time')


admin.site.register(Doctors, DoctorsAdmin)
admin.site.register(Specials, SpecialsAdmin)
admin.site.register(Records, RecordsAdmin)
admin.site.register(Clients, ClientsAdmin)
