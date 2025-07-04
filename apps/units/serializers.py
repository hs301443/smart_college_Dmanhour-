from rest_framework import serializers
from .models import unit as UnitModel, UnitService
from apps.users.models import Staff

class UnitSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)
    class Meta:
        model = UnitModel
        fields = ['id', 'name', 'image', 'description']
    def get_image(self, obj):
        return self._abs_url(obj.image) if obj.image else None   

class StaffMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ['id', 'name', 'image', 'position']

class UnitServiceSerializer(serializers.ModelSerializer):
    unit = UnitSerializer(read_only=True)
    unit_id = serializers.PrimaryKeyRelatedField(
        queryset=UnitModel.objects.all(),
        source='unit',
        write_only=True
    )
    orgnization_structure = StaffMiniSerializer(many=True, read_only=True)
    orgnization_structure_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Staff.objects.all(),
        source='orgnization_structure',
        write_only=True,
        required=True
    )
    unit_objectives = serializers.SerializerMethodField()

    class Meta:
        model = UnitService
        fields = [
            'id', 'unit', 'unit_id', 'about_unit',
            'orgnization_structure', 'orgnization_structure_ids', 'unit_objectives'
        ]

    def get_unit_objectives(self, obj):
        """
        تحويل unit_objectives من string إلى list مفصول بالسطر الفاضي
        """
        if obj.unit_objectives:
            return [s.strip() for s in obj.unit_objectives.split('\r\n\r\n') if s.strip()]
        return []

    def validate_about_unit(self, value):
        if not value:
            raise serializers.ValidationError("about_unit is required.")
        return value

    def validate_unit_objectives(self, value):
        if not value:
            raise serializers.ValidationError("unit_objectives is required.")
        return value

    def validate_orgnization_structure_ids(self, value):
        if not value:
            raise serializers.ValidationError("orgnization_structure_ids is required.")
        return value
