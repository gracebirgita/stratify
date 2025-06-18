from django import forms
from .models import User, CompanyActivity

# class CompanyProfileForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = [
#             'company_name', 'company_logo', 'bio', 
#             'location', 'website', 'category', 'reputation', 
#             'vision', 'mission', 'umkm_level'
#         ]
#         widgets = {
#             'bio': forms.Textarea(attrs={'rows': 3}),
#             'vision': forms.Textarea(attrs={'rows': 3}),
#             'mission': forms.Textarea(attrs={'rows': 3}),
#         }

# class InvestorProfileForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ['profile_picture', 'bio', 'location', 'website']
#         widgets = {
#             'bio': forms.Textarea(attrs={'rows': 3}),
#         }