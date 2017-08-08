from django.shortcuts import render,redirect,HttpResponse
from homework import models
from choose import models as choose_models
# Create your views here.


def homework(request):
    if not request.session.get('username', None):
        return redirect("/login/")
    else:
        name = request.session['username']
        kind = request.session['user_kind']
        if kind == "student":
            homeworks = models.HomeWork.objects.filter(user__e_name=name)

            rocks = choose_models.Rocks.objects.all()
            return render(request, "homework.html", {"homeworks":homeworks,
                                                     "rocks":rocks})
        else:
            return HttpResponse("teacher")

