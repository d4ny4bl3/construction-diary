# from typing import Any
from django.db import models
from django.db.models import Sum
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.utils.text import slugify


class Project(models.Model):
    STATUS_CHOICES = [
        ("planned", "V plánu"),
        ("in_progress", "Probíhá"),
        ("completed", "Dokončeno"),
    ]
    
    name = models.CharField(max_length=100, unique=True, verbose_name="Název")
    location = models.CharField(max_length=50, verbose_name="Místo")
    start_date = models.DateField(verbose_name="Začátek projektu")
    end_date = models.DateField(null=True, blank=True, verbose_name="Konec projektu")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="planned", verbose_name="Stav")
    total_cost = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    slug = models.SlugField(max_length=100)
    
    class Meta:
        verbose_name_plural = "Projekty"
        verbose_name = "Projekt"
        
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def update_total_cost(self):
        self.total_cost = self.materials.aggregate(total=Sum("price"))["total"] or 0
        self.save()
    
    
class Material(models.Model):
    project = models.ForeignKey(Project, related_name="materials", on_delete=models.CASCADE)
    name = models.CharField(max_length=150, verbose_name="Materiál")
    quantity = models.IntegerField(validators=[MinValueValidator(1)], verbose_name="Množství")
    price = models.DecimalField(max_digits=20, decimal_places=2, verbose_name="Cena")
    
    class Meta:
        verbose_name_plural = "Materiály"
        verbose_name = "Materiál"
        
    def __str__(self):
        return f"{self.name} - {self.quantity} ks"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.project.update_total_cost()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.project.update_total_cost()
    
    
class DailyLog(models.Model):
    project = models.ForeignKey(Project, related_name="daily_logs", on_delete=models.CASCADE)
    date = models.DateField(verbose_name="Datum")
    work_time = models.DurationField(verbose_name="Doba práce")
    description = models.CharField(max_length=500, verbose_name="Popis činnosti")
    weather_temperature = models.DecimalField(null=True, blank=True, max_digits=3, decimal_places=2, verbose_name="Teplota") 
    
    class Meta:
        verbose_name_plural = "Denní zápisy"
        verbose_name = "Denní zápis"
    
    def __str__(self):
        return f"{self.project.name} - {self.date}"
    
    
class MaterialUsage(models.Model):
    daily_log = models.ForeignKey(DailyLog, related_name="daily_usages", on_delete=models.CASCADE)
    material = models.ForeignKey(Material, related_name="material_usages", on_delete=models.CASCADE, verbose_name="Použitý materiál")
    used_quantity = models.IntegerField(verbose_name="Použité množství")
    
    class Meta:
        verbose_name_plural = "Použité materiály"
        verbose_name = "Použitý materiál"
    
    def __str__(self):
        return f"{self.daily_log} : {self.material.name} - {self.used_quantity} ks"
    
    def clean(self, *args, **kwargs):
        super().clean()
        if self.used_quantity > self.material.quantity:
            raise ValidationError("Nedostatečné množství materiálu")
        
        # odečte použité množství od dostupného množství v Material
        self.material.quantity -= self.used_quantity
        self.material.save()  # uloží aktualizované množství v Material
        
        super().save(*args, **kwargs)  # uloží záznam v DailyLog
