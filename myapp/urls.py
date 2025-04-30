from django.urls import path
from . import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    path('admin_dashboard/',views.admin_dashboard, name='admin_dashboard'),
    path('project_manager_dashboard/<str:i>/<str:un>/<str:n>/<str:e>/<str:ut>/<str:lp>/',views.project_manager_dashboard, name='project_manager_dashboard'),
    path('user_dashboard/<str:i>/<str:un>/<str:n>/<str:e>/<str:ut>/<str:lp>/', views.user_dashboard, name='user_dashboard'),
   
    path('edit-profile-admin/<str:username>/', views.edit_profile_admin, name='edit_profile_admin'),
    path('delete-profile-admin/<str:username>/', views.delete_profile_admin, name='delete_profile_admin'),
    path('edit-profile-user/<id>', views.edit_profile_user, name='edit_profile_user'),
    path('edit-profile-manager/<id>', views.edit_profile_manager, name='edit_profile_manager'),
    path('bulk_upload/', views.bulk_upload_view, name='bulk_upload'),
    
    path("reset/", views.reset_password,  name="reset_password"),
    path("forgotpassword/", views.forgotpwdPage, name="forgotpassword"),
    path("verify_otp/<str:email>", views.verify_otp, name="verify_otp"),
    path("newpassword/<str:email>", views.new_password, name="newpassword"),

    path('feedback/<id>', views.feedback_view, name='feedback'),

    path('task/create/<str:username>/', views.create_task_view, name='create_task'),
    path('update_task/<int:pk>/<str:username>/', views.update_task, name='update_task'),
    path('update_task_user/<int:pk>/<str:username>/', views.update_task_user, name='update_task_user'),
    path('delete_task/<int:pk>/<str:username>/', views.delete_task, name='delete_task'),
    path('generate_text_report_task/',views.generate_text_report_task, name='generate_text_report_task'),
    path('generate_pdf_report_task/',views.generate_pdf_report_task, name='generate_pdf_report_task'),
    path('generate_excel_report_task/',views.generate_excel_report_task, name='generate_excel_report_task'),
    path('generate_csv_report_task/',views.generate_csv_report_task, name='generate_csv_report_task'),

    path('repository/new/', views.repository_create, name='repository_create'),
    path('update_repository_user/<int:pk>/<str:username>/', views.update_repository_user, name='update_repository_user'),
    path('update_repository/<int:pk>/<str:username>/', views.update_repository, name='update_repository'),
    path('delete_repository/<int:pk>/<str:username>/', views.delete_repository, name='delete_repository'),
    path('serve_file/<path:file_path>/', views.serve_file, name='serve_file'),

    path('projects/create/', views.project_create, name='project_create'),
    path('projects/update/<int:project_id>/', views.project_update, name='project_update'),
    path('projects/delete/<int:project_id>/', views.project_delete, name='project_delete'),
    path('update_status/<int:project_id>/<str:username>/', views.update_project_status, name='update_project_status'),
    
    path('collaborators/create/<id>', views.create_collaborator, name='create_collaborator'),
    path('collaborators/edit/<int:pk>/<str:username>/', views.update_collab, name='edit_collaborator'),
    path('collaborators/edit_user/<int:pk>/<str:username>/', views.update_collab_user, name='edit_collaborator_user'),
    path('collaborators/delete/<int:pk>/<str:username>/', views.delete_collab, name='delete_collaborator'),

]


