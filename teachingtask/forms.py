from django import forms
from teacher.models import Teacher
from teachingtask.models import TeachingTask
from administrative.models import TeacherDevelopment

class TaskForm(forms.Form):
    task = forms.CharField(widget=forms.HiddenInput(),label="")
    course = forms.CharField(label="",widget=forms.TextInput(attrs={"readonly":True, \
        "style":"width:150px"}))
    semester = forms.CharField(label="",widget=forms.TextInput(attrs={"readonly":True, \
        "style":"width:150px"}))
    classes = forms.CharField(label="",widget=forms.TextInput(attrs={"readonly":True, \
        "style":"width:200px"}))
    before_teacher = forms.CharField(label="",widget=forms.TextInput(attrs={"readonly":True, \
        "style":"width:100px"}))
    teacher = forms.ModelChoiceField(queryset=TeacherDevelopment.objects.filter(), \
        widget=forms.Select(attrs={'class':'form-control','onchange':'testajax(this);'}))
    aselect = forms.ModelChoiceField(queryset=Teacher.objects.filter(), \
        widget=forms.Select(attrs={'class':'form-control',}))
    

    def clean_aselect(self):
        aselect = self.cleaned_data['aselect']
        return aselect

    
#a new test use modelform
class Select_Teacher(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['teacher']

class TaskmodelForm(forms.ModelForm):
    teacher = forms.ModelChoiceField(queryset=Teacher.devel.get_queryset(), \
        widget=forms.Select(attrs={'class':'form-control',}))
    class Meta:
        model = TeachingTask
        fields = '__all__'


    '''
    teacher = forms.ModelChoiceField(queryset=None, \
        widget=forms.Select(attrs={'class':'form-control',}))

    def __init__(self,development = None ,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['teacher'].queryset = Teacher.objects.filter(belong_to = development )
    '''







