from django.db import models
from choose import models as choose_models
# Create your models here.


class HomeWork(models.Model):
    commit_order_choices = (
        ("1", "1"),
        ("2", "2"),
        ("3",  "3"),
        ("4", "4"),
        ("5", "5"),
        ("6", "6"),
        ("7", "7"),
        ("8", "8"),
        ("9", "9"),
        ("10", "10"),
    )
    score_choice = (
        ("A+", "A+"),
        ("A", "A"),
        ("A-",  "A-"),
        ("B+", "B+"),
        ("B", "B"),
        ("B-", "B-"),
        ("C+", "C+"),
        ("C", "C"),
        ("C-", "C-"),
    )

    user = models.ForeignKey(choose_models.User, related_name="user", verbose_name="学员")
    rock = models.ForeignKey(choose_models.Rocks, verbose_name="模块")
    order = models.CharField(max_length=32, choices=commit_order_choices, verbose_name="第几次作业")
    check_path = models.CharField(max_length=512, blank=True, null=True, verbose_name="检查后的文件")
    teacher = models.ForeignKey(choose_models.User, related_name="teacher", blank=True, null=True, verbose_name="批阅老师")
    score = models.CharField(max_length=32, choices=score_choice, blank=True, null=True, verbose_name="作业成绩")
    upload_time = models.DateTimeField(verbose_name="作业上传时间")
    check_time = models.DateTimeField(blank=True, null=True, verbose_name="作业批阅时间")

    def __str__(self):
        return self.user.c_name+"在["+self.rock.rock_name+"]的第"+self.order+"次作业"