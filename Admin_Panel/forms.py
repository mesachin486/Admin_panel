from django import forms
from .models import Admin_Panel
#DataFlair
class Admin_PanelCreate(forms.ModelForm):
    class Meta:
        model = Admin_Panel
        fields = '__all__'