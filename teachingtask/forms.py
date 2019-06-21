from django import forms
from teacher.models import Teacher
from teachingtask.models import TeachingTask

class TaskForm(forms.Form):

    task = forms.CharField(widget=forms.HiddenInput(),label="")
    course = forms.CharField(label="",widget=forms.TextInput(attrs={"readonly":True}))
    semester = forms.CharField(label="",widget=forms.TextInput(attrs={"readonly":True}))
    classes = forms.CharField(label="",widget=forms.TextInput(attrs={"readonly":True}))
    before_teacher = forms.CharField(label="",widget=forms.TextInput(attrs={"readonly":True}))
    
    teacher = forms.ModelChoiceField(queryset=None, \
        widget=forms.Select(attrs={'class':'form-control',}))

    def __init__(self,development = None ,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['teacher'].queryset = Teacher.objects.filter(belong_to = development )











