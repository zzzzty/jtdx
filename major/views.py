from django.shortcuts import render,HttpResponse
from .models import Major
from grade.models import Grade
from .forms import MajorForm
from django.forms import formset_factory
# Create your views here.

def major_insert(request):
    majorformset = formset_factory(MajorForm,extra=2)
    if request.method=='POST':
        majorform = majorformset(request.POST)
        if majorform.is_valid():
            majorandgrade = []
            #查看当前表单是否有重复数据
            for row in majorform:
                strcheck = row.cleaned_data['name']+row.cleaned_data['grade'].name
                if strcheck not in majorandgrade:
                    majorandgrade.append(strcheck)
                else:
                    message = "现在有重复的数据"
                    return render(request,'major/major_insert.html',locals())
            #将表单数据数据存入数据库
            for row in majorform:
                if row.is_valid():
                    newmajor = Major()
                    grade = row.cleaned_data['grade']
                    newmajor.name = row.cleaned_data['name']
                    newmajor.grade = grade
                    newmajor.save()
            message = "success"
            return render(request,'major/major_insert.html',locals())
        else:
            message = "something error"
            return render(request,'major/major_insert.html',locals())
    else:
        majorform = majorformset()
    return render(request,'major/major_insert.html',locals())

