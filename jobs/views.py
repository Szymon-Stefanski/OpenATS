from django.shortcuts import render, get_object_or_404
from .models import JobOffer

def job_list(request):
    offers = JobOffer.objects.all().order_by('-created_at')
    return render(request, 'jobs/job_list.html', {'offers': offers})

def job_detail(request, pk):
    offer = get_object_or_404(JobOffer, pk=pk)
    candidates = offer.candidates.all().order_by('-match_score')
    return render(request, 'jobs/job_detail.html', {'offer': offer, 'candidates': candidates})
