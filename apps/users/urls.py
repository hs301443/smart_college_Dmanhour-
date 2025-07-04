from django.urls import path
from .views import RegisterUserView, GraduationView, StaffView
from apps.users import views

urlpatterns = [
    path('token/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    
    path('register/', RegisterUserView.as_view(), name='register-user'),
    path('register/update/<int:user_id>/', RegisterUserView.as_view(), name='user-update'),
    path('user/<int:user_id>/', RegisterUserView.as_view(), name='user-info'),
    
    path('graduation/', GraduationView.as_view(), name='graduation-handler'),

    
    path('staff/', StaffView.as_view()),  # لو هتجيب الكل أو تعمل POST
    path('staff/<int:staff_id>/', StaffView.as_view()),  # لو هتجيب واحد أو تعمل PATCH


]

