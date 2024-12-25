from rest_framework import serializers

from construction_app import models


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Project
        fields = ("name", "location", "start_date", "end_date", "status")


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Material
        exclude = ("price_per_unit",)
