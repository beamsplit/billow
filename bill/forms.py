from django import forms

from bill.models import Bill, Deputy, Senator, Movement

class MyTDForm(forms.ModelForm):
    class Meta:
        model = Deputy
        fields = ('name', 'constituency')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['constituency'].queryset = Deputy.objects.none()

class MovementForm(forms.ModelForm):
    
    class Meta:
        model = Movement
        fields = ('title', 'text', 'url',)

