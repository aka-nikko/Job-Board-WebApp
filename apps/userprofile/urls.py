from django.urls import path, include

from .views import dashboard, list_jobs, view_application, view_dashboard_job, view_applied

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('list_jobs', list_jobs, name='list_jobs'),
    path('view_applied', view_applied, name='view_applied'),
    path('job/<int:job_id>/', view_dashboard_job, name='view_dashboard_job'),
    path('application/<int:application_id>/', view_application, name='view_application'),
]