from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .forms import StaffLeaveForm, EmployeeProfileForm, ExpatDocumentForm, StaffContractForm, SupplierContractForm
from .models import EmployeeProfile, StaffLeave, StaffContract, ExpatDocument, SupplierContract
from django.db.models import Count
from datetime import date, timedelta
import csv
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.utils.timezone import now  # ✅ Import `now`
from django.contrib.auth.hashers import make_password

def home(request):
    """Redirect users based on role after login"""
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('dashboard')  # Admins go to dashboard
        elif hasattr(request.user, 'employeeprofile'):
            return redirect('employee_profile', user_id=request.user.id)
        else:
            messages.error(request, "Your profile is incomplete. Contact HR.")
            return redirect('home')
    return render(request, 'tracker/home.html')


@login_required
def employee_list(request):
    """Admin can see all employees"""
    if not request.user.is_staff:
        return redirect('employee_profile', user_id=request.user.id)

    employees = EmployeeProfile.objects.select_related('user').all()
    return render(request, 'tracker/employee_list.html', {'employees': employees})


@login_required
def employee_profile(request, user_id):
    """Employees can only view their own profile, Admins can view all"""
    employee = get_object_or_404(EmployeeProfile, user__id=user_id)
    if not request.user.is_staff and request.user.id != employee.user.id:
        return redirect('employee_profile', user_id=request.user.id)

    contract = StaffContract.objects.filter(employee=employee).first()
    return render(request, 'tracker/employee_profile.html', {
        'employee': employee,
        'contract': contract
    })


@login_required
def add_employee(request):
    """Allow admins to add a new employee."""
    if not request.user.is_staff:
        return redirect('employee_list')

    if request.method == 'POST':
        form = EmployeeProfileForm(request.POST, request.FILES)
        if form.is_valid():
            employee = form.save(commit=False)
            employee.user.email = form.cleaned_data.get('email')
            employee.user.save()
            employee.save()
            return redirect('employee_list')
    else:
        form = EmployeeProfileForm()

    return render(request, 'tracker/add_employee.html', {'form': form})


@login_required
def edit_employee(request, user_id):
    """Allow admins and employees to edit their profile."""
    employee = get_object_or_404(EmployeeProfile, user_id=user_id)

    if request.method == "POST":
        form = EmployeeProfileForm(request.POST, request.FILES, instance=employee)
        if form.is_valid():
            employee.user.email = form.cleaned_data['email']
            employee.user.save()
            employee.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('employee_profile', user_id=user_id)
    else:
        form = EmployeeProfileForm(instance=employee, initial={'email': employee.user.email})

    return render(request, 'tracker/edit_employee.html', {'form': form, 'employee': employee})


@login_required
def delete_employee(request, user_id):
    """Delete an employee profile"""
    if not request.user.is_staff:
        return redirect('employee_list')

    employee = get_object_or_404(EmployeeProfile, user_id=user_id)

    if request.method == 'POST':
        employee.user.delete()
        return redirect('employee_list')

    return render(request, 'tracker/confirm_delete_employee.html', {'employee': employee})


@login_required
def staff_contracts(request):
    """Admin can view all staff contracts."""
    if not request.user.is_staff:
        return redirect('home')

    contracts = StaffContract.objects.select_related('employee__user').all()
    return render(request, 'tracker/staff_contracts.html', {'contracts': contracts})


from django.contrib.auth.models import User
from django.db import IntegrityError


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from .models import EmployeeProfile, StaffContract
from .forms import StaffContractForm

def add_staff_contract(request):
    employee = None
    existing_employee_id = request.GET.get("employee")

    if existing_employee_id:
        try:
            employee = EmployeeProfile.objects.get(id=existing_employee_id)
        except EmployeeProfile.DoesNotExist:
            messages.error(request, "Employee not found.")
            return redirect("add_staff_contract")

    if request.method == "POST":
        existing_employee_id = request.POST.get("employee")
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")
        contract_file = request.FILES.get("contract_file")

        # ✅ Handle Existing Employee Selection
        if existing_employee_id:
            employee = EmployeeProfile.objects.get(id=existing_employee_id)

        # ✅ Handle New Employee Creation
        else:
            new_username = request.POST.get("new_username")
            email = request.POST.get("email")
            password = request.POST.get("password")
            confirm_password = request.POST.get("confirm_password")
            employee_type = request.POST.get("employee_type")
            position = request.POST.get("position")
            department = request.POST.get("department")
            phone_number = request.POST.get("phone_number")
            hire_date = request.POST.get("hire_date")
            profile_picture = request.FILES.get("profile_picture")

            if User.objects.filter(username=new_username).exists():
                messages.error(request, "Username already exists! Choose a different username.")
                return redirect("add_staff_contract")

            if password != confirm_password:
                messages.error(request, "Passwords do not match! Please try again.")
                return redirect("add_staff_contract")

            # ✅ Create User Account
            user = User.objects.create(
                username=new_username,
                email=email,
                password=make_password(password)
            )
            user.save()

            # ✅ Create Employee Profile
            employee = EmployeeProfile.objects.create(
                user=user,
                employee_type=employee_type,
                position=position,
                department=department,
                phone_number=phone_number,
                hire_date=hire_date,
                profile_picture=profile_picture
            )

        # ✅ Create Staff Contract
        contract = StaffContract.objects.create(
            employee=employee,
            start_date=start_date,
            end_date=end_date,
            contract_file=contract_file
        )

        messages.success(request, "Staff contract added successfully.")
        return redirect("staff_contracts")

    else:
        form = StaffContractForm()

    return render(request, "tracker/add_staff_contract.html", {"form": form, "employee": employee})


@login_required
def edit_staff_contract(request, contract_id):
    """Allow admins to edit staff contracts."""
    if not request.user.is_staff:
        messages.error(request, "You do not have permission to edit contracts.")
        return redirect('staff_contracts')

    contract = get_object_or_404(StaffContract, id=contract_id)

    if request.method == 'POST':
        form = StaffContractForm(request.POST, request.FILES, instance=contract)
        if form.is_valid():
            contract = form.save(commit=False)

            # ✅ Retain the Employee (Do not change)
            contract.employee = contract.employee  # Ensure employee is retained

            # ✅ Update the Employee's Position
            contract.employee.position = request.POST.get('position')  # Get position from form
            contract.employee.save()  # ✅ Save employee profile changes

            # ✅ Save contract details
            contract.save()
            messages.success(request, "Contract updated successfully!")
            return redirect('staff_contracts')
        else:
            messages.error(request, "Error updating contract. Please check the form.")
    else:
        form = StaffContractForm(instance=contract, initial={'position': contract.employee.position})

    return render(request, 'tracker/edit_staff_contract.html', {'form': form, 'contract': contract})


@login_required
def delete_staff_contract(request, contract_id):
    """Admins can delete staff contracts."""
    contract = get_object_or_404(StaffContract, id=contract_id)

    if not request.user.is_staff:
        return redirect('staff_contracts')

    if request.method == "POST":
        contract.delete()
        messages.success(request, "Contract deleted successfully!")
        return redirect('staff_contracts')

    return render(request, 'tracker/confirm_delete_contract.html', {'contract': contract})


@login_required
def supplier_contracts(request):
    """List all supplier contracts (Admin Only)."""
    if not request.user.is_staff:
        return redirect('dashboard')

    contracts = SupplierContract.objects.all()
    return render(request, 'tracker/supplier_contracts.html', {'contracts': contracts})


@login_required
def add_supplier_contract(request):
    """Allow admins to add new supplier contracts."""
    if not request.user.is_staff:
        messages.error(request, "You do not have permission to add supplier contracts.")
        return redirect('supplier_contracts')

    if request.method == 'POST':
        form = SupplierContractForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # ✅ Save the contract to the database
            messages.success(request, "Supplier contract added successfully!")
            return redirect('supplier_contracts')
        else:
            messages.error(request, "There was an error adding the supplier contract. Please check your input.")
    else:
        form = SupplierContractForm()

    return render(request, 'tracker/add_supplier_contract.html', {'form': form})


@login_required
def delete_supplier_contract(request, contract_id):
    """Allow admins to delete supplier contracts."""
    if not request.user.is_staff:
        messages.error(request, "You do not have permission to delete contracts.")
        return redirect('supplier_contracts')

    contract = get_object_or_404(SupplierContract, id=contract_id)

    if request.method == "POST":
        contract.delete()
        messages.success(request, "Supplier contract deleted successfully!")
        return redirect('supplier_contracts')

    return render(request, 'tracker/confirm_delete_supplier_contract.html', {'contract': contract})

@login_required
def export_leave_report(request):
    """Generate CSV report of all leave requests"""
    if not request.user.is_staff:
        return redirect('dashboard')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="leave_requests.csv"'

    writer = csv.writer(response)
    writer.writerow(['Employee', 'Start Date', 'End Date', 'Status'])

    leaves = StaffLeave.objects.all()
    for leave in leaves:
        writer.writerow([leave.employee.username, leave.start_date, leave.end_date, leave.status])

    return response

@login_required
def request_leave(request):
    """Allow employees to request leave."""
    if request.method == 'POST':
        form = StaffLeaveForm(request.POST)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.employee = request.user  # Assign current user
            leave.save()
            messages.success(request, "Leave request submitted successfully.")
            return redirect('staff_leaves')
    else:
        form = StaffLeaveForm()

    return render(request, 'tracker/request_leave.html', {'form': form})

@login_required
def staff_leaves(request):
    """Show leave requests: employees see their own, admins see all."""
    if request.user.is_staff:
        leaves = StaffLeave.objects.all()  # Admin sees all leave requests
    else:
        leaves = StaffLeave.objects.filter(employee=request.user)  # Employees see only their own

    return render(request, 'tracker/staff_leaves.html', {'leaves': leaves})


@login_required
def approve_leave(request, leave_id):
    """Approve a leave request."""
    leave = get_object_or_404(StaffLeave, id=leave_id)

    if not request.user.is_staff:
        return redirect('staff_leaves')

    leave.status = "Approved"
    leave.approved_by = request.user
    leave.save()

    # ✅ Ensure employee has an email before sending notification
    if leave.employee.email:
        subject = "Leave Request Approved"
        message = f"Dear {leave.employee.username},\n\nYour leave request from {leave.start_date} to {leave.end_date} has been approved.\n\nBest regards,\nHR Team"
        send_mail(subject, message, 'tyaji247@gmail.com', [leave.employee.email], fail_silently=False)
    else:
        print(f"⚠ No email found for {leave.employee.username}. Email notification not sent.")

    return redirect('staff_leaves')


@login_required
def reject_leave(request, leave_id):
    """Reject a leave request and notify the employee via email."""
    leave = get_object_or_404(StaffLeave, id=leave_id)

    if not request.user.is_staff:
        return redirect('staff_leaves')

    leave.status = "Rejected"
    leave.approved_by = request.user
    leave.save()

    # ✅ Ensure employee has an email before sending notification
    if leave.employee.email:
        subject = "Leave Request Rejected"
        message = f"Dear {leave.employee.username},\n\nUnfortunately, your leave request from {leave.start_date} to {leave.end_date} has been rejected.\n\nBest regards,\nHR Team"
        send_mail(subject, message, 'tyaji247@gmail.com', [leave.employee.email], fail_silently=False)
    else:
        print(f"⚠ No email found for {leave.employee.username}. Email notification not sent.")

    return redirect('staff_leaves')


@login_required
def expat_documents(request):
    """Allow employees to see only their documents while admins see all."""
    if request.user.is_staff:
        documents = ExpatDocument.objects.all()  # Admin sees all documents
    else:
        documents = ExpatDocument.objects.filter(employee=request.user)  # Employees see only their own

    return render(request, 'tracker/expat_documents.html', {'documents': documents})


@login_required
def add_expat_document(request):
    """Allow employees to add their documents, admins can add for any employee."""
    if request.method == 'POST':
        form = ExpatDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)

            # ✅ Employees can only upload their own documents
            if not request.user.is_staff:
                document.employee = request.user
            else:
                # ✅ Admins select the employee manually
                document.employee = form.cleaned_data.get('employee')

            document.save()
            messages.success(request, "Expatriate document added successfully.")
            return redirect('expat_documents')
    else:
        form = ExpatDocumentForm()

    return render(request, 'tracker/add_expat_document.html', {'form': form})


@login_required
def dashboard(request):
    """Admin Dashboard View"""
    if not request.user.is_staff:
        return redirect('employee_profile', user_id=request.user.id)

    today = now().date()
    expiring_threshold = today + timedelta(days=7)

    # ✅ Contract Statistics
    total_contracts = StaffContract.objects.count()
    active_contracts = StaffContract.objects.filter(end_date__gte=today).count()
    expired_contracts = StaffContract.objects.filter(end_date__lt=today).count()

    # ✅ Fetching relevant data
    pending_leaves = StaffLeave.objects.filter(status="Pending")
    expiring_contracts = StaffContract.objects.filter(end_date__lte=expiring_threshold, end_date__gte=today)
    expired_contracts_list = StaffContract.objects.filter(end_date__lt=today)
    expiring_documents = ExpatDocument.objects.filter(expiry_date__lte=expiring_threshold, expiry_date__gte=today)
    expired_documents = ExpatDocument.objects.filter(expiry_date__lt=today)
    expiring_suppliers = SupplierContract.objects.filter(end_date__lte=expiring_threshold, end_date__gte=today)
    expired_supplier_contracts = SupplierContract.objects.filter(end_date__lt=today)

    # ✅ Leave Statistics
    total_leaves = StaffLeave.objects.count()
    approved_leaves = StaffLeave.objects.filter(status="Approved").count()
    rejected_leaves = StaffLeave.objects.filter(status="Rejected").count()

    context = {
        'total_contracts': total_contracts,
        'active_contracts': active_contracts,
        'expired_contracts': expired_contracts,
        'pending_leaves': pending_leaves,
        'expiring_contracts': expiring_contracts,
        'expired_contracts_list': expired_contracts_list,
        'expiring_documents': expiring_documents,
        'expired_documents': expired_documents,
        'expiring_suppliers': expiring_suppliers,
        'total_leaves': total_leaves,
        'approved_leaves': approved_leaves,
        'rejected_leaves': rejected_leaves,
        'expired_supplier_contracts': expired_supplier_contracts,
    }

    return render(request, 'tracker/dashboard.html', context)


@login_required
def edit_expat_document(request, document_id):
    """Allow admins to modify any expatriate document and employees to modify their own."""
    document = get_object_or_404(ExpatDocument, id=document_id)

    # Restrict normal employees from modifying other employees' documents
    if not request.user.is_staff and document.employee != request.user:
        messages.error(request, "You do not have permission to edit this document.")
        return redirect('expat_documents')

    if request.method == "POST":
        form = ExpatDocumentForm(request.POST, request.FILES, instance=document)
        if form.is_valid():
            form.save()
            messages.success(request, "Expatriate document updated successfully.")
            return redirect('expat_documents')
    else:
        form = ExpatDocumentForm(instance=document)

    return render(request, 'tracker/edit_expat_document.html', {'form': form, 'document': document})


@login_required
def edit_supplier_contract(request, contract_id):
    """Admins can edit supplier contracts."""
    contract = get_object_or_404(SupplierContract, id=contract_id)

    if not request.user.is_staff:
        messages.error(request, "You do not have permission to edit supplier contracts.")
        return redirect('supplier_contracts')

    if request.method == 'POST':
        form = SupplierContractForm(request.POST, request.FILES, instance=contract)
        if form.is_valid():
            updated_contract = form.save(commit=False)
            print("Updated contract details:", updated_contract.contract_details)  # ✅ Debugging
            updated_contract.save()
            messages.success(request, "Supplier contract updated successfully!")
            return redirect('supplier_contracts')  # ✅ Redirect after update
        else:
            print("Form errors:", form.errors)  # ✅ Debugging form issues
    else:
        form = SupplierContractForm(instance=contract)

    return render(request, 'tracker/edit_supplier_contract.html', {'form': form, 'contract': contract})



