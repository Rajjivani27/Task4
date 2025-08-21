from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Employee(models.Model):
    name = models.CharField(max_length=100)
    base_salary = models.IntegerField(default = 0)
    department = models.ForeignKey(Department,on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class LeaveApplication(models.Model):
    employeeId = models.ForeignKey(Employee,on_delete=models.CASCADE)
    month = models.CharField()
    year = models.CharField()
    leaves = models.IntegerField(default = 0)

    def payable_salary(self):
        employee = Employee.objects.get(id = self.employeeId)
        base_salary = employee.base_salary

        salary = base_salary - (self.leaves * (base_salary/25))

        return salary