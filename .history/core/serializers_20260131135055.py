from rest_framework import serializers
from .models import Employee, Attendance
from datetime import date

# Employee 

class EmployeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employee
        fields = "__all__"

    def validate_employee_id(self, value):
        if not value.isalnum():
            raise serializers.ValidationError(
                "Employee ID must be alphanumeric."
            )
        return value

# Attendance 

class MarkAttendanceSerializer(serializers.ModelSerializer):
    employee_id = serializers.CharField(write_only=True)

    class Meta:
        model = Attendance
        fields = ["employee_id", "status"]

    def validate(self, attrs):
        employee_id = attrs.get("employee_id")
        today = date.today()

        try:
            employee = Employee.objects.get(employee_id=employee_id)
        except Employee.DoesNotExist:
            raise serializers.ValidationError(
                {"employee_id": "Employee does not exist."}
            )

        if Attendance.objects.filter(employee=employee, date=today).exists():
            raise serializers.ValidationError(
                "Attendance already marked for today."
            )

        # Attach employee object for create()
        attrs["employee"] = employee
        return attrs

    def create(self, validated_data):
        validated_data.pop("employee_id")
        validated_data["date"] = date.today()
        return Attendance.objects.create(**validated_data)

class AttendanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attendance
        fields = "__all__"

    def validate(self, attrs):
        employee = attrs.get("employee")
        date = attrs.get("date")

        if Attendance.objects.filter(employee=employee, date=date).exists():
            raise serializers.ValidationError(
                "Attendance already marked for this employee on this date."
            )
        return attrs
