from rest_framework import serializers
from .models import unit, UnitService
from users.models import Staff

class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = unit
        fields = [
            'id',
            'name',
            'description',
            'image',
            'created_at',
            'updated_at',
        ]

class StaffMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ['id', 'name', 'image', 'position']

class UnitServiceSerializer(serializers.ModelSerializer):
    unit = UnitSerializer(read_only=True)
    unit_id = serializers.PrimaryKeyRelatedField(
        queryset=unit.objects.all(),
        source='unit',
        required=True,  # مطلوب عند الإنشاء
        write_only=True
    )

    orgnization_structure = StaffMiniSerializer(many=True, read_only=True)
    orgnization_structure_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Staff.objects.all(),
        source='orgnization_structure',
        required=False,
        write_only=True
    )

    class Meta:
        model = UnitService
        fields = [
            'id',
            'unit',
            'unit_id',
            'abou_unit',
            'orgnization_structure',
            'orgnization_structure_ids',
            'unit_objectives',
        ]

    def validate_abou_unit(self, value):
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
