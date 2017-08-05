from django.contrib import admin
from choose import models
# Register your models here.


class TestBedsAdmin(admin.ModelAdmin):
    list_display = ("rock","bed_name")

    class meta:
        verbose_name = "试验台"
        verbose_name_plural = "试验台"


class RowsAdmin(admin.ModelAdmin):
    list_display = ("test_bed", "time_zone")
    pass


class NodesAdmin(admin.ModelAdmin):
    list_display = ("weekday", "row", "owner")


admin.site.register(models.Rocks)
admin.site.register(models.Rows, RowsAdmin)
admin.site.register(models.User)
admin.site.register(models.Nodes, NodesAdmin)
admin.site.register(models.Weekdays)
admin.site.register(models.TestBeds, TestBedsAdmin)