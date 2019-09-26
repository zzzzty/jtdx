import os 
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE','jtdx.settings')
django.setup()

import xlrd
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password,check_password

basename =os.path.dirname(os.path.abspath(__file__)) 
tablename = os.path.join(basename,"name.xlsx")


table = xlrd.open_workbook(tablename)
data = table.sheets()[0]
nrows = data.nrows
ncols = data.ncols


def get_value(data,row_index,col_index):
    the_value = data.cell(row_index,col_index).ctype
    if the_value == 2:
        the_value = str(int(data.cell(row_index,col_index).value))
    else:
        the_value = str(data.cell(row_index,col_index).value)
    return the_value


for i in range(1,nrows):
    #班级
    num = get_value(data,i,2)
    name = get_value(data,i,3)
    classes = get_value(data,i,4)
    grade = get_value(data,i,34)

    print(grade)