from django import forms
from .models import Score
class IScore(forms.Form):
    student_username = forms.CharField(widget=forms.HiddenInput(),label="")
    task = forms.CharField(widget=forms.HiddenInput(),label="")
    student_num = forms.CharField(label="",widget=forms.TextInput(attrs={"readonly":True}))
    student = forms.CharField(label="",widget=forms.TextInput(attrs={"readonly":True}))
    score = forms.IntegerField(label="",widget=forms.TextInput())

    def clean_score(self):
        score = self.cleaned_data['score']
        if score > 100 or score<0:
            raise forms.ValidationError('应该为0~100的整数')
        else:
            return score

class CScore(forms.Form):
    changescore = forms.CharField(widget=forms.HiddenInput(),label="")
    #控制是否允许更改
    task = forms.CharField(label="",widget=forms.TextInput(attrs={"readonly":True,"class":""}))
    student_num = forms.CharField(label="",widget=forms.TextInput(attrs={"readonly":True}))
    student = forms.CharField(label="",widget=forms.TextInput(attrs={"readonly":True,"width":"10"}))
    old_score = forms.CharField(label="",widget=forms.TextInput(attrs={"readonly":True}))
    change_to = forms.IntegerField(label="",widget=forms.TextInput())
    change_reason = forms.CharField(
        widget=forms.Select(choices=(
        ('录入串行','录入串行'),
        ('计算错误','计算错误'),
    ))
    )
    #clean + 字段名称才能执行+ return 相应的字段
    def clean_change_to(self):
        change_to = self.cleaned_data['change_to']
        if change_to > 100 or change_to < 0:
            raise forms.ValidationError('应该为0~100的整数')
        else:
            return change_to


# class IScore(forms.ModelForm):
#     class Meta:
#         model = Score
#         fields = ['score','task','student']