from .models import *
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from mongoengine.errors import DoesNotExist

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id','name']

    def validate(self, data):
        if not data['name']:
            raise ValidationError("name field is necessary")
        return data

    def create(self, validated_data):
        department = Department(**validated_data)
        department.save()

        return department
        

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id','name','base_salary','department']

    def validate(self, data):
        print(data)
        if not data['name']:
            raise ValidationError("name is a required field")
        
        if not data['department']:
            raise ValidationError("departmentId is required")
        return data
        
    def create(self, validated_data):
        try:
            dep_id = validated_data['department']
            print(dep_id)
            department = Department.objects.get(name = dep_id)
        except DoesNotExist:
            raise DoesNotExist("Entered department does not exist")
        
        employee = Employee(**validated_data)
        print("reached here")

        employee.save()

        return employee
    
class BaseSalarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['name','base_salary']

    def validate(self, attrs):
        if not attrs['name']:
            raise ValidationError("Name field is required")
        
        if not attrs['base_salary']:
            raise ValidationError("Base salary is required")
        return attrs

    def create(self, validated_data):
        try:
            name = validated_data['name']
            employee = Employee.objects.get(name = name)
        except DoesNotExist:
            raise DoesNotExist("Given employee is not in database")
        
        employee.base_salary = validated_data['base_salary']
        employee.save()

        return employee


class LeaveApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveApplication
        fields = ['employeeId','month','year','leaves']

    def validate(self, attrs):
        if not attrs['employeeId']:
            raise ValidationError("employeeId field is required")
        
        if not attrs['month']:
            raise ValidationError("month field is required")
        
        if not attrs['year']:
            raise ValidationError("year is a required field")
        
        if not attrs['leaves']:
            raise ValidationError("leave is a required field")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('leaves')
        leaveApplication = LeaveApplication(**validated_data)
        leaveApplication.save()

        return leaveApplication
    
    def update(self, instance, validated_data):
        instance = instance(**validated_data)

        instance.save()

        return instance
        
