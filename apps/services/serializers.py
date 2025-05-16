from rest_framework import serializers
from .models import section, acadmic_year


# ────────────────────────────
#   Section  Serializer
# ────────────────────────────
class SectionSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    pdf   = serializers.SerializerMethodField()

    class Meta:
        model  = section
        fields = [
            'id',
            'type',
            'title',
            'name',
            'description',
            'image',          # الآن يرجع URL
            'link',
            'pdf',            # الآن يرجع URL
        ]

    # ─── validation ──────────────────────────────────────────────────────────
    def validate_type(self, value):
        if not value:
            raise serializers.ValidationError("The 'type' field is required.")
        return value

    def validate_title(self, value):
        if not value:
            raise serializers.ValidationError("The 'title' field is required.")
        return value

    def validate_name(self, value):
        if not value:
            raise serializers.ValidationError("The 'name' field is required.")
        return value

    # ─── URL helpers ────────────────────────────────────────────────────────
    def _abs_url(self, file):
        request = self.context.get("request")
        return request.build_absolute_uri(file.url) if request else file.url

    def get_image(self, obj):
        return self._abs_url(obj.image) if obj.image else None

    def get_pdf(self, obj):
        return self._abs_url(obj.pdf) if obj.pdf else None



# ────────────────────────────
#   Academic Year Serializer
# ────────────────────────────
class AcademicYearSerializer(serializers.ModelSerializer):
    lecture_schedule = serializers.SerializerMethodField()
    practical_exam   = serializers.SerializerMethodField()
    exam             = serializers.SerializerMethodField()
    seating_number   = serializers.SerializerMethodField()

    class Meta:
        model  = acadmic_year
        fields = [
            'id',
            'year',
            'lecture_schedule',   # URL
            'practical_exam',     # URL
            'exam',               # URL
            'seating_number',     # URL
        ]

    # ─── validation ──────────────────────────────────────────────────────────
    def validate_year(self, value):
        if not value:
            raise serializers.ValidationError("The 'year' field is required.")
        return value

    # ─── URL helpers ────────────────────────────────────────────────────────
    def _abs_url(self, file):
        request = self.context.get("request")
        return request.build_absolute_uri(file.url) if request else file.url

    def get_lecture_schedule(self, obj):
        return self._abs_url(obj.lecture_schedule) if obj.lecture_schedule else None

    def get_practical_exam(self, obj):
        return self._abs_url(obj.practical_exam) if obj.practical_exam else None

    def get_exam(self, obj):
        return self._abs_url(obj.exam) if obj.exam else None

    def get_seating_number(self, obj):
        return self._abs_url(obj.seating_number) if obj.seating_number else None
