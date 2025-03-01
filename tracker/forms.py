from django import forms
from .models import StaffLeave, ExpatDocument, SupplierContract, EmployeeProfile, StaffContract

class StaffLeaveForm(forms.ModelForm):
    class Meta:
        model = StaffLeave
        fields = ['start_date', 'end_date', 'description']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class ExpatDocumentForm(forms.ModelForm):
    class Meta:
        model = ExpatDocument
        fields = ['document_type', 'document_file', 'expiry_date']  # ✅ Remove 'employee' field
        widgets = {
            'expiry_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

class SupplierContractForm(forms.ModelForm):
    class Meta:
        model = SupplierContract
        fields = ['supplier_name', 'contract_details', 'start_date', 'end_date', 'contract_file']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

class EmployeeProfileForm(forms.ModelForm):
    email = forms.EmailField(required=True)  # ✅ Make Email Required
    class Meta:
        model = EmployeeProfile
        fields = ['employee_type', 'email', 'position', 'department', 'phone_number', 'hire_date', 'profile_picture']
        widgets = {
            'hire_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

class StaffContractForm(forms.ModelForm):
    # ✅ Fields for creating a new user
    new_username = forms.CharField(
        required=False,
        label="New Employee Username",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    email = forms.EmailField(required=False, label="Email")
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Password"
    )

    # ✅ Fields for employee profile
    employee_type = forms.ChoiceField(choices=[('National Staff', 'National Staff'), ('Expatriate Staff', 'Expatriate Staff')])
    position = forms.CharField(max_length=255)
    department = forms.CharField(max_length=255, required=False)
    phone_number = forms.CharField(max_length=20, required=False)
    hire_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    profile_picture = forms.ImageField(required=False)

    # ✅ Select an existing employee
    employee = forms.ModelChoiceField(
        queryset=EmployeeProfile.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Select Existing Employee"
    )

    class Meta:
        model = StaffContract
        fields = ['employee', 'start_date', 'end_date', 'contract_file']