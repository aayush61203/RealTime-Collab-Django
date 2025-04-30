from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Task, Repository
from .forms import UserRegistrationForm,LoginForm,UserProfileForm,RepositoryForm
from django.contrib.auth.hashers import make_password, check_password
from .models import UserProfile,passwordToken
import random
from django.core.mail import send_mail  # Import the send_mail function

def index(request):
    return render(request, 'index.html')

def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})



from django.shortcuts import render
from .models import UserProfile

def admin_dashboard(request):
    admins = UserProfile.objects.filter(usertype="admin")
    managers = UserProfile.objects.filter(usertype="project_manager")
    users = UserProfile.objects.filter(usertype="user")
    projects = Project.objects.all()
    repos = Repository.objects.all()
    tasks = Task.objects.all()
    feeds = Feedback.objects.all()
    return render(request, 'admin_dashboard.html', {'admins':admins,'managers': managers,'users':users,'projects': projects,'repos':repos,'tasks':tasks,'feeds':feeds})

    
from django.shortcuts import render, get_object_or_404
from .models import Project
from django.contrib.auth.models import User

def project_manager_dashboard(request, i, un, n, e, ut, lp):
    user_projects = Project.objects.filter(assigned_to=i)
    project_ids = user_projects.values_list('id', flat=True)
    
    project_tasks = Task.objects.filter(project_id__in=project_ids)
    user = get_object_or_404(UserProfile, id=i)  # Assuming 'i' is the ID of the user
    repos = Repository.objects.all()
    projects = []
    if user.email == e and user.username == un:  # Checking if the user email and username match
        projects = Project.objects.filter(assigned_to=user)
    
    return render(request, 'project_manager_dashboard.html', {'project_tasks': project_tasks,'repos': repos,
        'projects': projects,
        'i': i,
        'un': un,
        'n': n,
        'e': e,
        'ut': ut,
        'lp': lp
    })


def user_dashboard(request,i,un,n,e,ut,lp):
    cc = Collaborator.objects.filter(created_by=i)
    ac = Collaborator.objects.filter(assigned_to=i)
    user_tasks = Task.objects.filter(assigned_to=i)  # Adjust the filter according to your model structure
    user = get_object_or_404(UserProfile, id=i)  # Assuming 'i' is the ID of the user
    repos = []
    if user.email == e and user.username == un:  # Checking if the user email and username match
        repos = Repository.objects.filter(assigned_to=user)
    return render(request,'user_dashboard.html',{'cc':cc,'ac':ac,'user_tasks': user_tasks,'repos': repos,'i':i,'un':un,'n':n,'e':e,'ut':ut,'lp':lp})

def login_user(request):
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            try:
                user = UserProfile.objects.get(username=username)
                
                if check_password(password, user.password):
                    if user.usertype == 'admin':
                        return redirect('admin_dashboard')
                        
                    elif user.usertype == 'project_manager':
                        i=user.id
                        un=user.username
                        n=user.name
                        e=user.email
                        ut=user.usertype
                        lp=user.language_preference
                        return redirect('project_manager_dashboard',i=i,un=un,n=n,e=e,ut=ut,lp=lp)
                        
                    else:
                        i=user.id
                        un=user.username
                        n=user.name
                        e=user.email
                        ut=user.usertype
                        lp=user.language_preference
                        return redirect('user_dashboard',i=i,un=un,n=n,e=e,ut=ut,lp=lp)
                    
                else:
                    messages.error(request, 'Invalid password')
            except UserProfile.DoesNotExist:
                messages.error(request, 'User does not exist')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('index')

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from .models import UserProfile
from .forms import UserProfileForm_admin  # Ensure you have created this form as mentioned earlier

def edit_profile_admin(request, username):
    user_profile = get_object_or_404(UserProfile, username=username)
    
    if request.method == 'POST':
        form = UserProfileForm_admin(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            # Redirect to a success page or user profile page
            return redirect('admin_dashboard')
    else:
        form = UserProfileForm_admin(instance=user_profile)
    
    return render(request, 'editprofile.html', {'form': form})

from django.shortcuts import get_object_or_404, redirect
from .models import UserProfile

def delete_profile_admin(request, username):
    user_profile = get_object_or_404(UserProfile, username=username)
    
    if request.method == 'POST':
        user_profile.delete()
        return redirect('admin_dashboard')
    return render(request, 'confirm_delete_profile.html', {'user_profile': user_profile})


def edit_profile_manager(request,id):
    data = UserProfile.objects.get(pk=id)
    
    un = data.username
    if request.method == "POST":
        form = UserProfileForm(request.POST,instance=data)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Profile Updated Successfully.")
            i=user.id
            un=user.username
            n=user.name
            e=user.email
            ut=user.usertype
            lp=user.language_preference
            return redirect('project_manager_dashboard',i=i,un=un,n=n,e=e,ut=ut,lp=lp)

    else:
        form = UserProfileForm(instance=data)
    return render(request, 'editprofile.html', {'form': form, 'form_title': 'Edit Profile','un':un})
    
def edit_profile_user(request,id):
    data = UserProfile.objects.get(pk=id)
    
    un = data.username
    if request.method == "POST":
        form = UserProfileForm(request.POST,instance=data)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Profile Updated Successfully.")
            i=user.id
            un=user.username
            n=user.name
            e=user.email
            ut=user.usertype
            lp=user.language_preference
            return redirect('user_dashboard',i=i,un=un,n=n,e=e,ut=ut,lp=lp)

    else:
        form = UserProfileForm(instance=data)
    return render(request, 'editprofile.html', {'form': form, 'form_title': 'Edit Profile','un':un})

from django.contrib.auth.hashers import make_password
import pandas as pd
from .models import UserProfile

def bulk_upload_from_excel(file_path):
    try:
        # Load Excel file into a pandas DataFrame
        excel_data = pd.read_excel(file_path)

        # Iterate through each row in the DataFrame and create UserProfile instances
        for index, row in excel_data.iterrows():
            username = row['username']
            name = row['name']
            email = row['email']
            raw_password = row['password']  # Retrieve the raw password from the Excel file
            usertype = row['usertype']
            language_preference = row['language_preference']

            # Hash the password using Django's make_password function
            hashed_password = make_password(raw_password)

            # Create UserProfile instance with hashed password
            UserProfile.objects.create(
                username=username,
                name=name,
                email=email,
                password=hashed_password,
                usertype=usertype,
                language_preference=language_preference
            )
        
        # Return success message or handle completion
        return "Bulk upload completed successfully!"
    
    except Exception as e:
        # Handle exceptions such as file not found, incorrect data, etc.
        return f"Error during bulk upload: {str(e)}"


from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import ExcelUploadForm  # Create a form for file upload

def bulk_upload_view(request):
    if request.method == 'POST':
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            # Process the file using the previously defined bulk_upload_from_excel function
            result_message = bulk_upload_from_excel(file)
            return HttpResponse('<script>window.close();</script>')  # Return JavaScript to close the window
    else:
        form = ExcelUploadForm()

    return render(request, 'bulkUpload.html', {'form': form})

from django.contrib.auth.models import User
from .models import UserProfile, Feedback
from .forms import FeedbackForm

def feedback_view(request, id):
    try:
        user_profile = UserProfile.objects.get(pk=id)
    except UserProfile.DoesNotExist:
        # Handle case where UserProfile with the provided ID doesn't exist
        # You might want to return an error or redirect to an error page
        pass

    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.username = user_profile.name
            feedback.email = user_profile.email
            feedback.save()

            # Sending email to admin
            admin_email = 'rtct.site@gmail.com'  # Replace with your admin's email
            subject = 'Feedback Received'
            message = f"Name : {user_profile.name}\nEmail : {user_profile.email}\nDescription : {feedback.message}"  # Assuming description is a field in the Feedback model
            sender_email = user_profile.email

            send_mail(subject, message, sender_email, [admin_email], fail_silently=False)

            i = user_profile.id
            un = user_profile.username
            n = user_profile.name
            e = user_profile.email
            ut = user_profile.usertype
            lp = user_profile.language_preference
            return redirect('user_dashboard', i=i, un=un, n=n, e=e, ut=ut, lp=lp)
    else:
        form = FeedbackForm()
    
    return render(request, 'feedback_form.html', {'form': form})



from django.shortcuts import render, get_object_or_404, redirect
from .models import Collaborator
from .forms import CollaboratorForm 


def create_collaborator(request,id):
    user = UserProfile.objects.get(id=id)
    i = user.id  # Get the user ID
    un=user.username
    n=user.name
    e=user.email
    ut=user.usertype
    lp=user.language_preference
    if request.method == 'POST':
        form = CollaboratorForm(user_id=i, data=request.POST)
        if form.is_valid():
            collaborator = form.save(commit=False)
            collaborator.created_by = user  # Set the created_by field to the user
            collaborator.save()
            return redirect('user_dashboard',i=i,un=un,n=n,e=e,ut=ut,lp=lp)
    else:
        form = CollaboratorForm(user_id=i)
    return render(request, 'collaborators/collaborator_form.html', {'form': form})

from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from .models import Task
from .forms import TaskForm

def update_collab(request, pk, username):
    collab = get_object_or_404(Collaborator, pk=pk)
    # Fetching user details based on the username
    try:
        user = UserProfile.objects.get(username=username)
        i=user.id
        un=user.username
        n=user.name
        e=user.email
        ut=user.usertype
        lp=user.language_preference
        if request.method == 'POST':
            form = CollaboratorForm(user_id=i, data=request.POST, instance=collab)
            if form.is_valid():
                form.save()
                return redirect('user_dashboard',i=i,un=un,n=n,e=e,ut=ut,lp=lp)
        else:
            form = CollaboratorForm(user_id=i, instance=collab)
        
        return render(request, 'collaborators/update_collaborator.html', {'form': form, 'collab': collab})
    
    except User.DoesNotExist:
        pass


from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from .models import Task
from .forms import CollaboratorForm_user

def update_collab_user(request, pk, username):
    collab = get_object_or_404(Collaborator, pk=pk)
    
    # Fetching user details based on the username
    try:
        user = UserProfile.objects.get(username=username)
        i=user.id
        un=user.username
        n=user.name
        e=user.email
        ut=user.usertype
        lp=user.language_preference
        if request.method == 'POST':
            form = CollaboratorForm_user(request.POST, request.FILES, instance=collab)
            if form.is_valid():
                form.save()
                return redirect('user_dashboard',i=i,un=un,n=n,e=e,ut=ut,lp=lp)
        else:
            form = CollaboratorForm_user(instance=collab)
        
        return render(request, 'collaborators/update_collaborator.html', {'form': form, 'collab': collab})
    except User.DoesNotExist:
        pass


from django.shortcuts import get_object_or_404, redirect

def delete_collab(request, pk, username):
    collab = get_object_or_404(Collaborator, pk=pk)
    user = UserProfile.objects.get(username=username)
    i=user.id
    un=user.username
    n=user.name
    e=user.email
    ut=user.usertype
    lp=user.language_preference
    if request.method == 'POST':
        collab.delete()
        return redirect('user_dashboard',i=i,un=un,n=n,e=e,ut=ut,lp=lp)
    return render(request, 'collaborators/confirm_delete.html', {'collab': collab})


from django.shortcuts import render, redirect
from .forms import TaskForm

def create_task_view(request,username):
    user = UserProfile.objects.get(username=username)
    i = user.id  # Get the user ID
    un=user.username
    n=user.name
    e=user.email
    ut=user.usertype
    lp=user.language_preference
    if request.method == 'POST':
        form = TaskForm(user_id=i, data=request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = user  # Set the created_by field to the user
            task.save()
            #form.save()
            return redirect('project_manager_dashboard',i=i,un=un,n=n,e=e,ut=ut,lp=lp)
    else:
        form = TaskForm(user_id=i)
    
    return render(request, 'task/task_create.html', {'form': form})

from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from .models import Task
from .forms import TaskForm

def update_task(request, pk, username):
    task = get_object_or_404(Task, pk=pk)
    # Fetching user details based on the username
    try:
        user = UserProfile.objects.get(username=username)
        i=user.id
        un=user.username
        n=user.name
        e=user.email
        ut=user.usertype
        lp=user.language_preference
        if request.method == 'POST':
            #form = TaskForm(request.POST, request.FILES, instance=task)
            form = TaskForm(user_id=i, data=request.POST, instance=task)
            if form.is_valid():
                form.save()
                return redirect('project_manager_dashboard',i=i,un=un,n=n,e=e,ut=ut,lp=lp)
        else:
            form = TaskForm(user_id=i, instance=task)
        
        return render(request, 'task/update_task.html', {'form': form, 'task': task})
    
    except User.DoesNotExist:
        # Handle the case where the user is not found
        pass


from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from .models import Task
from .forms import TaskUpdateForm_user

def update_task_user(request, pk, username):
    task = get_object_or_404(Task, pk=pk)
    
    # Fetching user details based on the username
    try:
        user = UserProfile.objects.get(username=username)
        i=user.id
        un=user.username
        n=user.name
        e=user.email
        ut=user.usertype
        lp=user.language_preference
        if request.method == 'POST':
            form = TaskUpdateForm_user(request.POST, request.FILES, instance=task)
            if form.is_valid():
                form.save()
                return redirect('user_dashboard',i=i,un=un,n=n,e=e,ut=ut,lp=lp)
        else:
            form = TaskUpdateForm_user(instance=task)
        
        return render(request, 'task/update_task.html', {'form': form, 'task': task})
    
    except User.DoesNotExist:
        # Handle the case where the user is not found
        pass


from django.shortcuts import get_object_or_404, redirect

def delete_task(request, pk, username):
    task = get_object_or_404(Task, pk=pk)
    user = UserProfile.objects.get(username=username)
    i=user.id
    un=user.username
    n=user.name
    e=user.email
    ut=user.usertype
    lp=user.language_preference
    if request.method == 'POST':
        task.delete()
        return redirect('project_manager_dashboard',i=i,un=un,n=n,e=e,ut=ut,lp=lp)
    return render(request, 'task/delete_task.html', {'task': task})


from django.http import HttpResponse

def generate_text_report_task(request):
    tasks = Task.objects.all()
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="task_report.txt"'

    for task in tasks:
        response.write(f"ID: {task.id}\n")
        response.write(f"Name: {task.name}\n")
        response.write(f"Description: {task.description}\n")
        response.write(f"Project: {task.project.title if task.project else 'N/A'}\n")
        response.write(f"Assigned to: {task.assigned_to.username if task.assigned_to else 'N/A'}\n")
        response.write(f"Priority: {dict(Task.PRIORITY_CHOICES)[task.priority]}\n")
        response.write(f"Completed: {dict(Task.COMPLETED_CHOICES)[task.completed]}\n")
        response.write(f"Created By: {task.created_by.username if task.created_by else 'N/A'}\n")
        response.write("----------------------\n")
	
    return response

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle,Paragraph
from django.http import HttpResponse
from io import BytesIO

def generate_pdf_report_task(request):
    tasks = Task.objects.all()
    buffer = BytesIO()
    pdf = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    # Title
    title_style = getSampleStyleSheet()["Title"]
    title = title_style.clone("Title")
    title.alignment = 1  # Center alignment
    elements.append(Paragraph("TASK REPORT", title))

    # Table Header
    table_data = [
        ["Name", "Description", "Project", "Assigned to", "Priority", "Completed", "Created By"]
    ]

    for task in tasks:
        table_data.append([
            task.name,
            task.description,
            task.project.title if task.project else 'N/A',
            task.assigned_to.username if task.assigned_to else 'N/A',
            dict(Task.PRIORITY_CHOICES)[task.priority],
            dict(Task.COMPLETED_CHOICES)[task.completed],
            task.created_by.username if task.created_by else 'N/A'
        ])

    # Table Style
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),  # Header background color
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),  # Header text color
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center alignment for cells
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Header font style
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Bottom padding for header cells
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),  # Alternate row background color
    ])

    table = Table(table_data)
    table.setStyle(table_style)
    elements.append(table)

    pdf.build(elements)

    buffer.seek(0)

    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="task_report.pdf"'
    return response

from openpyxl import Workbook
from openpyxl.styles import Font
from django.http import HttpResponse

def generate_excel_report_task(request):
    tasks = Task.objects.all()

    # Create a new workbook and select the active sheet
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = 'Task Report'

    # Add header row
    header = ["Name", "Description", "Project", "Assigned to", "Priority", "Completed", "Created By"]
    sheet.append(header)

    header_cells = sheet[1]
    for cell in header_cells:
        cell.font = Font(bold=True)
    # Add data rows
    for task in tasks:
        row = [
            task.name,
            task.description,
            task.project.title if task.project else 'N/A',
            task.assigned_to.username if task.assigned_to else 'N/A',
            dict(Task.PRIORITY_CHOICES)[task.priority],
            dict(Task.COMPLETED_CHOICES)[task.completed],
            task.created_by.username if task.created_by else 'N/A'
        ]
        sheet.append(row)

    # Create the HTTP response
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="task_report.xlsx"'

    # Save the workbook to the response
    workbook.save(response)
    return response

import csv
from django.http import HttpResponse

def generate_csv_report_task(request):
    tasks = Task.objects.all()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="task_report.csv"'

    # Create a CSV writer
    csv_writer = csv.writer(response)
    
    # Write header row
    header = ["Name", "Description", "Project", "Assigned to", "Priority", "Completed", "Created By"]
    csv_writer.writerow(header)

    # Write data rows
    for task in tasks:
        row = [
            task.name,
            task.description,
            task.project.title if task.project else 'N/A',
            task.assigned_to.username if task.assigned_to else 'N/A',
            dict(Task.PRIORITY_CHOICES)[task.priority],
            dict(Task.COMPLETED_CHOICES)[task.completed],
            task.created_by.username if task.created_by else 'N/A'
        ]
        csv_writer.writerow(row)

    return response



from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RepositoryForm

def repository_create(request):
    if request.method == 'POST':
        form = RepositoryForm(request.POST, request.FILES)
        if form.is_valid():
            repository = form.save()
            messages.success(request, f"Repository '{repository.name}' created successfully!")
            return HttpResponse('<script>window.close();</script>')  # Return JavaScript to close the window
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RepositoryForm()
    
    return render(request, 'repository/repository_form.html', {'form': form})

# views.py
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from .models import Repository

def update_repository(request, pk, username):
    repository = get_object_or_404(Repository, pk=pk)
    
    # Fetching user details based on the username
    try:
        user = UserProfile.objects.get(username=username)
        i=user.id
        un=user.username
        n=user.name
        e=user.email
        ut=user.usertype
        lp=user.language_preference
        if request.method == 'POST':
            form = RepositoryForm(request.POST, request.FILES, instance=repository)
            if form.is_valid():
                form.save()
                return redirect('project_manager_dashboard',i=i,un=un,n=n,e=e,ut=ut,lp=lp)
        else:
            form = RepositoryForm(instance=repository)
        
        return render(request, 'repository/update_repository.html', {'form': form, 'repository': repository})
    
    except User.DoesNotExist:
        # Handle the case where the user is not found
        pass


from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from .models import Repository
from .forms import RepositoryUpdateForm_user

def update_repository_user(request, pk, username):
    repository = get_object_or_404(Repository, pk=pk)
    
    # Fetching user details based on the username
    try:
        user = UserProfile.objects.get(username=username)
        i=user.id
        un=user.username
        n=user.name
        e=user.email
        ut=user.usertype
        lp=user.language_preference
        if request.method == 'POST':
            form = RepositoryUpdateForm_user(request.POST, request.FILES, instance=repository)
            if form.is_valid():
                form.save()
                return redirect('user_dashboard',i=i,un=un,n=n,e=e,ut=ut,lp=lp)
        else:
            form = RepositoryUpdateForm_user(instance=repository)
        
        return render(request, 'repository/update_repository.html', {'form': form, 'repository': repository})
    
    except User.DoesNotExist:
        # Handle the case where the user is not found
        pass


from django.shortcuts import get_object_or_404, redirect

def delete_repository(request, pk, username):
    repository = get_object_or_404(Repository, pk=pk)
    user = UserProfile.objects.get(username=username)
    i=user.id
    un=user.username
    n=user.name
    e=user.email
    ut=user.usertype
    lp=user.language_preference
    if request.method == 'POST':
        repository.delete()
        return redirect('project_manager_dashboard',i=i,un=un,n=n,e=e,ut=ut,lp=lp)
    return render(request, 'repository/delete_repository.html', {'repository': repository})


from django.http import FileResponse

def serve_file(request, file_path):
    # Logic to retrieve the file based on file_path
    # Ensure to set appropriate content-type headers
    file = open(file_path, 'rb')
    return FileResponse(file)


def forgotpwdPage(request):
    return render(request, "forgotpwd.html")

def OTP_generate():
    return str(random.randint(100000, 999999))

def reset_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        print(email)

        user = UserProfile.objects.filter(email=email).first()
        if user:
            otp = OTP_generate()
            user = UserProfile.objects.get(email=email)

            # Use .first() to get the first passwordToken if multiple are found
            token = passwordToken.objects.filter(email=user.email).first()
            if token:
                token.otp = otp
            else:
                token = passwordToken.objects.create(email=user.email, otp=otp)
            token.save()
            print("Generated OTP:", otp)

            subject = "OTP for resetting the password"
            message = f"Please verify and check the OTP for resetting the password: {otp}"
            from_email = "rtct.site@gmail.com"
            recipients = [user.email]

            send_mail(subject, message, from_email, recipients)

            return render(request, 'otp.html', {'email': user.email})
        else:
            msg = "Provide a valid email address"
            return HttpResponse("Email does not exist!!")


def verify_otp(request, email):
    if request.method == 'POST':
        otp_entered = request.POST.get('otp')
        user = passwordToken.objects.filter(email=email).first()
        if user:
            print("Entered OTP:", otp_entered)
            print("Stored OTP:", user.otp)
            if user.otp == otp_entered:
                print("OTP matched")
                user.delete()
                return render(request, 'resetpwd.html', {'email': email})
            else:
                return HttpResponse("Entered OTP is not valid!! Try again")
        else:
            return HttpResponse("User not found")


def new_password(request, email):
    if request.method == 'POST':
        password = request.POST.get('password')
        user = UserProfile.objects.filter(email=email).first()
        if user:
            pwd = make_password(password)
            chnge = UserProfile.objects.filter(email=user.email).update(password=pwd)

            if chnge:
                passwordToken.objects.filter(email=email).delete()
                #return HttpResponse("Password changed")
                return redirect('login')
            else:
                return HttpResponse("Unable to reset password")
        else:
            return HttpResponse("User not found")

def update_profile(request):
    if request.method == 'POST':
        username = request.POST.get('username')  # Get the username from the form
        user = get_object_or_404(UserProfile, username=username)
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            # Redirect to the user's profile page after the update
            return redirect('user_profile', username=username)
    else:
        # Render the update form initially
        form = UserProfileForm()
    
    return render(request, 'update_profile.html', {'form': form})


# views.py

from django.shortcuts import render, get_object_or_404, redirect
from .models import Project
from .forms import ProjectForm

# Create
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save()
            #return redirect('project_detail', project_id=project.id)
            return HttpResponse('<script>window.close();</script>')  # Return JavaScript to close the window
    else:
        form = ProjectForm()
    return render(request, 'project/admin/project_create.html', {'form': form})

# Update
def project_update(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
           # return redirect('project_detail', project_id=project.id)
            return redirect('admin_dashboard')
    else:
        form = ProjectForm(instance=project)
    return render(request, 'project/admin/project_update.html', {'form': form})

# Delete
def project_delete(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        project.delete()
        #return redirect('project_list')
        return redirect('admin_dashboard')
    return render(request, 'project/admin/project_delete.html', {'project': project})

# views.py

from django.shortcuts import get_object_or_404, redirect
from .models import Project

def update_project_status(request, project_id, username):
    user = UserProfile.objects.get(username=username)
    i=user.id
    un=user.username
    n=user.name
    e=user.email
    ut=user.usertype
    lp=user.language_preference
    if request.method == 'POST':
        new_status = request.POST.get('new_status')
        project = get_object_or_404(Project, pk=project_id)

        if new_status in dict(Project.STATUS_CHOICES).keys():
            project.status = new_status
            project.save()

    return redirect('project_manager_dashboard',i=i,un=un,n=n,e=e,ut=ut,lp=lp)
