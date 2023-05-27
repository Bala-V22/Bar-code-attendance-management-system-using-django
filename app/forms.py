from django import forms
from .models import studends,Detected,staff

class studentForm(forms.ModelForm):

    class Meta:
        model = studends
        fields = ('id', 'name', 'email',)

class StaffForm(forms.ModelForm):

    class Meta:
        model = staff
        fields = ('id', 'name', 'email',)        


class ManualForm(forms.ModelForm):

    class Meta:
        model = Detected
        fields = ('emp_id', 'time_stamp',)