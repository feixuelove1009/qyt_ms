from django.shortcuts import render, redirect, HttpResponse
from django.http import StreamingHttpResponse
from homework import models
from choose import models as choose_models
import os
from qyt_ms import settings
import datetime
import re
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
            homeworks = models.HomeWork.objects.all()
            return render(request, "teacher_homework.html", {"homeworks": homeworks})


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
            ret["message"] = "只支持doc或docx文件!"
            return render(request, "upload.html", {"ret": ret,
                                                   "rocks": rocks})

        # 准备保存文件
        file_name = rock_name + "-day" + order + "-" + request.session['username'] + ".doc"
        print(file_name)
        destination_folder = os.path.join(settings.BASE_DIR, "uploads", rock_name)
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)
        destination_file = os.path.join(destination_folder, file_name)

        # if os.path.exists(destination_file):
        #     ret["message"] = "作业已经上传过!请不要重复上传!"
        #     return render(request, "upload.html", {"ret": ret,
        #                                            "rocks": rocks})
        # h = models.HomeWork.objects.filter(user__e_name=request.session["username"],
        #                                 rock__rock_name=rock_name, order=order)
        # if h and h.check_path:
        #     ret["message"] = "作业已经批阅，不能再修改了!"
        #     return render(request, "upload.html", {"ret": ret,
        #                                            "rocks": rocks})

        try:
            with open(destination_file, 'wb') as f:  # 打开特定的文件进行二进制的写操作
                for chunk in my_file.chunks():  # 分块写入文件
                    f.write(chunk)
        except (IOError, OSError) as e:
            print(e)
            ret["message"] = "上传过程出现错误，请重新上传！"
            return render(request, "upload.html", {"ret": ret,
                                                   "rocks": rocks})
        else:
            if not models.HomeWork.objects.filter(user__e_name=request.session["username"],
                                                  rock__rock_name=rock_name, order=order):
                user = choose_models.User.objects.get(e_name=request.session["username"])
                rock = choose_models.Rocks.objects.get(rock_name=rock_name)
                models.HomeWork.objects.create(user=user, rock=rock, order=order, upload_time=datetime.datetime.now())
            else:
                current = models.HomeWork.objects.get(user__e_name=request.session["username"],
                                                      rock__rock_name=rock_name, order=order)
                current.upload_time = datetime.datetime.now()
                current.save()
        ret["message"] = "上传完毕!"
        return render(request, "upload.html", {"ret": ret,
                                               "rocks": rocks})

    return render(request, "upload.html", {"rocks": rocks})


def download_file(request):
    def file_iterator(file_name, chunk_size=512):
        with open(file_name, "rb") as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

    file = request.GET.get("file_name", None)
    if not file:
        return redirect("/homework/")
    rock_name = file.split("-")[0]
    file_path = os.path.join(settings.BASE_DIR, "uploads", rock_name, file)
    try:
        response = StreamingHttpResponse(file_iterator(file_path))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file)
    except (IOError, OSError) as e:
        print(e)
        return HttpResponse("下载失败！")
    return response


def teacher_upload_file(request):
    if not request.session.get("username", None):
        return redirect("/")

    ret = {"status": False, "message": ""}
    homeworks = models.HomeWork.objects.all()

    if request.method == "POST":

        file_name = request.FILES.get("myfile", None)
        oraginfile_name = request.POST.get("oraginfile", None)
        print(file_name)
        print("oraginfile_name >>>", oraginfile_name)

        if not file_name:
            ret["message"] = "上传失败！请选择文件！"
            return render(request, "teacher_homework.html", {"ret": ret, "homeworks": homeworks})

        if not file_name.name.startswith(oraginfile_name):
            ret["message"] = "文件不匹配！请按对应作业上传批阅后的文件！"
            return render(request, "teacher_homework.html", {"ret": ret, "homeworks": homeworks})

        result = re.findall(r"(.*?)-day(\d+?)-(.*?)-([ABCabc][\+\-]?)\.doc", file_name.name)
        print(result)

        if not result or len(result[0]) != 4 or not result[0][3]:
            ret["message"] = "文件格式不对！请按类似【CCNAsec-day1-username-A+】的格式命名文件！"
            return render(request, "teacher_homework.html", {"ret": ret, "homeworks": homeworks})

        homework_obj = models.HomeWork.objects.get(user__e_name=result[0][2],
                                                   rock__rock_name=result[0][0], order=result[0][1])

        homework_obj.teacher = choose_models.User.objects.get(e_name=request.session["username"])
        homework_obj.check_path = file_name.name
        homework_obj.score = result[0][3].upper()
        homework_obj.check_time = datetime.datetime.now()
        homework_obj.save()

        ret["message"] = "上传成功！"
        return render(request, "teacher_homework.html", {"ret": ret, "homeworks": homeworks})

    return redirect("/homework/")
