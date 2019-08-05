import django_tables2 as tables 
from .models import DocFile

class DocFileTable(tables.Table):
    name = tables.Column()
    class Meta:
        model = DocFile
        template_name = 'django_tables2/bootstrap.html'