"""
from .models import Schedule
from django import forms

class ScheduleForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        self.current_user = user
        super().__init__(*args, **kwargs)

    def method(self):
        model = Schedule
        model.objects.filter(user=self.current_user)
        fields = ('date', 'user', 'base', 'seat')

    # フォームを綺麗にするための記載
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'