from django import forms
from .models import BorrowRecord, Equipment, MaintenanceRecord
from django.utils import timezone
class BorrowForm(forms.ModelForm):
    class Meta:
        model = BorrowRecord
        fields = ['equipment', 'expected_return_date']
        widgets = {
            'expected_return_date': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'form-control'}
            ),
            'equipment': forms.Select(attrs={'class': 'form-control'})
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['equipment'].queryset = Equipment.objects.filter(status='available')
    def clean_expected_return_date(self):
        expected_date = self.cleaned_data.get('expected_return_date')
        if expected_date and expected_date < timezone.now():
            raise forms.ValidationError("Giờ hẹn trả không hợp lệ (không được nằm trong quá khứ).")
        return expected_date
class MaintenanceRecordForm(forms.ModelForm):
    class Meta:
        model = MaintenanceRecord
        fields = ['maintenance_date', 'description', 'cost', 'next_maintenance_date']
        widgets = {
            'maintenance_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'cost': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'step': '1000'}),
            'next_maintenance_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }