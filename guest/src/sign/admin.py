from django.contrib import admin
from sign.models import Event, Guest

# Register your models here.
# admin.site.register(Event)
# admin.site.register(Guest)


class EventAdmin(admin.ModelAdmin):
    list_display = ["name", "limit", "address",
                    "status", "start_time", "create_time", "id"]
    search_fields = ["name", "start_time"]
    list_filter = ["status"]


class GuestAdmin(admin.ModelAdmin):
    list_display = ["realname", "phone",
                    "email", "sign", "create_time", "event"]
    search_fields = ["realname", "phone"]
    list_filter = ["sign"]


admin.site.register(Event, EventAdmin)
admin.site.register(Guest, GuestAdmin)
