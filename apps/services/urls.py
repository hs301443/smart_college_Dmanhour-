from django.urls import path
from . import views

urlpatterns = [
    # API لـ عرض الوحدات وإنشاء وحدة جديدة
    path('section/', views.SectionListCreateAPIView.as_view(), name='section-list-create'),
    # API لـ عرض وتحديث وحذف وحدة معينة
    path('section/<int:pk>/', views.SectionDetailAPIView.as_view(), name='section-detail'),
    
    
    path('academic-years/', views.AcademicYearListCreateAPIView.as_view(), name='academic-year-list-create'),
    path('academic-years/<int:pk>/', views.AcademicYearDetailAPIView.as_view(), name='academic-year-detail'),

    

]
