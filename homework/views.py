from django.shortcuts import render,redirect,HttpResponse
from homework import models
from choose import models as choose_models
# Create your views here.


def homework(request):
    if not request.session.get('username', None):
        ret = {"status": False, "message": ""}
        ret["message"] = "访问此模块需要先登录！"
        return render(request, "login.html", {"ret": ret})
    else:
        name = request.session['username']
        kind = request.session['user_kind']
        if kind == "student":
            homeworks = models.HomeWork.objects.filter(user__e_name=name).order_by("rock__rock_name")

            return render(request, "homework.html", {"homeworks":homeworks})
        else:
            return HttpResponse("teacher")

def upload(request):
    if not request.session.get("username", None):
        return redirect("/")

    return render(request, "upload.html")