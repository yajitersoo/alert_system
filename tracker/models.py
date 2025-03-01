from django.contrib.auth.models import User
from django.db import models
from datetime import date

EMPLOYEE_TYPES = [
    ('National Staff', 'National Staff'),
    ('Expatriate Staff', 'Expatriate Staff'),
]

LEAVE_STATUS = [
    ('Pending', 'Pending'),
    ('Approved', 'Approved'),
    ('Rejected', 'Rejected'),
]

DOCUMENT_TYPES = [
    ('National ID', 'National ID'),
    ('Work Permit', 'Work Permit'),
    ('Residency Permit', 'Residency Permit'),
]


class EmployeeProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(null=True, blank=True)  # ✅ Fixed typo (null=True)
    employee_type = models.CharField(max_length=20, choices=EMPLOYEE_TYPES)
    position = models.CharField(max_length=255)
    department = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    hire_date = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', default='profile_pictures/default.jpg', blank=True, null=True)

    def is_admin(self):
        return self.user.is_staff or self.user.is_superuser

    def __str__(self):
        role = "Admin" if self.user.is_staff else "Employee"
        return f"{self.user.username} - {self.position} ({role})"


class StaffContract(models.Model):
    employee = models.ForeignKey(EmployeeProfile, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    contract_file = models.FileField(upload_to='contracts/', blank=True, null=True)

    @property
    def is_expiring_soon(self):
        return (self.end_date - date.today()).days <= 30

    def __str__(self):
        return f"Contract for {self.employee.user.username}"


class StaffLeave(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField()
    status = models.CharField(max_length=10, choices=LEAVE_STATUS, default='Pending')
    approved_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="approved_leaves")

    @property
    def requested_days(self):
        return (self.end_date - self.start_date).days + 1

    def __str__(self):
        return f"{self.employee.username} - {self.start_date} to {self.end_date} ({self.status})"


class ExpatDocument(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    document_type = models.CharField(max_length=50, choices=DOCUMENT_TYPES)
    document_file = models.FileField(upload_to='expat_documents/')
    expiry_date = models.DateField()

    @property
    def is_expiring_soon(self):
        return (self.expiry_date - date.today()).days <= 30

    def __str__(self):
        return f"{self.document_type} for {self.employee.username}"


class SupplierContract(models.Model):
    supplier_name = models.CharField(max_length=255)
    contract_details = models.TextField(null=True, blank=True)  # ✅ Ensure this field exists
    start_date = models.DateField()
    end_date = models.DateField()
    contract_file = models.FileField(upload_to='supplier_contracts/', null=True, blank=True)

    def __str__(self):
        return f"{self.supplier_name} ({self.start_date} - {self.end_date})"



