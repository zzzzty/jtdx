from django.shortcuts import render,render_to_response,\
    get_object_or_404,HttpResponse,redirect
from grade.models import Grade
from django.contrib import auth

def home(request):
    context ={}
    context['classes'] = Grade.objects.all()
    return render(request,'home.html',context=context)


def logout(request):
    auth.logout(request)
    return redirect('/')

def search(request):
    tst = request.GET.get('teachersearchtask',None)
    return HttpResponse(tst)