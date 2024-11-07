from django.contrib import admin
from .models import Project, Material, DailyLog, MaterialUsage

from django.utils.html import format_html


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "location", "start_date", "end_date", "status", "total_cost")
    prepopulated_fields = {"slug": ("name",)}
    list_filter = ("status",)
    
    
@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ("name", "quantity", "price", "project")
    list_filter = ("project__name",)
    
    
@admin.register(DailyLog)
class DailyLogAdmin(admin.ModelAdmin):
    list_display = ("date", "project", "description", "get_used_materials", "weather_temperature")
    list_filter = ("project__name",)
    
    def get_used_materials(self, obj):
        materials = MaterialUsage.objects.filter(daily_log=obj)
        return format_html("<br>".join(f"{material.material.name} - {material.used_quantity} ks" for material in materials))
    get_used_materials.short_description = "Použité materiály"
    
    
@admin.register(MaterialUsage)
class MaterialUsageAdmin(admin.ModelAdmin):
    list_display = ("daily_log", "material", "used_quantity")
    list_filter = ("daily_log__project__name",)
