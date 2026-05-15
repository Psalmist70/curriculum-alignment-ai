from django.db import models


# =========================================================
# CURRICULUM UPLOAD
# =========================================================
class CurriculumUpload(models.Model):
    title = models.CharField(max_length=255)
    uploaded_file = models.FileField(upload_to="curriculum_files/")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# =========================================================
# ANALYSIS RESULT (ONE CURRICULUM → MANY RESULTS)
# =========================================================
class AnalysisResult(models.Model):
    curriculum = models.ForeignKey(
        CurriculumUpload,
        on_delete=models.CASCADE,
        related_name="results"
    )

    course_name = models.CharField(max_length=255)
    matched_job = models.CharField(max_length=255)

    similarity_score = models.FloatField()

    extracted_skills = models.TextField(blank=True)
    missing_skills = models.TextField(blank=True)
    recommendations = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.course_name} → {self.matched_job}"