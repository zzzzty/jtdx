from django import forms
from django.contrib.contenttypes.models import ContentType
from django.db.models import ObjectDoesNotExist
from ckeditor.widgets import CKEditorWidget
from .models import Comment
from teachingtask.models import Semester,TeachingTask

class CommentForm(forms.Form):
    #teacher = forms.CharField(widget=forms.HiddenInput)
    #course = forms.CharField(widget=forms.HiddenInput)
    teacher_id = forms.IntegerField(widget=forms.HiddenInput)
    course_id = forms.IntegerField(widget=forms.HiddenInput)
    
    text = forms.CharField(widget=CKEditorWidget(config_name='comment_ckeditor'), \
                         error_messages={'required':'评论内容不能为空'})

    def __init__(self,*agrs,**kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(CommentForm,self).__init__(*agrs,**kwargs)

    def clean(self):
        #判断用户是否登陆
        if self.user.is_authenticated:
            self.cleaned_data['user'] = self.user
        else:
            raise forms.ValidationError('用户尚未登陆')
        #评论对象判断
        teacher_id = self.cleaned_data['teacher_id']
        course_id = self.cleaned_data['course_id']
        user = self.cleaned_data['user']
        semester = Semester.objects.filter(is_execute=True)[0]
        try:
            #不能用get方法,没有检测班级信息
            task = TeachingTask.objects.filter(semester=semester,teacher_id=teacher_id,course_id=course_id)[0]
            self.cleaned_data['task'] = task
        except ObjectDoesNotExist:
            raise forms.ValidationError('教学任务不存在')
        return self.cleaned_data