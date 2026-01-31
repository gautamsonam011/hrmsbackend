# core-backend/core/urls.py
import core.views as views
from django.urls import path, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
   openapi.Info(
      title="HRMS API",
      default_version='v1',
      description="API documentation for the hrms application, providing endpoints for user management, employee management, attendance operations, and more.",
      terms_of_service="https://www.google.com/policies/terms/", 
      contact=openapi.Contact(email="contact@hrms.local"), 
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
   # Support Bearer token authentication
   authentication_classes=[],
)

urlpatterns = [
    # --- Swagger & ReDoc ---
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # --- Authentication & User Management (General) ---
    path('employees/', views.EmployeeListCreateAPIView.as_view(), name='employee'),
    path("employees/<int:pk>/", views.EmployeeDeleteAPIView.as_view(), name='employee-delete'),
    path('attendance/', views.AttendanceListAPIView.as_view(), name='attendance')
    
]
    
    
