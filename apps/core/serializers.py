from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from . import models as core_models
from project.shortcuts import IsAuth
from django.utils import timezone
import requests
# Serializers

class VisionMissionSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)
    class Meta:
        model = core_models.VisionMission
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

    def get_image(self, obj):
        return obj.image.url if obj.image else None

    def validate_title(self, value):
        if len(value.strip()) < 3:
            raise serializers.ValidationError("title must be at least 3 characters long.")
        return value

    def validate_content(self, value):
        if len(value.strip()) < 10:
            raise serializers.ValidationError("content must be at least 10 characters long.")
        return value


        
class SliderSerializer(serializers.ModelSerializer):
    video = serializers.FileField(use_url=True, required=False)

    class Meta:
        model = core_models.slider
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

   

        
               

class FacultyInfoSerializer(serializers.ModelSerializer):
    video = serializers.FileField(use_url=True, required=False)
    class Meta:
        model = core_models.FacultyInfo
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

    

    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError("title is required.")
        return value

    def validate_content(self, value):
        if len(value.strip()) < 10:
            raise serializers.ValidationError("content must be at least 10 characters long.")
        return value


        
class StatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = core_models.Statistics
        fields = '__all__'

    def validate(self, data):
        for key in ['instructors', 'students', 'managers', 'masters_students']:
            if data[key] < 0:
                raise serializers.ValidationError({key: "must be a positive number."})
        return data

        
  


class CollegeleadersSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)
    cv = serializers.FileField(write_only=True, required=False)
    cv_url = serializers.CharField(source='cv', read_only=True)

    class Meta:
        model = core_models.Collegeleaders
        fields = '__all__'

    def validate_cv(self, value):
        if value and not value.name.endswith('.pdf'):
            raise serializers.ValidationError("CV must be a PDF file.")
        return value

    def upload_pdf_to_gofile(self, file):
        try:
            # Step 1: Get GoFile server
            server_resp = requests.get("https://api.gofile.io/getServer")
            if server_resp.status_code != 200:
                raise serializers.ValidationError("Failed to get GoFile server.")

            try:
                server_data = server_resp.json()
            except Exception:
                raise serializers.ValidationError(f"Invalid server response: {server_resp.text}")

            if server_data.get("status") != "ok":
                raise serializers.ValidationError("GoFile server status not ok.")

            server = server_data["data"]["server"]

            # Step 2: Upload file
            upload_url = f"https://{server}.gofile.io/uploadFile"
            files = {"file": (file.name, file.read())}
            response = requests.post(upload_url, files=files)

            if response.status_code != 200:
                raise serializers.ValidationError("File upload failed.")

            try:
                data = response.json()
            except Exception:
                raise serializers.ValidationError(f"Upload response is not JSON: {response.text}")

            if data.get("status") == "ok":
                return data["data"]["downloadPage"]
            else:
                raise serializers.ValidationError("Upload status not ok.")
        except Exception as e:
            raise serializers.ValidationError(f"Upload error: {str(e)}")

    def create(self, validated_data):
        cv_file = validated_data.pop('cv', None)
        if cv_file:
            validated_data['cv'] = self.upload_pdf_to_gofile(cv_file)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        cv_file = validated_data.pop('cv', None)
        if cv_file:
            validated_data['cv'] = self.upload_pdf_to_gofile(cv_file)
        return super().update(instance, validated_data)



#الشكاوى والمقترحات

# apps/core/serializers.py

from rest_framework import serializers
from .models import Collegeleaders, Complaint

class ComplaintSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Complaint
        fields = ['id', 'title', 'content', 'response', 'created_at', 'updated_at', 'user_email', 'user_name']
        read_only_fields = ['response', 'created_at', 'updated_at', 'user_email', 'user_name']


class ComplaintResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complaint
        fields = ['response']

    def update(self, instance, validated_data):
        instance.response = validated_data.get('response', instance.response)
        instance.updated_at = timezone.now()
        instance.save()
        return instance


class ComplaintUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complaint
        fields = ['title', 'content']
