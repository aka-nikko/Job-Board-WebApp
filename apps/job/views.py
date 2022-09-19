from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .forms import AddJobForm, ApplicationForm
from .models import Job

from apps.notification.utilities import create_notification

def search(request):
    jobs = Job.objects.all().order_by('-created_at')
    return render(request, 'job/search.html', {'userprofile': request.user.userprofile,'jobs': jobs})

def job_detail(request, job_id):
    job = Job.objects.get(pk=job_id)

    return render(request, 'job/job_detail.html', {'userprofile': request.user.userprofile,'job': job})

@login_required
def apply_for_job(request, job_id):
    job = Job.objects.get(pk=job_id)

    if request.method == 'POST':
        form = ApplicationForm(request.POST)

        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.created_by = request.user
            application.save()

            create_notification(request, job.created_by, 'application', extra_id=application.id)

            return redirect('dashboard')
    else:
        form = ApplicationForm()
    
    return render(request, 'job/apply_for_job.html', {'userprofile': request.user.userprofile,'form': form, 'job': job})

@login_required
def add_job(request):
    if request.method == 'POST':
        form = AddJobForm(request.POST)

        if form.is_valid():
            job = form.save(commit=False)
            job.created_by = request.user
            job.save()

            return redirect('list_jobs')
    else:
        form = AddJobForm()
    
    return render(request, 'job/add_job.html', {'userprofile': request.user.userprofile,'form': form})

@login_required
def edit_job(request, job_id):
    job = get_object_or_404(Job, pk=job_id, created_by=request.user)

    if request.method == 'POST':
        form = AddJobForm(request.POST, instance=job)

        if form.is_valid():
            job = form.save(commit=False)
            job.status = request.POST.get('status')
            job.save()

            return redirect('dashboard')
    else:
        form = AddJobForm(instance=job)
    
    return render(request, 'job/edit_job.html', {'userprofile': request.user.userprofile,'form': form, 'job': job})