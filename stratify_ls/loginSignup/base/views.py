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


from django.http import HttpResponse

#based on ROLES
from .decorators import role_required # add @role_required([1]) -> company

#admin account superuser
# user name : grace
# password : 1

@login_required
def Home(request):
    add_fake_data(request)

    # take param main search
    search_query = request.GET.get('search', '')
    companies, investors = search_user(search_query)

    #filter
    role_filter = request.GET.get('role', '')
    category_filter = request.GET.get('category', '')
    reputation_filter = request.GET.get('reputation', '')

    print(f"Search Query: {search_query}")
    print(f"Role Filter: {role_filter}")
    print(f"Category Filter: {category_filter}")
    print(f"Reputation Filter: {reputation_filter}")

    if role_filter == 'Company':
        investors=investors.none() #investor empty
    elif role_filter == 'Investor':
        companies = companies.none() # company empty

    if category_filter or reputation_filter:
        investors = investors.none()
        if category_filter:
            companies = companies.filter(category__icontains=category_filter)

        if reputation_filter:
            companies = companies.filter(reputation__icontains=reputation_filter)

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
def view_profile(request, user_id):
    if request.method == 'POST':
        user_id = request.POST.get('id')  # Ambil ID dari POST data
        user = get_object_or_404(User, id=user_id)
        return render(request, 'profile.html', {'user': user})
    return render(request, 'profile.html')

@login_required
def MyActivities(request):
    return render(request, 'my_activities.html')

@login_required
def Messages(request):
    return render(request, 'messages.html')

# Regist, login

def RegisterView(request):
    if request.method == "POST":
        first_name =  request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role') # take value role from regist form

        user_data_has_error = False

        print("role : ", role)

        #role checked
        if not role:
            user_data_has_error=True
            messages.error(request, 'Please select a role (Company or Investor)')

        if User.objects.filter(username=username).exists():
            user_data_has_error=True
            messages.error(request, 'Username already exists')

        if User.objects.filter(email=email).exists():
            user_data_has_error=True
            messages.error(request, 'Email already exists')

        if len(password) < 5 :
            user_data_has_error=True
            messages.error(request, 'Passowrd must be at leat 5 characters')

        if user_data_has_error: # error stay in register
            # Kirim data yang sudah diisi kembali ke template
            context = {
                'first_name': first_name,
                'last_name': last_name,
                'username': username,
                'email': email,
                'role': role,
            }
            # return redirect('register') # based on name urls
            return render(request, 'register.html', context)
        else:
            #new user 
            new_user = User.objects.create_user(
                first_name = first_name,
                last_name = last_name,
                username=username,
                email=email,
                password=password
            )
            new_user.role = int(role) # set role to user

            # if role not in ['1', '2']:
            #     messages.error(request, 'Invalid role selected')
            #     return redirect('register')
            
            new_user.save() # save user to DB

            messages.success(request, 'Account has been created. Please Login')
            return redirect('login')

    return render(request, 'register.html')

def LoginView(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request,  username=username, password=password)

        if user is not None:
            login(request, user)

            return redirect('home')
        else:
            messages.error(request, 'Invalid login')
            return redirect('login')

    return render(request, 'login.html')

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