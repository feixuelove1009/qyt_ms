from django.shortcuts import render, redirect, HttpResponse
from homework import models
from choose import models as choose_models
import os
# Create your views here.


def homework(request):
    ret = {"status": False, "message": ""}
    if not request.session.get('username', None):
        ret["message"] = "访问此模块需要先登录！"
        return render(request, "login.html", {"ret": ret})
    else:
        name = request.session['username']
        kind = request.session['user_kind']
        if kind == "student":
            homeworks = models.HomeWork.objects.filter(user__e_name=name).order_by("rock__rock_name")

            return render(request, "homework.html", {"homeworks": homeworks})
        else:
            return HttpResponse("teacher")


def upload_file(request):
    rocks = choose_models.Rocks.objects.all()
    numbers = range(1, 11)
    if not request.session.get("username", None):
        return redirect("/")

    if request.method == "POST":  # 请求方法为POST时，进行处理
        ret = {"status": False, "message": ""}

        my_file = request.FILES.get("myfile", None)  # 获取上传的文件，如果没有文件，则默认为None
        if not my_file:
            ret["message"] = "请选择要上传的文件!"
            return render(request, "upload.html", {"ret": ret,
                                                   "rocks": rocks,
                                                   "numbers": numbers})
        try:
            with open(os.path.join("f:\\upload", my_file.name), 'wb') as destination:  # 打开特定的文件进行二进制的写操作
                for chunk in my_file.chunks():  # 分块写入文件
                    destination.write(chunk)
        except IOError as e:
            print(e)
            ret["message"] = "上传过程出现错误，请重新上传！"
            return render(request, "upload.html", {"ret": ret,
                                                   "rocks": rocks,
                                                   "numbers": numbers})

        ret["message"] = "上传完毕!"
        return render(request, "upload.html", {"ret": ret,
                                               "rocks": rocks,
                                               "numbers": numbers})

    return render(request, "upload.html", {"rocks": rocks,
                                           "numbers": numbers})