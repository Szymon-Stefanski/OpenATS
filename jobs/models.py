import fitz
from django.db import models
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class JobOffer(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Candidate(models.Model):
    job_offer = models.ForeignKey(JobOffer, on_delete=models.CASCADE, related_name="candidates")
    full_name = models.CharField(max_length=200)
    cv_file = models.FileField(upload_to='cv_uploads/')
    match_score = models.FloatField(default=0.0)
    extracted_text = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.cv_file and not self.extracted_text:
            text = ""
            with fitz.open(self.cv_file.path) as doc:
                for page in doc:
                    text += page.get_text()

            self.extracted_text = text

            if self.job_offer.description:
                documents = [self.job_offer.description, self.extracted_text]
                count_vectorizer = TfidfVectorizer()
                sparse_matrix = count_vectorizer.fit_transform(documents)

                similarity_matrix = cosine_similarity(sparse_matrix[0:1], sparse_matrix[1:2])
                self.match_score = round(similarity_matrix[0][0] * 100, 2)

                super().save(update_fields=['extracted_text', 'match_score'])

    def __str__(self):
        return f"{self.full_name} ({self.match_score}%)"
