from django import forms

from .models import UserProfile

class UserRegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = UserProfile
        fields = ['username', 'name', 'email', 'password', 'confirm_password', 'usertype', 'language_preference']
        widgets = {
            'password': forms.PasswordInput(),
        }

# forms.py
from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, required=True)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput, required=True)

from django import forms
from .models import UserProfile

class UserProfileForm_admin(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ['password']  # Exclude the password field from the form


from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['name', 'email', 'language_preference']

from django import forms

class ExcelUploadForm(forms.Form):
    file = forms.FileField()

from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['message']  # Specify the fields you want to include in the form


from .models import Task
class TaskForm(forms.ModelForm):
    def __init__(self, user_id, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        
        if user_id:
            # Filter the queryset for 'project' based on the user ID
            self.fields['project'].queryset = Project.objects.filter(assigned_to=user_id)

            # Filter the queryset for 'assigned_to' based on usertype='user'
            self.fields['assigned_to'].queryset = UserProfile.objects.filter(usertype='user')

    class Meta:
        model = Task
        fields = ['project', 'assigned_to', 'name', 'description', 'priority', 'completed']

from django import forms
from .models import Task

class TaskUpdateForm_user(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['completed']


from django import forms
from django.contrib.auth.models import User
from .models import Collaborator, UserProfile

class CollaboratorForm(forms.ModelForm):
    def __init__(self,user_id, *args, **kwargs):
        user = kwargs.pop('user', None)  # Retrieve the user from kwargs
        super(CollaboratorForm, self).__init__(*args, **kwargs)
    
        if user_id:
            self.fields['assigned_to'].queryset = UserProfile.objects.filter(usertype='user').exclude(id=user_id)

    class Meta:
        model = Collaborator
        fields = ['assigned_to', 'description']

class CollaboratorForm_user(forms.ModelForm):
    class Meta:
        model = Collaborator
        fields = ['description']


from django import forms
from django.contrib.auth.forms import PasswordChangeForm

class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput)
    new_password1 = forms.CharField(widget=forms.PasswordInput)
    new_password2 = forms.CharField(widget=forms.PasswordInput)
    


from django import forms
from .models import Project
from django.contrib.auth.models import User

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'assigned_to', 'status']

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.fields['assigned_to'].queryset = UserProfile.objects.filter(usertype='project_manager')


from django import forms
from .models import Project

class ProjectStatusForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['status']

from django import forms
from .models import Repository, UserProfile

class RepositoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RepositoryForm, self).__init__(*args, **kwargs)

        # Filter users by usertype 'user'
        # self.fields['assigned_to'].queryset = UserProfile.objects.filter(usertype='user').values_list('user', flat=True)
        self.fields['assigned_to'].queryset = UserProfile.objects.filter(usertype='user')
    class Meta:
        model = Repository
        fields = ['name', 'description', 'assigned_to', 'upload_file']
    

# from django import forms
# from .models import Repository

# class RepositoryUpdateForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super(RepositoryForm, self).__init__(*args, **kwargs)

#         # Filter users by usertype 'user'
#         # self.fields['assigned_to'].queryset = UserProfile.objects.filter(usertype='user').values_list('user', flat=True)
#         self.fields['assigned_to'].queryset = UserProfile.objects.filter(usertype='user')
#     class Meta:
#         model = Repository
#         fields = ['name', 'description', 'assigned_to', 'upload_file']


from django import forms
from .models import Repository

class RepositoryUpdateForm_user(forms.ModelForm):
    class Meta:
        model = Repository
        fields = ['upload_file']