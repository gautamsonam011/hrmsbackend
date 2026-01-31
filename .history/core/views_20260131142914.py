from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
# models 
from .models import Employee, Attendance
# serializers
from .serializers import EmployeeSerializer, MarkAttendanceSerializer, AttendanceSerializer
# swagger 
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
    
    @swagger_auto_schema(
        operation_summary="Delete an employee by ID",
        manual_parameters=[
            openapi.Parameter(
                "id",
                openapi.IN_QUERY,
                description="Employee ID (primary key)",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        responses={
            204: "Employee deleted successfully",
            400: "Employee ID is required",
            404: "Employee not found"
        }
    )
    def delete(self, request):
        employee_id = request.query_params.get("id")

        if not employee_id:
            return Response(
                {
                    "success": False,
                    "message": "Employee ID is required"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        employee = get_object_or_404(Employee, id=employee_id)
        employee.delete()

        return Response(
            {
                "success": True,
                "message": "Employee deleted successfully"
            },
            status=status.HTTP_204_NO_CONTENT
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
        queryset = Attendance.objects.select_related("employee")

        employee_id = request.query_params.get("employee_id")
        attendance_date = request.query_params.get("date")

        if employee_id:
            queryset = queryset.filter(employee__id=employee_id)

        if attendance_date:
            queryset = queryset.filter(date=attendance_date)

        serializer = AttendanceSerializer(queryset, many=True)

        if not queryset.exists():
            return Response(
                {
                    "success": "success",
                    "message": "No attendance records found",
                    "data": []
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                "success": "success",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )
    
    @swagger_auto_schema(
        operation_summary="Mark today's attendance",
        request_body=MarkAttendanceSerializer,
        responses={
            201: "Attendance marked successfully",
            400: "Attendance already marked for today / Invalid data"
        }
    )
    def post(self, request):
        serializer = MarkAttendanceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {
                "success": True,
                "message": "Attendance marked successfully for today"
            },
            status=status.HTTP_201_CREATED
        )
