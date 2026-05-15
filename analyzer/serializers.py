from rest_framework import serializers
from .models import CurriculumUpload, AnalysisResult


# =========================================================
# CURRICULUM SERIALIZER
# =========================================================
class CurriculumUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurriculumUpload
        fields = "__all__"


# =========================================================
# ANALYSIS RESULT SERIALIZER
# =========================================================
class AnalysisResultSerializer(serializers.ModelSerializer):

    class Meta:
        model = AnalysisResult
        fields = "__all__"