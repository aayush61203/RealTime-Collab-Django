from django.db import models


class UserProfile(models.Model):
    LANGUAGE_CHOICES = (
        ('python', 'Python'),
        ('javascript', 'JavaScript'),
        ('java', 'Java'),
        ('csharp', 'C#'),
        ('ruby', 'Ruby'),
        ('php', 'PHP'),
        ('other', 'Other'),
    )
    username = models.CharField(max_length=100, unique=True, null=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100, null=True)
    usertype = models.CharField(max_length=20, choices=[('admin', 'Admin'), ('project_manager', 'Project Manager'), ('user', 'User')],default='user')
    language_preference = models.CharField(max_length=30, choices=LANGUAGE_CHOICES, default='python')

    def __str__(self):
        return self.username    
    
    def createProfile(sender, **kwargs):
            if kwargs['created']:
                user_profile = UserProfile.objects.created(user=kwargs['instance'])
                post_save.connect(createProfile, sender=UserProfile)
    

class ProjectManagerUserManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(user_type='project_manager')


class passwordToken(models.Model):
    email = models.EmailField(max_length=30)
    otp = models.CharField(max_length=8, unique=False)
    timestamp = models.DateTimeField(auto_now_add=True)


from django.db import models
class Feedback(models.Model):
    username = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    message = models.TextField(null=True)

    def save(self, *args, **kwargs):
        if not self.pk:  # Check if the instance is being created
            user = kwargs.pop('user', None)  # Retrieve the user from kwargs
            if user:
                self.username = user.username
                self.email = user.email
        super(Feedback, self).save(*args, **kwargs)


from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    assigned_to = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    needs_approval = models.BooleanField(default=True)  # Example of adding a needs_approval field

    def __str__(self):
        return self.title


from django.db import models
from distutils.command.upload import upload
import email

class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE,null=True)
    assigned_to = models.ForeignKey(UserProfile, on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=100,null=True)
    description = models.TextField()

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    COMPLETED_CHOICES = [
        ('completed', 'Completed'),
        ('incompleted', 'Incomplete'),
    ]
    completed = models.CharField(max_length=20, choices=COMPLETED_CHOICES,default='incompleted')
    created_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='created_tasks', null=True, editable=False)
    def save(self, *args, **kwargs):
        if not self.pk:  # Check if the Task is being created
            user = kwargs.pop('user', None)  # Retrieve the user from kwargs
            if user:
                self.created_by = user
        super(Task, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - Assigned to: {self.assigned_to.username} - Project: {self.project.title}"



from django.db import models

class Collaborator(models.Model):
    created_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='created_collaborator', null=True, editable=False)
    description = models.TextField(null=True)
    assigned_to = models.ForeignKey(UserProfile, on_delete=models.CASCADE,null=True)
    def save(self, *args, **kwargs):
        if not self.pk:  # Check if the Task is being created
            user = kwargs.pop('user', None)  # Retrieve the user from kwargs
            if user:
                self.created_by = user
        super(Collaborator, self).save(*args, **kwargs)
    



from django.db import models
from django.contrib.auth.models import User
import os
from django.db import models

class Repository(models.Model):
    name = models.CharField(max_length=100,blank=True)
    description = models.TextField()
    assigned_to = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, blank=True, related_name='assigned_repositories', null=True)
    upload_file = models.FileField(upload_to='repository_files/', blank=True, null=True)
    full_file_path = models.CharField(max_length=300, blank=True)
    
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.upload_file:
            self.full_file_path = os.path.abspath(self.upload_file.path)  # Get the absolute file path
            super().save(*args, **kwargs)  # Save again to update the full_file_path field