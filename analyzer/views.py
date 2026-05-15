import pandas as pd
import numpy as np
import io

from django.http import JsonResponse

def health(request):
    return JsonResponse({"status": "ok"})

from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response

from .nlp_engine import run_alignment_analysis, search_jobs, get_job_by_index, extract_skills
from .skill_gap import detect_skill_gaps
from .recommendation import generate_recommendations
from .analytics import generate_analytics
from .serializers import AnalysisResultSerializer
from .models import CurriculumUpload, AnalysisResult

from sentence_transformers import SentenceTransformer

# =========================================================
# HEALTH CHECK
# =========================================================
@api_view(['GET'])
def health(request):
    return Response({"status": "ok"})


# =========================================================
# UPLOAD & ANALYZE CURRICULUM
# =========================================================
@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def upload_curriculum(request):

    uploaded_file = request.FILES.get("file")

    if not uploaded_file:
        return Response(
            {"error": "No file uploaded"},
            status=400
        )

    try:
        # =====================================================
        # READ FILE SAFELY (FIXES UTF-8 + EmptyData issues)
        # =====================================================
        content = uploaded_file.read()

        try:
            decoded = content.decode("utf-8")
        except UnicodeDecodeError:
            decoded = content.decode("latin1")

        df = pd.read_csv(io.StringIO(decoded))

        if df.empty:
            return Response(
                {"error": "Uploaded CSV is empty"},
                status=400
            )

        # =====================================================
        # SAVE UPLOAD
        # =====================================================
        curriculum = CurriculumUpload.objects.create(
            title=uploaded_file.name,
            uploaded_file=uploaded_file
        )

        # =====================================================
        # RUN NLP + FAISS PIPELINE
        # =====================================================
        results = run_alignment_analysis(df)

        # =====================================================
        # SAVE RESULTS TO DB
        # =====================================================
        for result in results:
            AnalysisResult.objects.create(
                curriculum=curriculum,
                course_name=result['course_name'],
                matched_job=result['matched_job'],
                similarity_score=result['similarity_score'],
                extracted_skills=', '.join(result['extracted_skills']),
                missing_skills=', '.join(result['missing_skills']),
                recommendations=', '.join(result['recommendations'])
            )

        # =====================================================
        # ANALYTICS
        # =====================================================
        analytics = generate_analytics(results)

        return Response({
            "message": "Analysis completed successfully",
            "analytics": analytics,
            "results": results
        })

    except Exception as e:
        return Response({
            "error": str(e)
        }, status=500)


# =========================================================
# FETCH SAVED RESULTS
# =========================================================
@api_view(['GET'])
def fetch_results(request, curriculum_id):

    results = AnalysisResult.objects.filter(
        curriculum_id=curriculum_id
    )

    serializer = AnalysisResultSerializer(results, many=True)

    return Response(serializer.data)