from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from project.shortcuts import IsAuth, has_permission
from .serializers import CustomUserSerializer, GraduationSerializer, StaffSerializer
from .models import CustomUser, Graduation, Staff
from django.shortcuts import get_object_or_404
from apps.users import serializers
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.parsers import MultiPartParser, FormParser



class RegisterUserView(APIView):
    
    # إنشاء مستخدم جديد
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # عرض بيانات مستخدم
    def get(self, request, user_id):
        if not IsAuth(request):
            return Response({"detail": "Authentication required"}, status=401)
        if not has_permission("core.change_visionmission", request):
            return Response({"detail": "Permission denied"}, status=403)
        user = get_object_or_404(CustomUser, id=user_id)
        serializer = CustomUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def patch(self, request, user_id):
        if not IsAuth(request):
            return Response({"detail": "Authentication required"}, status=401)
        
        user = get_object_or_404(CustomUser, id=user_id)
        serializer = CustomUserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            if 'password' in request.data:
                user.set_password(request.data['password'])
                user.save()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    

class GraduationView(APIView):
    parser_classes = [MultiPartParser, FormParser]    

    def post(self, request):
        serializer = GraduationSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            graduation = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def get(self, request, graduation_id):
        if not IsAuth(request):
            return Response({"detail": "Authentication required"}, status=401)  
        if not has_permission("core.change_visionmission", request):
            return Response({"detail": "Permission denied"}, status=403)
        graduation = get_object_or_404(Graduation, id=graduation_id)
        serializer = GraduationSerializer(graduation)
        return Response({
            "graduation_data": serializer.data
        }, status=status.HTTP_200_OK)



    def patch(self, request, graduation_id):
        if not IsAuth(request):
            return Response({"detail": "Authentication required"}, status=401)
        if not has_permission("core.change_visionmission", request):
            return Response({"detail": "Permission denied"}, status=403)
        graduation = get_object_or_404(Graduation, id=graduation_id)
        serializer = GraduationSerializer(graduation, data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Graduation data updated successfully.",
                "graduation_data": serializer.data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework.parsers import MultiPartParser, FormParser


class StaffView(APIView):
    parser_classes = [MultiPartParser, FormParser]    

    def post(self, request):
        if not IsAuth(request):
            return Response({"detail": "Authentication required"}, status=401)
        if not has_permission("core.change_visionmission", request):
            return Response({"detail": "Permission denied"}, status=403)
        serializer = StaffSerializer(data=request.data, context={"request": request})
        
        if serializer.is_valid():
            staff = serializer.save()
            return Response({
                "message": "Staff member created successfully.",
                "staff": StaffSerializer(staff).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, staff_id=None):
        if staff_id:
            staff = get_object_or_404(Staff, id=staff_id)
            serializer = StaffSerializer(staff)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            staff_list = Staff.objects.all()
            serializer = StaffSerializer(staff_list, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, staff_id):
        if not IsAuth(request):
            return Response({"detail": "Authentication required"}, status=401)
        if not has_permission("core.change_visionmission", request):
            return Response({"detail": "Permission denied"}, status=403)
        staff = get_object_or_404(Staff, id=staff_id)
        serializer = StaffSerializer(staff, data=request.data, partial=True, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Staff member updated successfully.",
                "staff_data": serializer.data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class CustomTokenObtainPairView(TokenObtainPairView):
     serializer_class = serializers.CustomTokenObtainPairSerializer