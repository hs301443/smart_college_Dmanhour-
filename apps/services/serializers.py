from rest_framework import serializers
from .models import section

class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = section
        fields = [
            'id',
            'type',
            'title',
            'name',
            'description',
            'image',
            'link',
            'pdf',
        ]

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
  
  
  
  #academic year serializer
  
  
from .models import acadmic_year

class AcademicYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = acadmic_year
        fields = [
            'id',
            'year',
            'leacture_schedule',
            'partical_exam',
            'exam',
            'seating_number',
        ]

    def validate_year(self, value):
        if not value:
            raise serializers.ValidationError("The 'year' field is required.")
        return value

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')

        if request:
            for field in ['leacture_schedule', 'partical_exam', 'exam', 'seating_number']:
                file = getattr(instance, field)
                if file:
                    data[field] = request.build_absolute_uri(file.url)
        return data
