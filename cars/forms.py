from django import forms

from cars.models import Car, CarModel, VehicleMaintenance


class CarCreateForm(forms.ModelForm):
    model = forms.ModelChoiceField(
        queryset=CarModel.objects.all(),
        required=False,
        empty_label="Create new model",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Car
        fields = ['license_plate', 'daily_price', 'mileage', 'status', 'location', 'description', 'model']
        widgets = {
            # 'location': GoogleMapPointFieldWidget(),
        }

    def clean_model(self):
        return self.cleaned_data['model']

    def is_valid(self):
        return super().is_valid()


class CarModelForm(forms.ModelForm):
    model1 = forms.CharField(label='Model', required=True, max_length=50)
    description1 = forms.CharField(label='Description', required=False, widget=forms.Textarea)

    class Meta:
        model = CarModel
        fields = ['brand', 'model1', 'year', 'body_type', 'fuel_type', 'transmission', 'default_image', 'description1']
        widgets = {
            'default_image': forms.FileInput(attrs={'accept': 'image/*'}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.model = self.cleaned_data['model1']
        instance.description = self.cleaned_data['description1']
        instance.default_image.name = f'{instance.brand} {instance.model}.{instance.default_image.name.split(".")[-1]}'
        if commit:
            instance.save()
        return instance


class VehicleMaintenanceForm(forms.ModelForm):
    class Meta:
        model = VehicleMaintenance
        fields = ['maintenance_date', 'maintenance_description', 'maintenance_cost']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance
