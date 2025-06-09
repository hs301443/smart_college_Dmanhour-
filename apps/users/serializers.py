from rest_framework import serializers

from apps.units.models import unit
from .models import CustomUser, Graduation, Staff
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils.timezone import now
from django.contrib.auth import get_user_model
from apps.academics.models import Department
from django.contrib.auth.hashers import make_password


class CustomUserSerializer(serializers.ModelSerializer):
    repeat_password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'password', 'repeat_password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        if data['password'] != data['repeat_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data.pop('repeat_password')
        user_type = validated_data.get('user_type')
        user = CustomUser.objects.create_user(**validated_data)

        # لو user_type = graduation يضيفه في جدول Graduation
        if user_type == 'graduation':
            Graduation.objects.create(user=user)

        return user

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['id'] = instance.id
        return rep

def make_password(password):
    raise NotImplementedError
    


class GraduationSerializer(serializers.ModelSerializer):
     password = serializers.CharField(write_only=True)
     repeat_password = serializers.CharField(write_only=True)

     class Meta:
        model = Graduation
        fields = [
            'email', 'username', 'password', 'repeat_password',
            'cv', 'employment_status', 'job_name', 'location',
            'company_email', 'company_phone', 'company_link', 'about_company',
            'is_active'
        ]

        def validate(self, data):
         if data['password'] != data['repeat_password']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
         return data

        def create(self, validated_data):
         validated_data.pop('repeat_password')
         password = validated_data.pop('password')
         validated_data['password'] = make_password(password) 
         return Graduation.objects.create(**validated_data)


    
        def to_representation(self, instance):
         rep = super().to_representation(instance)
         rep['id'] = instance.id
         return rep


class DepartmentBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name']

class UnitSerializers(serializers.ModelSerializer):
    class meta:
        model=unit
        fields = ['id', 'name']


class StaffSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)
    cv = serializers.FileField(use_url=True, required=False)
    department_detail = DepartmentBasicSerializer(source='department', many=True, read_only=True)
    unit_detail=UnitSerializers(source='units', many=True, read_only=True)
    class Meta:
        model = Staff
        fields = ['id', 'name', 'position', 'cv', 'image', 'department', 'department_detail','units','unit_detail']
        extra_kwargs = {
            'name': {'required': True},
            'position': {'required': True},
            'cv': {'required': True},
            'image': {'required': True},
            'department': {'required': True},
            'units': {'required': True},
        }

    def validate_name(self, value):
        if not value:
            raise serializers.ValidationError("Name cannot be empty.")
        if self.instance:
            if Staff.objects.exclude(id=self.instance.id).filter(name__iexact=value).exists():
                raise serializers.ValidationError("Staff name already exists.")
        else:
            if Staff.objects.filter(name__iexact=value).exists():
                raise serializers.ValidationError("Staff name already exists.")
        return value

    def validate_cv(self, value):
        if value and not value.name.endswith('.pdf'):
            raise serializers.ValidationError("CV must be a PDF file.")
        return value

    def validate(self, data):
        if not data.get('position'):
            raise serializers.ValidationError("Position cannot be empty.")
        return data
    
    



User = get_user_model()

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = User.EMAIL_FIELD  

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['user_type'] = 'Graduation' if Graduation.objects.filter(email=user.email).exists() else 'CustomUser'
        token['updatePassword'] = 1 if user.username == user.password else 0
        token['updateName'] = 0 if user.first_name else 1
        user.last_login = now()
        user.save(update_fields=['last_login'])
        return token
