from django import forms
from django.utils import timezone

from rent.models import Rental


class RentalCreateForm(forms.ModelForm):
    class Meta:
        model = Rental
        fields = ['start_date', 'end_date']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'date'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'date'}),
        }

    def clean_start_date(self):
        start_date = self.cleaned_data['start_date']
        if start_date < timezone.now() - timezone.timedelta(days=1):
            raise forms.ValidationError('The start date cannot be in the past')
        return start_date

    def clean_end_date(self):
        end_date = self.cleaned_data['end_date']
        if end_date < timezone.now():
            raise forms.ValidationError('The end date cannot be in the past')
        return end_date

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        if start_date and end_date and start_date > end_date:
            raise forms.ValidationError('The end date must be greater than the start date')
        return cleaned_data

    def save(self, commit=True) -> Rental:
        rental = super().save(commit=False)
        rental.total_price = rental.car.daily_price * (rental.end_date - rental.start_date).days
        if commit:
            rental.save()
        return rental
