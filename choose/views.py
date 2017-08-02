from django.shortcuts import render, HttpResponse
from choose import models

# Create your views here.

def index(request):
    test_beds = models.TestBeds.objects.filter(rock__rock_name="CCNAsec")
    rows = models.Rows.objects.filter(test_bed__rock__rock_name="CCNAsec")
    weekdays = models.Weekdays.objects.all()
    nodes = models.Nodes.objects.filter(row__test_bed__rock__rock_name="CCNAsec")
    return render(request, "index.html",{"test_beds":test_beds,
                                         "rows":rows,
                                         "weekdays":weekdays,
                                         "nodes":nodes})


def add_nodes(request):
    """
    用来初始化时间段，只允许运行一次！！！！
    :param request:
    :return:
    """
    row_list = models.Rows.objects.all()
    weekdays = models.Weekdays.objects.get(day_name="周日")
    print(weekdays)
    for rows in row_list:
        models.Nodes.objects.create(weekday=weekdays, row=rows)
    return HttpResponse("ok")