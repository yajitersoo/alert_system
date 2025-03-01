from django.contrib import admin
from .models import EmployeeProfile, StaffContract, StaffLeave, ExpatDocument, SupplierContract

admin.site.register(EmployeeProfile)
admin.site.register(StaffContract)
admin.site.register(StaffLeave)
admin.site.register(ExpatDocument)
admin.site.register(SupplierContract)
