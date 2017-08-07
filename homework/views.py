from django.shortcuts import render
from choose import models
# Create your views here.


def homework(request):
    rocks = models.Rocks.objects.all()
    rock_name = request.GET.get("rock", "CCNAsec")
    return render(request, "homework.html", {"rock_name":rock_name,
                                             "rocks":rocks})
