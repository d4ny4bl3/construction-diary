from datetime import timedelta

from django import forms
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory

from .models import Project, Material, DailyLog, MaterialUsage


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ("name", "location", "start_date", "status")


class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        exclude = ["price_per_unit"]


class DailyLogForm(forms.ModelForm):
    work_time_in_minutes = forms.IntegerField(
        label="Doba práce",
        min_value=0,
        required=True
    )

    class Meta:
        model = DailyLog
        fields = ("project", "title", "description", "date", "work_time_in_minutes", "temperature")

    def clean_work_time_in_minutes(self):
        # převede zadané minuty na timedelta objekt
        minutes = self.cleaned_data["work_time_in_minutes"]
        return timedelta(minutes=minutes)

    def save(self, commit=True):
        # přepisuje hodnotu work_time před uložením
        instance = super().save(commit=False)
        instance.work_time = self.cleaned_data["work_time_in_minutes"]
        if commit:
            instance.save()
        return instance


class MaterialUsageForm(forms.ModelForm):
    class Meta:
        model = MaterialUsage
        fields = "__all__"

    def clean_used_quantity(self):
        """
        Ověří, zda použité množství nepřesahuje dostupné množství.
        """
        used_quantity = self.cleaned_data.get("used_quantity")
        material = self.cleaned_data.get("material")
        if material and used_quantity > material.quantity:
            raise ValidationError("Nedostatečné množství materiálu")

        return used_quantity


MaterialUsageFormSet = forms.inlineformset_factory(
    DailyLog,
    MaterialUsage,
    fields=("material", "used_quantity"),
    extra=1
)
