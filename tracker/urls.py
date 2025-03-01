from django.urls import path
from .views import (
    home, employee_list, employee_profile, add_employee, edit_employee, delete_employee,
    request_leave, staff_leaves, approve_leave, reject_leave,
    expat_documents, add_expat_document,
    dashboard, export_leave_report, edit_expat_document,staff_contracts, add_staff_contract, edit_staff_contract, delete_staff_contract,
    supplier_contracts, add_supplier_contract, edit_supplier_contract, delete_supplier_contract
)
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', home, name='home'),
    path('employees/', employee_list, name='employee_list'),
    path('employees/add/', add_employee, name='add_employee'),  # ✅ Add employee
    path('employees/<int:user_id>/', employee_profile, name='employee_profile'),
    path('employees/edit/<int:user_id>/', edit_employee, name='edit_employee'),  # ✅ Edit employee
    path('employees/delete/<int:user_id>/', delete_employee, name='delete_employee'),  # ✅ Delete employee
    path('staff-leaves/request/', request_leave, name='request_leave'),
    path('staff-leaves/', staff_leaves, name='staff_leaves'),
    path('staff-leaves/approve/<int:leave_id>/', approve_leave, name='approve_leave'),
    path('staff-leaves/reject/<int:leave_id>/', reject_leave, name='reject_leave'),
    path('expat-documents/', expat_documents, name='expat_documents'),
    path('expat-documents/add/', add_expat_document, name='add_expat_document'),
    path('supplier-contracts/', supplier_contracts, name='supplier_contracts'),
    path('supplier-contracts/add/', add_supplier_contract, name='add_supplier_contract'),
    path('dashboard/', dashboard, name='dashboard'),
    path('export-leave-report/', export_leave_report, name='export_leave_report'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('expat-documents/edit/<int:document_id>/', edit_expat_document, name='edit_expat_document'),
    path('staff-contracts/', staff_contracts, name='staff_contracts'),
    path('staff-contracts/add/', add_staff_contract, name='add_staff_contract'),
    path('staff-contracts/edit/<int:contract_id>/', edit_staff_contract, name='edit_staff_contract'),
    path('staff-contracts/delete/<int:contract_id>/', delete_staff_contract, name='delete_staff_contract'),
    path('supplier-contracts/', supplier_contracts, name='supplier_contracts'),
    path('supplier-contracts/add/', add_supplier_contract, name='add_supplier_contract'),
    path('supplier-contracts/edit/<int:contract_id>/', edit_supplier_contract, name='edit_supplier_contract'),
    path('supplier-contracts/delete/<int:contract_id>/', delete_supplier_contract, name='delete_supplier_contract'),

]
