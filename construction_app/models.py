from django.db import models
from django.db.models import Sum, F
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.utils.text import slugify

from django.db.models.signals import post_delete
from django.dispatch import receiver


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
    total_cost = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=2, default=0)
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
        """
        Aktualizuje celkové náklady projektu na základě použitých materiálů v denních záznamech
        """
        self.total_cost = (
                self.daily_logs.aggregate(
                    total=Sum(
                        F("daily_usages__used_quantity") * F("daily_usages__material__price_per_unit")
                    )
                )["total"] or 0
        )
        self.save()


class Material(models.Model):
    UNIT_CHOICES = [
        ("ks", "ks"),
        ("kg", "kg"),
        ("m", "m"),
    ]

    name = models.CharField(max_length=150, verbose_name="Materiál")
    quantity = models.IntegerField(validators=[MinValueValidator(1)], verbose_name="Množství")
    unit = models.CharField(max_length=20, choices=UNIT_CHOICES, null=True, verbose_name="Jednotka")
    price = models.DecimalField(max_digits=20, decimal_places=2, verbose_name="Cena")
    price_per_unit = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Materiály"
        verbose_name = "Materiál"

    def __str__(self):
        return f"{self.name} - {self.quantity} {self.unit}"

    def save(self, *args, **kwargs):
        if not self.price_per_unit and self.quantity > 0:
            self.price_per_unit = self.price / self.quantity
        super().save(*args, **kwargs)


class DailyLog(models.Model):
    project = models.ForeignKey(Project, related_name="daily_logs", on_delete=models.PROTECT, null=True, verbose_name="Projekt")
    date = models.DateField(verbose_name="Datum")
    work_time = models.DurationField(verbose_name="Doba práce")
    description = models.TextField(verbose_name="Popis činnosti")
    temperature = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True, verbose_name="Teplota")

    class Meta:
        verbose_name_plural = "Denní zápisy"
        verbose_name = "Denní zápis"

    def __str__(self):
        return f"{self.date} - {self.project.name}"


class MaterialUsage(models.Model):
    daily_log = models.ForeignKey(DailyLog, related_name="daily_usages", on_delete=models.CASCADE)
    material = models.ForeignKey(Material, related_name="material_usages", on_delete=models.CASCADE)
    used_quantity = models.IntegerField(validators=[MinValueValidator(1)], verbose_name="Použité množství")

    class Meta:
        verbose_name_plural = "Použité materiály"
        verbose_name = "Použitý materiál"

    def __str__(self):
        return f"{self.daily_log.date} - {self.material.name}"

    def clean(self):
        if self.used_quantity > self.material.quantity:
            raise ValidationError("Nedostatečné množství materiálu")

    def save(self, *args, **kwargs):
        """
        Odebere požadované množství z Material.quantity a přepočítá celkové náklady projektu.
        """
        # Zavolání validace
        self.full_clean()

        self.material.quantity -= self.used_quantity
        self.material.save()
        super().save(*args, **kwargs)

        #  přepočet celkových nákladů
        self.daily_log.project.update_total_cost()


@receiver(post_delete, sender=MaterialUsage)
def return_material_stock(sender, instance, **kwargs):
    """
    Vrátí použité množství materiálu zpět a přepočítá celkové náklady projektu.
    """
    # Vrácení použitého množství do skladu
    if instance.material:
        instance.material.quantity += instance.used_quantity
        instance.material.save()

    # # Přepočet celkových nákladů projektu
    if instance.daily_log and instance.daily_log.project:
        instance.daily_log.project.update_total_cost()
