from django.shortcuts import render, redirect, HttpResponse
from homework import models
from choose import models as choose_models
import os
from qyt_ms import settings
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
            all_users = list({(homework.user.e_name, homework.user.c_name,) for homework in models.HomeWork.objects.all()})
            all_rocks = choose_models.Rocks.objects.all()

            if not request.GET.get("username", None):
                users = list({(homework.user.e_name, homework.user.c_name,) for homework in models.HomeWork.objects.all()})
            else:
                users = choose_models.User.objects.get(e_name=request.GET.get("username", None))

            if not request.GET.get("rock", None):
                rocks = all_rocks
            else:
                rocks = choose_models.Rocks.objects.filter(rock_name=request.GET.get("rock", None))

            order = request.GET.get("order", None)


            homeworks = models.HomeWork.objects.filter(user=users, rock=rocks, order=order)
            return render(request, "teacher_homework.html", {"homeworks": homeworks, "all_rocks": all_rocks, "all_users":all_users})



def upload_file(request):
    rocks = choose_models.Rocks.objects.all()
    if not request.session.get("username", None):
        return redirect("/")

    if request.method == "POST":  # 请求方法为POST时，进行处理
        ret = {"status": False, "message": ""}
        rock_name = request.POST.get("rock", None)
        order = request.POST.get("order", None)
        my_file = request.FILES.get("myfile", None)  # 获取上传的文件，如果没有文件，则默认为None
        print(rock_name, order, my_file)

        if not rock_name:
            ret["message"] = "请选择作业所属的模块!"
            return render(request, "upload.html", {"ret": ret,
                                                   "rocks": rocks})
        if not order:
            ret["message"] = "请选择第几次作业!"
            return render(request, "upload.html", {"ret": ret,
                                                   "rocks": rocks})

        if not my_file:
            ret["message"] = "请选择要上传的文件!"
            return render(request, "upload.html", {"ret": ret,
                                                   "rocks": rocks})

        suffix = my_file.name.split(".")[-1]
        if suffix not in ("doc", "docx"):
            ret["message"] = "只支持doc或docx文本文件!"
            return render(request, "upload.html", {"ret": ret,
                                                   "rocks": rocks})

        # 准备保存文件
        file_name = rock_name + "-day" + order + "-" + request.session['username'] + "." + suffix
        print(file_name)
        destination_folder = os.path.join(settings.BASE_DIR, "upload", rock_name)
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)
        destination_file = os.path.join(destination_folder, file_name)

        if os.path.exists(destination_file):
            ret["message"] = "作业已经上传过!请不要重复上传!"
            return render(request, "upload.html", {"ret": ret,
                                                   "rocks": rocks})
        if models.HomeWork.objects.filter(user__e_name=request.session["username"],
                                          rock__rock_name=rock_name, order=order):
            ret["message"] = "作业已经上传过!请不要重复上传!"
            return render(request, "upload.html", {"ret": ret,
                                                   "rocks": rocks})

        try:
            with open(destination_file, 'wb') as f:  # 打开特定的文件进行二进制的写操作
                for chunk in my_file.chunks():  # 分块写入文件
                    f.write(chunk)
        except IOError as e:
            print(e)
            ret["message"] = "上传过程出现错误，请重新上传！"
            return render(request, "upload.html", {"ret": ret,
                                                   "rocks": rocks})
        else:
            user = choose_models.User.objects.get(e_name=request.session["username"])
            rock = choose_models.Rocks.objects.get(rock_name=rock_name)
            models.HomeWork.objects.create(user=user, rock=rock, order=order)

        ret["message"] = "上传完毕!"
        return render(request, "upload.html", {"ret": ret,
                                               "rocks": rocks})

    return render(request, "upload.html", {"rocks": rocks})