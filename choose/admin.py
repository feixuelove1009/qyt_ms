from django.contrib import admin
from choose import models
# Register your models here.

class TestBedsAdmin(admin.ModelAdmin):
    list_display = ("bed_name", "rock")


class RowsAdmin(admin.ModelAdmin):
    # list_display = ("time_zone", "test_bed")
    pass


admin.site.register(models.Rocks)
admin.site.register(models.Rows, RowsAdmin)
admin.site.register(models.User)
admin.site.register(models.Nodes)
admin.site.register(models.Weekdays)
admin.site.register(models.TestBeds, TestBedsAdmin)