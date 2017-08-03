from django.db import models

# Create your models here.


class User(models.Model):
    # 英文名
    e_name = models.CharField(max_length=128)
    # 中文名
    c_name = models.CharField(max_length=128)

    def __str__(self):
        return self.c_name


class Nodes(models.Model):

    owner = models.ForeignKey("User", blank=True, null=True)
    weekday = models.ForeignKey("Weekdays")
    row = models.ForeignKey("Rows")

    def __str__(self):
        return self.row.test_bed.rock.rock_name + ":  " + \
               self.row.test_bed.bed_name + ":   " + \
               self.weekday.day_name + ":   " + self.row.time_zone


class Rows(models.Model):
    time_zone = models.CharField(max_length=32)
    test_bed = models.ForeignKey("TestBeds")

    def __str__(self):
        return self.test_bed.rock.rock_name + ":  " + self.test_bed.bed_name + ":  " + self.time_zone


class Weekdays(models.Model):
    day_name = models.CharField(max_length=32)

    def __str__(self):
        return self.day_name


class TestBeds(models.Model):
    bed_name = models.CharField(max_length=32)
    rock = models.ForeignKey("Rocks")

    def __str__(self):
        return self.bed_name


class Rocks(models.Model):

    rock_name = models.CharField(max_length=64)

    def __str__(self):
        return self.rock_name
