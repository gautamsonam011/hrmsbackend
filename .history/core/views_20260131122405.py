from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Employee, Attendance
from .serializers import EmployeeSerializer, AttendanceSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Create your views here.



class EmployeeListCreateAPIView(APIView):

    @swagger_auto_schema(
        operation_summary="List all employees",
        responses={200: EmployeeSerializer(many=True)}
    )
    def get(self, request):
        employees = Employee.objects.all()
        serializer = EmployeeSerializer(employees, many=True)
        return Response({"success": True, "data": serializer.data})

    @swagger_auto_schema(
        operation_summary="Create a new employee",
        request_body=EmployeeSerializer,
        responses={
            201: EmployeeSerializer,
            400: "Bad Request"
        }
    )
    def post(self, request):
        serializer = EmployeeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"success": True, "data": serializer.data},
            status=status.HTTP_201_CREATED
        )


class AttendanceListAPIView(APIView):

    @swagger_auto_schema(
        operation_summary="View attendance records",
        manual_parameters=[
            openapi.Parameter(
                "employee_id",
                openapi.IN_QUERY,
                description="Employee ID",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                "date",
                openapi.IN_QUERY,
                description="Attendance date (YYYY-MM-DD)",
                type=openapi.TYPE_STRING
            )
        ],
        responses={200: AttendanceSerializer(many=True)}
    )
    def get(self, request):
        queryset = Attendance.objects.all()

        employee_id = request.query_params.get("employee_id")
        date = request.query_params.get("date")

        if employee_id:
            queryset = queryset.filter(employee__employee_id=employee_id)

        if date:
            queryset = queryset.filter(date=date)

        serializer = AttendanceSerializer(queryset, many=True)
        return Response({"success": True, "data": serializer.data})
