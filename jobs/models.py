from django.db import models


class JobOffer(models.Model):
    title = models.CharField(max_length=200, verbose_name="Title")
    description = models.TextField(verbose_name="Description")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Candidate(models.Model):
    job_offer = models.ForeignKey(JobOffer, on_delete=models.CASCADE, related_name="candidates")
    full_name = models.CharField(max_length=200, verbose_name="Name and surname")
    cv_file = models.FileField(upload_to='cv_uploads/', verbose_name="CV file")


    match_score = models.FloatField(default=0.0, verbose_name="Matching score:")
    extracted_text = models.TextField(blank=True, verbose_name="Text from CV")

    def __str__(self):
        return f"{self.full_name} - {self.job_offer.title}"
