from django.db import models

class PatientRecord(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    symptoms = models.TextField()
    predicted_disease = models.CharField(max_length=100)
    description = models.TextField()
    precautions = models.TextField()
    medication = models.TextField()
    diet = models.TextField()
    workout = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)  # ✅ add this

    def __str__(self):
        return f"{self.name} - {self.predicted_disease}"
