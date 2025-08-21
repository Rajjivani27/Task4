from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

urlpatterns = [
    path('employee_create/',EmployeeCreateAPI.as_view(),name="employee-create"),
    path('dep_create/',DepartmentCreateAPI.as_view(),name="dep-create"),
    path('calculate_salary/',CalculateSalaryAPI.as_view(),name="calculate-salary"),
    path('base_salary_set/',BaseSalarySet.as_view(),name="base-salary-set"),
    path('leave_application/',LeaveApplicationAPI.as_view(),name="leave-application"),
    path('top_high_earner/<int:pk>/',HighEarnersOnBaseSalary.as_view(),name="top-high-earner"),
] + router.urls