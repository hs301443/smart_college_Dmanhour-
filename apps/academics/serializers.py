from rest_framework import serializers
from .models import Department, SpecialProgram, MastersProgram
from apps.users.models import Staff 

class StaffMiniSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    cv = serializers.SerializerMethodField()

    class Meta:
        model = Staff
        fields = ('id', 'cv', 'position', 'image', 'name')

    def get_image(self, obj):
        if obj.image:
            return obj.image.url
        return None

    def get_cv(self, obj):
        if obj.cv:
            return obj.cv.url
        return None


class DepartmentSerializer(serializers.ModelSerializer):
    doctors = serializers.PrimaryKeyRelatedField(many=True, queryset=Staff.objects.all(), required=False)
    doctors_detail = StaffMiniSerializer(source='doctors', many=True, read_only=True)
    image = serializers.SerializerMethodField()
    pdf = serializers.SerializerMethodField()

    class Meta:
        model = Department
        fields = [
            'id', 'name', 'about', 'image', 'vision', 'mission',
            'doctors', 'doctors_detail',
            'pdf', 'created_at', 'updated_at',
        ]
        read_only_fields = ('created_at', 'updated_at')

    def get_image(self, obj):
        if obj.image:
            return obj.image.url
        return None

    def get_pdf(self, obj):
        if obj.pdf:
            return obj.pdf.url
        return None

    # باقي الكود كما هو بدون تغيير
    def validate_name(self, value):
        if not value:
            raise serializers.ValidationError("The department name cannot be empty.")

        if self.instance:
            if Department.objects.exclude(id=self.instance.id).filter(name__iexact=value).exists():
                raise serializers.ValidationError("A department with this name already exists.")
        else:
            if Department.objects.filter(name__iexact=value).exists():
                raise serializers.ValidationError("A department with this name already exists.")
        return value

    def validate_pdf(self, value):
        if value and not value.name.endswith('.pdf'):
            raise serializers.ValidationError("The uploaded file must be a PDF.")
        return value

    def validate_doctors(self, value):
        if not value:
            raise serializers.ValidationError("At least one doctor must be assigned to the department.")
        return value

    def validate(self, data):
        if not data.get('vision') or not data.get('mission'):
            raise serializers.ValidationError("Vision and mission cannot be empty.")
        return data

    def create(self, validated_data):
        doctors = validated_data.pop('doctors', [])
        department = Department.objects.create(**validated_data)
        department.doctors.set(doctors)
        # إزالة مزامنة العلاقة العكسية لأنها غالباً غير موجودة
        return department

    def update(self, instance, validated_data):
        doctors = validated_data.pop('doctors', None)
        instance = super().update(instance, validated_data)
        if doctors is not None:
            instance.doctors.set(doctors)
        return instance


class SpecialProgramSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = SpecialProgram
        fields = '__all__'

    def get_image(self, obj):
        if obj.image:
            return obj.image.url
        return None

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Program name is required.")
        return value

    def validate_about(self, value):
        if len(value.strip()) < 10:
            raise serializers.ValidationError("Program description must be at least 10 characters long.")
        return value


class MastersProgramSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = MastersProgram
        fields = '__all__'

    def get_image(self, obj):
        if obj.image:
            return obj.image.url
        return None

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Masters program name is required.")
        return value

    def validate_about(self, value):
        if len(value.strip()) < 10:
            raise serializers.ValidationError("Masters program description must be at least 10 characters long.")
        return value