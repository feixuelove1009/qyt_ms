from django.db import models

# Create your models here.


class User(models.Model):
    # 英文名
    e_name = models.CharField(max_length=128, verbose_name="英文名")
    # 中文名
    c_name = models.CharField(max_length=128, verbose_name="中文名")

    def __str__(self):
        return self.c_name


class Nodes(models.Model):

    owner = models.ForeignKey("User", blank=True, null=True, verbose_name="拥有者")
    weekday = models.ForeignKey("Weekdays", verbose_name="星期")
    row = models.ForeignKey("Rows", verbose_name="时间段")

    def __str__(self):
        return self.row.test_bed.rock.rock_name + ":  " + \
               self.row.test_bed.bed_name + ":   " + \
               self.weekday.day_name + ":   " + self.row.time_zone


class Rows(models.Model):
    time_zone = models.CharField(verbose_name="时间段", max_length=32)
    test_bed = models.ForeignKey("TestBeds", verbose_name="试验台")

    def __str__(self):
        return self.test_bed.rock.rock_name + ":  " + self.test_bed.bed_name + ":  " + self.time_zone


class Weekdays(models.Model):
    day_name = models.CharField(max_length=32, verbose_name="星期")

    def __str__(self):
        return self.day_name


class TestBeds(models.Model):
    bed_name = models.CharField(max_length=32, verbose_name="试验台")
    rock = models.ForeignKey("Rocks", verbose_name="种类")

    def __str__(self):
        return self.rock.rock_name + ":" + self.bed_name


class Rocks(models.Model):

    rock_name = models.CharField(max_length=64, verbose_name="种类")

    def __str__(self):
        return self.rock_name
