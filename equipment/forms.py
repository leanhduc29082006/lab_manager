from django import forms
from .models import BorrowRecord, Equipment
class BorrowForm(forms.ModelForm):
    class Meta:
        model = BorrowRecord
        fields = ['equipment', 'expected_return_date']
        widgets = {
            'expected_return_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'equipment': forms.Select(attrs={'class': 'form-control'})
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['equipment'].queryset = Equipment.objects.filter(status='available')