from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin,ListModelMixin
from rest_framework.views import APIView
from rest_framework.mixins import UpdateModelMixin
from django.core.exceptions import ObjectDoesNotExist

class DepartmentCreateAPI(GenericAPIView,CreateModelMixin):
    serializer_class = DepartmentSerializer
    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)
    
    def create(self, request, *args, **kwargs):
        try:
            data = request.POST
            serializer = DepartmentSerializer(data = data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        except AssertionError:
            return Response({"Server Broke : Something is wrong on server side"})
        
class EmployeeCreateAPI(GenericAPIView,CreateModelMixin):
    serializer_class = EmployeeSerializer
    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)


    def create(self,request,*args,**kwargs):
        data = request.POST

        serializer = EmployeeSerializer(data = data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data,status = status.HTTP_201_CREATED)
    
class BaseSalarySet(GenericAPIView,CreateModelMixin):
    serializer_class = BaseSalarySerializer
    def post(self,request,*args,**kwargs):
        print(request.POST)
        return self.create(request,*args,**kwargs)
    
    def create(self, request, *args, **kwargs):
        data = request.POST

        serializer = BaseSalarySerializer(data = data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data,status=status.HTTP_201_CREATED)
    

class LeaveApplicationAPI(GenericAPIView,CreateModelMixin,UpdateModelMixin):
    serializer_class = LeaveApplicationSerializer
    queryset = LeaveApplication.objects.all()

    def post(self,request,*args,**kwargs):
        return self.partial_update(request,*args,**kwargs)
    
    def create(self,request):
        data = request.POST

        serializer = LeaveApplicationSerializer(data = data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data,status = status.HTTP_201_CREATED)

    def partial_update(self, request, *args, **kwargs):
        data = request.POST
        self.create(request)

        employeeId = request.POST.get('employeeId')
        month = request.POST.get('month')
        year = request.POST.get('year')
        print("Reached Here")
        leaveApplication = LeaveApplication.objects.get(employeeId = employeeId,month=month,year=year)
        print(leaveApplication)

        print("Reached Here also")
        serializer = LeaveApplicationSerializer(instance=leaveApplication,data=data,partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        print("Reached here now")

        return Response(serializer.data,status=status.HTTP_206_PARTIAL_CONTENT)
    
class CalculateSalaryAPI(GenericAPIView):
    serializer_class = EmployeeSerializer
    def post(self,request):
        employee = request.POST.get('employee')
        month = request.POST.get('month')
        year = request.POST.get('year')

        try:
            leaveApplication = LeaveApplication.objects.get(name=employee,month=month,year=year)
        except DoesNotExist:
            raise DoesNotExist("As per given details,any record is not available in database")
        
        salary = leaveApplication.payable_salary()

        return Response(salary,status=status.HTTP_200_OK)
    
class HighEarnersOnBaseSalary(GenericAPIView,ListModelMixin):
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()

    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)

    def list(self, request, *args, **kwargs):
        dep = kwargs['pk']

        try:
            dep = Department.objects.get(id = dep)
        except ObjectDoesNotExist:
            return Response("Department does not exist",status=status.HTTP_404_NOT_FOUND)
        employees = Employee.objects.filter(department = dep).order_by('-base_salary')

        serializer = EmployeeSerializer(employees,many=True)

        return Response(serializer.data,status=status.HTTP_200_OK)





        
# Create your views here.
