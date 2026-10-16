from django import forms

from .models import BorrowRecord, Equipment, MaintenanceRecord


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