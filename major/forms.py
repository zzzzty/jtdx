from django import forms
from grade.models import Grade
from .models import Major
class MajorForm(forms.Form):
    choices_list = []
    #choices_list = [(i['name'],i['name']) for i in Grade.objects.values('name')]
    choices_list.insert(0,("","年级"))#select 选择第一个元素是什么
    name = forms.CharField(label='专业名称')
    grade = forms.ChoiceField(choices=choices_list,label='年级')

    def clean(self):
        grade = Grade.objects.filter(name = self.cleaned_data['grade'])[0]
        self.cleaned_data['grade'] = grade
        if Major.objects.filter(name=self.cleaned_data['name'],grade=grade).exists():
            raise forms.ValidationError('专业名称重复')
        return self.cleaned_data

