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

    class Meta:
        model = Attendance
        fields = ["employee", "status"]

    def validate(self, attrs):
        employee = attrs.get("employee")
        today = date.today()

        if Attendance.objects.filter(
            employee=employee,
            date=today
        ).exists():
            raise serializers.ValidationError(
                "Attendance already marked for today."
            )

        return attrs

    def create(self, validated_data):
        validated_data["date"] = date.today()
        return super().create(validated_data)

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
