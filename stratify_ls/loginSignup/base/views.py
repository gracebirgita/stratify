# from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages # memberi pesan error
from django.conf import settings
from django.core.mail import EmailMessage
from django.utils import timezone
from django.urls import reverse
from .models import *
from django.http import HttpResponseForbidden
from django.db.models import F, ExpressionWrapper, BooleanField, Q
from base.forms import UploadCSVForm
import pandas as pd
import io
from datetime import datetime
import json



#based on ROLES
from .decorators import role_required # add @role_required([1]) -> company
from .forms import  ActivityForm

#admin account superuser
# user name : grace
# password : 1

@login_required
def Home(request):
    add_fake_data(request)

    # take param main search
    search_query = request.GET.get('search', '')
    #filter
    role_filter = request.GET.get('role', '')
    category_filter = request.GET.get('category', '')
    reputation_filter = request.GET.get('reputation', '')

    print(f"Search Query: {search_query}")
    print(f"Role Filter: {role_filter}")
    print(f"Category Filter: {category_filter}")
    print(f"Reputation Filter: {reputation_filter}")
    
    # Apply search filter
    companies, investors = search_user(search_query)
 
    #sort based on avaibility of category and reputation
    companies = companies.annotate(
        has_reputation=ExpressionWrapper(~Q(reputation='') & ~Q(reputation=None), output_field=BooleanField()),
        has_category=ExpressionWrapper(~Q(category='') & ~Q(category=None), output_field=BooleanField())
    ).order_by('-has_reputation', '-has_category', 'username')
    


    if role_filter == 'Company':
        investors=investors.none() #investor empty
    elif role_filter == 'Investor':
        companies = companies.none() # company empty
    elif role_filter == 'All' or role_filter == '': #investor and company not empty
        pass

    if category_filter or reputation_filter:
        investors = investors.none()
        if category_filter:
            companies = companies.filter(category__icontains=category_filter)

        if reputation_filter:
            companies = companies.filter(reputation__icontains=reputation_filter)
        
    # limit company & investor reduce lag
    companies = companies[:10]
    investors = investors[:10]

    #send data to template
    context = {
        'companies': companies,
        'investors': investors,
        'search_query' : search_query,
        'role_filter' : role_filter,
        'category_filter' : category_filter,
        'reputation_filter' : reputation_filter,
    }
    return render(request, 'index.html', context)

def search_user(search_query):

    companies = User.objects.filter(role=1, is_staff = False)
    investors = User.objects.filter(role=2, is_staff = False)

    if search_query:
        companies = companies.filter(username__icontains=search_query)
        investors = investors.filter(username__icontains=search_query)
    
    return companies, investors

#View profile, other features

@login_required
def MyActivities(request):
    return render(request, 'my_activities.html')

@login_required
def Messages(request):
    return render(request, 'messages.html')

def landingPage(request):
    return render(request, 'landingPage.html')

# @login_required
# def analyticsCompany(request):
#     selected_chart_ids = UserChartSelection.objects.filter(user=request.user).values_list('chart_id', flat=True)
#     selected_charts = ChartData.objects.filter(id__in=selected_chart_ids)
#     charts = list(selected_charts.values('labels', 'values'))  # Adjust based on your ChartData model fields
#     charts_json = json.dumps(charts)
#     return render(request, 'analytics.html',{'charts':charts_json})

# recently searched
@login_required
def index(request):
    search_query = request.GET.get('search')
    if search_query:
        # Ambil recent_searches dari session, jika belum ada buat list kosong
        recent_searches = request.session.get('recent_searches', [])
        # Tambahkan search baru jika belum ada
        if search_query not in recent_searches:
            recent_searches.insert(0, search_query)
        # Batasi hanya 5 pencarian terakhir
        recent_searches = recent_searches[:5]
        request.session['recent_searches'] = recent_searches
    else:
        recent_searches = request.session.get('recent_searches', [])
    # ...existing code...
    return render(request, 'index.html', {
        # ...context lain...
        'recent_searches': recent_searches,
    })

@login_required
def view_profile(request, name):
    profile_user = get_object_or_404(User, username=name)
    is_owner = request.user == profile_user
    context = {
        'profile_user': profile_user,
        'is_owner': is_owner,
    }

    
    if profile_user.role == 1:  # Company
        activities = CompanyActivity.objects.filter(company=profile_user).order_by('-date')
        context['activities'] = activities
        return render(request, 'view_profile.html', context)
    else:  # Investor
        investments = profile_user.investment_history.all()
        context['investments'] = investments
        return render(request, 'view_profile.html', context)


@login_required
def edit_profile(request, name):
    profile_user = get_object_or_404(User, username=name)

    if request.user != profile_user:
        return HttpResponseForbidden("You don't have permission to edit this profile.")

    if request.method == 'POST':
        user = request.user

        # Fields shared by both roles
        user.bio = request.POST.get('bio')
        user.location = request.POST.get('location')
        user.website = request.POST.get('website')
        user.vision = request.POST.get('vision')
        user.mission = request.POST.get('mission')
   
        # Fields specific to role
        if user.role == 1:  # Company
            user.company_name = request.POST.get('company_name')
            if User.objects.exclude(pk=user.pk).filter(username=user.company_name).exists():
                messages.error(request, 'This name is already taken by another user.')
                return redirect('edit_profile', name=user.username)
            else:
                user.username = user.company_name
                
                
            user.reputation = request.POST.get('reputation')
            user.category = request.POST.get('category')
            user.umkm_level = request.POST.get('umkm_level')
            
        elif user.role == 2:  # Investor
            user.investor_name = request.POST.get('investor_name')
            if User.objects.exclude(pk=user.pk).filter(username=user.investor_name).exists():
                messages.error(request, 'This name is already taken by another user.')
                return redirect('edit_profile', name=user.username)
            else:
                user.username = user.investor_name
            
        # Handle bg picture
        if 'profile_bg' in request.FILES:
            user.profile_bg = request.FILES['profile_bg']
            
            
        # Handle profile picture (both roles)
        if 'profile_picture' in request.FILES:
            user.profile_picture = request.FILES['profile_picture']
        

        user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('view_profile', name=user.username)

    return render(request, 'edit_profile.html', {'profile_user': profile_user})

@login_required
def invest(request, company_name):
    if request.user.role != 2:
        return HttpResponseForbidden("Only investors can invest.")
    
    company = get_object_or_404(User, username=company_name, role=1)
    request.user.investment_history.add(company)
    messages.success(request, f'You have successfully invested in {company.username}!')
    return redirect('view_profile', name=company_name)


# Regist, login

# ==== loginRegister ====

def getFirstName(username):
    if username:
        return username.split()[0]
    return ""

def getLastName(username):
    if username:
        return username.split()[-1]
    return ""

def loginRegisterView(request):
    
    if request.method == 'POST':
        # ===== LOGIN =====
        if 'login' in request.POST:
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(request, username=username, password=password)
            
       

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid login', extra_tags='login-error')
                return redirect('login')  

        # ===== REGISTER =====
        elif 'register' in request.POST:
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            role = request.POST.get('role')
            confirm_password = request.POST.get('confirmPassword')

            first_name = getFirstName(username)
            last_name = getLastName(username)

            user_data_has_error = False
            
            #password validation
            if password != confirm_password:
                messages.error(request, 'Passwords do not match', extra_tags='register-error')
                return redirect('register')
            
            # Role checking
            if not role:
                user_data_has_error = True
                messages.error(request, 'Please select a role (Company or Investor)')

            if User.objects.filter(username=username).exists():
                user_data_has_error = True
                messages.error(request, 'Username already exists', extra_tags='register-error')

            if User.objects.filter(email=email).exists():
                user_data_has_error = True
                messages.error(request, 'Email already exists', extra_tags='register- error')

            if len(password) < 5:
                user_data_has_error = True
                messages.error(request, 'Password must be at least 5 characters', extra_tags='register-error')

            if user_data_has_error:
                # Stay on register page with previous form data
                context = {
                    'username': username,
                    'email': email,
                    'role': role,
                }
                return render(request, 'loginRegister.html', context)
        
            # Create new user
            new_user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password=password
            )
        
            new_user.role = int(role)  # Assuming your User model has a `role` field
            new_user.save()

            messages.success(request, 'Account has been created. Please login.', extra_tags='register')
            return redirect('login')

    # GET request: just show login or register template
    return render(request, 'loginRegister.html') 



# def RegisterView(request):
#     if request.method == "POST":
#         first_name =  request.POST.get('first_name')
#         last_name = request.POST.get('last_name')
#         username = request.POST.get('username')
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         role = request.POST.get('role') # take value role from regist form

#         user_data_has_error = False

#         print("role : ", role)

#         #role checked
#         if not role:
#             user_data_has_error=True
#             messages.error(request, 'Please select a role (Company or Investor)')

#         if User.objects.filter(username=username).exists():
#             user_data_has_error=True
#             messages.error(request, 'Username already exists')

#         if User.objects.filter(email=email).exists():
#             user_data_has_error=True
#             messages.error(request, 'Email already exists')

#         if len(password) < 5 :
#             user_data_has_error=True
#             messages.error(request, 'Passowrd must be at leat 5 characters')

#         if user_data_has_error: # error stay in register
#             # Kirim data yang sudah diisi kembali ke template
#             context = {
#                 'first_name': first_name,
#                 'last_name': last_name,
#                 'username': username,
#                 'email': email,
#                 'role': role,
#             }
#             # return redirect('register') # based on name urls
#             return render(request, 'register.html', context)
#         else:
#             #new user 
#             new_user = User.objects.create_user(
#                 first_name = first_name,
#                 last_name = last_name,
#                 username=username,
#                 email=email,
#                 password=password
#             )
#             new_user.role = int(role) # set role to user

#             # if role not in ['1', '2']:
#             #     messages.error(request, 'Invalid role selected')
#             #     return redirect('register')
            
#             new_user.save() # save user to DB

#             messages.success(request, 'Account has been created. Please Login')
#             return redirect('login')

#     return render(request, 'register.html')


# def LoginView(request):
#     if request.method == "POST":
#         username = request.POST.get("username")
#         password = request.POST.get("password")

#         user = authenticate(request,  username=username, password=password)

#         if user is not None:
#             login(request, user)

#             return redirect('home')
#         else:
#             messages.error(request, 'Invalid login')
#             return redirect('login')

#     return render(request, 'login.html')

def LogoutView(request):
    logout(request)
    return redirect('login') # landing page


def ForgotPassword(request):
    if request.method == "POST":
        email = request.POST.get('email')

        try:
            user = User.objects.get(email=email)

            #create new reset_id
            new_password_reset = PasswordReset(user=user)
            new_password_reset.save()

            #create password reset url
            password_reset_url = reverse('reset-password', kwargs={'reset_id':new_password_reset.reset_id})

            full_password_reset_url = f'{request.scheme}://{request.get_host()}{password_reset_url}'

            #email content
            email_body = f'Reset your password using the link below: \n\n\n{full_password_reset_url}'            

            email_message= EmailMessage(
                'Reset your password', # email subject
                email_body,
                settings.EMAIL_HOST_USER, #email sender
                [email] #email receiver
            )

            email_message.fail_silently=True
            email_message.send()

            return redirect('password-reset-sent', reset_id=new_password_reset.reset_id)

        except User.DoesNotExist:
            messages.error(request, f"No user with email '{email}' found")
            return redirect('forgot-password') 
         
    return render(request, 'forgot_password.html')

def PasswordResetSent(request, reset_id):
    if PasswordReset.objects.filter(reset_id=reset_id).exists():
        return render(request, 'password_reset_sent.html')
    else:
        messages.error(request, 'Invalid reset id')
        return redirect('forgot-password')    

    # return render(request, 'password_reset_sent.html')

def ResetPassword(request, reset_id):
    try:
        password_reset_id = PasswordReset.objects.get(reset_id=reset_id)
        if request.method =="POST":
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            password_have_error = False

            if password != confirm_password:
                password_have_error=True
                messages.error(request, 'Password do not match')
                print("pass not match")
            
            if len(password) < 5:
                password_have_error=True
                messages.error(request, 'Password must at least 5 character')

            expiration_time = password_reset_id.created_when + timezone.timedelta(minutes=10)

            if timezone.now() > expiration_time:
                password_have_error = True
                messages.error(request, 'Reset link has expired')

                password_reset_id.delete()


            #password not error
            if not password_have_error:
                user = password_reset_id.user
                user.set_password(password)
                user.save()

                # delete reset id after use
                password_reset_id.delete()

                #redirect to login
                messages.success(request, 'Password reset. Procees to login')
                return redirect('login')
            else:
                #if error redirect to page reset pass
                return redirect('reset-password', reset_id=reset_id)


    except PasswordReset.DoesNotExist:
        messages.error(request, 'Invalid reset id')
        return redirect('forgot-password')

    return render(request, 'reset_password.html')


# views.py

from faker import Faker
from django.http import JsonResponse
import random

# Create your views here.

def add_fake_data(request):
    fake = Faker()

    categories = ['FnB', 'Jasa', 'Grosir', 'Peralatan Gudang', 'Dekorasi', 'Other']
    reputations = ['Basic', 'Intermediate', 'Professional']

    for _ in range(5):  # Generating 5 fake company
        while True:
            username = fake.company()
            if not User.objects.filter(username=username).exists():
                break

        User.objects.create_user(
            username = username,
            email=fake.company_email(),
            password= "password123",
            role=1, # role company
            category = random.choice(categories),
            reputation = random.choice(reputations)
        )

    for _ in range(5):  # Generating 5 fake investor
        while True:
            username=fake.name()
            if not User.objects.filter(username=username).exists():
                break
        User.objects.create_user(
            username = username,
            email=fake.email(),
            password= "password123",
            role=2, # role company
            # reputation = random.choice(reputations)
        )
    
    return JsonResponse({"message": "Fake data added successfully!"})
        # Student.objects.create(
        #     name=fake.name(),
        #     roll_number=fake.random_int(min=1000, max=9999),
        #     age=fake.random_int(min=15, max=18),
        #     grade=fake.random_element(elements=('A', 'B', 'C', 'D'))   

def show_fake_data(request):
    user = User.objects.all()
    template_name = "index.html"
    context = {"User": user}
    return render(request, template_name, context)

# Analitics in dashboard company -> recap analytics company 
@role_required([1]) # company
def analytics_dash_company(request):
    pass

# Analitics in dashboard investor -> recap best company 
@role_required([2]) # investor
def analytics_dash_investor(request):
    pass

# messages
# For login errors:

#<=============================================>
#Analytics
@login_required
def area_chart(request):
    return render(request, 'area_chart.html')

@login_required
def upload_csv(request):
    if request.method == 'POST':
        form = UploadCSVForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = form.cleaned_data['file']
            chart_type = form.cleaned_data['chart_type']

            # Baca isi CSV
            data = csv_file.read().decode('utf-8')
            df = pd.read_csv(io.StringIO(data))

            # Ambil label dan value dari kolom pertama dan kedua
            labels_list = df.iloc[:, 0].tolist()
            values_list = df.iloc[:, 1].tolist()

            # ⬇ Tambahkan kode ini di sini
            ChartData.objects.create(
                user=request.user,
                title='Chart {}'.format(datetime.now().strftime('%H:%M:%S')),
                labels=labels_list,
                values=values_list,
                chart_type=chart_type
            )
            return render(request, 'show_chart.html', {'chart_type': chart_type, 'csv_file': csv_file})
    else:
        form = UploadCSVForm()
    return render(request, 'upload.html', {'form': form})

@login_required
def delete_chart(request, chart_id):
    if request.method == 'POST':
        chart = get_object_or_404(ChartData, id=chart_id, user=request.user)
        chart.delete()
    return redirect('analyticIndex')

@login_required
def show_selected_charts(request):
    if request.method == 'POST':
        selected_ids = request.POST.getlist('selected_charts')
        charts = ChartData.objects.filter(id__in=selected_ids, user=request.user)

        # Simpan pilihan ke database (jika pakai model UserChartSelection)
        UserChartSelection.objects.filter(user=request.user).delete()
        for cid in selected_ids:
            UserChartSelection.objects.create(user=request.user, chart_id=cid)

        return render(request, 'selected_charts.html', {'charts': charts})
    return redirect('analytic.html')

@login_required
def analyticIndex(request):
    if request.method == 'POST':
        form = UploadCSVForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = form.cleaned_data['csv_file']
            chart_type = form.cleaned_data['chart_type']

            data = csv_file.read().decode('utf-8')
            df = pd.read_csv(io.StringIO(data))

            labels_list = df.iloc[:, 0].tolist()
            values_list = df.iloc[:, 1].tolist()

            ChartData.objects.create(
                user=request.user,
                title=form.cleaned_data['title'],
                labels=labels_list,
                values=values_list,
                chart_type=chart_type
            )

            return redirect('analyticIndex')
    else:
        form = UploadCSVForm()

    charts = ChartData.objects.filter(user=request.user).order_by('-created_at')
    selected_chart_ids = UserChartSelection.objects.filter(user=request.user).values_list('chart_id', flat=True)

    return render(request, 'BACKUP.html', {
        'form': form,
        'charts': charts,
        'selected_chart_ids': selected_chart_ids
    })